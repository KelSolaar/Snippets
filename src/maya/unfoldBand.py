# Unfold Band.
import maya.cmds as cmds
import maya.mel as mel

def unfoldBand(object, divisions=1, history=True):
	cmds.select(object)
	edgesCount = cmds.polyEvaluate(object, edge=True)
	edges = cmds.ls(object +".e[0:" + str(edgesCount-1) + "]", fl=True, l=True)

	cmds.polySelectConstraint(m=3, t=0x8000, w=1)
	mel.eval("resetPolySelectConstraint;")
	for i in range(divisions):
		mel.eval("GrowPolygonSelectionRegion();")
	bandEdges = cmds.ls(sl=True, fl=True, l=True)
	bandFaces = cmds.ls(cmds.polyListComponentConversion(bandEdges, fe=True, tf=True), fl=True)
	cmds.select(bandFaces)
	cmds.polyForceUV(unitize=True)
	cmds.polySelectConstraint(m=3, t=0x8000, sm=1)
	seamsEdges = cmds.ls(sl=True, fl=True, l=True)
	weldEdges = list(set(bandEdges).difference(set(seamsEdges)))
	cmds.polyMapSewMove(weldEdges)
	cmds.polyLayoutUV(bandFaces, scale=1, rotateForBestFit=0, layout=1)
	uvs = cmds.polyListComponentConversion(bandFaces, toUV=1)
	cmds.polyEditUV(uvs, u=1, v=0)

	not history and cmds.delete(object, ch=True)

for object in cmds.ls(sl=True):
	unfoldBand(object, divisions=10, history=False)