import os
from gpt_migrate.agents.agent import Agent
from langgraph.graph import StateGraph, END
from gpt_migrate.utils.util import is_ignored, parse_code_string
from gpt_migrate.agents.doc_agent.state import DocAgentState
from gpt_migrate.agents.doc_agent.prompts import PROMPT, PROMPT_SUMMARY


class DocAgent(Agent):
    def __init__(self, model, tools):
        super().__init__(model, tools)
        self.doc_chain = PROMPT | self.model
        self.summary_chain = PROMPT_SUMMARY | self.model
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
            "document_file", self.should_continue,
            {
                "start": "start",
                "end": END
            }
        )

        graph.add_conditional_edges(
            "readme_creator", self.should_continue,
            {
                "start": "start",
                "end": END
            }
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
        ) or (
            state["current_path"] is None
            and state["directory_stack"][-1]["count"] == 0
            and len(state["directory_stack"]) == 1
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
        if os.path.isdir(path):
            if current_path is not None and os.path.join(
                state["directory_stack"][-1]["path"], state["current_path"]
            ) not in [d["path"] for d in state["directory_stack"]]:

                state["directory_stack"].append(
                    {
                        "path": os.path.join(
                            state["directory_stack"][-1]["path"],
                            state["current_path"]
                        ),
                        "count": -1,
                    }
                )

            if state["directory_stack"][-1]["count"] == -1:
                items = os.listdir(path)
                state["directory_stack"][-1]["count"] = len(items)

                if items_to_process is None:
                    items_to_process = items
                else:
                    items_to_process = items + items_to_process

            if current_path is not None:
                prefix = '├── ' if state["directory_stack"][-1]["count"] > 0 \
                        else '└── '

                state["directory_structure"] += state["indent"] + prefix + \
                    current_path + "/\n"

                state["indent"] += "│   " if \
                    state["directory_stack"][-1]["count"] > 0 else "    "

        return {
            "items_to_process": items_to_process,
            "current_path": current_path,
            "directory_structure": state["directory_structure"],
            "indent": state["indent"],
        }

    def directory_processor_node(self, state: DocAgentState):
        if state["items_to_process"]:
            while True:
                state["directory_stack"][-1]["count"] -= 1  # Decrease count
                if state["directory_stack"][-1]["count"] == -1:
                    state["indent"] = state["indent"][:-4]
                    return {"current_path": None, "indent": state["indent"]}
                next_item = state["items_to_process"].pop(0)
                if not is_ignored(next_item, state["ignore_list"]):
                    break
            return {"current_path": next_item}

        else:
            return {"current_path": None}

    def document_file_node(self, state: DocAgentState):
        # TODO: Invoke the model to document the file.
        code_file = None
        message = None
        with open(
                os.path.join(state["directory_stack"][-1]["path"], state[
                    "current_path"
                ]), "r",
        ) as f:
            code_file = f.read()
        start_pos = state["directory_stack"][-1]["path"]. \
            find(
                state["entry_path"]
            )

        relative_path = state["directory_stack"][-1]["path"][
            start_pos + len(state["entry_path"]):
        ]
        if relative_path is not None and len(relative_path) > 0:
            if relative_path[0] == '/':
                relative_path = relative_path[1:]

        output_path = os.path.join(state["output_path"], relative_path)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        if not os.path.exists(
            os.path.join(
                output_path,
                state["current_path"])):
            doc_commented_code_file = parse_code_string(
                self.doc_chain.invoke({
                    "language": state["legacy_language"],
                    "framework": state["legacy_framework"],
                    "code_file": code_file
                }).content
            )

            try:
                with open(
                    os.path.join(output_path, state["current_path"]),
                    "w"
                ) as f:
                    f.write(doc_commented_code_file)
            except IOError:
                if os.path.exists(
                    os.path.join(
                        output_path,
                        state["current_path"]
                    )
                ):
                    os.remove(os.path.join(output_path, state["current_path"]))
                print("Error writing file")

            # pass doc_commented_code_file to the model again with the
            # summary chain to create a summary of the file and write the
            # summary along with the path to the messages in state
            code_file_summary = self.summary_chain.invoke({
                "language": state["legacy_language"],
                "framework": state["legacy_framework"],
                "code_file": doc_commented_code_file
            })
            code_file_summary.additional_kwargs["directory_path"] = \
                state["directory_stack"][-1]["path"]
            code_file_summary.additional_kwargs["file_name"] = \
                state["current_path"]
            message = code_file_summary

        prefix = '├── ' if state["directory_stack"][-1]["count"] > 0 \
            else '└── '
        state["directory_structure"] = state["directory_structure"] + \
            state["indent"] + prefix + state["current_path"] + "\n"

        if message is not None:
            return {
                "directory_structure": state["directory_structure"],
                "messages": [message]
            }

        return {
            "directory_structure": state["directory_structure"],
        }

    def readme_creator_node(self, state: DocAgentState):
        # Pop the last directory from the stack
        state["directory_stack"].pop(-1)

        # write this README.md in the output_path and add
        # the contents of README.md to the messages in state
        # with the path in the last position in the directory_stack
        # in state
        import pdb
        pdb.set_trace()
