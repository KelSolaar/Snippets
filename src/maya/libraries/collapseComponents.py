import inspect
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import re

def stacksHandler(object_):
	"""
	This Decorator Is Used To Handle Various Maya Stacks.

	@param object_: Python Object ( Object )
	@return: Python Function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This Decorator Is Used To Handle Various Maya Stacks.

		@return: Python Object. ( Python )
		"""
		
		cmds.undoInfo(openChunk=True)
		value = object_(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya Produces A Weird Command Error If Not Wrapped Here.
		try:
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")"% (__name__, __name__, object_.__name__), addCommandLabel=object_.__name__)
		except:
			pass
		return value

	return stacksHandlerCall

def getTransform(node, fullPath=True):
	"""
	This Definition Returns Transform Of The Provided Node.

	@param node: Current Object. ( String )
	@param fullPath: Current Full Path State. (Boolean)
	@return: Object Transform. ( String )
	"""
	
	transform = node
	if cmds.nodeType(node) != "transform":
		parents = cmds.listRelatives(node, fullPath=fullPath, parent=True)
		transform = parents[0]
	return transform

def getAverageVector(vectors):
	"""
	This Definition Returns The Average Vector From A List Of Vectors.

	@param vectors: Vectors To Get The Average One. ( List )
	@return: Average Vector. ( List )
	"""
	
	averageVector = [0, 0, 0]
	for vector in vectors:
		for i in range(3):
			averageVector[i] += vector[i]
	for i in range(3):
		averageVector[i]=averageVector[i] / len(vectors)
	return averageVector

def collapseComponents(components, axis=("X", "Y", "Z")):
	"""
	This Definition Collapses The Provided Components.

	@param components: Components To Collapse. ( List )
	@param axis: Collapse Axis. ( Tuple )
	"""
	
	vertices = cmds.ls(cmds.polyListComponentConversion(components, toVertex=True), fl=True)
	barycenters=[]
	barycenters.extend((cmds.xform(vertice, q=True, t=True, ws=True) for vertice in vertices))
	barycenter = getAverageVector(barycenters)
	for vertex in vertices:
		xValue = "X" in axis and barycenter[0] or cmds.xform(vertex, q=True, t=True, ws=True)[0]
		yValue = "Y" in axis and barycenter[1] or cmds.xform(vertex, q=True, t=True, ws=True)[1]
		zValue = "Z" in axis and barycenter[2] or cmds.xform(vertex, q=True, t=True, ws=True)[2]
		
		cmds.xform(vertex, ws=True, t=(xValue, yValue, zValue))

@stacksHandler
def ICollapseComponents():
	"""
	This Definition Is The collapseComponents Method Interface.
	"""
	
	selection = cmds.ls(sl=True, l=True)
	selection and collapseComponents(selection)

def collapseComponentsOnX():
	"""
	This Definition Triggers The collapseComponents Method On X Axis.
	"""
	
	selection = cmds.ls(sl=True, l=True)
	selection and collapseComponents(selection, axis=("X", ))

@stacksHandler
def ICollapseComponentsOnX():
	"""
	This Definition Is The collapseComponentsOnX Method Interface.
	"""
	
	collapseComponentsOnX()

def collapseComponentsOnY():
	"""
	This Definition Triggers The collapseComponents Method On Y Axis.
	"""
	
	selection = cmds.ls(sl=True, l=True)
	selection and collapseComponents(selection, axis=("Y", ))

@stacksHandler
def ICollapseComponentsOnY():
	"""
	This Definition Is The collapseComponentsOnY Method Interface.
	"""
	
	collapseComponentsOnY()
	
def collapseComponentsOnZ():
	"""
	This Definition Triggers The collapseComponents Method On Z Axis.
	"""
	
	selection = cmds.ls(sl=True, l=True)
	selection and collapseComponents(selection, axis=("Z", ))

@stacksHandler
def ICollapseComponentsOnZ():
	"""
	This Definition Is The collapseComponentsOnZ Method Interface.
	"""
	
	collapseComponentsOnZ()
