#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**activateBlendshapes.py**

**Platform :**
	Windows, Linux, Mac Os X.

**Description :**
	Activate blendshapes Module.

**Others :**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import maya.cmds as cmds
import maya.mel as mel

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacksHandler",
			"weight_floatSliderGrp_OnValueChanged",
			"setWeight",
			"activateBlendshapes_window",
			"activateBlendshapes",
			"IActivateBlendshapes"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
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

def weight_floatSliderGrp_OnValueChanged(value):
	"""
	Defines the slot triggered by 'weight_floatSliderGrp' slider when value changed.

	:param value: Value.
	:type value: float
	"""

	setWeight(cmds.floatSliderGrp("weight_floatSliderGrp", query=True, value=True))

def setWeight(value):
	"""
	Activates every first blendshape node slot in the scene.

	:param value: Activation value.
	:type value: float
	"""

	blendShapesNodes = cmds.ls(type="blendShape")
	for blendShapesNode in blendShapesNodes :
		targets = cmds.listAttr(blendShapesNode + ".w", m=True)
		for target in targets:
			try:
				cmds.setAttr("%s.%s" % (blendShapesNode, target), value)
			except:
				pass

def activateBlendshapes_window():
	"""
	Creates the 'Activate Blendshapes' main window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("activateBlendshapes_window", exists=True)):
		cmds.deleteUI("activateBlendshapes_window")

	cmds.window("activateBlendshapes_window",
		title="Activate Blendshapes",
		width=320)

	spacing = 5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.separator(height=10, style="singleDash")

	cmds.floatSliderGrp("weight_floatSliderGrp", label="Weight", field=True, minValue=0, maxValue=1, fieldMinValue=0, fieldMaxValue=1, sliderStep=0.01, value=0, changeCommand=weight_floatSliderGrp_OnValueChanged, dragCommand=weight_floatSliderGrp_OnValueChanged)

	cmds.separator(height=10, style="singleDash")

	cmds.showWindow("activateBlendshapes_window")

	cmds.windowPref(enableAll=True)

def activateBlendshapes():
	"""
	Launches the 'Activate Blendshapes' main window.
	"""

	activateBlendshapes_window()

@stacksHandler
def IActivateBlendshapes():
	"""
	Defines the activateBlendshapes definition Interface.
	"""

	activateBlendshapes()
