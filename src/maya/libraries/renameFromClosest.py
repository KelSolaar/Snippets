# Rename From Closest.
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

def getMPoint(point):
	return OpenMaya.MPoint(point[0], point[1], point[2])

def norme(pointA, pointB):
	mPointA = getMPoint(pointA)
	mPointB = getMPoint(pointB)
	mVector = mPointA - mPointB
	return mVector.length()

def renameFromClosest(sources, target, suffixe="_"):
    targetBarycenter = cmds.objectCenter(target, gl=True)
    
    normes = {}
    for source in sources:
        normes[source] = norme(targetBarycenter, cmds.objectCenter(source, gl=True))
    closest = min(normes, key=lambda item: normes[item])
    cmds.rename(target, "%s%s" % (closest.split("|")[-1], suffixe) )

def IRenameFromClosest():
	sources = cmds.ls(sl=True, l=True)
	targets = cmds.ls(sl=True, l=True)

	for target in targets:
    		renameFromClosest(sources, target)
