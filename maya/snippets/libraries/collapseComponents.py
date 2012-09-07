import inspect
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import re

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacksHandler",
			"getTransform",
			"getAverageVector",
			"collapseComponents",
			"ICollapseComponents",
			"collapseComponentsOnX",
			"ICollapseComponentsOnX",
			"collapseComponentsOnY",
			"ICollapseComponentsOnY",
			"collapseComponentsOnZ",
			"ICollapseComponentsOnZ"]

def stacksHandler(object):
	"""
	This decorator is used to handle various Maya stacks.

	:param object: Python object. ( Object )
	:return: Python function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This decorator is used to handle various Maya stacks.

		:return: Python object. ( Python )
		"""

		cmds.undoInfo(openChunk=True)
		value = object(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya produces a weird command error if not wrapped here.
		try:
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")" % (__name__, __name__, object.__name__), addCommandLabel=object.__name__)
		except:
			pass
		return value

	return stacksHandlerCall

def getTransform(node, fullPath=True):
	"""
	This definition returns transform of the given node.

	:param node: Current object. ( String )
	:param fullPath: Current full path state. (Boolean)
	:return: Object transform. ( String )
	"""

	transform = node
	if cmds.nodeType(node) != "transform":
		parents = cmds.listRelatives(node, fullPath=fullPath, parent=True)
		transform = parents[0]
	return transform

def getAverageVector(vectors):
	"""
	This definition returns the average vector from a list of vectors.

	:param vectors: Vectors to get the average one. ( List )
	:return: Average vector. ( List )
	"""

	averageVector = [0, 0, 0]
	for vector in vectors:
		for i in range(3):
			averageVector[i] += vector[i]
	for i in range(3):
		averageVector[i] = averageVector[i] / len(vectors)
	return averageVector

def collapseComponents(components, axis=("X", "Y", "Z")):
	"""
	This definition collapses the given Components.

	:param components: Components to collapse. ( List )
	:param axis: Collapse axis. ( Tuple )
	"""

	vertices = cmds.ls(cmds.polyListComponentConversion(components, toVertex=True), fl=True)
	barycenters = []
	barycenters.extend((cmds.xform(vertex, q=True, t=True, ws=True) for vertex in vertices))
	barycenter = getAverageVector(barycenters)
	for vertex in vertices:
		xValue = "X" in axis and barycenter[0] or cmds.xform(vertex, q=True, t=True, ws=True)[0]
		yValue = "Y" in axis and barycenter[1] or cmds.xform(vertex, q=True, t=True, ws=True)[1]
		zValue = "Z" in axis and barycenter[2] or cmds.xform(vertex, q=True, t=True, ws=True)[2]

		cmds.xform(vertex, ws=True, t=(xValue, yValue, zValue))

@stacksHandler
def ICollapseComponents():
	"""
	This definition is the collapseComponents definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and collapseComponents(selection)

def collapseComponentsOnX():
	"""
	This definition triggers the collapseComponents method on x axis.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and collapseComponents(selection, axis=("X",))

@stacksHandler
def ICollapseComponentsOnX():
	"""
	This definition is the collapseComponentsOnX definition Interface.
	"""

	collapseComponentsOnX()

def collapseComponentsOnY():
	"""
	This definition triggers the collapseComponents method on y axis.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and collapseComponents(selection, axis=("Y",))

@stacksHandler
def ICollapseComponentsOnY():
	"""
	This definition is the collapseComponentsOnY definition Interface.
	"""

	collapseComponentsOnY()

def collapseComponentsOnZ():
	"""
	This definition triggers the collapseComponents method on z axis.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and collapseComponents(selection, axis=("Z",))

@stacksHandler
def ICollapseComponentsOnZ():
	"""
	This definition is the collapseComponentsOnZ definition Interface.
	"""

	collapseComponentsOnZ()
