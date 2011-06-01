# Cleanup Hierarchical Subdivision Polygon Conversion.
import maya.cmds as cmds

def cleanupHierarchicalSubdivisionConversion(object):
	cmds.select(object)
	cmds.polySelectConstraint(m=3, t=8, sz=3)
	cmds.polySelectConstraint(dis=True)
	nsidesFaces = cmds.ls(sl=True, l=True, fl=True)
	cmds.select(nsidesFaces)
	cmds.polySelectConstraint(m=3, t=1, order=True, orb=(3, 3))
	cmds.polySelectConstraint(dis=True)
	nsideVertices = cmds.ls(sl=True, l=True, fl=True)
	offendingEdges = []
	for vertice in nsideVertices:
	    faces = cmds.ls(cmds.polyListComponentConversion(vertice, fv=True, tf=True), fl=True, l=True)
	    faces = [face for face in faces if not face in nsidesFaces]
	    if len(faces) == 2:
	        faceEdgesA = cmds.ls(cmds.polyListComponentConversion(faces[0], ff=True, te=True), fl=True, l=True)
	        faceEdgesB = cmds.ls(cmds.polyListComponentConversion(faces[1], ff=True, te=True), fl=True, l=True)
	        sharedEdge = list(set(faceEdgesA).intersection(faceEdgesB))
	        offendingEdges.append(sharedEdge[0])
	cmds.polySelectSp(offendingEdges, loop=True)
	cmds.polyDelEdge(cmds.ls(sl=True), cv=True, ch=True)
	cmds.select(object)

def ICleanupHierarchicalSubdivisionConversion():
	for object in cmds.ls(sl=True, l=True):
		cleanupHierarchicalSubdivisionConversion(object)
