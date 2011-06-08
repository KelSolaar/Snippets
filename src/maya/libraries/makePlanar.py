# Credits: Fiend3d (Vlad Tagincev).
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya

def stacksHandler(object_):
	'''
	This Decorator Is Used To Handle Various Maya Stacks.

	@param object_: Python Object ( Object )
	@return: Python Function. ( Function )
	'''

	def stacksHandlerCall(*args, **kwargs):
		'''
		This Decorator Is Used To Handle Various Maya Stacks.

		@return: Python Object. ( Python )
		'''
		
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
	'''
	This Definition Returns Transform Of The Provided Node.

	@param node: Current Object. ( String )
	@param fullPath: Current Full Path State. ( Boolean )
	@return: Object Transform. ( String )
	'''
	
	transform = node
	if cmds.nodeType(node) != "transform":
		parents = cmds.listRelatives(node, fullPath=fullPath, parent=True)
		transform = parents[0]
	return transform

def getMVector(vector):
	'''
	This Definition Returns An MVector.

	@param vector: Vector. ( List )
	@return: MVector ( MVector )
	'''
	
	return OpenMaya.MVector(vector[0], vector[1], vector[2])

def getMMatrix(matrix):
	'''
	This Definition Returns An MMatrix.

	@param matrix: matrix. ( List )
	@return: MMatrix ( MMatrix )
	'''
	
	mMatrix = OpenMaya.MMatrix()
	OpenMaya.MScriptUtil.createMatrixFromList(matrix, mMatrix)
	return mMatrix

def normalize(vector):
	'''
	This Definition Returns The Normalized Vector.

	@param vector: Vector. ( List )
	@return: Normalized Vector ( Tuple )
	'''
	
	mVector = getMVector(vector)
	mVector.normalize()
	return (mVector.x, mVector.y, mVector.z)

def vectorMatrixMultiplication(vector, matrix):
	'''
	This Definition Returns The Vector Multiplication Between A Vector And A Matrix.

	@param vector: Vector. ( List )
	@param matrix: matrix. ( List )
	@return: Matrix Multiplied Vector. ( Tuple )
	'''
	
	mVector = getMVector(vector)
	mMatrix = getMMatrix(matrix)
	mVector = mVector * mMatrix
	return (mVector.x, mVector.y, mVector.z)

def dot(vectorA, vectorB):
	'''
	This Definition Returns The Dot Product Between Two Vectors.

	@param vectorA: Vector A. ( List )
	@param vectorB: Vector B. ( List )
	@return: Dot Product. ( Float )
	'''
	
	mVectorA = getMVector(vectorA)
	mVectorB = getMVector(vectorB)
	return mVectorA * mVectorB

def getAverageVector(vectors):
	'''
	This Definition Returns The Average Vector From A List Of Vectors.

	@param vectors: Vectors To Get The Average One. ( List )
	@return: Average Vector. ( List )
	'''
	
	averageVector = [0, 0, 0]
	for vector in vectors:
		for i in range(3):
			averageVector[i] += vector[i]
	for i in range(3):
		averageVector[i]=averageVector[i] / len(vectors)
	return averageVector

def makePlanar(components):
	'''
	This Definition Planarizes The Provided Components.

	@param components: Components To Planarizes. ( List )
	'''
	
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
	'''
	This Definition Is The makePlanar Method Interface.
	'''
	
	makePlanar(cmds.ls(sl=True))
