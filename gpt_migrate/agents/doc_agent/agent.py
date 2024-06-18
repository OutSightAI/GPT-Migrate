import os
from gpt_migrate.agents.agent import Agent
from langgraph.graph import StateGraph, END
from gpt_migrate.utils.util import is_ignored
from gpt_migrate.agents.doc_agent.state import DocAgentState


class DocAgent(Agent):
    def __init__(self, model, tools):
        super().__init__(model, tools)
        # creating Agent graph
        graph = StateGraph(DocAgentState)

        # Adding nodes
        graph.add_node("start", self.start_node)
        graph.add_node("directory_processor", self.directory_processor_node)
        graph.add_node("document_file", self.document_file_node)
        graph.add_node("readme_creator", self.readme_creator_node)

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

        # compiling graph
        self.graph = graph.compile()

    def __call__(self, state: DocAgentState):
        return self.graph.invoke(state, config={"recursion_limit": 1000})

    def process_directory_or_file(self, state: DocAgentState):
        if state["current_path"] is not None:
            if os.path.isdir(
                os.path.join(
                    state["directory_stack"][-1]["path"], state["current_path"]
                )
            ):
                return "start"
            else:
                return "document_file"
        if (
            state["current_path"] is None
            and state["directory_stack"][-1]["count"] == -1
        ):
            return "readme_creator"
        else:
            return "end"

    def should_continue(self, state: DocAgentState):
        if state["items_to_process"] is not None:
            return "start"
        else:
            return "end"

    def start_node(self, state: DocAgentState):
        current_path = state["current_path"]

        items_to_process = state["items_to_process"]
        path = (
            os.path.join(state["directory_stack"][-1]["path"], current_path)
            if current_path is not None
            else state["directory_stack"][-1]["path"]
        )
        import pdb

        pdb.set_trace()
        if os.path.isdir(path):
            if current_path is not None and os.path.join(
                state["directory_stack"][-1]["path"], state["current_path"]
            ) not in [d["path"] for d in state["directory_stack"]]:

                state["directory_stack"].append(
                    {
                        "path": os.path.join(
                            state["directory_stack"][-1]["path"], state["current_path"]
                        ),
                        "count": -1,
                    }
                )
            items = os.listdir(path)
            assert state["directory_stack"][-1]["count"] == -1
            state["directory_stack"][-1]["count"] = len(items)

            if items_to_process is None:
                items_to_process = items
            else:
                items_to_process = items + items_to_process

        return {"items_to_process": items_to_process, "current_path": current_path}

    def directory_processor_node(self, state: DocAgentState):
        if state["items_to_process"]:
            while True:
                state["directory_stack"][-1]["count"] -= 1  # Decrease count
                if state["directory_stack"][-1]["count"] == -1:
                    return {"current_path": None}
                next_item = state["items_to_process"].pop(0)
                if not is_ignored(next_item, state["ignore_list"]):
                    break
            return {"current_path": next_item}

        else:
            return {"current_path": None}

    def document_file_node(self, state: DocAgentState):
        # TODO: Invoke the model to document the file.
        print(state["current_path"])

    def readme_creator_node(self, state: DocAgentState):
        ## Pop the last directory from the stack
        # state["directory_stack"].pop(-1)
        pass
