import maya.cmds as cmds
import operator

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacks_handler",
           "select_star_vertices",
           "select_triangles_faces",
           "select_nsides_faces",
           "select_boundary_edges",
           "select_border_edges",
           "select_creases_edges",
           "select_hard_edges",
           "select_non_manifold_vertices",
           "select_isolated_vertices",
           "select_lamina_faces",
           "select_zero_geometry_area_faces",
           "select_side_vertices",
           "select_left_vertices",
           "select_right_vertices"]

__interfaces__ = ["select_star_vertices",
                  "select_triangles_faces",
                  "select_nsides_faces",
                  "select_boundary_edges",
                  "select_border_edges",
                  "select_creases_edges",
                  "select_hard_edges",
                  "select_non_manifold_vertices",
                  "select_isolated_vertices",
                  "select_lamina_faces",
                  "select_zero_geometry_area_faces",
                  "select_left_vertices",
                  "select_right_vertices"]


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
            cmds.repeatLast(addCommand="python(\"import {0}; {1}.{2}()\")".format(
                __name__, __name__, object.__name__), addCommandLabel=object.__name__)
        except:
            pass
        return value

    return stacks_handler_wrapper


@stacks_handler
def select_star_vertices():
    """
    Selects star vertices.
    """

    cmds.polySelectConstraint(m=3, t=1, order=True, orb=(5, 65535))
    cmds.polySelectConstraint(dis=True)


@stacks_handler
def select_triangles_faces():
    """
    Selects triangles faces.
    """

    cmds.polySelectConstraint(m=3, t=8, sz=1)
    cmds.polySelectConstraint(dis=True)


@stacks_handler
def select_nsides_faces():
    """
    Selects nsides faces.
    """

    cmds.polySelectConstraint(m=3, t=8, sz=3)
    cmds.polySelectConstraint(dis=True)


@stacks_handler
def select_boundary_edges():
    """
    Selects boundaries edges.
    """

    selection = cmds.ls(sl=True, l=True)
    selection and cmds.select(cmds.polyListComponentConversion(selection, te=True, bo=True))


@stacks_handler
def select_border_edges():
    """
    Selects border edges.
    """

    cmds.polySelectConstraint(m=3, t=0x8000, w=1)
    cmds.polySelectConstraint(m=0)


@stacks_handler
def select_creases_edges():
    """
    Selects creases edges
    """

    selection = cmds.ls(sl=True, l=True)
    if not selection:
        return

    edges = cmds.ls("{0}.e[0:{1}]".format(object, cmds.polyEvaluate(object, edge=True) - 1), fl=True)
    crease_edges = [edge for edge in edges if cmds.polyCrease(edge, q=True, v=True)[0] > 0.0]
    if crease_edges:
        cmds.select(crease_edges)


@stacks_handler
def select_hard_edges():
    """
    Selects hard edges.
    """

    cmds.polySelectConstraint(m=3, t=0x8000, sm=1)
    cmds.polySelectConstraint(m=0)


@stacks_handler
def select_non_manifold_vertices():
    """
    Selects non manifold vertices.
    """

    cmds.polySelectConstraint(m=3, t=1, nonmanifold=True)
    cmds.polySelectConstraint(m=0)


@stacks_handler
def select_isolated_vertices():
    """
    Selects isolated vertices.
    """

    selection = cmds.ls(sl=True, l=True)
    if not selection:
        return

    cmds.select(cl=True)
    isolated_vertices = []
    vertices = cmds.ls(cmds.polyListComponentConversion(selection, toVertex=True), fl=True)
    for vertex in vertices:
        edges = cmds.ls(cmds.polyListComponentConversion(vertex, toEdge=True), flatten=True)
        if len(edges) == 2:
            if len(cmds.ls(cmds.polyListComponentConversion(edges, toFace=True), flatten=True)) == 1:
                continue

            isolated_vertices.append(vertex)
    isolated_vertices and cmds.select(isolated_vertices)


@stacks_handler
def select_lamina_faces():
    """
    Selects lamina faces.
    """

    cmds.polySelectConstraint(m=3, t=8, tp=2)
    cmds.polySelectConstraint(m=0)


@stacks_handler
def select_zero_geometry_area_faces(treshold=0.001):
    """
    Selects the zero geometry area faces.

    :param treshold: Selection treshold.
    :type treshold: float
    """

    cmds.polySelectConstraint(m=3, t=8, ga=True, gab=(0, treshold))
    cmds.polySelectConstraint(m=0)


@stacks_handler
def select_side_vertices(object, positive=True):
    """
    Selects given side geometry vertices.

    :param object: Object to select vertices.
    :type object: str
    :param positive: Select positive vertices.
    :type positive: bool
    """

    comparison = positive and operator.gt or operator.lt
    vertices_count = cmds.polyEvaluate(object, vertex=True)
    vertices = cmds.ls(object + ".vtx[0:{0}]".format(str(vertices_count - 1)), fl=True, l=True)
    cmds.select(filter(lambda x: comparison(cmds.xform(x, q=True, t=True, ws=True)[0], 0), vertices))


@stacks_handler
def select_left_vertices(object):
    """
    Selects left side geometry vertices.
    """

    selection = cmds.ls(sl=True, l=True)
    selection and select_side_vertices(selection[0], positive=True)


@stacks_handler
def select_right_vertices():
    """
    Selects right side geometry vertices.
    """

    selection = cmds.ls(sl=True, l=True)
    selection and select_side_vertices(selection[0], positive=False)
