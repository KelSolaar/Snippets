# Rename From Closest.
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

def stacksHandler(object):
	"""
	This Decorator Is Used To Handle Various Maya Stacks.

	@param object: Python Object. ( Object )
	@return: Python Function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This Decorator Is Used To Handle Various Maya Stacks.

		@return: Python Object. ( Python )
		"""

		cmds.undoInfo(openChunk=True)
		value = object(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya Produces A Weird Command Error If Not Wrapped Here.
		try:
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")"% (__name__, __name__, object.__name__), addCommandLabel=object.__name__)
		except:
			pass
		return value

	return stacksHandlerCall

def getMPoint(point):
	"""
	This Definition Returns An MPoint.

	@param point: Point. ( List )
	@return: MPoint ( MVector )
	"""

	return OpenMaya.MPoint(point[0], point[1], point[2])

def norme(pointA, pointB):
	"""
	This Definition Returns The Norme Of A Vector.

	@param pointA: Point A. ( List )
	@param pointB: Point B. ( List )
	@return: Norme ( Float )
	"""

	mPointA = getMPoint(pointA)
	mPointB = getMPoint(pointB)
	mVector = mPointA - mPointB
	return mVector.length()

def renameTargetsFromClosestSources(sources, targets, suffixe="__"):
	"""
	This Definition Renames The Targets From Closest Sources.

	@param sources: Sources. ( List )
	@param targets: Targets. ( List )
	@param suffixe: Suffixe. ( String )
	"""

	for target in targets:
		targetBarycenter=cmds.objectCenter(target, gl=True)
		normes = {}
		for source in sources:
			normes[source] = norme(targetBarycenter, cmds.objectCenter(source, gl=True))
		closest = min(normes, key=lambda item: normes[item])
		cmds.rename(target, "%s%s" % (closest.split("|")[-1], suffixe))

@stacksHandler
def pickSources_Button_OnClicked(state=None):
	"""
	This Definition Is Triggered By The pickSources_Button Button When Clicked.

	@param state: Button State. ( Boolean )
	"""

	cmds.textField("sources_TextField", edit=True, text=", ".join(cmds.ls(sl=True, l=True)))

@stacksHandler
def pickTargets_Button_OnClicked(state=None):
	"""
	This Definition Is Triggered By The pickTargets_Button Button When Clicked.

	@param state: Button State. ( Boolean )
	"""

	cmds.textField("targets_TextField", edit=True, text=", ".join(cmds.ls(sl=True, l=True)))

@stacksHandler
def renameFromClosest_Button_OnClicked(state=None):
	"""
	This Definition Is Triggered By The renameFromClosest_Button Button When Clicked.

	@param state: Button State. ( Boolean )
	"""

	sources = [source for source in cmds.textField("sources_TextField", query=True, text=True).split(", ") if cmds.objExists(source)]
	targets = [target for target in cmds.textField("targets_TextField", query=True, text=True).split(", ")  if cmds.objExists(target)]


	renameTargetsFromClosestSources(sources, targets)

def renameFromClosest_Window():
	"""
	This Definition Creates The Rename From Closest Main Window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("renameFromClosest_Window", exists=True)):
		cmds.deleteUI("renameFromClosest_Window")

	cmds.window("renameFromClosest_Window",
		title="Rename From Closest",
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

	cmds.button("renameFromClosest_Button", label="Rename Targets!", command=renameFromClosest_Button_OnClicked)

	cmds.showWindow("renameFromClosest_Window")

	cmds.windowPref(enableAll=True)

def renameFromClosest():
	"""
	This Definition Launches The Rename From Closest Main Window.
	"""

	renameFromClosest_Window()

@stacksHandler
def IRenameFromClosest():
	"""
	This Definition Is The renameFromClosest Method Interface.
	"""

	renameFromClosest()
