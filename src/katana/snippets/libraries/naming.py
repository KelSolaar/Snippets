import re

import snippets.libraries.utilities

NODES_NAMES_MAPPING_TABLE = {"PrmanShadingNode" : "PrmanSN"}

def getDefaultNodeName(node, mappingTable=NODES_NAMES_MAPPING_TABLE):
	"""
	This definition returns given node default name.

	:param nodes: Node to get the default name. ( Node )
	:param mappingTable: Names mapping table. ( Dictionary )
	:return: Node default name. ( String )
	"""
	
	nodeType = node.getType()
	name = mappingTable.get(nodeType, nodeType)
	if nodeType == "PrmanShadingNode":
		coShader = re.sub(r":.*", str(), node.getParameter("nodeType").getValue(0))
		return "{0}_{1}".format( mappingTable.get(coShader, coShader), name)
	else:
		return name
		
def setNodeNames(nodes, prefix, mappingTable=NODES_NAMES_MAPPING_TABLE, traverse=True):
	"""
	This definition sets given nodes names using given prefix.

	:param nodes: Nodes to search and replace. ( List )
	:param prefix: Prefix. ( String )
	:param mappingTable: Names mapping table. ( Dictionary )
	:param traverse: Traverse nodes children. ( Boolean )
	:return: Definition success. ( Boolean )
	"""

	for node in nodes:
		node.setName("{0}{1}".format(prefix, getDefaultNodeName(node, mappingTable)))
		if not traverse:
			continue

		for childNode in snippets.libraries.utilities.nodesWalker(node):
			childNode.setName("{0}{1}".format(prefix, getDefaultNodeName(childNode, mappingTable)))
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
		node.setName(re.sub(searchPattern, replacementPattern, node.getName(), flags))
		if not traverse:
			continue

		for childNode in snippets.libraries.utilities.nodesWalker(node):
			childNode.setName(re.sub(searchPattern, replacementPattern, childNode.getName(), flags))
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
