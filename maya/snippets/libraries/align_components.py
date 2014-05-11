# Credits: Zananick (Unknown).
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["ALIGNEMENT_ANCHORS",
            "stacks_handler",
            "get_mvector",
            "normalize",
            "align_components_between_anchors",
            "select_anchors_button__on_clicked",
            "align_button__on_clicked",
            "align_on_x_axis_button__on_clicked",
            "align_on_y_axis_button__on_clicked",
            "align_on_z_axis_button__on_clicked",
            "align_components_window",
            "align_components"]

__interfaces__ = ["align_components"]

ALIGNEMENT_ANCHORS = None

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

def get_mvector(vector):
    """
    Returns an MVector.

    :param vector: Vector.
    :type vector: list
    :return: MVector
    :rtype: MVector
    """

    return OpenMaya.MVector(vector[0], vector[1], vector[2])

def normalize(vector):
    """
    Returns the normalized vector.

    :param vector: Vector.
    :type vector: list
    :return: Normalized vector
    :rtype: tuple
    """

    mvector = get_mvector(vector)
    mvector.normalize()
    return (mvector.x, mvector.y, mvector.z)

@stacks_handler
def align_components_between_anchors(anchor_a, anchor_b, components, axis=("X", "Y", "Z")):
    """
    Aligns given components between the two anchors.

    :param anchor_a: Anchor a.
    :type anchor_a: str
    :param anchor_b: Anchor b.
    :type anchor_b: str
    :param components: Components to align.
    :type components: list
    :param axis: Collapse axis.
    :type axis: tuple
    """

    vertices = cmds.ls(cmds.polyListComponentConversion(components, toVertex=True), fl=True)

    point_a = cmds.xform(anchor_a, q=True, t=True, ws=True)
    point_b = cmds.xform(anchor_b, q=True, t=True, ws=True)
    vector_a = normalize([point_j - point_i for point_i, point_j in zip(point_a, point_b)])

    for vertex in vertices:
        point_c = cmds.xform(vertex, q=True, ws=True, t=True)
        vector_b = [point_k - point_i for point_i, point_k in zip(point_a, point_c)]
        mvector_a = get_mvector(vector_a)
        mvector_b = get_mvector(vector_b)
        dot = mvector_b * mvector_a
        mvector_a *= dot
        offset = mvector_b - mvector_a

        x_value = -offset.x if "X" in axis else 0
        y_value = -offset.y if "Y" in axis else 0
        z_value = -offset.z if "Z" in axis else 0

        cmds.xform(vertex, ws=True, r=True, t=(x_value, y_value, z_value))

@stacks_handler
def select_anchors_button__on_clicked(state=None):
    """
    Defines the slot triggered by **select_anchors_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    global ALIGNEMENT_ANCHORS

    selection = cmds.ls(sl=True, l=True, fl=True)
    if len(selection) == 2:
        ALIGNEMENT_ANCHORS = (selection[0], selection[1])
    else:
        mel.eval("warning(\"%s | failed to retrieve anchors, you need to select exactly two objects or components!\")" % __name__)

@stacks_handler
def align_button__on_clicked(state=None):
    """
    Defines the slot triggered by **align_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    if ALIGNEMENT_ANCHORS:
        selection = cmds.ls(sl=True, l=True)
        selection and align_components_between_anchors(ALIGNEMENT_ANCHORS[0], ALIGNEMENT_ANCHORS[1], selection)

@stacks_handler
def align_on_x_axis_button__on_clicked(state=None):
    """
    Defines the slot triggered by **align_on_x_axis_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    if ALIGNEMENT_ANCHORS:
        selection = cmds.ls(sl=True, l=True)
        selection and align_components_between_anchors(ALIGNEMENT_ANCHORS[0], ALIGNEMENT_ANCHORS[1], selection, axis=("X"))

@stacks_handler
def align_on_y_axis_button__on_clicked(state=None):
    """
    Defines the slot triggered by **align_on_y_axis_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    if ALIGNEMENT_ANCHORS:
        selection = cmds.ls(sl=True, l=True)
        selection and align_components_between_anchors(ALIGNEMENT_ANCHORS[0], ALIGNEMENT_ANCHORS[1], selection, axis=("Y"))

@stacks_handler
def align_on_z_axis_button__on_clicked(state=None):
    """
    Defines the slot triggered by **align_on_z_axis_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    if ALIGNEMENT_ANCHORS:
        selection = cmds.ls(sl=True, l=True)
        selection and align_components_between_anchors(ALIGNEMENT_ANCHORS[0], ALIGNEMENT_ANCHORS[1], selection, axis=("Z"))

def align_components_window():
    """
    Creates the 'Align Components' main window.
    """

    cmds.windowPref(enableAll=False)

    if (cmds.window("align_components_window", exists=True)):
        cmds.deleteUI("align_components_window")

    cmds.window("align_components_window",
        title="Align Components",
        width=320)

    spacing = 5

    cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

    cmds.button("select_anchors_button", label="Select Anchors!", command=select_anchors_button__on_clicked)

    cmds.separator(height=10, style="singleDash")

    cmds.button("align_button", label="Align Selection!", command=align_button__on_clicked)

    cmds.separator(height=10, style="singleDash")

    cmds.button("align_on_x_axis_button", label="Align Selection On X!", command=align_on_x_axis_button__on_clicked)
    cmds.button("align_on_y_axis_button", label="Align Selection On Y!", command=align_on_y_axis_button__on_clicked)
    cmds.button("align_on_z_axis_button", label="Align Selection On Z!", command=align_on_z_axis_button__on_clicked)

    cmds.showWindow("align_components_window")

    cmds.windowPref(enableAll=True)

@stacks_handler
def align_components():
    """
    Launches the 'Align Components' main window.
    """

    align_components_window()
