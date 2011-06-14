import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import math

def stacksHandler(object_):
	"""
	This Decorator Is Used To Handle Various Maya Stacks.

	@param object_: Python Object. ( Object )
	@return: Python Function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This Decorator Is Used To Handle Various Maya Stacks.

		@return: Python Object. ( Python )
		"""
		
		cmds.undoInfo(openChunk=True)
		value = object_(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya Produces A Weird Command Error If Not Wrapped Here.
		try:
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")"% (__name__, __name__, object_.__name__), addCommandLabel=object_.__name__)
		except:
			pass
		return value

	return stacksHandlerCall

def getTransform(node, fullPath=True):
	"""
	This Definition Returns Transform Of The Provided Node.

	@param node: Current Object. ( String )
	@param fullPath: Current Full Path State. ( Boolean )
	@return: Object Transform. ( String )
	"""
	
	transform = node
	if cmds.nodeType(node) != "transform":
		parents = cmds.listRelatives(node, fullPath=fullPath, parent=True)
		transform = parents[0]
	return transform

def getMVector(vector):
	"""
	This Definition Returns An MVector.

	@param vector: Vector. ( List )
	@return: MVector ( MVector )
	"""
	
	return OpenMaya.MVector(vector[0], vector[1], vector[2])

def getMMatrix(matrix):
	"""
	This Definition Returns An MMatrix.

	@param matrix: matrix. ( List )
	@return: MMatrix ( MMatrix )
	"""
	
	mMatrix = OpenMaya.MMatrix()
	OpenMaya.MScriptUtil.createMatrixFromList(matrix, mMatrix)
	return mMatrix

def normalize(vector):
	"""
	This Definition Returns The Normalized Vector.

	@param vector: Vector. ( List )
	@return: Normalized Vector ( Tuple )
	"""
	
	mVector = getMVector(vector)
	mVector.normalize()
	return (mVector.x, mVector.y, mVector.z)

def vectorMatrixMultiplication(vector, matrix):
	"""
	This Definition Returns The Vector Multiplication Between A Vector And A Matrix.

	@param vector: Vector. ( List )
	@param matrix: matrix. ( List )
	@return: Matrix Multiplied Vector. ( Tuple )
	"""
	
	mVector = getMVector(vector)
	mMatrix = getMMatrix(matrix)
	mVector = mVector * mMatrix
	return (mVector.x, mVector.y, mVector.z)

def dot(vectorA, vectorB):
	"""
	This Definition Returns The Dot Product Between Two Vectors.

	@param vectorA: Vector A. ( List )
	@param vectorB: Vector B. ( List )
	@return: Dot Product. ( Float )
	"""
	
	mVectorA = getMVector(vectorA)
	mVectorB = getMVector(vectorB)
	return mVectorA * mVectorB

def getAverageVector(vectors):
	"""
	This Definition Returns The Average Vector From A List Of Vectors.

	@param vectors: Vectors To Get The Average One. ( List )
	@return: Average Vector. ( List )
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
	This Definition Returns The Angle Between Two Vectors.

	@param vectorA: Vector A. ( List )
	@param vectorB: Vector B. ( List )
	@return: Angle Between Vector A and Vector B. ( Float )
	"""

	return math.degrees(math.acos(dot(vectorA, vectorB)))

def hasBorderEdges(object):
	"""
	This Definition Returns If An Object Has Border Edges.
	
	@param object: Object. ( String )
	@return: Has Object Border Edges. ( Boolean )
	"""

	cmds.select(object)
	cmds.polySelectConstraint(m=3, t=0x8000, w=1)
	cmds.polySelectConstraint(m=0)
	if cmds.ls(sl=True):
		return True

def solidifyObject(object, height=1, divisions=2, history=True):
	"""
	This Definition Solidifies Provided Object.
	
	@param object: Object. ( String )
	@param height: Extrusion Height. ( Float )
	@param division: Extrusion Divisions. ( Float )
	@param history: Keep Construction History. ( Boolean )
	"""

	if  hasBorderEdges(object):
		transform = getTransform(object)
		vertices = cmds.ls(cmds.polyListComponentConversion(object, toVertex = True), fl = True)

		barycenters = cmds.xform(vertices, q = True, t = True, ws = True)
		barycenter = getAverageVector([(barycenters[i], barycenters[i + 1], barycenters[i + 2]) for i in range(0, len(barycenters), 3)])

		normals = cmds.polyNormalPerVertex(cmds.polyListComponentConversion(object, toVertexFace = True), q = True, xyz = True)
		normals = [(normals[i], normals[i + 1], normals[i + 2]) for i in range(0, len(normals), 3)]
		averageNormal = vectorMatrixMultiplication(normalize(getAverageVector(normals)), cmds.xform(transform, query = True, matrix = True, worldSpace = True))

		facesCount = cmds.polyEvaluate(object, face=True)
		faces = object +".f[0:" + str(facesCount-1) + "]"
		extrude = cmds.polyExtrudeFacet(faces, constructionHistory=1, keepFacesTogether=1, divisions=divisions)
		cmds.setAttr(extrude[0] + ".localTranslateZ", height)
		borderEdges = cmds.polyListComponentConversion(faces, te=True, bo=True)
		cmds.polyMapCut(borderEdges)
		uvs = cmds.polyListComponentConversion(object +".f[0:" + str(facesCount-1) + "]", toUV=1)
		cmds.polyEditUV(uvs, u=1, v=0)

		extendedFaces = cmds.ls(faces, fl=True)
		for i in range(divisions):
			adjacentEdges = cmds.polyListComponentConversion(extendedFaces, ff=True, te=True)
			extendedFaces.extend(cmds.ls(cmds.polyListComponentConversion(adjacentEdges, fe=True, tf=True), fl=True))

		borderFaces = list(set(extendedFaces).difference(set(cmds.ls(faces, fl=True))))
		cmds.select(borderFaces)
		cmds.polyAutoProjection(borderFaces, t=barycenter, ry=getAngle((0,0,1), averageNormal), rz=getAngle((1,0,0), averageNormal))
		uvs = cmds.polyListComponentConversion(borderFaces, toUV=1)
		cmds.polyEditUV(uvs, u=2, v=0)
	
		not history and cmds.delete(object, ch=True)

def solidify_Button_OnClicked(state):
	"""
	This Definition Is Triggered By The solidify_Button Button When Clicked.
	
	@param state: Button State. ( Boolean )
	"""
	
	for object in cmds.ls(sl=True, l=True, o=True):
		solidifyObject(object, height=cmds.floatSliderGrp("height_FloatSliderGrp", q=True, v=True), divisions=cmds.intSliderGrp("divisions_IntSliderGrp", q=True, v=True), history=cmds.checkBox("keepConstructionHistory_CheckBox", q=True, v=True))
	
def solidify_Window():
	"""
	This Definition Creates The Solidify Main Window.
	"""
	
	cmds.windowPref(enableAll=False)

	if (cmds.window("solidify_Window", exists=True)):
		cmds.deleteUI("solidify_Window")

	cmds.window("solidify_Window",
		title="Solidify",
		width=320)

	spacing=5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.separator(height=10, style="singleDash")

	cmds.floatSliderGrp("height_FloatSliderGrp", label="Height", field=True, minValue=-10, maxValue=10, fieldMinValue=-65535, fieldMaxValue=65535, value=0.1)
	cmds.intSliderGrp("divisions_IntSliderGrp", label="Divisions", field=True, minValue=0, maxValue=10, fieldMinValue=0, fieldMaxValue=65535, value=2)
	
	cmds.separator(style="single")
	
	cmds.columnLayout(columnOffset=("left", 140) )
	cmds.checkBox("keepConstructionHistory_CheckBox", label="Keep Construction History",  v=True)
	cmds.setParent(topLevel=True)

	cmds.separator(height=10, style="singleDash")
	
	cmds.button("solidify_Button", label="Solidify!", command=solidify_Button_OnClicked)

	cmds.showWindow("solidify_Window")

	cmds.windowPref(enableAll=True)

def solidify():
	"""
	This Definition Launches The Solidify Main Window.
	"""

	solidify_Window()

@stacksHandler
def ISolidify():
	"""
	This Definition Is The solidify Method Interface.
	"""
	
	solidify()	
