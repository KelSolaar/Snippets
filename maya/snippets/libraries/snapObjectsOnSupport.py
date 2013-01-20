import maya.cmds as cmds

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacksHandler",
			"getShapes",
			"snapObjectsOnSupport",
			"ISnapObjectsOnSupport"]

def stacksHandler(object):
	"""
	This decorator is used to handle various Maya stacks.

	:param object: Python object. ( Object )
	:return: Python function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This decorator is used to handle various Maya stacks.

		:return: Python object. ( Python )
		"""

		cmds.undoInfo(openChunk=True)
		value = object(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya produces a weird command error if not wrapped here.
		try:
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")" % (__name__, __name__, object.__name__), addCommandLabel=object.__name__)
		except:
			pass
		return value

	return stacksHandlerCall

def getShapes(object, fullPathState=False, noIntermediateState=True):
	"""
	This definition returns shapes of the given object.

	:param object: Current object. ( String )
	:param fullPath: Current full path state. ( Boolean )
	:param noIntermediate: Current no intermediate state. ( Boolean )
	:return: Objects shapes. ( List )
	"""

	objectShapes = []
	shapes = cmds.listRelatives(object, fullPath=fullPathState, shapes=True, noIntermediate=noIntermediateState)
	if shapes != None:
		objectShapes = shapes

	return objectShapes

def snapObjectsOnSupport(objects, support):
	"""
	This definition snaps objects on support.

	:param objects: Objects to snap. ( List )
	:param value: Support. ( String )
	"""

	if cmds.pluginInfo("nearestPointOnMesh", q=True, loaded=False):
		cmds.loadPlugin("nearestPointOnMesh")

	nearestPointOnMesh = cmds.createNode("nearestPointOnMesh")
	supportShape = getShapes(support)[0]
	cmds.connectAttr(supportShape + ".outMesh", nearestPointOnMesh + ".inMesh", f=True)

	allAxis = ("X", "Y", "Z")
	for object in objects:
		for axis in allAxis:
			cmds.setAttr(nearestPointOnMesh + ".inPosition" + axis, cmds.getAttr(object + ".translate" + axis))
		for axis in allAxis:
			cmds.setAttr(object + ".translate" + axis, cmds.getAttr(nearestPointOnMesh + ".position" + axis))

	cmds.delete(nearestPointOnMesh)

@stacksHandler
def ISnapObjectsOnSupport():
	"""
	This definition is the snapObjectsOnSupport definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and snapObjectsOnSupport(selection[:-1], selection[-1])
