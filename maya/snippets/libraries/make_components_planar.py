# Credits: Fiend3d (Vlad Tagincev).
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya

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
            "make_components_planar",
            "make_selected_components_planar"]

__interfaces__ = ["make_selected_components_planar"]

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

    mmatrix = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList(matrix, mmatrix)
    return mmatrix

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
    mmatrix = get_mmatrix(matrix)
    mvector = mvector * mmatrix
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

@stacks_handler
def make_components_planar(components):
    """
    Planarizes given components.

    :param components: Components to planarizes.
    :type components: list
    """

    object = cmds.ls(components, o=True)
    if object:
        transform = get_transform(object)
        vertices = cmds.ls(cmds.polyListComponentConversion(components, toVertex=True), fl=True)

        barycenters = cmds.xform(vertices, q=True, t=True, ws=True)
        barycenter = get_average_vector([(barycenters[i], barycenters[i + 1], barycenters[i + 2]) for i in range(0, len(barycenters), 3)])

        normals = [float(normal) for data in cmds.polyInfo(cmds.polyListComponentConversion(components, toFace=True), faceNormals=True) for normal in data.split()[2:5]]
        normals = [(normals[i], normals[i + 1], normals[i + 2]) for i in range(0, len(normals), 3)]
        average_normal = vector_matrix_multiplication(normalize(get_average_vector(normals)), cmds.xform(transform, query=True, matrix=True, worldSpace=True))

        offset = -dot(average_normal, barycenter)

        for vertex in vertices:
            position = cmds.xform(vertex, q=True, t=True, ws=True)
            distance = -(dot(average_normal, position) + offset)
            cmds.xform(vertex, r=True, t=(average_normal[0] * distance, average_normal[1] * distance, average_normal[2] * distance))

@stacks_handler
def make_selected_components_planar():
    """
    Planarizes selected components.
    """

    make_components_planar(cmds.ls(sl=True))
