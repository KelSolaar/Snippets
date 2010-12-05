import random
import maya.cmds as cmds

def replaceObjects( sources, targets, inPlace = False, usePivot = False, useInstances = False ) :

	replacementObjects = []
	for target in targets :
		replacementObject = cmds.duplicate( sources[random.randrange(0, len(sources))], rr = True )[0]
		replacementObjects.append(replacementObject)
		if inPlace :
			pass
		else :
			if usePivot :
				components = ( "rx", "ry", "rz", "sx", "sy", "sz")
				pivot = cmds.xform( target, query = True, worldSpace = True, rotatePivot = True )
				for i, component  in enumerate( ("tx", "ty", "tz") ) :
					cmds.setAttr(replacementObject + "." + component, pivot[i])
			else :
				components = ( "tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz")
				
			for component in components :
				cmds.setAttr(replacementObject + "." + component, cmds.getAttr(target + "." + component))

	if not inPlace :
		replacementGrp = cmds.group( em = True )
		for replacementObject in replacementObjects :
			cmds.parent(replacementObject, replacementGrp)
		cmds.rename(replacementGrp, "replacement_grp")

sources = cmds.listRelatives( "sources_grp", fullPath = True )
targets = cmds.ls( sl = True, l = True)
replaceObjects( sources, targets, False, True, False )