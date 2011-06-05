# Rename From Closest.
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

def getMPoint(point):
	'''
	This Definition Returns An MPoint.

	@param point: Point. ( List )
	@return: MPoint ( MVector )
	'''
	
	return OpenMaya.MPoint(point[0], point[1], point[2])

def norme(pointA, pointB):
	'''
	This Definition Returns The Norme Of A Vector.

	@param pointA: Point A. ( List )
	@param pointB: Point B. ( List )
	@return: Norme ( Float )
	'''
	
	mPointA = getMPoint(pointA)
	mPointB = getMPoint(pointB)
	mVector = mPointA - mPointB
	return mVector.length()

def renameFromClosest(sources, targets, suffixe="_"):
 	'''
	This Definition Returns The Norme Of A Vector.

	@param sources: Sources Objects. ( List )
	@param targets: Targets Objects. ( List )
	@param suffixe: Rename Suffixe. ( String )
	'''
	
	for target in targets:
		targetBarycenter = cmds.objectCenter(target, gl=True)
       	normes = {}
    	for source in sources:
        	normes[source] = norme(targetBarycenter, cmds.objectCenter(source, gl=True))
    		closest = min(normes, key=lambda item: normes[item])
    		cmds.rename(target, "%s%s" % (closest.split("|")[-1], suffixe) )

def IRenameFromClosest():
	'''
	This Definition Is The renameFromClosest Method Interface.
	'''

	renameFromClosest(sources, targets)
