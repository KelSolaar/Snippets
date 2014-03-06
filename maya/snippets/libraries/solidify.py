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

__all__ = ["stacksHandler",
			"getTransform",
			"getMVector",
			"getMMatrix",
			"normalize",
			"vectorMatrixMultiplication",
			"dot",
			"getAverageVector",
			"getAngle",
			"hasBorderEdges",
			"solidifyObject",
			"solidify_button_OnClicked",
			"solidify_window",
			"solidify",
			"ISolidify"]

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

def getAngle(vectorA, vectorB):
	"""
	Returns the angle between two vectors.

	:param vectorA: Vector A.
	:type vectorA: list
	:param vectorB: Vector B.
	:type vectorB: list
	:return: Angle between Vector A and Vector B.
	:rtype: float
	"""

	return math.degrees(math.acos(dot(vectorA, vectorB)))

def hasBorderEdges(object):
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

def solidifyObject(object, height=1, divisions=2, history=True):
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

	if hasBorderEdges(object):
		transform = getTransform(object)
		vertices = cmds.ls(cmds.polyListComponentConversion(object, toVertex=True), fl=True)

		barycenters = cmds.xform(vertices, q=True, t=True, ws=True)
		barycenter = getAverageVector([(barycenters[i], barycenters[i + 1], barycenters[i + 2]) for i in range(0, len(barycenters), 3)])

		normals = cmds.polyNormalPerVertex(cmds.polyListComponentConversion(object, toVertexFace=True), q=True, xyz=True)
		normals = [(normals[i], normals[i + 1], normals[i + 2]) for i in range(0, len(normals), 3)]
		averageNormal = vectorMatrixMultiplication(normalize(getAverageVector(normals)), cmds.xform(transform, query=True, matrix=True, worldSpace=True))

		facesCount = cmds.polyEvaluate(object, face=True)
		faces = object + ".f[0:" + str(facesCount - 1) + "]"
		extrude = cmds.polyExtrudeFacet(faces, constructionHistory=1, keepFacesTogether=1, divisions=divisions)
		cmds.setAttr(extrude[0] + ".localTranslateZ", height)
		borderEdges = cmds.polyListComponentConversion(faces, te=True, bo=True)
		cmds.polyMapCut(borderEdges)
		uvs = cmds.polyListComponentConversion(object + ".f[0:" + str(facesCount - 1) + "]", toUV=1)
		cmds.polyEditUV(uvs, u=0, v=-5)

		extendedFaces = cmds.ls(faces, fl=True)
		for i in range(divisions):
			adjacentEdges = cmds.polyListComponentConversion(extendedFaces, ff=True, te=True)
			extendedFaces.extend(cmds.ls(cmds.polyListComponentConversion(adjacentEdges, fe=True, tf=True), fl=True))

		borderFaces = list(set(extendedFaces).difference(set(cmds.ls(faces, fl=True))))
		cmds.select(borderFaces)
		cmds.polyAutoProjection(borderFaces, t=barycenter, ry=getAngle((0, 0, 1), averageNormal), rz=getAngle((1, 0, 0), averageNormal))
		uvs = cmds.polyListComponentConversion(borderFaces, toUV=1)
		cmds.polyEditUV(uvs, u=0, v=-5)

		not history and cmds.delete(object, ch=True)

@stacksHandler
def solidify_button_OnClicked(state=None):
	"""
	Defines the slot triggered by **solidify_button** button when clicked.

	:param state: Button state.
	:type state: bool
	"""

	for object in cmds.ls(sl=True, l=True, o=True):
		solidifyObject(object, height=cmds.floatSliderGrp("height_floatSliderGrp", q=True, v=True), divisions=cmds.intSliderGrp("divisions_intSliderGrp", q=True, v=True), history=cmds.checkBox("keepConstructionHistory_checkBox", q=True, v=True))

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
	cmds.checkBox("keepConstructionHistory_checkBox", label="Keep Construction History", v=True)
	cmds.setParent(topLevel=True)

	cmds.separator(height=10, style="singleDash")

	cmds.button("solidify_button", label="Solidify!", command=solidify_button_OnClicked)

	cmds.showWindow("solidify_window")

	cmds.windowPref(enableAll=True)

def solidify():
	"""
	Launches the 'Solidify' main window.
	"""

	solidify_window()

@stacksHandler
def ISolidify():
	"""
	Defines the solidify definition Interface.
	"""

	solidify()
