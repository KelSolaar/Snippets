import NodegraphAPI
import RenderingAPI
import os
import re
import sys

import snippets.libraries.utilities

def getGiggleMetaData(path):
	"""
	This definition returns the Giggle metaData of give '.slo' file path.

	:param path: File get the MetaData from. ( String )
	:return: MetaData. ( List )
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
	This definition lists given metaData.

	:param metaData: MetaData to list. ( List )
	:return: Formated metaData. ( String )
	"""

	output = ""
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
	This definition returns gviven coshader '.slo' file path.

	:param coshader: Coshader name. ( String )
	:return: Coshader '.slo' file path. ( String )
	"""

	rendererInfo = RenderingAPI.RenderPlugins.GetInfoPluginName("prman")
	plugin = RenderingAPI.RendererInfo.GetPlugin(rendererInfo)
	return plugin.getRendererObjectInfo(coshader).getFullPath()

def listNodeGiggleMetaData(node):
	"""
	This definition lists given node metaData.

	:param node: Node to list metaData. ( Object )
	:return: Formated metaData list. ( String )
	"""

	output = ""
	if node.getType() == "PrmanShadingNode":
		path = getCoshaderSloFile(node.getParameter("nodeType").getValue(0))
		if os.path.exists(path):
			for metaData in getGiggleMetaData(path):
				output += listGiggleMetaData(metaData)
	return output

def listNodesGiggleMetaData(nodes, traverse=True):
	"""
	This definition lists given nodes metaData.

	:param node: Node to list metaData. ( Object )
	:param traverse: Traverse nodes children. ( Boolean )
	:return: Formated metaData. ( String )
	"""

	output = ""
	for node in nodes:
		output += listNodeGiggleMetaData(node)
		if not traverse:
			continue

		for childNode in snippets.libraries.utilities.nodesWalker(node):
			output += listNodeGiggleMetaData(childNode)
	return output
	
def lisObjectNames():
	"""
	This definition lists PRMan object names ( Shaders ).

	:return: PRMan Object names. ( List )
	"""
	
	return snippets.libraries.utilities.listRendererObjectNames("prman")
