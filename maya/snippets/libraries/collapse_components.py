import inspect
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import re

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacks_handler",
			"get_transform",
			"get_average_vector",
			"collapse_components",
            "collapse_selected_components",
            "collapse_selected_components_on_x",
            "collapse_selected_components_on_y",
            "collapse_selected_components_on_z"]

__interfaces__ = ["collapse_selected_components",
			"collapse_selected_components_on_x",
			"collapse_selected_components_on_y",
			"collapse_selected_components_on_z"]

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

def get_transform(node, full_path=True):
	"""
	Returns transform of the given node.

	:param node: Current object.
	:type node: str
	:param full_path: Current full path state.
	:type full_path: bool
	:return: Object transform.
	:rtype: str
	"""

	transform = node
	if cmds.nodeType(node) != "transform":
		parents = cmds.listRelatives(node, fullPath=full_path, parent=True)
		transform = parents[0]
	return transform

def get_average_vector(vectors):
	"""
	Returns the average vector from a list of vectors.

	:param vectors: Vectors to get the average one.
	:type vectors: list
	:return: Average vector.
	:rtype: list
	"""

	average_vector = [0, 0, 0]
	for vector in vectors:
		for i in range(3):
			average_vector[i] += vector[i]
	for i in range(3):
		average_vector[i] = average_vector[i] / len(vectors)
	return average_vector

@stacks_handler
def collapse_components(components, axis=("X", "Y", "Z")):
	"""
	Collapses given components.

	:param components: Components to collapse.
	:type components: list
	:param axis: Collapse axis.
	:type axis: tuple
	"""

	vertices = cmds.ls(cmds.polyListComponentConversion(components, toVertex=True), fl=True)
	barycenters = []
	barycenters.extend((cmds.xform(vertex, q=True, t=True, ws=True) for vertex in vertices))
	barycenter = get_average_vector(barycenters)
	for vertex in vertices:
		x_value = barycenter[0] if "X" in axis else cmds.xform(vertex, q=True, t=True, ws=True)[0]
		y_value = barycenter[1] if "Y" in axis else cmds.xform(vertex, q=True, t=True, ws=True)[1]
		z_value = barycenter[2] if "Z" in axis else cmds.xform(vertex, q=True, t=True, ws=True)[2]

		cmds.xform(vertex, ws=True, t=(x_value, y_value, z_value))

@stacks_handler
def collapse_selected_components():
	"""
	Collapses selected components.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and collapse_components(selection)

@stacks_handler
def collapse_selected_components_on_x():
	"""
	Collapses selected components on 'x' axis.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and collapse_components(selection, axis=("X",))

@stacks_handler
def collapse_selected_components_on_y():
	"""
	Collapses selected components on 'y' axis.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and collapse_components(selection, axis=("Y",))

@stacks_handler
def collapse_selected_components_on_z():
	"""
	Collapses selected components on 'z' axis.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and collapse_components(selection, axis=("Z",))
