import os
from litellm import completion


class LLM:
    def __init__(self, model_params):
        for key, value in model_params.items():
            setattr(self, key, value)

    async def call_lm(self, *args):
        """Call the Language Model"""
        return await self._call_completion(*args)

    async def _call_completion(self, messages, **kwargs):
        """Call a Large Language Model to get Text Completion"""
        return await completion(model=self.name, messages=messages**kwargs)
