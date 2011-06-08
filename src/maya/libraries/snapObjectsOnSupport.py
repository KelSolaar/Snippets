import maya.cmds as cmds

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

def getShapes(object, fullPathState = False, noIntermediateState = True):
	'''
	This Definition Returns Shapes Of The Provided Object.

	@param object_: Current Object. ( String )
	@param fullPath: Current Full Path State. ( Boolean )
	@param noIntermediate: Current No Intermediate State. ( Boolean )
	@return: Objects Shapes. ( List )
	'''

	objectShapes = []
	shapes = cmds.listRelatives(object, fullPath = fullPathState, shapes = True, noIntermediate = noIntermediateState)
	if shapes != None:
		objectShapes = shapes

	return objectShapes

def snapObjectsOnSupport(objects, support):
	'''
	This Definition Snaps Objects On Support.

	@param objects : Objects To Snap. ( List )
	@param value : Support. ( String )
	'''

	if cmds.pluginInfo("nearestPointOnMesh", q = True, loaded = False):
		cmds.loadPlugin("nearestPointOnMesh")

	nearestPointOnMesh = cmds.createNode("nearestPointOnMesh")
	supportShape = getShapes(support)[0]
	cmds.connectAttr(supportShape + ".outMesh", nearestPointOnMesh + ".inMesh", f = True)

	allAxis = ("X", "Y", "Z")
	for object in objects:
		for axis in allAxis:
			cmds.setAttr(nearestPointOnMesh + ".inPosition" + axis, cmds.getAttr(object + ".translate" + axis))
		for axis in allAxis:
			cmds.setAttr(object + ".translate" + axis, cmds.getAttr(nearestPointOnMesh + ".position" + axis))

	cmds.delete(nearestPointOnMesh)

@stacksHandler
def ISnapObjectsOnSupport():
	'''
	This Definition Is The snapObjectsOnSupport Method Interface.
	'''

	selection = cmds.ls(sl = True, l = True)
	selection and snapObjectsOnSupport(selection[:-1], selection[-1])
