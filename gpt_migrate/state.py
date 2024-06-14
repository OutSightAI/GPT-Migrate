import operator
from typing import TypedDict, Annotated


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
