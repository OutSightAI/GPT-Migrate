from dotenv import load_dotenv
from gpt_migrate.agents.intro_agent.intro_agent import IntroAgent

load_dotenv()


def main():
    agent = IntroAgent()
    result = agent.run()
    print(result.choices[0].message.content)


if __name__ == "__main__":
    main()
