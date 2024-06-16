import os
from typing import Dict, Any, List
from gpt_migrate.agents.state import AgentState


class DocAgentState(AgentState): 
    entry_path: str
    output_path: str
    current_path: str
    current_file: str
    items_to_process: List[str]
    directory_structure: str
