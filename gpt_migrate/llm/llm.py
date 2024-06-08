import os
from litellm import completion

class LLM: 
    def __init__(self, model_params):
        for key, value in model_params.items():
            setattr(self, key, value)
    
    async def call(self, *args):
        return await _call_completion(*args)

    async def _call_completion(self, messages, **kwargs):
        return await completion(
                model=self.name,
                messages=messages
                **kwargs
            )

        
