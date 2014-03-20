#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**materializeTargets.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Materializes blendshape node targets.

**Others:**

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
           "pickBlendShape_button_OnClicked",
           "pickExtractionSource_button_OnClicked",
           "materializeTargets_button_OnClicked",
           "materializeBlendshapeTargets",
           "materializeTargets_window",
           "materializeTargets"]

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
            cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")" % (__name__, __name__, object.__name__),
                            addCommandLabel=object.__name__)
        except:
            pass
        return value

    return stacksHandlerCall

def pickBlendShape_button_OnClicked(state=None):
    """
    Defines the slot triggered by **pickBlendShape_Button** button when clicked.

   :param state: Button state.
   :type state: bool
    """
    cmds.textField("blendShapeNode_TextField", edit=True, text=cmds.ls(sl=True, l=True)[0])

def pickExtractionSource_button_OnClicked(state=None):
    """
    Defines the slot triggered by **pickExtractionSource** button when clicked.

   :param state: Button state.
   :type state: bool
    """
    cmds.textField("extractionSource_TextField", edit=True, text=cmds.ls(sl=True, l=True)[0])

@stacksHandler
def materializeTargets_button_OnClicked(state=None):
    """
    Defines the slot triggered by **materializeTargets_Button** button when clicked.

   :param state: Button state.
   :type state: bool
    """
    blendShapesNode = cmds.textField("blendShapeNode_TextField", query=True, text=True)
    duplicationSource = cmds.textField("extractionSource_TextField", query=True, text=True)

    if blendShapesNode != "" and duplicationSource != "":
        materializeBlendshapeTargets(blendShapesNode, duplicationSource)

@stacksHandler
def materializeBlendshapeTargets(blendShapeNode, duplicationSource):
    """
    Materializes targets from given blendshape node using given duplication source.

   :param blendShapeNode: Blendshape node.
   :type blendShapeNode: unicode
   :param duplicationSource: Duplication source.
   :type duplicationSource: unicode
    """

    targets = cmds.listAttr("{0}.w".format(blendShapeNode), m=True)
    for target in targets:
        try:
            cmds.setAttr("{0}.{1}".format(blendShapeNode, target), 1)
        except:
            pass

        duplicatedNodes = cmds.duplicate(duplicationSource, rr=True)
        cmds.rename(duplicatedNodes[0], target)

        try:
            cmds.setAttr("{0}.{1}".format(blendShapeNode, target), 0)
        except:
            pass

def materializeTargets_window():
    cmds.windowPref(enableAll=False)

    if cmds.window("materializeTargets_window", exists=True):
        cmds.deleteUI("materializeTargets_window")

    cmds.window("materializeTargets_window",
                title="Materialize Blendshape Targets",
                width=320)

    spacing = 5

    cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"),
                   columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
    cmds.text(label="BlendShape Node:")
    blendShapeNode_TextField = cmds.textField("blendShapeNode_TextField")
    cmds.button("pickBlendShapeNode_Button", label="Pick BlendShape Node!",
                command=pickBlendShape_button_OnClicked)
    cmds.setParent(topLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"),
                   columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
    cmds.text(label="Extraction Source:")
    extractionSource_TextField = cmds.textField("extractionSource_TextField")
    cmds.button("pickExtractionSource_Button", label="Pick Extraction Source!",
                command=pickExtractionSource_button_OnClicked)
    cmds.setParent(topLevel=True)

    cmds.separator(style='single')

    cmds.button("materializeTargets_Button", label="Extract Targets!",
                command=materializeTargets_button_OnClicked)

    cmds.showWindow("materializeTargets_window")

    cmds.windowPref(enableAll=True)

def materializeTargets():
    """
    Launches the 'Materialize Blendshape Targets' main window.
    """

    materializeTargets_window()

@stacksHandler
def IMaterializeTargets():
    """
    Defines the materializeTargets definition Interface.
    """

    materializeTargets()
