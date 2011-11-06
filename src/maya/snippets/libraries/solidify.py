import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import math

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2011 - Thomas Mansencal"
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
	This decorator is used to handle various Maya stacks.

	:param object: Python object. ( Object )
	:return: Python function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This decorator is used to handle various Maya stacks.

		:return: Python object. ( Python )
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
	This definition returns transform of the given node.

	:param node: Current object. ( String )
	:param fullPath: Current full path state. ( Boolean )
	:return: Object transform. ( String )
	"""

	transform = node
	if cmds.nodeType(node) != "transform":
		parents = cmds.listRelatives(node, fullPath=fullPath, parent=True)
		transform = parents[0]
	return transform

def getMVector(vector):
	"""
	This definition returns an MVector.

	:param vector: Vector. ( List )
	:return: MVector ( MVector )
	"""

	return OpenMaya.MVector(vector[0], vector[1], vector[2])

def getMMatrix(matrix):
	"""
	This definition returns an MMatrix.

	:param matrix: matrix. ( List )
	:return: MMatrix ( MMatrix )
	"""

	mMatrix = OpenMaya.MMatrix()
	OpenMaya.MScriptUtil.createMatrixFromList(matrix, mMatrix)
	return mMatrix

def normalize(vector):
	"""
	This definition returns the normalized vector.

	:param vector: Vector. ( List )
	:return: Normalized vector ( Tuple )
	"""

	mVector = getMVector(vector)
	mVector.normalize()
	return (mVector.x, mVector.y, mVector.z)

def vectorMatrixMultiplication(vector, matrix):
	"""
	This definition returns the vector multiplication between a Vector And a matrix.

	:param vector: Vector. ( List )
	:param matrix: matrix. ( List )
	:return: Matrix multiplied vector. ( Tuple )
	"""

	mVector = getMVector(vector)
	mMatrix = getMMatrix(matrix)
	mVector = mVector * mMatrix
	return (mVector.x, mVector.y, mVector.z)

def dot(vectorA, vectorB):
	"""
	This definition returns the dot product between two vectors.

	:param vectorA: Vector A. ( List )
	:param vectorB: Vector B. ( List )
	:return: Dot product. ( Float )
	"""

	mVectorA = getMVector(vectorA)
	mVectorB = getMVector(vectorB)
	return mVectorA * mVectorB

def getAverageVector(vectors):
	"""
	This definition returns the average vector from a list of vectors.

	:param vectors: Vectors to get the average one. ( List )
	:return: Average vector. ( List )
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
	This definition returns the angle between two vectors.

	:param vectorA: Vector A. ( List )
	:param vectorB: Vector B. ( List )
	:return: Angle between Vector A and Vector B. ( Float )
	"""

	return math.degrees(math.acos(dot(vectorA, vectorB)))

def hasBorderEdges(object):
	"""
	This definition returns if an object has border edges.

	:param object: Object. ( String )
	:return: Has object border edges. ( Boolean )
	"""

	cmds.select(object)
	cmds.polySelectConstraint(m=3, t=0x8000, w=1)
	cmds.polySelectConstraint(m=0)
	if cmds.ls(sl=True):
		return True

def solidifyObject(object, height=1, divisions=2, history=True):
	"""
	This definition solidifies given object.

	:param object: Object. ( String )
	:param height: Extrusion height. ( Float )
	:param division: Extrusion divisions. ( Float )
	:param history: Keep construction history. ( Boolean )
	"""

	if	hasBorderEdges(object):
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
		cmds.polyEditUV(uvs, u=1, v=0)

		extendedFaces = cmds.ls(faces, fl=True)
		for i in range(divisions):
			adjacentEdges = cmds.polyListComponentConversion(extendedFaces, ff=True, te=True)
			extendedFaces.extend(cmds.ls(cmds.polyListComponentConversion(adjacentEdges, fe=True, tf=True), fl=True))

		borderFaces = list(set(extendedFaces).difference(set(cmds.ls(faces, fl=True))))
		cmds.select(borderFaces)
		cmds.polyAutoProjection(borderFaces, t=barycenter, ry=getAngle((0, 0, 1), averageNormal), rz=getAngle((1, 0, 0), averageNormal))
		uvs = cmds.polyListComponentConversion(borderFaces, toUV=1)
		cmds.polyEditUV(uvs, u=2, v=0)

		not history and cmds.delete(object, ch=True)

@stacksHandler
def solidify_button_OnClicked(state=None):
	"""
	This definition is triggered by the **solidify_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	for object in cmds.ls(sl=True, l=True, o=True):
		solidifyObject(object, height=cmds.floatSliderGrp("height_floatSliderGrp", q=True, v=True), divisions=cmds.intSliderGrp("divisions_intSliderGrp", q=True, v=True), history=cmds.checkBox("keepConstructionHistory_checkBox", q=True, v=True))

def solidify_window():
	"""
	This definition creates the 'Solidify' main window.
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

	cmds.floatSliderGrp("height_floatSliderGrp", label="Height", field=True, minValue= -10, maxValue=10, fieldMinValue= -65535, fieldMaxValue=65535, value=0.1)
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
	This definition launches the 'Solidify' main window.
	"""

	solidify_window()

@stacksHandler
def ISolidify():
	"""
	This definition is the solidify definition Interface.
	"""

	solidify()
