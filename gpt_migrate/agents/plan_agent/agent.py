import os
import operator
from typing import Any

from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage


class PlanAgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    output_path: str
    current_path: str
    directory_stack: list[dict[str, Any]]
    items_to_process: list[str]
    legacy_language: str
    legacy_framework: str
    indent: str


class PlanAgent:
    def __init__(self, model, tools):
        graph = StateGraph(PlanAgentState)

        graph.add_node("start", self.start_node)
        graph.add_node("directory_processor", self.get_repo_details_node)
        graph.add_node("readme_creator", self.plan_creator_node)

        graph.set_entry_point("start")
        graph.add_edge("start", "directory_processor")

        # Adding edges
        graph.add_conditional_edges(
            "directory_processor",
            self.process_directory_or_file,
            {
                "start": "start",
                "document_file": "document_file",
                "readme_creator": "readme_creator",
                "end": END,
            },
        )

        graph.add_conditional_edges(
            "document_file", self.should_continue, {"start": "start", "end": END}
        )

        graph.add_conditional_edges(
            "readme_creator", self.should_continue, {"start": "start", "end": END}
        )

        self.graph = graph.compile()

    def __call__(self, state: PlanAgentState):
        return self.graph.invoke(state, config={"recursion_limit": 1000})

    def process_directory_or_file(self, state: PlanAgentState): ...

    def should_continue(self, state: PlanAgentState): ...

    def start_node(self, state: PlanAgentState):
        ...
        # TODO: Collect all the Detals

    def get_repo_details_node(self, state: PlanAgentState):
        ...
        # TODO: Get Repo Details After DocAgent has documented it

    def plan_creator_node(self, state: PlanAgentState):
        ...
        # TODO: Formulate the Plan
