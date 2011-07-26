#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**snapOnClosestVertex.py**

**Platform :**
	Windows, Linux, Mac Os X.

**Description :**
	Snap On Closest Vertex Module.

**Others :**

"""

#***********************************************************************************************
#***	Python Begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports.
#***********************************************************************************************
import math
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.mel as mel
import re
import functools
#***********************************************************************************************
#***	Overall Variables.
#***********************************************************************************************
TOLERANCE=64
MAXIMUM_SEARCH_DISTANCE=2**32-1

#***********************************************************************************************
#***	Module Classes And Definitions.
#***********************************************************************************************
def stacksHandler(object):
	"""
	This Decorator Is Used To Handle Various Maya Stacks.

	@param object: Python Object. ( Object )
	@return: Python Function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This Decorator Is Used To Handle Various Maya Stacks.

		@return: Python Object. ( Python )
		"""
		
		cmds.undoInfo(openChunk=True)
		value = object(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya Produces A Weird Command Error If Not Wrapped Here.
		try:
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")"% (__name__, __name__, object.__name__), addCommandLabel=object.__name__)
		except:
			pass
		return value

	return stacksHandlerCall

def getMPoint(point):
	"""
	This Definition Returns An MPoint.

	@param point: Point. ( List )
	@return: MPoint ( MVector )
	"""
	
	return OpenMaya.MPoint(point[0], point[1], point[2])

def norme(pointA, pointB):
	"""
	This Definition Returns The Norme Of A Vector.

	@param pointA: Point A. ( List )
	@param pointB: Point B. ( List )
	@return: Norme ( Float )
	"""
	
	mPointA = getMPoint(pointA)
	mPointB = getMPoint(pointB)
	mVector = mPointA - mPointB
	return mVector.length()

def getShapes(object, fullPathState = False, noIntermediateState = True):
	"""
	This Definition Returns Shapes Of The Provided Object.

	@param object: Current Object. ( String )
	@param fullPath: Current Full Path State. ( Boolean )
	@param noIntermediate: Current No Intermediate State. ( Boolean )
	@return: Objects Shapes. ( List )
	"""

	objectShapes = []
	shapes = cmds.listRelatives(object, fullPath = fullPathState, shapes = True, noIntermediate = noIntermediateState)
	if shapes != None:
		objectShapes = shapes

	return objectShapes
	
@stacksHandler
def getReferenceObject_OnClicked(state=None):
	"""
	This Definition Is Triggered By The getReferenceObject Button When Clicked.
	
	@param state: Button State. ( Boolean )
	"""
	
	selection = cmds.ls(sl=True, type="transform")
	
	if selection :
		cmds.textField("referenceObject_TextField", edit=True, text=selection[0])

def loadPlugin(plugin):
	"""
	This Function Loads A Plugin.

	@param plugin: Plugin To Load. (String)
	"""
	
	not cmds.pluginInfo(plugin, query=True, loaded=True) and cmds.loadPlugin(plugin)
	
def snapComponentsOnClosestVertex(referenceObject, components, tolerance) :
	"""
	This Function Snaps Vertices Onto The Reference Object Vertices.

	@param referenceObject: Reference Mesh. (String)
	@param components: Components. (List)
	"""
	
	vertices = cmds.ls(cmds.polyListComponentConversion(components, toVertex=True), fl=True)

	progressBar = mel.eval("$container=$gMainProgressBar");

	cmds.progressBar(progressBar, edit=True, beginProgress=True, isInterruptable=True, status="Snapping Vertices ...", maxValue=len(vertices)) 
	
	loadPlugin("nearestPointOnMesh")

	nearestPointOnMeshNode=mel.eval("nearestPointOnMesh " +  referenceObject)
	
	for vertex in vertices :
		if cmds.progressBar(progressBar, query=True, isCancelled=True) :
			break
		
		closestDistance=MAXIMUM_SEARCH_DISTANCE

		vertexPosition = cmds.pointPosition(vertex, world=True)
		cmds.setAttr(nearestPointOnMeshNode + ".inPosition", vertexPosition[0], vertexPosition[1], vertexPosition[2])
		associatedFaceId = cmds.getAttr(nearestPointOnMeshNode + ".nearestFaceIndex")
		vtxsFaces = cmds.filterExpand(cmds.polyListComponentConversion((referenceObject + ".f[" + str(associatedFaceId) + "]"), fromFace=True,  toVertexFace=True ), sm=70, expand=True)
		
		closestPosition = []
		for vtxsFace in vtxsFaces :
			associatedVtx = cmds.polyListComponentConversion(vtxsFace, fromVertexFace=True, toVertex=True)
			associatedVtxPosition = cmds.pointPosition(associatedVtx, world=True)
			
			distance = norme(vertexPosition, associatedVtxPosition)

			if distance < closestDistance :
				closestDistance=distance
				closestPosition=associatedVtxPosition
			
			if closestDistance < tolerance :
				cmds.move(closestPosition[0], closestPosition[1], closestPosition[2], vertex, worldSpace=True)

		cmds.progressBar(progressBar, edit=True, step=1)
	
	cmds.progressBar(progressBar, edit=True, endProgress=True)

	cmds.delete(nearestPointOnMeshNode)

@stacksHandler
def snapIt_Button_OnClicked(state=None):
	"""
	This Definition Is Triggered By The snapIt Button When Clicked.
	
	@param state: Button State. ( Boolean )
	"""
	
	referenceObject = cmds.textField("referenceObject_TextField", query=True, text=True)

	referenceObjectShapes = cmds.objExists(referenceObject) and getShapes(referenceObject) or None
	
	selection = cmds.ls(sl=True, fl=True)
	referenceObjectShapes and selection and snapComponentsOnClosestVertex(referenceObjectShapes[0], selection, TOLERANCE)

def snapOnClosestVertex_Window():
	"""
	This Definition Creates The Snap On Closest Vertex Window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("snapOnClosestVertex_Window", exists=True)):
		cmds.deleteUI("snapOnClosestVertex_Window")

	cmds.window("snapOnClosestVertex_Window",
		title="Snap On Closest Vertex",
		width=320)

	spacing = 5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
	cmds.text(label="Reference Object:")
	referenceObject_TextField = cmds.textField("referenceObject_TextField")
	cmds.button("getReferenceObject_Button", label="Get Reference Object!", command=getReferenceObject_OnClicked)
	cmds.setParent(topLevel=True)

	cmds.separator(style="single")	
	
	cmds.button("snapIt_Button", label="Snap It !", al="center", command=snapIt_Button_OnClicked)

	cmds.showWindow("snapOnClosestVertex_Window")
	cmds.windowPref(enableAll=True)

def snapOnClosestVertex():
	"""
	This Definition Launches The Snap On Closest Vertex Main Window.
	"""
	
	snapOnClosestVertex_Window()

@stacksHandler
def ISnapOnClosestVertex():
	"""
	This Definition Is The snapOnClosestVertex Method Interface.
	"""

	snapOnClosestVertex()

#***********************************************************************************************
#***	Python End.
#***********************************************************************************************
