#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**materialize_targets.py**

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

__all__ = ["stacks_handler",
           "pick_blend_shape_button__on_clicked",
           "pick_extraction_source_button__on_clicked",
           "materialize_targets_button__on_clicked",
           "materialize_blendshape_targets",
           "materialize_targets_window",
           "materialize_targets"]

__interfaces__ = ["materialize_targets"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def stacks_handler(object):
    """
    Handles Maya stacks.

   :param object: Python object.
   :type object: object
   :return: Python function.
   :rtype: object
    """

    def stacks_handler_wrapper(*args, **kwargs):
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

    return stacks_handler_wrapper

def pick_blend_shape_button__on_clicked(state=None):
    """
    Defines the slot triggered by **pick_blend_shape_button** button when clicked.

    :param state: button state.
    :type state: bool
    """
    cmds.textField("blend_shape_node_TextField", edit=True, text=cmds.ls(sl=True, l=True)[0])

def pick_extraction_source_button__on_clicked(state=None):
    """
    Defines the slot triggered by **pick_extraction_source_button** button when clicked.

    :param state: button state.
    :type state: bool
    """
    cmds.textField("extractionSource_TextField", edit=True, text=cmds.ls(sl=True, l=True)[0])

@stacks_handler
def materialize_targets_button__on_clicked(state=None):
    """
    Defines the slot triggered by **materialize_targets_button** button when clicked.

   :param state: button state.
   :type state: bool
    """
    blend_shapes_node = cmds.textField("blend_shape_node_TextField", query=True, text=True)
    duplication_source = cmds.textField("extractionSource_TextField", query=True, text=True)

    if blend_shapes_node != "" and duplication_source != "":
        materialize_blendshape_targets(blend_shapes_node, duplication_source)

@stacks_handler
def materialize_blendshape_targets(blend_shape_node, duplication_source):
    """
    Materializes targets from given blendshape node using given duplication source.

   :param blend_shape_node: Blendshape node.
   :type blend_shape_node: unicode
   :param duplication_source: Duplication source.
   :type duplication_source: unicode
    """

    targets = cmds.listAttr("{0}.w".format(blend_shape_node), m=True)
    for target in targets:
        try:
            cmds.setAttr("{0}.{1}".format(blend_shape_node, target), 1)
        except:
            pass

        duplicatedNodes = cmds.duplicate(duplication_source, rr=True)
        cmds.rename(duplicatedNodes[0], target)

        try:
            cmds.setAttr("{0}.{1}".format(blend_shape_node, target), 0)
        except:
            pass

def materialize_targets_window():
    cmds.windowPref(enableAll=False)

    if cmds.window("materialize_targets_window", exists=True):
        cmds.deleteUI("materialize_targets_window")

    cmds.window("materialize_targets_window",
                title="Materialize Blendshape Targets",
                width=320)

    spacing = 5

    cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"),
                   columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
    cmds.text(label="BlendShape Node:")
    blend_shape_node_TextField = cmds.textField("blend_shape_node_TextField")
    cmds.button("pick_blend_shapeNode_button", label="Pick BlendShape Node!",
                command=pick_blend_shape_button__on_clicked)
    cmds.setParent(topLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"),
                   columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
    cmds.text(label="Extraction Source:")
    extractionSource_TextField = cmds.textField("extractionSource_TextField")
    cmds.button("pick_extraction_source_button", label="Pick Extraction Source!",
                command=pick_extraction_source_button__on_clicked)
    cmds.setParent(topLevel=True)

    cmds.separator(style="single")

    cmds.button("materialize_targets_button", label="Extract Targets!",
                command=materialize_targets_button__on_clicked)

    cmds.showWindow("materialize_targets_window")

    cmds.windowPref(enableAll=True)

def materialize_targets():
    """
    Launches the 'Materialize Blendshape Targets' main window.
    """

    materialize_targets_window()
