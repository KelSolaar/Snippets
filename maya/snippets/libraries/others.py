import maya.cmds as cmds
import maya.mel as mel

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["DEFAULTS_HOTKEYS",
			"TRANSFERT_SELECTION_HOTKEY",
			"stacks_handler",
			"get_shapes",
			"transfert_vertices_positions_in_uvs_space",
			"transfert_selected_objects_vertices_positions_in_uvs_space",
			"transfert_vertices_positions_in_world_space",
			"transfert_selected_objects_vertices_positions_in_world_space",
			"transfert_uvs_in_topology_space",
			"transfert_selected_objects_uvs_in_topology_space",
			"toggle_selection_highlight",
			"toggle_geometries_visibility",
			"toggle_shading_override",
			"toggle_selected_objects_shading_override",
			"isolate_selected_objects",
			"split_ring_middle",
			"split_ring_middle_selected_objects",
			"symmetrical_instance",
			"symmetrical_instance_selected_objects",
			"pivots_identity",
			"pivots_identity_selected_objects",
			"flattenHierarchy",
			"flatten_selected_objects_hierachy",
			"transfert_selection",
			"transfert_selection_to_user_target",
			"pick_target_button__on_clicked",
			"transfert_selection_button__on_clicked",
			"transfert_selection_to_target_window",
			"transfert_selection_to_target"]

__interfaces__ = ["transfert_selected_objects_vertices_positions_in_uvs_space",
				"transfert_selected_objects_vertices_positions_in_world_space",
				"transfert_selected_objects_uvs_in_topology_space",
				"toggle_selection_highlight",
				"toggle_geometries_visibility",
				"toggle_selected_objects_shading_override",
				"isolate_selected_objects",
				"split_ring_middle_selected_objects",
				"symmetrical_instance_selected_objects",
				"pivots_identity_selected_objects",
				"flatten_selected_objects_hierachy",
				"transfert_selection",
				"transfert_selection_to_target"]

DEFAULTS_HOTKEYS = {}
TRANSFERT_SELECTION_HOTKEY = "t"

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
def transfert_vertices_positions_in_uvs_space(targets, source):
	"""
	Transfers vertices positions from source to target objects in Uvs space.

	:param targets: Sources objects.
	:type targets: list
	:param source: Target object.
	:type source: str
	"""

	for target in targets:
		cmds.transferAttributes(source, target, transferPositions=1, sampleSpace=3)
		cmds.delete(source, ch=True)

@stacks_handler
def transfert_selected_objects_vertices_positions_in_uvs_space():
	"""
	Transfers vertices positions from selected source to selected target objects in Uvs space.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and transfert_vertices_positions_in_uvs_space(selection[:-1], selection[-1])

@stacks_handler
def transfert_vertices_positions_in_world_space(targets, source, search_method=0):
	"""
	Transfers vertices positions from source to target objects in world space.

	:param targets: Sources objects.
	:type targets: list
	:param source: Target object.
	:type source: str
	:param search_method: Current search method.
	:type search_method: int
	"""

	for target in targets:
		cmds.transferAttributes(source, target, transferPositions=1, sampleSpace=0, searchMethod=3)
		cmds.delete(source, ch=True)

@stacks_handler
def transfert_selected_objects_vertices_positions_in_world_space():
	"""
	Transfers vertices positions from selected source to selected target objects in world space.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and transfert_vertices_positions_in_world_space(selection[:-1], selection[-1], 0)

@stacks_handler
def transfert_uvs_in_topology_space(targets, source):
	"""
	Transfers Uvs from source to targets object in topology space.

	:param targets: Sources objects.
	:type targets: list
	:param source: Target object.
	:type source: str
	"""

	for target in targets:
		cmds.transferAttributes(source, target, transferUvs=2, sampleSpace=5)
		cmds.delete(source, ch=True)

@stacks_handler
def transfert_selected_objects_uvs_in_topology_space():
	"""
	Transfers Uvs from selected source to selected target objects in topology space.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and transfert_uvs_in_topology_space(selection[:-1], selection[-1])

@stacks_handler
def toggle_selection_highlight():
	"""
	Toggles active modeling panel selection highlight.
	"""

	panel = cmds.getPanel(withFocus=True)
	try:
		cmds.modelEditor(panel, e=True, sel=not cmds.modelEditor(panel, q=True, sel=True))
	except:
		pass

@stacks_handler
def toggle_geometries_visibility():
	"""
	Toggles active modeling panel geometries visibility highlight.
	"""

	panel = cmds.getPanel(withFocus=True)
	try:
		cmds.modelEditor(panel, e=True, nurbsCurves=not cmds.modelEditor(panel, q=True, nurbsCurves=True))
		cmds.modelEditor(panel, e=True, nurbsSurfaces=not cmds.modelEditor(panel, q=True, nurbsSurfaces=True))
		cmds.modelEditor(panel, e=True, polymeshes=not cmds.modelEditor(panel, q=True, polymeshes=True))
		cmds.modelEditor(panel, e=True, subdivSurfaces=not cmds.modelEditor(panel, q=True, subdivSurfaces=True))
	except:
		pass

@stacks_handler
def toggle_shading_override(objects):
	"""
	Toggles geometries shading override.
	
	:param objects: Objects to toggle shading override on.
	:type objects: list
	"""

	for object in objects:
		shape = get_shapes(object, True)[0]
		cmds.setAttr("{0}.overrideEnabled".format(shape), 1)
		cmds.setAttr("{0}.overrideShading".format(shape), not cmds.getAttr("{0}.overrideShading".format(shape)))

@stacks_handler
def toggle_selected_objects_shading_override():
	"""
	Toggles selected objects shading override.
	"""

	selection = cmds.ls(sl=True, l=True, type="transform")
	selection and toggle_shading_override(selection)

@stacks_handler
def isolate_selected_objects():
	"""
	Isolates current selection.
	"""

	panel = cmds.getPanel(withFocus=True)
	try:
		mel.eval("enableIsolateSelect {0} {1};".format(panel, str(not cmds.isolateSelect(panel, q=True, state=True)).lower()))
	except:
		pass

@stacks_handler
def split_ring_middle(nodes):
	"""
	Sets the polysplitring nodes weights to 0.5.

	:param nodes: Nodes to retrieve history from.
	:type nodes: list
	"""

	for node in nodes:
		for history_node in cmds.listHistory(node):
			if cmds.nodeType(history_node) == "polySplitRing":
				cmds.setAttr("{0}.weight".format(history_node), 0.5)

@stacks_handler
def split_ring_middle_selected_objects():
	"""
	Sets the selected polysplitring nodes weights to 0.5.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and split_ring_middle(selection)

@stacks_handler
def symmetrical_instance(object):
	"""
	Creates a symmetrical instance on given object.

	:param object: Object to symmetrical instantiate.
	:type object: str
	"""

	instance = cmds.instance(object)
	cmds.setAttr("{0}.sx".format(object), -1)

@stacks_handler
def symmetrical_instance_selected_objects():
	"""
	Creates a symmetrical instance on selected object.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	for object in selection:
		symmetrical_instance(object)

@stacks_handler
def pivots_identity(transforms):
	"""
	Puts given transforms pivots to origin.

	:param transforms: Transforms to affect pivots.
	:type transforms: list
	"""

	for transform in transforms:
		try:
			for pivotType in ("scalePivot", "rotatePivot"):
				cmds.move(0, 0, 0, "{0}.{1}".format(transform, pivotType))
		except:
			pass

@stacks_handler
def pivots_identity_selected_objects():
	"""
	Puts selected transforms pivots to origin.
	"""

	selection = cmds.ls(sl=True, l=True, type="transform")
	selection and pivots_identity(selection)

@stacks_handler
def flatten_hierachy(object):
	"""
	Flattens given object hierarchy.
	
	:return: Definition succes.
	:rtype: bool
	"""

	relatives = cmds.listRelatives(object, allDescendents=True, full_path=True)
	for relative in relatives:
		if not get_shapes(relative):
			continue
		if cmds.listRelatives(relative, full_path=True, parent=True)[0] != object:
			cmds.parent(relative, object)

	relatives = cmds.listRelatives(object, full_path=True)
	if relatives:
		for relative in relatives:
			if not get_shapes(relative):
				cmds.delete(relative)
	return True

@stacks_handler
def flatten_selected_objects_hierachy():
	"""
	Flattens selected object hierarchy.
	"""

	selection = cmds.ls(sl=True, l=True)
	for object in selection:
		flatten_hierachy(object)

@stacks_handler
def transfert_selection():
	"""
	Transfers a component selection to another object.
	
	:return: Definition succes.
	:rtype: bool
	"""

	selection = cmds.ls(sl=True, long=True)

	target_object = ""
	for item in selection:
		if "." not in item:
			target_object = item
			break

	if target_object != "":
		cmds.hilite(target_object, replace=True)
		cmds.selectMode(component=True)
		next_selection = []
		for item in selection:
			if item != target_object:
				if "." in item:
					item_tokens = item.split(".")
					next_selection.append("{0}.{1}".format(target_object, item_tokens[1]))
		next_selection and cmds.select(next_selection)
	return True

@stacks_handler
def transfert_selection_to_user_target():
	"""
	Transfers a component selection to user target object.
	"""

	source = cmds.textField("target_textField", query=True, text=True)
	if not source:
		return

	if not cmds.ls(source):
		return

	cmds.select(source, add=True)
	return transfert_selection()

@stacks_handler
def pick_target_button__on_clicked(state=None):
	"""
	Defines the slot triggered by **pick_target_button** button when clicked.

	:param state: Button state.
	:type state: bool
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and cmds.textField("target_textField", edit=True, text=selection[0])

@stacks_handler
def set_unset_context_hotkeys():
	"""
	Sets / unsets context hotkeys.
	"""

	sequence = TRANSFERT_SELECTION_HOTKEY
	command = "python(\"import snippets.libraries.others as others; reload(others); others.transfert_selection_to_user_target()\")"
	name = "transfert_selectionNamedCommand"
	if cmds.hotkey(sequence, query=True, name=True) != name:
		print("{0} | Assigning '{1}' hotkey to '{2}' command!".format(__name__, sequence, name))
		DEFAULTS_HOTKEYS[sequence] = {"name" : cmds.hotkey(sequence, query=True, name=True),
								"releaseName" : cmds.hotkey(sequence, query=True, releaseName=True)}

		cmds.nameCommand(name, annotation="Transfert Selection", command=command)
		cmds.hotkey(k=sequence, rcr=True, name=name)
	else:
		hotkey = DEFAULTS_HOTKEYS.get(sequence)
		if hotkey:
			print("{0} | Unassigning '{1}' hotkey from '{2}' command!".format(__name__, sequence, name))
			cmds.hotkey(k=sequence, name=hotkey.get("name"), releaseName=hotkey.get("releaseName"))
	return True

@stacks_handler
def transfert_selection_button__on_clicked(state=None):
	"""
	Defines the slot triggered by **transfert_selection_button** button when clicked.

	:param state: Button state.
	:type state: bool
	"""

	transfert_selection_to_user_target()

def transfert_selection_to_target_window():
	"""
	Creates the 'Transfert Selection To Target' main window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("transfert_selection_to_target_window", exists=True)):
		cmds.deleteUI("transfert_selection_to_target_window")

	cmds.window("transfert_selection_to_target_window",
		title="Transfert Selection To Target",
		width=320)

	spacing = 5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
	cmds.text(label="Target:")
	sources_textField = cmds.textField("target_textField")
	cmds.button("pick_target_button", label="Pick Target!", command=pick_target_button__on_clicked)
	cmds.setParent(topLevel=True)

	cmds.separator(style="single")

	cmds.button("transfert_selection_button", label="Transfert Selection!", command=transfert_selection_button__on_clicked)

	set_unset_context_hotkeys()
	scriptJob = cmds.scriptJob(uiDeleted=("transfert_selection_to_target_window", set_unset_context_hotkeys), runOnce=True)

	cmds.showWindow("transfert_selection_to_target_window")

	cmds.windowPref(enableAll=True)

@stacks_handler
def transfert_selection_to_target():
	"""
	Launches the 'Transfert Selection To Target' main window.
	"""

	transfert_selection_to_target_window()

