from abc import abstractmethod


class Agent:
    def __init__(self, model, tools):
        if tools is not None and len(tools) != 0:
            self.tools = {t.name: t for t in tools}
            self.model = model.bind_tools(tools)
        else:
            self.model = model

    @abstractmethod
    def __call__(**kwargs):
        """
        This method should call the agent graph in the derived agent classes
        """
