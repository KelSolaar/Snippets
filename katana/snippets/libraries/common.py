import ast
import re

import snippets.libraries.utilities

def resetNodesParameters(nodes, traverse=True):
	"""
	This definition resets given nodes parameters.

	:param nodes: Nodes to search and replace. ( List )
	:param traverse: Traverse nodes children. ( Boolean )
	:return: Definition success. ( Boolean )
	"""

	for node in nodes:
		snippets.libraries.utilities.resetNodeParameters(node)
		if not traverse:
			continue

		for childNode in snippets.libraries.utilities.nodesWalker(node):
			snippets.libraries.utilities.resetNodeParameters(childNode)
	return True