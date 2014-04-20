import maya.cmds as cmds
import maya.mel as mel
import os

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["USER_HOOK",
			"EXPORT_DIRECTORY",
			"FILE_DEFAULT_PREFIX",
			"FILE_TYPES",
			"stacks_handler",
			"get_transform",
			"set_padding",
			"get_user_export_directory",
			"export_objects_to_files",
			"export_selected_objects_to_short_obj_files",
			"export_selected_objects_to_long_obj_files",
            "export_first_selected_object_to_default_object",
			"export_selected_object_to_uvlayout",
			"import_default_object"]

__interfaces__ = ["export_selected_objects_to_short_obj_files",
			"export_selected_objects_to_long_obj_files",
			"export_first_selected_object_to_default_object",
			"export_selected_object_to_uvlayout",
			"import_default_object"]

USER_HOOK = "@user"
EXPORT_DIRECTORY = "textures/images/%s/objs" % USER_HOOK
FILE_DEFAULT_PREFIX = "Export"
FILE_TYPES = {"Obj" : {"extension" : "obj", "type" : "OBJexport", "options" : "groups=1;ptgroups=1;materials=0;smoothing=1;normals=1"}}

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

def set_padding(data, padding, affix="0"):
	"""
	Pads the given data.

	:param data: Data to pad.
	:type data: str
	:param padding: Padding.
	:type padding: int
	:param affix: Padding affix.
	:type affix: str
	"""

	while len(data) < padding:
		data = affix + data
	return data

def get_user_export_directory():
	"""
	Gets the user export directory.

	:return: Export directory.
	:rtype: str
	"""

	workspace = cmds.workspace(q=True, rd=True)
	user = os.environ["USER"]
	return os.path.join(workspace, EXPORT_DIRECTORY.replace(USER_HOOK, user))

@stacks_handler
def export_objects_to_files(objects, export_type, use_objects_names=True, use_long_names=False):
	"""
	Export given objects to files.

	:param objects: Objects to export.
	:type objects: list
	:param export_type: Export type.
	:type export_type: str
	:param use_objects_names: Use objects names.
	:type use_objects_names: bool
	:param use_long_names: Use long Maya names.
	:type use_long_names: bool
	:return: Exported files.
	:rtype: list
	"""

	export_directory = get_user_export_directory()
	not os.path.exists(export_directory) and os.makedirs(export_directory)

	exported_files = []
	for i, object in enumerate(objects):
		if use_objects_names:
			basename = use_long_names and object.replace("|", "_") or object.split("|")[-1]
		else:
			basename = "{0}_{1}".format(FILE_DEFAULT_PREFIX, set_padding(str(i), 3))
		name = os.path.join(export_directory, "{0}.{1}".format(basename, FILE_TYPES[export_type]["extension"]))
		print("{0} | Export '{1}' to '{2}'!".format(__name__, object, name))
		cmds.select(object)
		cmds.file(name, force=True, options=FILE_TYPES[export_type]["options"], typ=FILE_TYPES[export_type]["type"], es=True)
		exported_files.append(name)
	return exported_files

@stacks_handler
def export_selected_objects_to_short_obj_files():
	"""
	Exports selected objects to short named obj files.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	selection and export_objects_to_files(selection, "Obj", True, False)

@stacks_handler
def export_selected_objects_to_long_obj_files():
	"""
	Exports selected objects to long named obj files.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	selection and export_objects_to_files(selection, "Obj", True, True)

@stacks_handler
def export_first_selected_object_to_default_object():
	"""
	Exports the first selected object to default object.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	if selection:
		export_objects_to_files((selection[0],), "Obj", False)

@stacks_handler
def export_selected_object_to_uvlayout():
	"""
	Exports the selected object to uvlayout.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	if selection:
		file = export_objects_to_files((selection[0],), "Obj", False)[0]
		os.system("uvlayout {0}&".format(file))

@stacks_handler
def import_default_object():
	"""
	Imports the default object: 'Export_000.obj'.
	"""

	name = os.path.join(get_user_export_directory(), "{0}.{1}".format("{0}_{1}".format(FILE_DEFAULT_PREFIX, set_padding(str(0), 3)), FILE_TYPES["Obj"]["extension"]))
	if os.path.exists(name):
		nodesBefore = cmds.ls()
		cmds.file(name, r=True, dns=True)
		cmds.select([node for node in list(set(cmds.ls()).difference(set(nodesBefore))) if cmds.nodeType(node) == "transform"])
	else:
		mel.eval("warning(\"{0} | '{1}' file doesn't exists!\")".format(__name__, name))
