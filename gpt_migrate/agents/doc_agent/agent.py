import os
from gpt_migrate.agents.agent import Agent
from langgraph.graph import StateGraph, END
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
        #graph.add_node("readme_creator", self.readme_creator_node)

        graph.set_entry_point("start")
        graph.add_edge("start", "directory_processor")

        # Adding edges
        graph.add_conditional_edges(
            "directory_processor", 
            self.should_process, 
            {
                "start_node": "start",
                "document_file": "document_file",
                "end": END
            }
        )
        graph.add_edge("document_file", END)
        
        #compiling graph 
        self.graph = graph.compile()
    

    def __call__(self, state: DocAgentState):
        return self.graph.invoke(state)
        
    def should_process(self, state: DocAgentState):
        if state["current_path"] is not None:
            if os.path.isdir(state["current_path"]): 
                return "start_node"
            else: 
                return "document_file"
        else: 
            return "end"
    
    def start_node(self, state: DocAgentState):
        current_path = state["current_path"]
        if current_path is None:
            current_path = state["entry_path"]
        items = os.listdir(current_path)
        return {"items_to_process": items, "current_path": current_path}

    def directory_processor_node(self, state: DocAgentState):
        if state["items_to_process"]:
            next_item = state["items_to_process"].pop(0)
            next_item_path = os.path.join(state["current_path"], next_item)
            return {"current_path": next_item_path}
        else:
            return {"current_path": None}
    
    def document_file_node(self, state: DocAgentState):
        pass

    def readme_creator_node(self, state: DocAgentState):
        pass