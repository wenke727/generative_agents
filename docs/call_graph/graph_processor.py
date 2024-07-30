import sys
from loguru import logger
import pygraphviz as pgv

def load_graph(file_path):
    """Load a graph from a Graphviz file."""
    with open(file_path) as file:
        graphviz_content = file.read()
    graph = pgv.AGraph(string=graphviz_content)
    return graph

def delete_ignore_node(graph, ignore_paths=None):
    """Delete nodes that match any of the patterns in ignore_paths."""
    if ignore_paths is None:
        ignore_paths = ['.vscode', 'envs/x']

    for node in graph.nodes():
        for pattern in ignore_paths:
            if pattern in str(node):
                logger.debug(f"delete node: {node}")
                graph.delete_node(node)
    return graph

def rename_nodes(graph, old_prefix, new_prefix='./'):
    """Rename nodes by replacing old_prefix with new_prefix."""
    graph_str = graph.to_string()
    new_graph_str = graph_str.replace(old_prefix, new_prefix)
    new_graph = pgv.AGraph(string=new_graph_str)
    return new_graph

def process_graph(file_path, old_prefix, new_prefix='./', ignore_paths=None):
    """Load, process, and save the graph."""
    graph = load_graph(file_path)
    graph = delete_ignore_node(graph, ignore_paths)
    graph = rename_nodes(graph, old_prefix, new_prefix)
    logger.debug(f"{graph.to_string()}")

    out_fn = ".".join(file_path.split(".")[:-1]) + "_simplified.svg"
    graph.write(out_fn)

    logger.info(f"Modified graph written to {out_fn}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python x.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]
    old_prefix = "/Users/wenke/Documents/generative_agents/reverie/backend_server/"
    process_graph(file_name, old_prefix)
