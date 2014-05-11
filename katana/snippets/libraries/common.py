import ast
import re

import snippets.libraries.utilities

def reset_nodes_parameters(nodes, traverse=True):
    """
    Resets given nodes parameters.

    :param nodes: Nodes to search and replace.
    :type nodes: list
    :param traverse: Traverse nodes children.
    :type traverse: bool
    :return: Definition success.
    :rtype: bool
    """

    for node in nodes:
        snippets.libraries.utilities.reset_node_parameters(node)
        if not traverse:
            continue

        for child_node in snippets.libraries.utilities.nodes_walker(node):
            snippets.libraries.utilities.reset_node_parameters(child_node)
    return True
