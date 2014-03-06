import inspect
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import re

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
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
	Handles Maya stacks.

	:param object: Python object.
	:type object: object
	:return: Python function.
	:rtype: object
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		Handles Maya stacks.

		:return: Python object.
		:rtype: object
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
	Returns transform of the given node.

	:param node: Current object.
	:type node: str
	:param fullPath: Current full path state.
	:type fullPath: bool
	:return: Object transform.
	:rtype: str
	"""

	transform = node
	if cmds.nodeType(node) != "transform":
		parents = cmds.listRelatives(node, fullPath=fullPath, parent=True)
		transform = parents[0]
	return transform

def getAverageVector(vectors):
	"""
	Returns the average vector from a list of vectors.

	:param vectors: Vectors to get the average one.
	:type vectors: list
	:return: Average vector.
	:rtype: list
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
	Collapses the given Components.

	:param components: Components to collapse.
	:type components: list
	:param axis: Collapse axis.
	:type axis: tuple
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
	Defines the collapseComponents definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and collapseComponents(selection)

def collapseComponentsOnX():
	"""
	Triggers the collapseComponents method on x axis.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and collapseComponents(selection, axis=("X",))

@stacksHandler
def ICollapseComponentsOnX():
	"""
	Defines the collapseComponentsOnX definition Interface.
	"""

	collapseComponentsOnX()

def collapseComponentsOnY():
	"""
	Triggers the collapseComponents method on y axis.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and collapseComponents(selection, axis=("Y",))

@stacksHandler
def ICollapseComponentsOnY():
	"""
	Defines the collapseComponentsOnY definition Interface.
	"""

	collapseComponentsOnY()

def collapseComponentsOnZ():
	"""
	Triggers the collapseComponents method on z axis.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and collapseComponents(selection, axis=("Z",))

@stacksHandler
def ICollapseComponentsOnZ():
	"""
	Defines the collapseComponentsOnZ definition Interface.
	"""

	collapseComponentsOnZ()
