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
	Snap on closest vertex Module.

**Others :**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import math
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.mel as mel
import re
import functools
#***********************************************************************************************
#***	Overall variables.
#***********************************************************************************************
TOLERANCE=64
MAXIMUM_SEARCH_DISTANCE=2**32-1

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
def stacksHandler(object):
	"""
	This decorator is used to handle various Maya stacks.

	@param object: Python object. ( Object )
	@return: Python function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This decorator is used to handle various Maya stacks.

		@return: Python object. ( Python )
		"""

		cmds.undoInfo(openChunk=True)
		value = object(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya produces a weird command error if not wrapped here.
		try:
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")"% (__name__, __name__, object.__name__), addCommandLabel=object.__name__)
		except:
			pass
		return value

	return stacksHandlerCall

def getMPoint(point):
	"""
	This definition returns an MPoint.

	@param point: Point. ( List )
	@return: MPoint ( MVector )
	"""

	return OpenMaya.MPoint(point[0], point[1], point[2])

def norme(pointA, pointB):
	"""
	This definition returns the norme of a vector.

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
	This definition returns shapes of the provided object.

	@param object: Current object. ( String )
	@param fullPath: Current full path state. ( Boolean )
	@param noIntermediate: Current no intermediate state. ( Boolean )
	@return: Objects shapes. ( List )
	"""

	objectShapes = []
	shapes = cmds.listRelatives(object, fullPath = fullPathState, shapes = True, noIntermediate = noIntermediateState)
	if shapes != None:
		objectShapes = shapes

	return objectShapes

@stacksHandler
def getReferenceObject_button_OnClicked(state=None):
	"""
	This definition is triggered by the getReferenceObject_button button when clicked.

	@param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, type="transform")

	if selection :
		cmds.textField("referenceObject_textField", edit=True, text=selection[0])

def loadPlugin(plugin):
	"""
	This function loads a plugin.

	@param plugin: Plugin to load. (String)
	"""

	not cmds.pluginInfo(plugin, query=True, loaded=True) and cmds.loadPlugin(plugin)

def snapComponentsOnClosestVertex(referenceObject, components, tolerance) :
	"""
	This function snaps vertices onto the reference object vertices.

	@param referenceObject: Reference mesh. (String)
	@param components: Components. (List)
	"""

	vertices = cmds.ls(cmds.polyListComponentConversion(components, toVertex=True), fl=True)

	progressBar = mel.eval("$container=$gMainProgressBar");

	cmds.progressBar(progressBar, edit=True, beginProgress=True, isInterruptable=True, status="Snapping vertices ...", maxValue=len(vertices))

	loadPlugin("nearestPointOnMesh")

	nearestPointOnMeshNode=mel.eval("nearestPointOnMesh " + referenceObject)

	for vertex in vertices :
		if cmds.progressBar(progressBar, query=True, isCancelled=True) :
			break

		closestDistance=MAXIMUM_SEARCH_DISTANCE

		vertexPosition = cmds.pointPosition(vertex, world=True)
		cmds.setAttr(nearestPointOnMeshNode + ".inPosition", vertexPosition[0], vertexPosition[1], vertexPosition[2])
		associatedFaceId = cmds.getAttr(nearestPointOnMeshNode + ".nearestFaceIndex")
		vtxsFaces = cmds.filterExpand(cmds.polyListComponentConversion((referenceObject + ".f[" + str(associatedFaceId) + "]"), fromFace=True,	toVertexFace=True ), sm=70, expand=True)

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
def snapIt_button_OnClicked(state=None):
	"""
	This definition is triggered by the snapIt_button button when clicked.

	@param state: Button state. ( Boolean )
	"""

	referenceObject = cmds.textField("referenceObject_textField", query=True, text=True)

	referenceObjectShapes = cmds.objExists(referenceObject) and getShapes(referenceObject) or None

	selection = cmds.ls(sl=True, fl=True)
	referenceObjectShapes and selection and snapComponentsOnClosestVertex(referenceObjectShapes[0], selection, TOLERANCE)

def snapOnClosestVertex_window():
	"""
	This definition creates the 'Snap On Closest Vertex' vertex window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("snapOnClosestVertex_window", exists=True)):
		cmds.deleteUI("snapOnClosestVertex_window")

	cmds.window("snapOnClosestVertex_window",
		title="Snap On Closest Vertex",
		width=320)

	spacing = 5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
	cmds.text(label="Reference Object:")
	referenceObject_textField = cmds.textField("referenceObject_textField")
	cmds.button("getReferenceObject_button", label="Get Reference Object!", command=getReferenceObject_button_OnClicked)
	cmds.setParent(topLevel=True)

	cmds.separator(style="single")

	cmds.button("snapIt_button", label="Snap It!", al="center", command=snapIt_button_OnClicked)

	cmds.showWindow("snapOnClosestVertex_window")
	cmds.windowPref(enableAll=True)

def snapOnClosestVertex():
	"""
	This definition launches the 'Snap On Closest Vertex' main window.
	"""

	snapOnClosestVertex_window()

@stacksHandler
def ISnapOnClosestVertex():
	"""
	This definition is the snapOnClosestVertex definition Interface.
	"""

	snapOnClosestVertex()

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************
