import NodegraphAPI
import RenderingAPI
import os
import re
import sys

import snippets.libraries.utilities


def get_giggle_meta_data(path):
    """
    Returns the Giggle metadata of give '.slo' file path.

    :param path: File get the MetaData from.
    :type path: str
    :return: MetaData.
    :rtype: list
    """

    metadata = []
    with open(path) as file:
        for line in file:
            if not re.match(r"\s*\$meta_\<ggl\>", line):
                continue

            metadata.append(line.split("\\n")[1:-1])
    return metadata


def list_giggle_meta_data(metadata, indentation="\t"):
    """
    Lists given metadata.

    :param metadata: MetaData to list.
    :type metadata: list
    :return: Formated metadata.
    :rtype: str
    """

    output = ""
    entry_counter = 0
    for token in metadata:
        search = re.search(r"\<(?P<key>\w+)\>(?P<value>.*)\</\w+\>", token)
        if not search:
            continue

        key, value = search.group("key"), search.group("value")
        if key in ("name", "label"):
            output += "{0}:\n".format(value)
        elif key == "description":
            output += "{0}Description: {1}\n".format(indentation, value)
        elif key == "type":
            output += "{0}Type: {1}\n".format(indentation, value)
        elif key == "default":
            output += "{0}Default Value: {1}\n".format(indentation, value)
        elif key == "entry":
            output += "{0}Entry '{1}': {2}\n".format(indentation, entry_counter, value)
            entry_counter += 1
    return output


def get_coshader_slo_file(coshader):
    """
    Returns gviven coshader '.slo' file path.

    :param coshader: Coshader name.
    :type coshader: str
    :return: Coshader '.slo' file path.
    :rtype: str
    """

    renderer_info = RenderingAPI.RenderPlugins.GetInfoPluginName("prman")
    plugin = RenderingAPI.RendererInfo.GetPlugin(renderer_info)
    return plugin.getRendererObjectInfo(coshader).getFullPath()


def list_node_giggle_metadata(node):
    """
    Lists given node metadata.

    :param node: Node to list metadata.
    :type node: object
    :return: Formated metadata list.
    :rtype: str
    """

    output = ""
    if node.getType() == "PrmanShadingNode":
        path = get_coshader_slo_file(node.getParameter("nodeType").getValue(0))
        if os.path.exists(path):
            for metadata in get_giggle_meta_data(path):
                output += list_giggle_meta_data(metadata)
    return output


def list_nodes_giggle_metadata(nodes, traverse=True):
    """
    Lists given nodes metadata.

    :param node: Node to list metadata.
    :type node: object
    :param traverse: Traverse nodes children.
    :type traverse: bool
    :return: Formated metadata.
    :rtype: str
    """

    output = ""
    for node in nodes:
        output += list_node_giggle_metadata(node)
        if not traverse:
            continue

        for child_node in snippets.libraries.utilities.nodes_walker(node):
            output += list_node_giggle_metadata(child_node)
    return output


def list_object_names():
    """
    Lists PRMan object names.

    :return: PRMan Object names.
    :rtype: list
    """

    return snippets.libraries.utilities.list_renderer_object_names("prman")
