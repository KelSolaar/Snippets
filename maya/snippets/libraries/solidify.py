import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import math

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacks_handler",
            "get_transform",
            "get_mvector",
            "get_mmatrix",
            "normalize",
            "vector_matrix_multiplication",
            "dot",
            "get_average_vector",
            "get_angle",
            "has_border_edges",
            "solidify_object",
            "solidify_button__on_clicked",
            "solidify_window",
            "solidify"]

__interfaces__ = ["solidify"]

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

def get_transform(node, full_path=True):
    """
    Returns transform of the given node.

    :param node: Current object.
    :type node: str
    :param full_path: Current full path state.
    :type full_path: bool
    :return: Object transform.
    :rtype: str
    """

    transform = node
    if cmds.nodeType(node) != "transform":
        parents = cmds.listRelatives(node, fullPath=full_path, parent=True)
        transform = parents[0]
    return transform

def get_mvector(vector):
    """
    Returns an MVector.

    :param vector: Vector.
    :type vector: list
    :return: MVector
    :rtype: MVector
    """

    return OpenMaya.MVector(vector[0], vector[1], vector[2])

def get_mmatrix(matrix):
    """
    Returns an MMatrix.

    :param matrix: matrix.
    :type matrix: list
    :return: MMatrix
    :rtype: MMatrix
    """

    mMatrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList(matrix, mMatrix)
    return mMatrix

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

def vector_matrix_multiplication(vector, matrix):
    """
    Returns the vector multiplication between a Vector And a matrix.

    :param vector: Vector.
    :type vector: list
    :param matrix: matrix.
    :type matrix: list
    :return: Matrix multiplied vector.
    :rtype: tuple
    """

    mvector = get_mvector(vector)
    mMatrix = get_mmatrix(matrix)
    mvector = mvector * mMatrix
    return (mvector.x, mvector.y, mvector.z)

def dot(vector_a, vector_b):
    """
    Returns the dot product between two vectors.

    :param vector_a: Vector A.
    :type vector_a: list
    :param vector_b: Vector B.
    :type vector_b: list
    :return: Dot product.
    :rtype: float
    """

    mvector_a = get_mvector(vector_a)
    mvector_b = get_mvector(vector_b)
    return mvector_a * mvector_b

def get_average_vector(vectors):
    """
    Returns the average vector from a list of vectors.

    :param vectors: Vectors to get the average one.
    :type vectors: list
    :return: Average vector.
    :rtype: list
    """

    average_vector = [0, 0, 0]
    for vector in vectors:
        for i in range(3):
            average_vector[i] += vector[i]
    for i in range(3):
        average_vector[i] = average_vector[i] / len(vectors)
    return average_vector

def get_angle(vector_a, vector_b):
    """
    Returns the angle between two vectors.

    :param vector_a: Vector A.
    :type vector_a: list
    :param vector_b: Vector B.
    :type vector_b: list
    :return: Angle between Vector A and Vector B.
    :rtype: float
    """

    return math.degrees(math.acos(dot(vector_a, vector_b)))

def has_border_edges(object):
    """
    Returns if an object has border edges.

    :param object: Object.
    :type object: str
    :return: Has object border edges.
    :rtype: bool
    """

    cmds.select(object)
    cmds.polySelectConstraint(m=3, t=0x8000, w=1)
    cmds.polySelectConstraint(m=0)
    if cmds.ls(sl=True):
        return True

def solidify_object(object, height=1, divisions=2, history=True):
    """
    Solidifies given object.

    :param object: Object.
    :type object: str
    :param height: Extrusion height.
    :type height: float
    :param division: Extrusion divisions.
    :type division: float
    :param history: Keep construction history.
    :type history: bool
    """

    if has_border_edges(object):
        transform = get_transform(object)
        vertices = cmds.ls(cmds.polyListComponentConversion(object, toVertex=True), fl=True)

        barycenters = cmds.xform(vertices, q=True, t=True, ws=True)
        barycenter = get_average_vector([(barycenters[i], barycenters[i + 1], barycenters[i + 2]) for i in range(0, len(barycenters), 3)])

        normals = cmds.polyNormalPerVertex(cmds.polyListComponentConversion(object, toVertexFace=True), q=True, xyz=True)
        normals = [(normals[i], normals[i + 1], normals[i + 2]) for i in range(0, len(normals), 3)]
        average_normal = vector_matrix_multiplication(normalize(get_average_vector(normals)), cmds.xform(transform, query=True, matrix=True, worldSpace=True))

        faces_count = cmds.polyEvaluate(object, face=True)
        faces = "{0}.f[0:{1}]".format(object, faces_count - 1)
        extrude = cmds.polyExtrudeFacet(faces, constructionHistory=1, keepFacesTogether=1, divisions=divisions)
        cmds.setAttr("{0}.localTranslateZ".format(extrude[0]), height)
        border_edges = cmds.polyListComponentConversion(faces, te=True, bo=True)
        cmds.polyMapCut(border_edges)
        uvs = cmds.polyListComponentConversion("{0}.f[0:{1}]".format(object, faces_count - 1), toUV=1)
        cmds.polyEditUV(uvs, u=0, v= -5)

        extended_faces = cmds.ls(faces, fl=True)
        for i in range(divisions):
            adjacent_edges = cmds.polyListComponentConversion(extended_faces, ff=True, te=True)
            extended_faces.extend(cmds.ls(cmds.polyListComponentConversion(adjacent_edges, fe=True, tf=True), fl=True))

        border_faces = list(set(extended_faces).difference(set(cmds.ls(faces, fl=True))))
        cmds.select(border_faces)
        cmds.polyAutoProjection(border_faces, t=barycenter, ry=get_angle((0, 0, 1), average_normal), rz=get_angle((1, 0, 0), average_normal))
        uvs = cmds.polyListComponentConversion(border_faces, toUV=1)
        cmds.polyEditUV(uvs, u=0, v= -5)

        not history and cmds.delete(object, ch=True)

@stacks_handler
def solidify_button__on_clicked(state=None):
    """
    Defines the slot triggered by **solidify_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    for object in cmds.ls(sl=True, l=True, o=True):
        solidify_object(object, height=cmds.floatSliderGrp("height_floatSliderGrp", q=True, v=True), divisions=cmds.intSliderGrp("divisions_intSliderGrp", q=True, v=True), history=cmds.checkBox("keep_construction_history_checkBox", q=True, v=True))

def solidify_window():
    """
    Creates the 'Solidify' main window.
    """

    cmds.windowPref(enableAll=False)

    if (cmds.window("solidify_window", exists=True)):
        cmds.deleteUI("solidify_window")

    cmds.window("solidify_window",
        title="Solidify",
        width=320)

    spacing = 5

    cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

    cmds.separator(height=10, style="singleDash")

    cmds.floatSliderGrp("height_floatSliderGrp", label="Height", field=True, precision=3, minValue= -10, maxValue=10, fieldMinValue= -65535, fieldMaxValue=65535, value=0.1)
    cmds.intSliderGrp("divisions_intSliderGrp", label="Divisions", field=True, minValue=0, maxValue=10, fieldMinValue=0, fieldMaxValue=65535, value=2)

    cmds.separator(style="single")

    cmds.columnLayout(columnOffset=("left", 140))
    cmds.checkBox("keep_construction_history_checkBox", label="Keep Construction History", v=True)
    cmds.setParent(topLevel=True)

    cmds.separator(height=10, style="singleDash")

    cmds.button("solidify_button", label="Solidify!", command=solidify_button__on_clicked)

    cmds.showWindow("solidify_window")

    cmds.windowPref(enableAll=True)

def solidify():
    """
    Launches the 'Solidify' main window.
    """

    solidify_window()
