import ast
import re

import snippets.libraries.utilities
reload(snippets.libraries.utilities)

NODES_NAMES_MAPPING_TABLE = {"ArnoldShadingNode" : "ArnoldSN",
							"PrmanShadingNode" : "PrmanSN"}

def getDefaultNodeName(node, mappingTable=NODES_NAMES_MAPPING_TABLE):
	"""
	This definition returns given node default name.

	:param nodes: Node to get the default name. ( Node )
	:param mappingTable: Names mapping table. ( Dictionary )
	:return: Node default name. ( String )
	"""

	nodeType = node.getType()
	name = mappingTable.get(nodeType, nodeType)
	if nodeType in ("ArnoldShadingNode", "PrmanShadingNode"):
		coShader = re.sub(r":.*", str(), node.getParameter("nodeType").getValue(0))
		return "{0}_{1}".format( mappingTable.get(coShader, coShader), name)
	else:
		return name

def setNodeName(node, name):
	"""
	This definition sets given node name.

	:param node: Node to set the name. ( Object )
	:param name: Node name. ( String )
	:return: Definition success. ( Boolean )
	"""

	node.setName(name)

	nodeType = node.getType()
	if nodeType in ("ArnoldShadingNode", "PrmanShadingNode"):
		node.getParameter("name").setValue(node.getName(), 0)

	return True

def setNodeNames(nodes, prefix, mappingTable=NODES_NAMES_MAPPING_TABLE, traverse=True):
	"""
	This definition sets given nodes names using given prefix.

	:param nodes: Nodes to set the names. ( List )
	:param prefix: Prefix. ( String )
	:param mappingTable: Names mapping table. ( Dictionary )
	:param traverse: Traverse nodes children. ( Boolean )
	:return: Definition success. ( Boolean )
	"""

	for node in nodes:
		setNodeName(node, "{0}{1}".format(prefix, getDefaultNodeName(node, mappingTable)))
		if not traverse:
			continue

		for childNode in snippets.libraries.utilities.nodesWalker(node):
			setNodeName(childNode, "{0}{1}".format(prefix, getDefaultNodeName(childNode, mappingTable)))
	return True

def searchAndReplaceNodesNames(nodes, searchPattern, replacementPattern, flags=0, traverse=True):
	"""
	This definition search and replace given nodes names.

	:param nodes: Nodes to search and replace. ( List )
	:param searchPattern: Search pattern. ( String )
	:param replacementPattern: Replacement pattern. ( String )
	:param flags: Matching regex flags. ( Integer )
	:param traverse: Traverse nodes children. ( Boolean )
	:return: Definition success. ( Boolean )
	"""

	searchPattern = re.compile(searchPattern)
	for node in nodes:
		setNodeName(node, re.sub(searchPattern, replacementPattern, node.getName(), flags))
		if not traverse:
			continue

		for childNode in snippets.libraries.utilities.nodesWalker(node):
			setNodeName(childNode, re.sub(searchPattern, replacementPattern, childNode.getName(), flags))
	return True

def removeNodesNamesTrailingNumbers(nodes, traverse=True):
	"""
	This definition removes given nodes names trailing numbers.

	:param nodes: Nodes to search and replace. ( List )
	:param traverse: Traverse nodes children. ( Boolean )
	:return: Definition success. ( Boolean )
	"""

	return searchAndReplaceNodesNames(nodes, r"\d+$", str(), traverse=traverse)

def prefixNodesNames(nodes, prefix, traverse=True):
	"""
	This definition prefixes given nodes names using given prefix.

	:param nodes: Nodes to search and replace. ( List )
	:param prefix: Prefix. ( String )
	:param traverse: Traverse nodes children. ( Boolean )
	:return: Definition success. ( Boolean )
	"""

	return searchAndReplaceNodesNames(nodes, r".*", lambda x: "{0}{1}".format(prefix, x.group(0)), traverse=traverse)

def searchAndReplaceHintsParameter(parameter, searchPattern, replacementPattern, flags=0, time=0, keys=None):
	"""
	This definition search and replace given hint parameter.

	:param parameter: Hint parameter to search and replace. ( Object )
	:param searchPattern: Search pattern. ( String )
	:param replacementPattern: Replacement pattern. ( String )
	:param flags: Matching regex flags. ( Integer )
	:param time: Time to set the value to. ( Integer )
	:param keys: Hints keys to search and replace in. ( List )
	:return: Definition success. ( Boolean )
	"""
	
	data = ast.literal_eval(parameter.getValue(time))
	for key, value in data.iteritems():
		if keys and key not in keys:
			continue

		data[key] = re.sub(searchPattern, replacementPattern, value, flags)
	parameter.setValue(str(data), time)
	return True

def searchAndReplaceHintsParameters(nodes, searchPattern, replacementPattern, flags=0, time=0, keys=None, traverse=True):
	"""
	This definition search and replace given nodes hints parameters.

	:param nodes: Nodes to search and replace. ( List )
	:param searchPattern: Search pattern. ( String )
	:param replacementPattern: Replacement pattern. ( String )
	:param flags: Matching regex flags. ( Integer )
	:param time: Time to set the value to. ( Integer )
	:param keys: Hints keys to search and replace in. ( List )
	:param traverse: Traverse nodes children. ( Boolean )
	:return: Definition success. ( Boolean )
	"""

	searchPattern = re.compile(searchPattern)
	for node in nodes:
		for parameter in snippets.libraries.utilities.filterNodeParameters(node, "^hints$"):
			searchAndReplaceHintsParameter(parameter, searchPattern, replacementPattern, flags, time, keys)
		if not traverse:
			continue

		for childNode in snippets.libraries.utilities.nodesWalker(node):
			for parameter in snippets.libraries.utilities.filterNodeParameters(childNode, "^hints$"):
				searchAndReplaceHintsParameter(parameter, searchPattern, replacementPattern, flags, time, keys)
	return True
