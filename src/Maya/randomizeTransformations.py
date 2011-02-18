import random
import maya.cmds as cmds

def randomizeTranslations( objects, randomRange = 15 ):
	for object in objects:
		cmds.setAttr( object + ".tx", cmds.getAttr( object + ".tx" ) + random.randrange( -randomRange, randomRange ) )
		cmds.setAttr( object + ".ty", cmds.getAttr( object + ".ty" ) + random.randrange( -randomRange, randomRange ) )
		cmds.setAttr( object + ".tz", cmds.getAttr( object + ".tz" ) + random.randrange( -randomRange, randomRange ) )

def randomizeRotations( objects, randomRange = 5 ):
	for object in objects:
		cmds.setAttr( object + ".rx", cmds.getAttr( object + ".rx" ) + random.randrange( -randomRange, randomRange ) )
		cmds.setAttr( object + ".ry", cmds.getAttr( object + ".ry" ) + random.randrange( -randomRange, randomRange ) )
		cmds.setAttr( object + ".rz", cmds.getAttr( object + ".rz" ) + random.randrange( -randomRange, randomRange ) )

def randomizeScales( objects, randomRange = 2 ):
	for object in objects:
		randomValue = random.randrange( -randomRange, randomRange ) * ( random.random() / 10 )
		cmds.setAttr( object + ".sx", cmds.getAttr( object + ".sx" ) + randomValue )
		cmds.setAttr( object + ".sy", cmds.getAttr( object + ".sy" ) + randomValue )
		cmds.setAttr( object + ".sz", cmds.getAttr( object + ".sz" ) + randomValue )

objects = cmds.ls( sl = True, l = True )
randomizeTranslations( objects, 25 )
randomizeRotations( objects, 24 )
randomizeScales( objects, 5 )
