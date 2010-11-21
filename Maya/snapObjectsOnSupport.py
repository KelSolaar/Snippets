import maya.cmds as cmds

def getShapes( object, fullPathState = False, noIntermediateState = True ):

	objectShapes = []
	shapes = cmds.listRelatives( object, fullPath = fullPathState, shapes = True, noIntermediate = noIntermediateState )
	if shapes != None :
		objectShapes = shapes

	return objectShapes

def snapObjectsOnSupport( support, objects ) :
    if cmds.pluginInfo( "nearestPointOnMesh", q = True, loaded = False ) :
    	cmds.loadPlugin( "nearestPointOnMesh" )
    
    nearestPointOnMesh = cmds.createNode( "nearestPointOnMesh" )
    supportShape = getShapes(support)[0]
    cmds.connectAttr( supportShape + ".outMesh", nearestPointOnMesh + ".inMesh", f = True )
    
    allAxis = ("X", "Y", "Z")
    for object in objects :
        for axis in allAxis :
            cmds.setAttr(nearestPointOnMesh + ".inPosition" + axis, cmds.getAttr(object + ".translate" + axis) )
        for axis in allAxis :
            cmds.setAttr(object + ".translate" + axis, cmds.getAttr(nearestPointOnMesh + ".position" + axis) )

    cmds.delete( nearestPointOnMesh )
        
objects = cmds.ls(sl = True, l = True)
snapObjectsOnSupport( "ground", objects)