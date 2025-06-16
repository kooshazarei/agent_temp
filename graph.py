import os
from typing import Dict, List, Literal, cast, Any, Union
from typing import Annotated, Optional
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt
from langchain_core.runnables import RunnableConfig
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
    SystemMessage,
    AnyMessage,
)
from langsmith import Client
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain.callbacks.base import BaseCallbackHandler, AsyncCallbackHandler


from state import State, InputState
from langfuse import Langfuse
from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI


# model_supervisor = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         temperature=0.1,
#         # max_tokens=None,
#         # timeout=None,
#         # max_retries=1,
#         api_key=API_KEY_GEMINI
#         # other params...
#     )


def load_prompt(prompt_name: str) -> str:
    # Fall back to local file
    print(f"Using local prompt '{prompt_name}'")
    with open(os.path.join(os.path.dirname(__file__), f'prompts/{prompt_name}.txt'), 'r') as file:
        return file.read()



async def make_graph():

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0.2)
    tools = []
    llm_with_tools = llm.bind_tools(tools)

    # load prompts
    prompt_decorator = load_prompt("Prompt_Decorators")
    simple_system_message = load_prompt("Agent_Instructions")
    prompt_workflow_spec = load_prompt("workflow_spec")
    prompt_integration_actions = load_prompt("integration_actions")
    prompt_workflow_context = load_prompt("workflow_context")

    class InputCheck(TypedDict):
        """Simple schema to get a definitive TRUE/FALSE response"""
        needs_more_input: bool
        """based on assistant response, Whether the model/agent asks for more information or other input from the user"""


    async def chatbot(state: State, config: Optional[RunnableConfig] = None):

        messages = [
            {"role": "system", "content": prompt_decorator},
            {"role": "system", "content": prompt_workflow_spec},
            {"role": "system", "content": prompt_integration_actions},
            {"role": "system", "content": prompt_workflow_context},
            {"role": "system", "content": simple_system_message},
        ] + list(state.messages)

        # First request: Get the main response with tool calls
        response = await llm_with_tools.ainvoke(
            messages,
            config=config or {},
        )

        # input_check_messages = messages + [
        #     {"role": "system", "content": simple_system_message},
        #     {"role": "assistant", "content": response.content},
        #     {"role": "user", "content": "Based on the user request and your/assistant response, do you need additional information from user?"}
        # ]

        # Use structured output to force a boolean response
        # input_check = await llm.with_structured_output(InputCheck).ainvoke(input_check_messages)
        # asking_for_input = input_check["needs_more_input"]

        return {
            "messages": [
                AIMessage(content=response.content, tool_calls=response.tool_calls)
            ],
        }


    # Conditional edge function to route to the tool node or end based upon whether the LLM made a tool call
    def should_continue(state: State):
        """Route to the tool node or end based on tool calls."""
        last_message = state.messages[-1]
        if last_message.tool_calls:
            return "Action"
        return END

    # Build the graph
    graph_builder = StateGraph(State, input=InputState)
    graph_builder.add_node("agent", chatbot)
    graph_builder.add_node("tools", ToolNode(tools=tools))
    graph_builder.set_entry_point("agent")
    graph_builder.add_conditional_edges(
        "agent",
        should_continue,
        {
            "Action": "tools",
            END: END,
        },
    )
    graph_builder.add_edge("tools", "agent")

    memory = MemorySaver()
    graph = graph_builder.compile(
        # checkpointer=memory,
        # interrupt_before=[],
        # interrupt_after=[],
    )
    graph.name = "AirOPS Koosha"
    return graph
