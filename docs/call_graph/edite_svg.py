import sys
import re
from loguru import logger

def remove_nodes(file_path, dirs_to_remove):
    with open(file_path, 'r') as file:
        graph_def = file.read()

    # Split the graph definition into lines
    lines = graph_def.split('\n')

    # Initialize a list to hold the new lines of the graph definition
    new_lines = []

    # Pattern to match node definitions
    node_pattern = re.compile(r'{(.+?)(\[label=".+?"\])}')

    # Loop through each line in the original graph definition
    for line in lines:
        # Check if the line contains a node definition
        match = node_pattern.search(line)
        if match:
            logger.debug(match)
            # Extract the node identifier (file path)
            node_id = match.group(1)
            # Check if the node is in one of the directories to remove
            if any(node_id.startswith(dir) for dir in dirs_to_remove):
                logger.debug(node_id)
                continue  # Skip this node
        new_lines.append(line)

    # Join the new lines back into a single string
    new_graph_def = '\n'.join(new_lines)
    return new_graph_def

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python x.py <path>")
        sys.exit(1)

    file_path = sys.argv[1]
    dirs_to_remove = [
        "/Users/wenke/.vscode/extensions/ms-python.vscode-pylance-2024.7.1/"
    ]

    modified_graph = remove_nodes(file_path, dirs_to_remove)
    edit_file_path = file_path.replace('.svg', '_edit.svg')

    with open(edit_file_path, 'w') as file:
        file.write(modified_graph)

    print(f"Modified graph saved to {edit_file_path}")