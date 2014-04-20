import maya.cmds as cmds

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacks_handler",
			"get_shapes",
			"snap_objects_on_support",
			"snap_selected_objects_on_support"]

__interfaces__ = ["snap_selected_objects_on_support"]

def stacks_handler(object):
	"""
	Handles Maya stacks.

	:param object: Python object.
	:type object: object
	:return: Python function.
	:rtype: object
	"""

	def stacks_handler_wrapper(*args, **kwargs):
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
			cmds.repeatLast(addCommand="python(\"import {0}; {1}.{2}()\")".format(__name__, __name__, object.__name__), addCommandLabel=object.__name__)
		except:
			pass
		return value

	return stacks_handler_wrapper

def get_shapes(object, full_path=False, no_intermediate=True):
	"""
	Returns shapes of the given object.

	:param object: Current object.
	:type object: str
	:param full_path: Current full path state.
	:type full_path: bool
	:param noIntermediate: Current no intermediate state.
	:type noIntermediate: bool
	:return: Objects shapes.
	:rtype: list
	"""

	object_shapes = []
	shapes = cmds.listRelatives(object, fullPath=full_path, shapes=True, noIntermediate=no_intermediate)
	if shapes != None:
		object_shapes = shapes

	return object_shapes

@stacks_handler
def snap_objects_on_support(objects, support):
	"""
	Snaps objects on support.

	:param objects: Objects to snap.
	:type objects: list
	:param value: Support.
	:type value: str
	"""

	if cmds.pluginInfo("nearestPointOnMesh", q=True, loaded=False):
		cmds.loadPlugin("nearestPointOnMesh")

	nearest_point_on_mesh = cmds.createNode("nearestPointOnMesh")
	support_shape = get_shapes(support)[0]
	cmds.connectAttr("{0}.outMesh".format(support_shape), nearest_point_on_mesh + ".inMesh", f=True)

	all_axis = ("X", "Y", "Z")
	for object in objects:
		position = cmds.xform(object, q=True, rp=True, ws=True, a=True)
		for i, axis in enumerate(all_axis):
			cmds.setAttr("{0}.inPosition{1}".format(nearest_point_on_mesh, axis), position[i])

		cmds.select(object)
		cmds.move(cmds.getAttr("{0}.positionX".format(nearest_point_on_mesh)),
				cmds.getAttr("{0}.positionY".format(nearest_point_on_mesh)),
				cmds.getAttr("{0}.positionZ".format(nearest_point_on_mesh)),
				rpr=True)

	cmds.delete(nearestPointOnMesh)

@stacks_handler
def snap_selected_objects_on_support():
	"""
	Snaps selected objects on support.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and snap_objects_on_support(selection[:-1], selection[-1])
