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



@dataclass
class State(InputState):
    """Represents the complete state of the agent, extending InputState with additional attributes."""

    is_last_step: bool = field(default=False)
    last_agent_worker: str = field(default="")
    """
    The name of the last agent worker that produced a message and did the work.
    This is a 'managed' variable, controlled by the state machine rather than user code.
    """