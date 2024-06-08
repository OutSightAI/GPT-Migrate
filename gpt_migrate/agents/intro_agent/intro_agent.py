from gpt_migrate.agents.intro_agent.intro_prompts import intro_prompt, intro_sys_prompt
from gpt_migrate.llm import LLM


class IntroAgent:
    def run(self):
        return LLM(model_params={"model": "gpt-3.5-turbo"}).call_lm(
            messages=[
                {"content": intro_sys_prompt, "role": "system"},
                {"content": intro_prompt, "role": "user"},
            ]
        )
