# Solidify.
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import math

def getTransform(object, fullPathState = True):
	if (cmds.nodeType(object) != "transform"):
		parents = cmds.listRelatives(object, fullPath = fullPathState, parent = True)
		return parents[0]
	return object

def getMVector(vector):
	return OpenMaya.MVector(vector[0], vector[1], vector[2])

def getMMatrix(matrix):
	mMatrix = OpenMaya.MMatrix()
	OpenMaya.MScriptUtil.createMatrixFromList(matrix, mMatrix)
	return mMatrix

def normalize(vector):
	mVector = getMVector(vector)
	mVector.normalize()
	return (mVector.x, mVector.y, mVector.z)

def vectorMatrixMultiplication(vector, matrix):
	mVector = getMVector(vector)
	mMatrix = getMMatrix(matrix)
	mVector = mVector * mMatrix
	return (mVector.x, mVector.y, mVector.z)

def dot(vectorA, vectorB):
	mVectorA = getMVector(vectorA)
	mVectorB = getMVector(vectorB)
	return mVectorA * mVectorB

def getAverageVector(vectors):
	averageVector = [0, 0, 0]
	for vector in vectors:
		for i in range(3):
			averageVector[i] += vector[i]
	for i in range(3):
		averageVector[i] = averageVector[i] / len(vectors)
	return averageVector

def getAngle(vectorA, vectorB):
	return math.degrees(math.acos(dot(vectorA, vectorB)))

def solidify(object, height=1, divisions=2, history=True):
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

def ISolidify():
	for object in cmds.ls(sl=True, l=True):
		solidify(object, height=-.5, divisions=2, history=False)
