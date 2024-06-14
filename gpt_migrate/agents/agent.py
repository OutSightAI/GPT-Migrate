import os


class Agent: 
    def __init__(self, model, tools):
        self.tools {t.name: t for t in tools}
        self.model = model.bind_tools(tools)
    
    @abstractmethod
    def __call__(**kwargs):
        """
        This method should call the agent graph in the derived agent classes
        """
        
