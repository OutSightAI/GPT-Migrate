import os
import fnmatch
import re


def read_gitignore(path):
    gitignore_path = os.path.join(path, ".gptignore")
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    return patterns


def is_ignored(entry_path, gitignore_patterns):
    for pattern in gitignore_patterns:
        if fnmatch.fnmatch(entry_path, pattern):
            return True
    return False


def parse_code_string(code_string):

    pattern = re.compile(r'```(.+?)\n(.*?)\n```', re.DOTALL)

    match = pattern.match(code_string)
    if match:
        _, code = match.groups()
        return code
    return code_string
