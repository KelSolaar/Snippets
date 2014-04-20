import random
import maya.cmds as cmds

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacks_handler",
			"replace_targets_objects_with_sources",
			"pick_sources_button__on_clicked",
			"pick_targets_button__on_clicked",
			"replace_objects_button__on_clicked",
			"replace_objects_window",
			"replace_objects"]

__interfaces__ = ["replace_objects"]

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

@stacks_handler
def replace_targets_objects_with_sources(sources, targets, in_place=False, use_pivot=False, as_instance=False, delete_targets=True):
	"""
	Replaces the targets with sources.

	:param sources: Sources.
	:type sources: list
	:param targets: Targets.
	:type targets: list
	:param in_place: In place replacement.
	:type in_place: bool
	:param use_pivot: Use target pivot.
	:type use_pivot: bool
	:param as_instance: Duplicate as instances.
	:type as_instance: bool
	:param delete_targets: Delete targets.
	:type delete_targets: bool
	"""

	duplicated_objects = []
	for target in targets:
		if not as_instance:
			duplicated_object = cmds.duplicate(sources[random.randrange(0, len(sources))], rr=True)[0]
		else:
			duplicated_object = cmds.instance(sources[random.randrange(0, len(sources))])[0]

		duplicated_objects.append(duplicated_object)
		if not in_place:
			if use_pivot:
				components = ("rx", "ry", "rz", "sx", "sy", "sz")
				pivot = cmds.xform(target, query=True, worldSpace=True, rotatePivot=True)
				for i, component  in enumerate(("tx", "ty", "tz")):
					cmds.setAttr(duplicated_object + "." + component, pivot[i])
			else:
				components = ("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz")

			for component in components:
				cmds.setAttr("{0}.{1}".format(duplicated_object, component), cmds.getAttr("{0}.{1}".format(target, component)))
		if delete_targets:
			cmds.delete(target)

	if duplicated_objects:
		if not in_place:
			duplicationGrp = cmds.group(em=True)
			for duplicated_object in duplicated_objects:
				cmds.parent(duplicated_object, duplicationGrp)
			cmds.rename(duplicationGrp, "duplication_grp")

@stacks_handler
def pick_sources_button__on_clicked(state=None):
	"""
	Defines the slot triggered by **pick_sources_button** button when clicked.

	:param state: Button state.
	:type state: bool
	"""

	cmds.textField("sources_textField", edit=True, text=", ".join(cmds.ls(sl=True, l=True)))

@stacks_handler
def pick_targets_button__on_clicked(state=None):
	"""
	Defines the slot triggered by **pick_targets_button** button when clicked.

	:param state: Button state.
	:type state: bool
	"""

	cmds.textField("targets_textField", edit=True, text=", ".join(cmds.ls(sl=True, l=True)))

@stacks_handler
def replace_objects_button__on_clicked(state=None):
	"""
	Defines the slot triggered by **replace_objects_button** button when clicked.

	:param state: Button state.
	:type state: bool
	"""

	sources = [source for source in cmds.textField("sources_textField", query=True, text=True).split(", ") if cmds.objExists(source)]
	targets = [target for target in cmds.textField("targets_textField", query=True, text=True).split(", ")	if cmds.objExists(target)]

	replace_targets_objects_with_sources(sources, targets, cmds.checkBox("duplicate_in_place_checkBox", q=True, v=True), cmds.checkBox("use_targets_pivots_checkBox", q=True, v=True), 	cmds.checkBox("duplicate_as_instances_checkBox", q=True, v=True))

def replace_objects_window():
	"""
	Creates the 'Replace Objects' main window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("replace_objects_window", exists=True)):
		cmds.deleteUI("replace_objects_window")

	cmds.window("replace_objects_window",
		title="Replace Objects",
		width=320)

	spacing = 5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
	cmds.text(label="Sources:")
	sources_textField = cmds.textField("sources_textField")
	cmds.button("pick_sources_button", label="Pick Sources!", command=pick_sources_button__on_clicked)
	cmds.setParent(topLevel=True)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
	cmds.text(label="Targets:")
	targets_textField = cmds.textField("targets_textField")
	cmds.button("pick_targets_button", label="Pick Targets!", command=pick_targets_button__on_clicked)
	cmds.setParent(topLevel=True)

	cmds.separator(style="single")

	cmds.columnLayout(columnOffset=("left", 40))
	cmds.checkBox("duplicate_in_place_checkBox", label="Duplicate In Place")
	cmds.checkBox("use_targets_pivots_checkBox", label="Use Targets Pivots", v=True)
	cmds.checkBox("duplicate_as_instances_checkBox", label="Duplicate As Instances")
	cmds.checkBox("delete_targets_checkBox", label="Delete Targets", 	 v=True)
	cmds.setParent(topLevel=True)

	cmds.separator(style="single")

	cmds.button("replace_objects_button", label="Replace Objects!", command=replace_objects_button__on_clicked)

	cmds.showWindow("replace_objects_window")

	cmds.windowPref(enableAll=True)

def replace_objects():
	"""
	Launches the 'Replace Objects' main window.
	"""

	replace_objects_window()
