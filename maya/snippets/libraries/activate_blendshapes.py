#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**activate_blendshapes.py**

**Platform :**
    Windows, Linux, Mac Os X.

**Description :**
    Activate blendshapes Module.

**Others :**

"""

from __future__ import unicode_literals

import maya.cmds as cmds


__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacks_handler",
            "weight_floatSliderGrp__on_value_changed",
            "set_weight",
            "activate_blendshapes_window",
            "activate_blendshapes"]

__interfaces__ = ["activate_blendshapes"]

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
            cmds.repeatLast(addCommand="python(\"import {0}; {1}.{2}()\")".format(__name__, __name__, object.__name__), addCommandLabel=object.__name__)
        except:
            pass
        return value

    return stacks_handler_wrapper

def weight_floatSliderGrp__on_value_changed(value):
    """
    Defines the slot triggered by 'weight_floatSliderGrp' slider when value changed.

    :param value: Value.
    :type value: float
    """

    set_weight(cmds.floatSliderGrp("weight_floatSliderGrp", query=True, value=True))

def set_weight(value):
    """
    Activates every first blendshape node slot in the scene.

    :param value: Activation value.
    :type value: float
    """

    blend_shapes_nodes = cmds.ls(type="blendShape")
    for blend_shapes_node in blend_shapes_nodes :
        targets = cmds.listAttr("{0}.w".format(blend_shapes_node), m=True)
        for target in targets:
            try:
                cmds.setAttr("{0}.{1}".format(blend_shapes_node, target), value)
            except:
                pass

def activate_blendshapes_window():
    """
    Creates the 'Activate Blendshapes' main window.
    """

    cmds.windowPref(enableAll=False)

    if (cmds.window("activate_blendshapes_window", exists=True)):
        cmds.deleteUI("activate_blendshapes_window")

    cmds.window("activate_blendshapes_window",
        title="Activate Blendshapes",
        width=320)

    spacing = 5

    cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

    cmds.separator(height=10, style="singleDash")

    cmds.floatSliderGrp("weight_floatSliderGrp", label="Weight", field=True, minValue=0, maxValue=1, fieldMinValue=0, fieldMaxValue=1, sliderStep=0.01, value=0, changeCommand=weight_floatSliderGrp__on_value_changed, dragCommand=weight_floatSliderGrp__on_value_changed)

    cmds.separator(height=10, style="singleDash")

    cmds.showWindow("activate_blendshapes_window")

    cmds.windowPref(enableAll=True)

def activate_blendshapes():
    """
    Launches the 'Activate Blendshapes' main window.
    """

    activate_blendshapes_window()
