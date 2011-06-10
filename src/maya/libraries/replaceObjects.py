import random
import maya.cmds as cmds

def stacksHandler(object_):
	"""
	This Decorator Is Used To Handle Various Maya Stacks.

	@param object_: Python Object ( Object )
	@return: Python Function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This Decorator Is Used To Handle Various Maya Stacks.

		@return: Python Object. ( Python )
		"""
		
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

def replaceTargetsObjectsWithSources(sources, targets, inPlace=False, usePivot=False, asInstance=False, deleteTargets = True):
	"""
	This Definition Replaces The Targets With Sources.

	@param sources: Sources. ( List )
	@param targets: Targets. ( List )
	@param inPlace: In Place Replacement. ( Boolean )
	@param usePivot: Use Target Pivot. ( Boolean )
	@param asInstance: Duplicate As Instances. ( Boolean )
	@param deleteTargets: Delete Targets. ( Boolean )
	"""
	
	duplicatedObjects = []
	for target in targets:
		if not asInstance:
			duplicatedObject = cmds.duplicate(sources[random.randrange(0, len(sources))], rr = True)[0]
		else:
			duplicatedObject = cmds.instance(sources[random.randrange(0, len(sources))])[0]
			
		duplicatedObjects.append(duplicatedObject)
		if not inPlace:
			if usePivot:
				components = ("rx", "ry", "rz", "sx", "sy", "sz")
				pivot = cmds.xform(target, query = True, worldSpace = True, rotatePivot = True)
				for i, component  in enumerate(("tx", "ty", "tz")):
					cmds.setAttr(duplicatedObject + "." + component, pivot[i])
			else:
				components = ("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz")
				
			for component in components:
				cmds.setAttr(duplicatedObject + "." + component, cmds.getAttr(target + "." + component))
		if deleteTargets:
			cmds.delete(target)
	
	if duplicatedObjects:
		if not inPlace:
			duplicationGrp = cmds.group(em = True)
			for duplicatedObject in duplicatedObjects:
				cmds.parent(duplicatedObject, duplicationGrp)
			cmds.rename(duplicationGrp, "duplication_grp")
	
def pickSources_Button_OnClicked(state):
	"""
	This Definition Is Triggered By The pickSources_Button Button When Clicked.
	
	@param state: Button State. ( Boolean )
	"""
	
	cmds.textField("sources_TextField", edit=True, text=", ".join(cmds.ls(sl=True, l=True)))

def pickTargets_Button_OnClicked(state):
	"""
	This Definition Is Triggered By The pickTargets_Button Button When Clicked.
	
	@param state: Button State. ( Boolean )
	"""

	cmds.textField("targets_TextField", edit=True, text=", ".join(cmds.ls(sl=True, l=True)))

def replaceObjects_Button_OnClicked(state):
	"""
	This Definition Is Triggered By The replaceObjects_Button Button When Clicked.
	
	@param state: Button State. ( Boolean )
	"""

	sources = [source for source in cmds.textField("sources_TextField", query=True, text=True).split(", ") if cmds.objExists(source)]
	targets = [target for target in cmds.textField("targets_TextField", query=True, text=True).split(", ")  if cmds.objExists(target)]

	replaceTargetsObjectsWithSources(sources, targets, cmds.checkBox("duplicateInPlace_CheckBox", q=True, v=True), cmds.checkBox("useTargetsPivots_CheckBox", q=True, v=True),  cmds.checkBox("duplicateAsInstances_CheckBox", q=True, v=True))

def replaceObjects_Window():
	"""
	This Definition Creates The Replace Objects Main Window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("replaceObjects_Window", exists=True)):
		cmds.deleteUI("replaceObjects_Window")

	cmds.window("replaceObjects_Window",
		title="Replace Objects",
		width=320)

	spacing=5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
	cmds.text(label="Sources:")
	sources_TextField=cmds.textField("sources_TextField")
	cmds.button("pickSources_Button", label="Pick Sources!", command=pickSources_Button_OnClicked)
	cmds.setParent(topLevel=True)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
	cmds.text(label="Targets:")
	targets_TextField=cmds.textField("targets_TextField")
	cmds.button("pickTargets_Button", label="Pick Targets!", command=pickTargets_Button_OnClicked)
	cmds.setParent(topLevel=True)
	
	cmds.separator(style="single")
	
	cmds.columnLayout(columnOffset=("left", 40) )
	cmds.checkBox("duplicateInPlace_CheckBox", label="Duplicate In Place")
	cmds.checkBox("useTargetsPivots_CheckBox", label="Use Targets Pivots", v=True)
	cmds.checkBox("duplicateAsInstances_CheckBox", label="Duplicate As Instances")
	cmds.checkBox("deleteTargets_CheckBox", label="Delete Targets",  v=True)
	cmds.setParent(topLevel=True)

	cmds.separator(style="single")

	cmds.button("replaceObjects_Button", label="Replace Objects!", command=replaceObjects_Button_OnClicked)

	cmds.showWindow("replaceObjects_Window")

	cmds.windowPref(enableAll=True)

def replaceObjects():
	"""
	This Definition Launches The Replace Objects Main Window.
	"""
	
	replaceObjects_Window()

@stacksHandler
def IReplaceObjects():
	"""
	This Definition Is The replaceObjects Method Interface.
	"""

	replaceObjects()
