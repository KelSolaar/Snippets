import NodegraphAPI
import RenderingAPI
import os
import re
import sys

import snippets.libraries.utilities

def getGiggleMetaData(path):
	"""
	Returns the Giggle metaData of give '.slo' file path.

	:param path: File get the MetaData from.
	:type path: str
	:return: MetaData.
	:rtype: list
	"""

	metaData = []
	with open(path) as file:
		for line in file:
			if not re.match(r"\s*\$meta_\<ggl\>", line):
				continue

			metaData.append(line.split("\\n")[1:-1])
	return metaData

def listGiggleMetaData(metaData, indentation="\t"):
	"""
	Lists given metaData.

	:param metaData: MetaData to list.
	:type metaData: list
	:return: Formated metaData.
	:rtype: str
	"""

	output = str()
	entryCounter = 0
	for token in metaData:
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
			output += "{0}Entry '{1}': {2}\n".format(indentation, entryCounter, value)
			entryCounter +=1
	return output

def getCoshaderSloFile(coshader):
	"""
	Returns gviven coshader '.slo' file path.

	:param coshader: Coshader name.
	:type coshader: str
	:return: Coshader '.slo' file path.
	:rtype: str
	"""

	rendererInfo = RenderingAPI.RenderPlugins.GetInfoPluginName("prman")
	plugin = RenderingAPI.RendererInfo.GetPlugin(rendererInfo)
	return plugin.getRendererObjectInfo(coshader).getFullPath()

def listNodeGiggleMetaData(node):
	"""
	Lists given node metaData.

	:param node: Node to list metaData.
	:type node: object
	:return: Formated metaData list.
	:rtype: str
	"""

	output = str()
	if node.getType() == "PrmanShadingNode":
		path = getCoshaderSloFile(node.getParameter("nodeType").getValue(0))
		if os.path.exists(path):
			for metaData in getGiggleMetaData(path):
				output += listGiggleMetaData(metaData)
	return output

def listNodesGiggleMetaData(nodes, traverse=True):
	"""
	Lists given nodes metaData.

	:param node: Node to list metaData.
	:type node: object
	:param traverse: Traverse nodes children.
	:type traverse: bool
	:return: Formated metaData.
	:rtype: str
	"""

	output = str()
	for node in nodes:
		output += listNodeGiggleMetaData(node)
		if not traverse:
			continue

		for childNode in snippets.libraries.utilities.nodesWalker(node):
			output += listNodeGiggleMetaData(childNode)
	return output
	
def lisObjectNames():
	"""
	Lists PRMan object names ( Shaders ).

	:return: PRMan Object names.
	:rtype: list
	"""
	
	return snippets.libraries.utilities.listRendererObjectNames("prman")
