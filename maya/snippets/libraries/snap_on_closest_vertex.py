#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**********************************************************************************************************************
#
# Copyright (C) 2010 - 2014 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#**********************************************************************************************************************

"""
**snap_on_closest_vertex.py**

**Platform :**
    Windows, Linux, Mac Os X.

**Description :**
    Snap on closest vertex Module.

**Others :**

"""

from __future__ import unicode_literals

import math
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.mel as mel
import re
import functools
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["TOLERANCE",
            "MAXIMUM_SEARCH_DISTANCE",
            "stacks_handler",
            "get_mpoint",
            "norme",
            "get_shapes",
            "get_reference_object_button__on_clicked",
            "load_plugin",
            "snap_components_on_closest_vertex",
            "snap_it_button__on_clicked",
            "snap_on_closest_vertex_window",
            "snap_on_closest_vertex"]

__interfaces__ = ["snap_on_closest_vertex"]

TOLERANCE = 64
MAXIMUM_SEARCH_DISTANCE = 2 ** 32 - 1

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

def get_mpoint(point):
    """
    Returns an MPoint.

    :param point: Point.
    :type point: list
    :return: MPoint
    :rtype: MVector
    """

    return OpenMaya.MPoint(point[0], point[1], point[2])

def norme(point_a, point_b):
    """
    Returns the norme of a vector.

    :param point_a: Point A.
    :type point_a: list
    :param point_b: Point B.
    :type point_b: list
    :return: Norme
    :rtype: float
    """

    mpoint_a = get_mpoint(point_a)
    mpoint_b = get_mpoint(point_b)
    mvector = mpoint_a - mpoint_b
    return mvector.length()

def get_shapes(object, full_path=False, no_intermediate=True):
    """
    Returns shapes of the given object.

    :param object: Current object.
    :type object: str
    :param full_path: Current full path state.
    :type full_path: bool
    :param noIntermediate: Current no intermediate state.
    :type noIntermediate: bool
    :return: Objects shapes.
    :rtype: list
    """

    object_shapes = []
    shapes = cmds.listRelatives(object, fullPath=full_path, shapes=True, noIntermediate=no_intermediate)
    if shapes != None:
        object_shapes = shapes

    return object_shapes

@stacks_handler
def get_reference_object_button__on_clicked(state=None):
    """
    Defines the slot triggered by **get_reference_object_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, type="transform")

    if selection :
        cmds.textField("reference_object_textField", edit=True, text=selection[0])

def load_plugin(plugin):
    """
    This function loads a plugin.

    :param plugin: Plugin to load.
    :type plugin: str
    """

    not cmds.pluginInfo(plugin, query=True, loaded=True) and cmds.loadPlugin(plugin)

def snap_components_on_closest_vertex(reference_object, components, tolerance) :
    """
    This function snaps vertices onto the reference object vertices.

    :param reference_object: Reference mesh.
    :type reference_object: str
    :param components: Components.
    :type components: list
    """

    vertices = cmds.ls(cmds.polyListComponentConversion(components, toVertex=True), fl=True)

    progressBar = mel.eval("$container=$gMainProgressBar");

    cmds.progressBar(progressBar, edit=True, beginProgress=True, isInterruptable=True, status="Snapping vertices ...", maxValue=len(vertices))

    load_plugin("nearestPointOnMesh")

    nearest_point_on_mesh = mel.eval("nearestPointOnMesh " + reference_object)

    for vertex in vertices :
        if cmds.progressBar(progressBar, query=True, isCancelled=True) :
            break

        closest_distance = MAXIMUM_SEARCH_DISTANCE

        vertex_position = cmds.pointPosition(vertex, world=True)
        cmds.setAttr("{0}.inPosition".format(nearest_point_on_mesh), vertex_position[0], vertex_position[1], vertex_position[2])
        associated_face_id = cmds.getAttr("{0}.nearestFaceIndex".format(nearest_point_on_mesh))
        vtxs_faces = cmds.filterExpand(cmds.polyListComponentConversion("{0}.f[{1}]".format(reference_object, associated_face_id), fromFace=True, toVertexFace=True), sm=70, expand=True)

        closest_position = []
        for vtxs_face in vtxs_faces :
            associated_vtx = cmds.polyListComponentConversion(vtxs_face, fromVertexFace=True, toVertex=True)
            associated_vtx_position = cmds.pointPosition(associated_vtx, world=True)

            distance = norme(vertex_position, associated_vtx_position)

            if distance < closest_distance :
                closest_distance = distance
                closest_position = associated_vtx_position

            if closest_distance < tolerance :
                cmds.move(closest_position[0], closest_position[1], closest_position[2], vertex, worldSpace=True)

        cmds.progressBar(progressBar, edit=True, step=1)

    cmds.progressBar(progressBar, edit=True, endProgress=True)

    cmds.delete(nearest_point_on_mesh)

@stacks_handler
def snap_it_button__on_clicked(state=None):
    """
    Defines the slot triggered by **snap_it_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    reference_object = cmds.textField("reference_object_textField", query=True, text=True)

    reference_objectShapes = cmds.objExists(reference_object) and get_shapes(reference_object) or None

    selection = cmds.ls(sl=True, fl=True)
    reference_objectShapes and selection and snap_components_on_closest_vertex(reference_objectShapes[0], selection, TOLERANCE)

def snap_on_closest_vertex_window():
    """
    Creates the 'Snap On Closest Vertex' vertex window.
    """

    cmds.windowPref(enableAll=False)

    if (cmds.window("snap_on_closest_vertex_window", exists=True)):
        cmds.deleteUI("snap_on_closest_vertex_window")

    cmds.window("snap_on_closest_vertex_window",
        title="Snap On Closest Vertex",
        width=320)

    spacing = 5

    cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
    cmds.text(label="Reference Object:")
    reference_object_textField = cmds.textField("reference_object_textField")
    cmds.button("get_reference_object_button", label="Get Reference Object!", command=get_reference_object_button__on_clicked)
    cmds.setParent(topLevel=True)

    cmds.separator(style="single")

    cmds.button("snap_it_button", label="Snap It!", al="center", command=snap_it_button__on_clicked)

    cmds.showWindow("snap_on_closest_vertex_window")
    cmds.windowPref(enableAll=True)

def snap_on_closest_vertex():
    """
    Launches the 'Snap On Closest Vertex' main window.
    """

    snap_on_closest_vertex_window()
