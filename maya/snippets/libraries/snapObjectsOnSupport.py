import maya.cmds as cmds

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
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
	Handles Maya stacks.

	:param object: Python object.
	:type object: object
	:return: Python function.
	:rtype: object
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		Handles Maya stacks.

		:return: Python object.
		:rtype: object
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
	Returns shapes of the given object.

	:param object: Current object.
	:type object: str
	:param fullPath: Current full path state.
	:type fullPath: bool
	:param noIntermediate: Current no intermediate state.
	:type noIntermediate: bool
	:return: Objects shapes.
	:rtype: list
	"""

	objectShapes = []
	shapes = cmds.listRelatives(object, fullPath=fullPathState, shapes=True, noIntermediate=noIntermediateState)
	if shapes != None:
		objectShapes = shapes

	return objectShapes

def snapObjectsOnSupport(objects, support):
	"""
	Snaps objects on support.

	:param objects: Objects to snap.
	:type objects: list
	:param value: Support.
	:type value: str
	"""

	if cmds.pluginInfo("nearestPointOnMesh", q=True, loaded=False):
		cmds.loadPlugin("nearestPointOnMesh")

	nearestPointOnMesh = cmds.createNode("nearestPointOnMesh")
	supportShape = getShapes(support)[0]
	cmds.connectAttr(supportShape + ".outMesh", nearestPointOnMesh + ".inMesh", f=True)

	allAxis = ("X", "Y", "Z")
	for object in objects:
		position = cmds.xform(object, q=True, rp=True, ws=True, a=True)
		for i, axis in enumerate(allAxis):
			cmds.setAttr(nearestPointOnMesh + ".inPosition" + axis, position[i])

		cmds.select(object)
		cmds.move(cmds.getAttr(nearestPointOnMesh + ".positionX"),
				cmds.getAttr(nearestPointOnMesh + ".positionY"),
				cmds.getAttr(nearestPointOnMesh + ".positionZ"),
				rpr=True)

	cmds.delete(nearestPointOnMesh)

@stacksHandler
def ISnapObjectsOnSupport():
	"""
	Defines the snapObjectsOnSupport definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and snapObjectsOnSupport(selection[:-1], selection[-1])
