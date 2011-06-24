#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
************************************************************************************************
***	activateBlendshapes.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	Activate Blendshapes Module.
***
***	Others :
***
************************************************************************************************
"""

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import maya.cmds as cmds
import maya.mel as mel

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions
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

def weightSlider_OnValueChanged(value):
	"""
	This Definition Is Triggered By The 'weightSlider' Slider When Its Value Changed.
	"""
	
	setWeight(cmds.floatSliderGrp("weight_FloatSliderGrp", query=True, value=True))

def setWeight(value):
	"""
	This Definition Activates Every First Blendshape Node Slot In The Scene.

	@param value : Activation Value. ( Float )
	"""

	blendShapesNodes=cmds.ls(type="blendShape")
	for blendShapesNode in blendShapesNodes :
		targets=cmds.listAttr(blendShapesNode + ".w", m=True)
		cmds.setAttr(blendShapesNode + "." + targets[0], value)

def activateBlendshapes_Window():
	"""
	This Definition Creates The Activate Blendshapes Main Window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("activateBlendshapes_Window", exists=True)):
		cmds.deleteUI("activateBlendshapes_Window")

	cmds.window("activateBlendshapes_Window",
		title="Activate Blendshapes",
		width=320)

	spacing=5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.separator(height=10, style="singleDash")

	cmds.floatSliderGrp("weight_FloatSliderGrp", label="Weight", field=True, minValue=0, maxValue=1, fieldMinValue=0, fieldMaxValue=1, sliderStep=0.01, value=0, changeCommand=weightSlider_OnValueChanged , dragCommand=weightSlider_OnValueChanged)

	cmds.separator(height=10, style="singleDash")

	cmds.showWindow("activateBlendshapes_Window")

	cmds.windowPref(enableAll=True)

def activateBlendshapes():
	"""
	This Definition Launches The Activate Blendshapes Main Window.
	"""

	activateBlendshapes_Window()

@stacksHandler
def IActivateBlendshapes():
	"""
	This Definition Is The activateBlendshapes Method Interface.
	"""
	
	activateBlendshapes()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
