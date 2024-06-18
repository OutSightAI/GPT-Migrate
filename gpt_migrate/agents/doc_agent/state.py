from typing import Dict, Any, List
from gpt_migrate.agents.state import AgentState


class DocAgentState(AgentState):
    entry_path: str
    output_path: str
    current_path: str
    current_file: str
    ignore_list: List[str]
    items_to_process: List[str]
    directory_structure: str
    directory_stack: List[Dict[str, Any]]
