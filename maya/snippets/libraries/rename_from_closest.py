# Rename from closest.
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacks_handler",
            "get_mpoint",
            "norme",
            "rename_targets_from_closest_sources",
            "pick_sources_button__on_clicked",
            "pick_targets_button__on_clicked",
            "rename_from_closest_button__on_clicked",
            "rename_from_closest_window",
            "rename_from_closest"]

__interfaces__ = ["rename_from_closest"]

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

@stacks_handler
def rename_targets_from_closest_sources(sources, targets, suffixe="__"):
    """
    Renames the targets from closest sources.

    :param sources: Sources.
    :type sources: list
    :param targets: Targets.
    :type targets: list
    :param suffixe: Suffixe.
    :type suffixe: str
    """

    for target in targets:
        target_barycenter = cmds.objectCenter(target, gl=True)
        normes = {}
        for source in sources:
            normes[source] = norme(target_barycenter, cmds.objectCenter(source, gl=True))
        closest = min(normes, key=lambda item: normes[item])
        cmds.rename(target, "{0}{1}".format(closest.split("|")[-1], suffixe))

@stacks_handler
def pick_sources_button__on_clicked(state=None):
    """
    Defines the slot triggered by **pick_sources_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    cmds.textField("sources_textField", edit=True, text=", ".join(cmds.ls(sl=True, l=True)))

@stacks_handler
def pick_targets_button__on_clicked(state=None):
    """
    Defines the slot triggered by **pick_targets_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    cmds.textField("targets_textField", edit=True, text=", ".join(cmds.ls(sl=True, l=True)))

@stacks_handler
def rename_from_closest_button__on_clicked(state=None):
    """
    Defines the slot triggered by **rename_from_closest_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    sources = [source for source in cmds.textField("sources_textField", query=True, text=True).split(", ") if cmds.objExists(source)]
    targets = [target for target in cmds.textField("targets_textField", query=True, text=True).split(", ")	if cmds.objExists(target)]

    rename_targets_from_closest_sources(sources, targets)

def rename_from_closest_window():
    """
    Creates the 'Rename From Closest' main window.
    """

    cmds.windowPref(enableAll=False)

    if (cmds.window("rename_from_closest_window", exists=True)):
        cmds.deleteUI("rename_from_closest_window")

    cmds.window("rename_from_closest_window",
        title="Rename From Closest",
        width=320)

    spacing = 5

    cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
    cmds.text(label="Sources:")
    sources_textField = cmds.textField("sources_textField")
    cmds.button("pick_sources_button", label="Pick Sources!", command=pick_sources_button__on_clicked)
    cmds.setParent(topLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
    cmds.text(label="Targets:")
    targets_textField = cmds.textField("targets_textField")
    cmds.button("pick_targets_button", label="Pick Targets!", command=pick_targets_button__on_clicked)
    cmds.setParent(topLevel=True)

    cmds.separator(style="single")

    cmds.button("rename_from_closest_button", label="Rename Targets!", command=rename_from_closest_button__on_clicked)

    cmds.showWindow("rename_from_closest_window")

    cmds.windowPref(enableAll=True)

def rename_from_closest():
    """
    Launches the 'Rename From Closest' main window.
    """

    rename_from_closest_window()
