from litellm import completion


class LLM:
    def __init__(self, model_params):
        for key, value in model_params.items():
            setattr(self, key, value)

    def call_lm(self, **kwargs):
        """Call the Language Model"""
        return self._call_completion(**kwargs)

    def _call_completion(self, messages, **kwargs):
        """Call a Large Language Model to get Text Completion"""
        return completion(model=self.model, messages=messages, **kwargs)
