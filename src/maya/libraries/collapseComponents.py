import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import re

def getTransform(node, fullPath=True):
	'''
	This Definition Returns Transform Of The Provided Node.

	@param node: Current Object. ( String )
	@param fullPath: Current Full Path State. (Boolean)
	@return: Object Transform. ( String )
	'''
	
	transform = node
	if cmds.nodeType(node) != "transform":
		parents = cmds.listRelatives(node, fullPath=fullPath, parent=True)
		transform = parents[0]
	return transform

def getAverageVector(vectors):
	'''
	This Definition Returns The Average Vector From A List Of Vectors.

	@param vectors: Vectors To Get The Average One. ( List )
	@return: Average Vector. ( List )
	'''
	
	averageVector = [0, 0, 0]
	for vector in vectors:
		for i in range(3):
			averageVector[i] += vector[i]
	for i in range(3):
		averageVector[i]=averageVector[i] / len(vectors)
	return averageVector

def collapseComponents(components, axis=("X", "Y", "Z")):
	'''
	This Definition Collapses The Provided Components.

	@param components: Components To Collapse. ( List )
	@param axis: Collapse Axis. ( Tuple )
	'''
	
	objects = list(set(cmds.ls(components, o=True)))
	if objects:
		barycenters=[]
		for object in objects:
			transform = getTransform(object)
			vertices = cmds.ls(cmds.polyListComponentConversion([component for component in components if re.search(transform, component)], toVertex=True), fl=True)
			barycenters.extend((cmds.xform(vertice, q=True, t=True, ws=True) for vertice in vertices))

		barycenter = getAverageVector(barycenters)
		print barycenter
		for vertex in vertices:
			xValue = "X" in axis and barycenter[0] or cmds.xform(vertex, q=True, t=True, ws=True)[0]
			yValue = "Y" in axis and barycenter[1] or cmds.xform(vertex, q=True, t=True, ws=True)[1]
			zValue = "Z" in axis and barycenter[2] or cmds.xform(vertex, q=True, t=True, ws=True)[2]

			cmds.xform(vertex, a=True, t=(xValue, yValue, zValue))

def ICollapseComponents():
	'''
	This Definition Is The collapseComponents Method Interface.
	'''
	
	collapseComponents(cmds.ls(sl=True))


def collapseComponentsOnX():
	'''
	This Definition Triggers The collapseComponents Method On X Axis.
	'''
	
	collapseComponents(cmds.ls(sl=True), axis=("X", ))

def ICollapseComponentsOnX():
	'''
	This Definition Is The collapseComponentsOnX Method Interface.
	'''
	
	collapseComponentsOnX()

def collapseComponentsOnY():
	'''
	This Definition Triggers The collapseComponents Method On Y Axis.
	'''
	
	collapseComponents(cmds.ls(sl=True), axis=("Y", ))

def ICollapseComponentsOnY():
	'''
	This Definition Is The collapseComponentsOnY Method Interface.
	'''
	
	collapseComponentsOnY()
	
def collapseComponentsOnZ():
	'''
	This Definition Triggers The collapseComponents Method On Z Axis.
	'''
	
	collapseComponents(cmds.ls(sl=True), axis=("Z", ))

def ICollapseComponentsOnZ():
	'''
	This Definition Is The collapseComponentsOnZ Method Interface.
	'''
	
	collapseComponentsOnZ()