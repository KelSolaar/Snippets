import Katana
import NodegraphAPI
import UI4
import ast
import os
import re

def console_print(*args):
    """
    Prints given message to KatanaConsole.

    :param \*args: Arguments.
    :type \*args: \*
    """

    UI4.App.Tabs.FindTopTab("Python").printMessage(" ".join(map(str, args)))

def list_renderer_object_names(renderer):
    """
    Lists given render object names ( Shaders ).

    :param renderer: Renderer to list the object names.
    :type renderer: str
    :return: Object names.
    :rtype: list
    """

    renderer_info = RenderingAPI.RenderPlugins.GetInfoPluginName(renderer)
    plugin = RenderingAPI.RendererInfo.GetPlugin(renderer_info)
    return plugin.getRendererObjectNames()

def list_node(node, indentation="\t", tab_level= -1):
    """
    Lists the current node and its children.

    :param node: Node to list.
    :type node: object
    :param indentation: Indentation character.
    :type indentation: str
    :param tab_level: Indentation level.
    :type tab_level: int
    :return: Node listing.
    :rtype: str
    """

    attribute = "getChildren"

    output = ""
    tab_level += 1

    for i in range(tab_level):
        output += indentation

    output += "|----'{0}'\n".format(node.getName())

    if hasattr(node,attribute):
        for child in getattr(node, attribute)() or []:
            if child is None:
                continue

            output += list_node(child, indentation, tab_level)

    tab_level -= 1
    return output

def list_hints_parameters(node, output_as_tree=False, indentation="\t", time=0):
    """
    Lists given node and children hints parameters.

    :param node: Node to list hint parameters.
    :type node: object
    :param output_as_tree: Output as groups output_as_tree.
    :type output_as_tree: bool
    :param indentation: Indentation character.
    :type indentation: str
    :param time: Time to get the hints parameters value.
    :type time: int
    :return: Hints parameters listing.
    :rtype: str
    """

    nodes = [node]
    nodes.extend(list(nodes_walker(node)))

    output = ""

    if output_as_tree:
        hints = {}
        for node in nodes:
            for parameter in filter_node_parameters(node, "^hints$"):
                value = ast.literal_eval(parameter.getValue(time))
                group = value.get("dstPage", "Undefined")
                if not hints.get(group):
                    hints[group] = []

                hints[group].append((node.getName(), parameter.getParent().getName(), value.get("dstName", "Undefined")))

        for group, children in sorted(hints.items()):
            output += "{0}:\n".format(group)
            for child in sorted(children, key=lambda x: x[2]):
                node, parameter, value = child
                output += "{0}{1}: {2}.{3}\n".format(indentation, value, node, parameter)
            output += "\n"
    else:
        for node in nodes:
            for parameter in filter_node_parameters(node, "^hints$"):
                value = ast.literal_eval(parameter.getValue(time))
                output += "{0}.{1}:\n".format(node.getName(), parameter.getParent().getName())
                output += "{0}Group: {1}\n".format(indentation, value.pop("dstPage", "Undefined"))
                output += "{0}Name: {1}\n".format(indentation, value.pop("dstName", "Undefined"))
                for name, hint in sorted(value.items()):
                    output += "{0}{1}: {2}\n".format(indentation, name.title(), hint)
                output += "\n"
    return output

def nodes_walker(node, ascendants=False):
    """
    Defines a generator used to walk into nodes hierarchy.

    :param node: Node to walk.
    :type node: object
    :param ascendants: Ascendants instead of descendants will be yielded.
    :type ascendants: bool
    :return: Node.
    :rtype: object
    """

    attribute = "getChildren" if not ascendants else "getParent"
    if not hasattr(node, attribute):
        return

    elements = getattr(node, attribute)
    elements = elements() if isinstance(elements(), list) else [elements()]

    for element in elements:
        if element is None:
            continue

        yield element

        if not hasattr(element, attribute):
            continue

        if not getattr(element, attribute):
            continue

        for sub_element in nodes_walker(element, ascendants=ascendants):
            if sub_element is None:
                continue

            yield sub_element

parameters_walker = nodes_walker

def filter_node_parameters(node, pattern=r".*", flags=0):
    """
    Filters given nodes parameters using given pattern.

    :param nodes: Nodes parameters to search and replace.
    :type nodes: list
    :param pattern: Matching pattern.
    :type pattern: str
    :param flags: Matching regex flags.
    :type flags: int
    :return: Definition success.
    :rtype: bool
    """

    return [parameter for parameter in parameters_walker(node.getParameters()) \
    if re.search(pattern, parameter.getName(), flags)]

def reset_node_parameters(node, pattern=r".*", flags=0):
    """
    Resets given nodes parameters using given pattern.

    :param nodes: Nodes parameters to search and replace.
    :type nodes: list
    :param pattern: Matching pattern.
    :type pattern: str
    :param flags: Matching regex flags.
    :type flags: int
    :return: Definition success.
    :rtype: bool
    """

    for parameter in filter_node_parameters(node, pattern, flags):
        parameter.setUseNodeDefault(True)
    return True

def import_script_node(path):
    """
    Imports given path script node.

    :param path: Script node path.
    :type path: str
    :return: Script node success.
    :rtype: object
    """

    if not os.path.exists(path):
        return

    nodes = NodegraphAPI.GetAllSelectedNodes()
    Katana.KatanaFile.Import(path)
    script_node = NodegraphAPI.GetAllSelectedNodes().pop()
    NodegraphAPI.SetAllSelectedNodes(nodes)
    for node in NodegraphAPI.GetAllEditedNodes():
        NodegraphAPI.SetNodeEdited(node, False)
    NodegraphAPI.SetNodeEdited(script_node, True)
    return script_node

def single_shot_script_node(path, parameter):
    """
    Executes given path script node parameter.

    :param path: Script node path.
    :type path: str
    :return: Definition success.
    :rtype: bool
    """

    if not os.path.exists(path):
        return

    edited_nodes = NodegraphAPI.GetAllEditedNodes()
    script_node = import_script_node(path)
    NodegraphAPI.UserParameters.ExecuteButton(script_node, parameter)
    script_node.delete()
    for node in edited_nodes:
        NodegraphAPI.SetNodeEdited(node, True)
    return True
