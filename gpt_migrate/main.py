import os
import sys
import yaml
import asyncio
import argparse
from dotenv import load_dotenv
from gpt_migrate.llm import get_llm
from gpt_migrate.utils.cfg import Config
from gpt_migrate.utils.util import read_gitignore
from gpt_migrate.agents.doc_agent.agent import DocAgent
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()


async def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("config_path", help="Path to config file")
    args = parser.parse_args(arguments)

    with open(args.config_path, "r") as fp:
        config_yaml = yaml.safe_load(fp)
    cfg = Config(config_yaml)
    model = get_llm(cfg.migrate.model)

    entry_path = cfg.entry_path
    output_path = cfg.output_path

    legacy_language = cfg.legacy_language
    legacy_framework = cfg.legacy_framework

    thread_id = cfg.thread_id

    memory = SqliteSaver.from_conn_string(os.path.join(
        output_path,
        "checkpoint.db"
    ))

    doc_agent = DocAgent(model, [], checkpointer=memory, thread_id=thread_id)

    init_state = doc_agent.graph.get_state(doc_agent.config)
    if init_state.created_at is None:
        init_state = {
                "entry_path": entry_path,
                "ignore_list": read_gitignore(entry_path),
                "directory_stack": [{"path": entry_path, "count": -1}],
                "output_path": output_path,
                "lagecy_language": legacy_language,
                "lagecy_framework": legacy_framework,
                "directory_structure": "",
                "indent": "",
        }
        result = doc_agent(init_state)
    elif init_state.created_at is not None:
        if len(init_state.values["items_to_process"]) != 0:
            result = doc_agent(init_state.values)
        else:
            result = init_state.values

    print(result)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
