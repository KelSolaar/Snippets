import Katana
import NodegraphAPI
import UI4
import ast
import os
import re

def consolePrint(*args):
	"""
	This definition prints given message to KatanaConsole.

	:param \*args: Arguments. ( \* )
	"""

	UI4.App.Tabs.FindTopTab("Python").printMessage(" ".join(map(str, args)))

def listNode(node, indentation="\t", tabLevel= -1):
	"""
	This definition lists the current node and its children.

	:param node: Node to list. ( Object )
	:param indentation: Indentation character. ( String )
	:param tabLevel: Indentation level. ( Integer )
	:return: Node listing. ( String )
	"""

	attribute = "getChildren"

	output = str()
	tabLevel += 1

	for i in range(tabLevel):
		output += indentation

	output += "|----'{0}'\n".format(node.getName())

	if hasattr(node,attribute):
		for child in getattr(node, attribute)() or []:
			if child is None:
				continue

			output += listNode(child, indentation, tabLevel)

	tabLevel -= 1
	return output

def listHintsParameters(node, outputAsTree=False, indentation="\t", time=0):
	"""
	This definition lists given node and children hints parameters.

	:param node: Node to list hint parameters. ( Object )
	:param outputAsTree: Output as groups outputAsTree. ( Boolean )
	:param indentation: Indentation character. ( String )
	:param time: Time to get the hints parameters value. ( Integer )
	:return: Hints parameters listing. ( String )
	"""

	nodes = [node]
	nodes.extend(list(nodesWalker(node)))

	output = str()

	if outputAsTree:
		hints = {}
		for node in nodes:
			for parameter in filterNodeParameters(node, "^hints$"):
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
			for parameter in filterNodeParameters(node, "^hints$"):
				value = ast.literal_eval(parameter.getValue(time))
				output += "{0}.{1}:\n".format(node.getName(), parameter.getParent().getName())
				output += "{0}Group: {1}\n".format(indentation, value.pop("dstPage", "Undefined"))
				output += "{0}Name: {1}\n".format(indentation, value.pop("dstName", "Undefined"))
				for name, hint in sorted(value.items()):
					output += "{0}{1}: {2}\n".format(indentation, name.title(), hint)
				output += "\n"
	return output

def nodesWalker(node, ascendants=False):
	"""
	This definition is a generator used to walk into nodes hierarchy.

	:param node: Node to walk. ( Object )
	:param ascendants: Ascendants instead of descendants will be yielded. ( Boolean )
	:return: Node. ( Object )
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

		for subElement in nodesWalker(element, ascendants=ascendants):
			if subElement is None:
				continue

			yield subElement

parametersWalker = nodesWalker

def filterNodeParameters(node, pattern, flags=0):
	"""
	This definition filters given nodes parameters using given pattern.

	:param nodes: Nodes to search and replace. ( List )
	:param pattern: Matching pattern. ( String )
	:param flags: Matching regex flags. ( Integer )
	:return: Definition success. ( Boolean )
	"""

	return [parameter for parameter in parametersWalker(node.getParameters()) \
	if re.search(pattern, parameter.getName(), flags)]

def importScriptNode(path):
	"""
	This definition imports given path script node.

	:param path: Script node path. ( String )
	:return: Definition success. ( Boolean )
	"""
	
	if not os.path.exists(path):
		return

	nodes = NodegraphAPI.GetAllSelectedNodes()
	Katana.KatanaFile.Import(path)
	scriptNode = NodegraphAPI.GetAllSelectedNodes().pop()
	NodegraphAPI.SetAllSelectedNodes(nodes)
	for node in NodegraphAPI.GetAllEditedNodes():
		NodegraphAPI.SetNodeEdited(node, False)
	NodegraphAPI.SetNodeEdited(scriptNode, True)