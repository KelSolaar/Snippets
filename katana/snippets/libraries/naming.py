import ast
import re

import snippets.libraries.utilities

NODES_NAMES_MAPPING_TABLE = {"ArnoldShadingNode": "ArnoldSN",
                             "PrmanShadingNode": "PrmanSN"}


def get_default_node_name(node, mapping_table=NODES_NAMES_MAPPING_TABLE):
    """
    Returns given node default name.

    :param nodes: Node to get the default name.
    :type nodes: Node
    :param mapping_table: Names mapping table.
    :type mapping_table: dict
    :return: Node default name.
    :rtype: str
    """

    node_type = node.getType()
    name = mapping_table.get(node_type, node_type)
    if node_type in ("ArnoldShadingNode", "PrmanShadingNode"):
        coshader = re.sub(r":.*", "", node.getParameter("nodeType").getValue(0))
        return "{0}_{1}".format(mapping_table.get(coshader, coshader), name)
    else:
        return name


def set_node_name(node, name):
    """
    Sets given node name.

    :param node: Node to set the name.
    :type node: object
    :param name: Node name.
    :type name: str
    :return: Definition success.
    :rtype: bool
    """

    node.setName(name)

    node_type = node.getType()
    if node_type in ("ArnoldShadingNode", "PrmanShadingNode"):
        node.getParameter("name").setValue(node.getName(), 0)

    return True


def set_node_names(nodes, prefix, mapping_table=NODES_NAMES_MAPPING_TABLE, traverse=True):
    """
    Sets given nodes names using given prefix.

    :param nodes: Nodes to set the names.
    :type nodes: list
    :param prefix: Prefix.
    :type prefix: str
    :param mapping_table: Names mapping table.
    :type mapping_table: dict
    :param traverse: Traverse nodes children.
    :type traverse: bool
    :return: Definition success.
    :rtype: bool
    """

    for node in nodes:
        set_node_name(node, "{0}{1}".format(prefix, get_default_node_name(node, mapping_table)))
        if not traverse:
            continue

        for child_node in snippets.libraries.utilities.nodes_walker(node):
            set_node_name(child_node, "{0}{1}".format(prefix, get_default_node_name(child_node, mapping_table)))
    return True


def search_and_replace_nodes_names(nodes, search_pattern, replacement_pattern, flags=0, traverse=True):
    """
    Search and replace given nodes names.

    :param nodes: Nodes to search and replace.
    :type nodes: list
    :param search_pattern: Search pattern.
    :type search_pattern: str
    :param replacement_pattern: Replacement pattern.
    :type replacement_pattern: str
    :param flags: Matching regex flags.
    :type flags: int
    :param traverse: Traverse nodes children.
    :type traverse: bool
    :return: Definition success.
    :rtype: bool
    """

    search_pattern = re.compile(search_pattern)
    for node in nodes:
        set_node_name(node, re.sub(search_pattern, replacement_pattern, node.getName(), flags))
        if not traverse:
            continue

        for child_node in snippets.libraries.utilities.nodes_walker(node):
            set_node_name(child_node, re.sub(search_pattern, replacement_pattern, child_node.getName(), flags))
    return True


def remove_nodes_names_trailing_numbers(nodes, traverse=True):
    """
    Removes given nodes names trailing numbers.

    :param nodes: Nodes to search and replace.
    :type nodes: list
    :param traverse: Traverse nodes children.
    :type traverse: bool
    :return: Definition success.
    :rtype: bool
    """

    return search_and_replace_nodes_names(nodes, r"\d+$", "", traverse=traverse)


def prefix_nodes_names(nodes, prefix, traverse=True):
    """
    Prefixes given nodes names using given prefix.

    :param nodes: Nodes to search and replace.
    :type nodes: list
    :param prefix: Prefix.
    :type prefix: str
    :param traverse: Traverse nodes children.
    :type traverse: bool
    :return: Definition success.
    :rtype: bool
    """

    return search_and_replace_nodes_names(nodes, r".*", lambda x: "{0}{1}".format(prefix, x.group(0)),
                                          traverse=traverse)


def search_and_replace_hints_parameter(parameter, search_pattern, replacement_pattern, flags=0, time=0, keys=None):
    """
    Search and replace given hint parameter.

    :param parameter: Hint parameter to search and replace.
    :type parameter: object
    :param search_pattern: Search pattern.
    :type search_pattern: str
    :param replacement_pattern: Replacement pattern.
    :type replacement_pattern: str
    :param flags: Matching regex flags.
    :type flags: int
    :param time: Time to set the value to.
    :type time: int
    :param keys: Hints keys to search and replace in.
    :type keys: list
    :return: Definition success.
    :rtype: bool
    """

    data = ast.literal_eval(parameter.getValue(time))
    for key, value in data.iteritems():
        if keys and key not in keys:
            continue

        if not isinstance(value, str):
            continue

        data[key] = re.sub(search_pattern, replacement_pattern, value, flags)
    parameter.setValue(str(data), time)
    return True


def search_and_replace_hints_parameters(nodes, search_pattern, replacement_pattern, flags=0, time=0, keys=None,
                                        traverse=True):
    """
    Search and replace given nodes hints parameters.

    :param nodes: Nodes to search and replace.
    :type nodes: list
    :param search_pattern: Search pattern.
    :type search_pattern: str
    :param replacement_pattern: Replacement pattern.
    :type replacement_pattern: str
    :param flags: Matching regex flags.
    :type flags: int
    :param time: Time to set the value to.
    :type time: int
    :param keys: Hints keys to search and replace in.
    :type keys: list
    :param traverse: Traverse nodes children.
    :type traverse: bool
    :return: Definition success.
    :rtype: bool
    """

    search_pattern = re.compile(search_pattern)
    for node in nodes:
        for parameter in snippets.libraries.utilities.filter_node_parameters(node, "^hints$"):
            search_and_replace_hints_parameter(parameter, search_pattern, replacement_pattern, flags, time, keys)
        if not traverse:
            continue

        for child_node in snippets.libraries.utilities.nodes_walker(node):
            for parameter in snippets.libraries.utilities.filter_node_parameters(child_node, "^hints$"):
                search_and_replace_hints_parameter(parameter, search_pattern, replacement_pattern, flags, time, keys)
    return True
