import maya.cmds as cmds
import maya.mel as mel
import re

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacks_handler",
            "unfold_band_uvs",
            "unfold_band_button__on_clicked",
            "unfold_band_window",
            "unfold_band",
            "unfold_tube",
            "unfold_tube_using_selected_edges"]

__interfaces__ = ["unfold_band",
                "unfold_tube_using_selected_edges"]

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

@stacks_handler
def unfold_band_uvs(object, divisions=1, history=True):
    """
    Unfolds object band Uvs.

    :param object: Object.
    :type object: str
    :param divisions: Extrusion divisions.
    :type divisions: int
    :param history: Keep construction history.
    :type history: bool
    """

    edges_count = cmds.polyEvaluate(object, edge=True)
    edges = cmds.ls("{0}.e[0:{1}]".format(object, edges_count - 1), fl=True, l=True)

    cmds.select(object)
    cmds.polySelectConstraint(m=3, t=0x8000, w=1)
    cmds.polySelectConstraint(m=0)
    for i in range(divisions):
        mel.eval("GrowPolygonSelectionRegion();")
    band_edges = cmds.ls(sl=True, fl=True, l=True)
    band_faces = cmds.ls(cmds.polyListComponentConversion(band_edges, fe=True, tf=True), fl=True)
    cmds.select(band_faces)
    cmds.polyForceUV(unitize=True)
    cmds.polySelectConstraint(m=3, t=0x8000, sm=1)
    seams_edges = cmds.ls(sl=True, fl=True, l=True)
    weld_edges = list(set(band_edges).difference(set(seams_edges)))
    cmds.polyMapSewMove(weld_edges)
    cmds.polyLayoutUV(band_faces, scale=1, rotateForBestFit=0, layout=1)
    uvs = cmds.polyListComponentConversion(band_faces, toUV=1)
    cmds.polyEditUV(uvs, u=1, v=0)

    not history and cmds.delete(object, ch=True)

@stacks_handler
def unfold_band_button__on_clicked(state=None):
    """
    Defines the slot triggered by **unfold_band_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    for object in cmds.ls(sl=True, l=True, o=True):
        unfold_band_uvs(object, divisions=cmds.intSliderGrp("divisions_intSliderGrp", q=True, v=True), history=cmds.checkBox("keep_construction_history_checkBox", q=True, v=True))

def unfold_band_window():
    """
    Creates the 'Unfold Band' main window.
    """

    cmds.windowPref(enableAll=False)

    if (cmds.window("unfold_band_window", exists=True)):
        cmds.deleteUI("unfold_band_window")

    cmds.window("unfold_band_window",
        title="Unfold Band",
        width=384)

    spacing = 5

    cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

    cmds.separator(height=10, style="singleDash")

    cmds.intSliderGrp("divisions_intSliderGrp", label="Divisions", field=True, minValue=0, maxValue=10, fieldMinValue=0, fieldMaxValue=65535, value=2)

    cmds.separator(style="single")

    cmds.columnLayout(columnOffset=("left", 140))
    cmds.checkBox("keep_construction_history_checkBox", label="Keep Construction History", v=True)
    cmds.setParent(topLevel=True)

    cmds.separator(height=10, style="singleDash")

    cmds.button("unfold_band_button", label="Unfold Band!", command=unfold_band_button__on_clicked)

    cmds.showWindow("unfold_band_window")

    cmds.windowPref(enableAll=True)

def unfold_band():
    """
    Launches the 'Unfold Band' main window.
    """

    unfold_band_window()

@stacks_handler
def unfold_tube(seams_edges, history=False):
    """
    Unfolds object using given seams edges.

    :param seams_edges: Seams edges.
    :type seams_edges: list
    :param history: Keep construction history.
    :type history: bool
    """

    seams_edges = filter(lambda x: re.search(r"e\[\d+\]", x), cmds.ls(seams_edges, fl=True, l=True))
    if not seams_edges:
        return

    object = seams_edges[0].split(".")[0]
    edges_count = cmds.polyEvaluate(object, edge=True)
    edges = cmds.ls("{0}.e[0:{1}]".format(object, edges_count - 1), fl=True, l=True)
    cmds.polyForceUV(object, unitize=True)
    cmds.select(list(set(edges).difference(seams_edges)))
    cmds.polyMapSewMove(list(set(edges).difference(seams_edges)), ch=True)

    not history and cmds.delete(object, ch=True)

@stacks_handler
def unfold_tube_using_selected_edges():
    """
    Unfolds object using selected seams edges.
    """

    selection = cmds.ls(sl=True, l=True)
    selection and unfold_tube(selection)
