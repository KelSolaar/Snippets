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

__all__ = ["stacksHandler",
			"getTransform",
			"getMVector",
			"getMMatrix",
			"normalize",
			"vectorMatrixMultiplication",
			"dot",
			"getAverageVector",
			"makePlanar",
			"IMakePlanar"]

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
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")" % (__name__, __name__, object.__name__), addCommandLabel=object.__name__)
		except:
			pass
		return value

	return stacksHandlerCall

def getTransform(node, fullPath=True):
	"""
	Returns transform of the given node.

	:param node: Current object.
	:type node: str
	:param fullPath: Current full path state.
	:type fullPath: bool
	:return: Object transform.
	:rtype: str
	"""

	transform = node
	if cmds.nodeType(node) != "transform":
		parents = cmds.listRelatives(node, fullPath=fullPath, parent=True)
		transform = parents[0]
	return transform

def getMVector(vector):
	"""
	Returns an MVector.

	:param vector: Vector.
	:type vector: list
	:return: MVector
	:rtype: MVector
	"""

	return OpenMaya.MVector(vector[0], vector[1], vector[2])

def getMMatrix(matrix):
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

	mVector = getMVector(vector)
	mVector.normalize()
	return (mVector.x, mVector.y, mVector.z)

def vectorMatrixMultiplication(vector, matrix):
	"""
	Returns the vector multiplication between a Vector And a matrix.

	:param vector: Vector.
	:type vector: list
	:param matrix: matrix.
	:type matrix: list
	:return: Matrix multiplied vector.
	:rtype: tuple
	"""

	mVector = getMVector(vector)
	mMatrix = getMMatrix(matrix)
	mVector = mVector * mMatrix
	return (mVector.x, mVector.y, mVector.z)

def dot(vectorA, vectorB):
	"""
	Returns the dot product between two vectors.

	:param vectorA: Vector A.
	:type vectorA: list
	:param vectorB: Vector B.
	:type vectorB: list
	:return: Dot product.
	:rtype: float
	"""

	mVectorA = getMVector(vectorA)
	mVectorB = getMVector(vectorB)
	return mVectorA * mVectorB

def getAverageVector(vectors):
	"""
	Returns the average vector from a list of vectors.

	:param vectors: Vectors to get the average one.
	:type vectors: list
	:return: Average vector.
	:rtype: list
	"""

	averageVector = [0, 0, 0]
	for vector in vectors:
		for i in range(3):
			averageVector[i] += vector[i]
	for i in range(3):
		averageVector[i] = averageVector[i] / len(vectors)
	return averageVector

def makePlanar(components):
	"""
	Planarizes the given Components.

	:param components: Components to planarizes.
	:type components: list
	"""

	object = cmds.ls(components, o=True)
	if object:
		transform = getTransform(object)
		vertices = cmds.ls(cmds.polyListComponentConversion(components, toVertex=True), fl=True)

		barycenters = cmds.xform(vertices, q=True, t=True, ws=True)
		barycenter = getAverageVector([(barycenters[i], barycenters[i + 1], barycenters[i + 2]) for i in range(0, len(barycenters), 3)])

		normals = [float(normal) for data in cmds.polyInfo(cmds.polyListComponentConversion(components, toFace=True), faceNormals=True) for normal in data.split()[2:5]]
		normals = [(normals[i], normals[i + 1], normals[i + 2]) for i in range(0, len(normals), 3)]
		averageNormal = vectorMatrixMultiplication(normalize(getAverageVector(normals)), cmds.xform(transform, query=True, matrix=True, worldSpace=True))

		offset = -dot(averageNormal, barycenter)

		for vertex in vertices:
			position = cmds.xform(vertex, q=True, t=True, ws=True)
			distance = -(dot(averageNormal, position) + offset)
			cmds.xform(vertex, r=True, t=(averageNormal[0] * distance, averageNormal[1] * distance, averageNormal[2] * distance))

@stacksHandler
def IMakePlanar():
	"""
	Defines the makePlanar definition Interface.
	"""

	makePlanar(cmds.ls(sl=True))
