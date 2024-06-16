import os
import sys
import yaml
import argparse
from dotenv import load_dotenv
from gpt_migrate.utils.cfg import Config
from gpt_migrate.llm import get_llm

load_dotenv()

def main(arguments): 
    parser = argparse.ArgumentParser()
    parser.add_argument('config_path', help='Path to config file')
    args = parser.parse_args(arguments)

    with open(args.config_path, 'r') as fp: 
        config_yaml = yaml.safe_load(fp) 
    cfg = Config(config_yaml)
    model = get_llm(cfg.migrate.model)
    
if __name__ == "__main__":
    main(sys.argv[1:])
