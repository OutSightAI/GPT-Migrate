import os
import sys
import yaml
import argparse
from dotenv import load_dotenv
from gpt_migrate.utils.cfg import Config
from gpt_migrate.llm import get_llm
from gpt_migrate.agents.doc_agent.agent import DocAgent

load_dotenv()

def main(arguments): 
    parser = argparse.ArgumentParser()
    parser.add_argument('config_path', help='Path to config file')
    args = parser.parse_args(arguments)

    with open(args.config_path, 'r') as fp: 
        config_yaml = yaml.safe_load(fp) 
    cfg = Config(config_yaml)
    model = get_llm(cfg.migrate.model)
    
    doc_agent = DocAgent(model, [])
    doc_agent({"entry_path": "/mnt/c/Users/amangokrani/OneDrive - Microsoft/Personal/mern-admin"})
    import pdb;pdb.set_trace()
if __name__ == "__main__":
    main(sys.argv[1:])
