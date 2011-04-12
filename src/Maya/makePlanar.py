# Original MelScript Code By Fiend3d (Vlad Tagincev).
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya

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

def makePlanar():
	object = cmds.ls(sl = True, o = True)
	if object:
		selection = cmds.ls(sl = True)
		transform = getTransform(object)
		vertices = cmds.ls(cmds.polyListComponentConversion(selection, toVertex = True), fl = True)

		barycenters = cmds.xform(vertices, q = True, t = True, ws = True)
		barycenter = getAverageVector([(barycenters[i], barycenters[i + 1], barycenters[i + 2]) for i in range(0, len(barycenters), 3)])

		normals = cmds.polyNormalPerVertex(cmds.polyListComponentConversion(selection, toVertexFace = True), q = True, xyz = True)
		normals = [(normals[i], normals[i + 1], normals[i + 2]) for i in range(0, len(normals), 3)]
		averageNormal = vectorMatrixMultiplication(normalize(getAverageVector(normals)), cmds.xform(transform, query = True, matrix = True, worldSpace = True))

		offset = -dot(averageNormal, barycenter)

		for vertex in vertices:
			position = cmds.xform(vertex, q = True, t = True, ws = True)
			distance = -(dot(averageNormal, position) + offset)
			cmds.xform(vertex, r = True, t = (averageNormal[0] * distance, averageNormal[1] * distance, averageNormal[2] * distance))

makePlanar()
