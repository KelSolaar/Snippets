import ast
import re

import snippets.libraries.utilities

def resetNodesParameters(nodes, traverse=True):
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
		snippets.libraries.utilities.resetNodeParameters(node)
		if not traverse:
			continue

		for childNode in snippets.libraries.utilities.nodesWalker(node):
			snippets.libraries.utilities.resetNodeParameters(childNode)
	return True