import ast
import re

import snippets.libraries.utilities

NODES_NAMES_MAPPING_TABLE = {"ArnoldShadingNode" : "ArnoldSN",
							"PrmanShadingNode" : "PrmanSN"}

def getDefaultNodeName(node, mappingTable=NODES_NAMES_MAPPING_TABLE):
	"""
	Returns given node default name.

	:param nodes: Node to get the default name.
	:type nodes: Node
	:param mappingTable: Names mapping table.
	:type mappingTable: dict
	:return: Node default name.
	:rtype: str
	"""

	nodeType = node.getType()
	name = mappingTable.get(nodeType, nodeType)
	if nodeType in ("ArnoldShadingNode", "PrmanShadingNode"):
		coShader = re.sub(r":.*", "", node.getParameter("nodeType").getValue(0))
		return "{0}_{1}".format( mappingTable.get(coShader, coShader), name)
	else:
		return name

def setNodeName(node, name):
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

	nodeType = node.getType()
	if nodeType in ("ArnoldShadingNode", "PrmanShadingNode"):
		node.getParameter("name").setValue(node.getName(), 0)

	return True

def setNodeNames(nodes, prefix, mappingTable=NODES_NAMES_MAPPING_TABLE, traverse=True):
	"""
	Sets given nodes names using given prefix.

	:param nodes: Nodes to set the names.
	:type nodes: list
	:param prefix: Prefix.
	:type prefix: str
	:param mappingTable: Names mapping table.
	:type mappingTable: dict
	:param traverse: Traverse nodes children.
	:type traverse: bool
	:return: Definition success.
	:rtype: bool
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
	Search and replace given nodes names.

	:param nodes: Nodes to search and replace.
	:type nodes: list
	:param searchPattern: Search pattern.
	:type searchPattern: str
	:param replacementPattern: Replacement pattern.
	:type replacementPattern: str
	:param flags: Matching regex flags.
	:type flags: int
	:param traverse: Traverse nodes children.
	:type traverse: bool
	:return: Definition success.
	:rtype: bool
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
	Removes given nodes names trailing numbers.

	:param nodes: Nodes to search and replace.
	:type nodes: list
	:param traverse: Traverse nodes children.
	:type traverse: bool
	:return: Definition success.
	:rtype: bool
	"""

	return searchAndReplaceNodesNames(nodes, r"\d+$", "", traverse=traverse)

def prefixNodesNames(nodes, prefix, traverse=True):
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

	return searchAndReplaceNodesNames(nodes, r".*", lambda x: "{0}{1}".format(prefix, x.group(0)), traverse=traverse)

def searchAndReplaceHintsParameter(parameter, searchPattern, replacementPattern, flags=0, time=0, keys=None):
	"""
	Search and replace given hint parameter.

	:param parameter: Hint parameter to search and replace.
	:type parameter: object
	:param searchPattern: Search pattern.
	:type searchPattern: str
	:param replacementPattern: Replacement pattern.
	:type replacementPattern: str
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

		data[key] = re.sub(searchPattern, replacementPattern, value, flags)
	parameter.setValue(str(data), time)
	return True

def searchAndReplaceHintsParameters(nodes, searchPattern, replacementPattern, flags=0, time=0, keys=None, traverse=True):
	"""
	Search and replace given nodes hints parameters.

	:param nodes: Nodes to search and replace.
	:type nodes: list
	:param searchPattern: Search pattern.
	:type searchPattern: str
	:param replacementPattern: Replacement pattern.
	:type replacementPattern: str
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
