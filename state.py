from dataclasses import dataclass, field
from typing import Literal, Annotated, Sequence
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

@dataclass
class InputState:
    """Defines the input state for the agent, representing a narrower interface to the outside world."""

    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )
    """
    Messages tracking the primary execution state of the agent.

    Typically accumulates a pattern of:
    1. HumanMessage - user input
    2. AIMessage with .tool_calls - agent picking tool(s) to use to collect information
    3. ToolMessage(s) - the responses (or errors) from the executed tools
    4. AIMessage without .tool_calls - agent responding in unstructured format to the user
    5. HumanMessage - user responds with the next conversational turn

    Steps 2-5 may repeat as needed.
    """


@dataclass
class State(InputState):
    """Represents the complete state of the agent, extending InputState with additional attributes."""

    is_last_step: bool = field(default=False)
    last_agent_worker: str = field(default="")
    """
    The name of the last agent worker that produced a message and did the work.
    This is a 'managed' variable, controlled by the state machine rather than user code.
    """
    sub_agent_asking_for_input: bool = field(default=False)
    """
    Indicates whether the sub-agent is requesting input from the user. to continue the conversation.
    """