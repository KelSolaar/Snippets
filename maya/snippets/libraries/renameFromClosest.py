# Rename from closest.
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacksHandler",
			"getMPoint",
			"norme",
			"renameTargetsFromClosestSources",
			"pickSources_button_OnClicked",
			"pickTargets_button_OnClicked",
			"renameFromClosest_button_OnClicked",
			"renameFromClosest_window",
			"renameFromClosest",
			"IRenameFromClosest"]

def stacksHandler(object):
	"""
	Handles Maya stacks.

	:param object: Python object. ( Object )
	:return: Python function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		Handles Maya stacks.

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

def getMPoint(point):
	"""
	Returns an MPoint.

	:param point: Point. ( List )
	:return: MPoint ( MVector )
	"""

	return OpenMaya.MPoint(point[0], point[1], point[2])

def norme(pointA, pointB):
	"""
	Returns the norme of a vector.

	:param pointA: Point A. ( List )
	:param pointB: Point B. ( List )
	:return: Norme ( Float )
	"""

	mPointA = getMPoint(pointA)
	mPointB = getMPoint(pointB)
	mVector = mPointA - mPointB
	return mVector.length()

def renameTargetsFromClosestSources(sources, targets, suffixe="__"):
	"""
	Renames the targets from closest sources.

	:param sources: Sources. ( List )
	:param targets: Targets. ( List )
	:param suffixe: Suffixe. ( String )
	"""

	for target in targets:
		targetBarycenter = cmds.objectCenter(target, gl=True)
		normes = {}
		for source in sources:
			normes[source] = norme(targetBarycenter, cmds.objectCenter(source, gl=True))
		closest = min(normes, key=lambda item: normes[item])
		cmds.rename(target, "%s%s" % (closest.split("|")[-1], suffixe))

@stacksHandler
def pickSources_button_OnClicked(state=None):
	"""
	Defines the slot triggered by **pickSources_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	cmds.textField("sources_textField", edit=True, text=", ".join(cmds.ls(sl=True, l=True)))

@stacksHandler
def pickTargets_button_OnClicked(state=None):
	"""
	Defines the slot triggered by **pickTargets_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	cmds.textField("targets_textField", edit=True, text=", ".join(cmds.ls(sl=True, l=True)))

@stacksHandler
def renameFromClosest_button_OnClicked(state=None):
	"""
	Defines the slot triggered by **renameFromClosest_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	sources = [source for source in cmds.textField("sources_textField", query=True, text=True).split(", ") if cmds.objExists(source)]
	targets = [target for target in cmds.textField("targets_textField", query=True, text=True).split(", ")	if cmds.objExists(target)]

	renameTargetsFromClosestSources(sources, targets)

def renameFromClosest_window():
	"""
	Creates the 'Rename From Closest' main window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("renameFromClosest_window", exists=True)):
		cmds.deleteUI("renameFromClosest_window")

	cmds.window("renameFromClosest_window",
		title="Rename From Closest",
		width=320)

	spacing = 5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
	cmds.text(label="Sources:")
	sources_textField = cmds.textField("sources_textField")
	cmds.button("pickSources_button", label="Pick Sources!", command=pickSources_button_OnClicked)
	cmds.setParent(topLevel=True)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
	cmds.text(label="Targets:")
	targets_textField = cmds.textField("targets_textField")
	cmds.button("pickTargets_button", label="Pick Targets!", command=pickTargets_button_OnClicked)
	cmds.setParent(topLevel=True)

	cmds.separator(style="single")

	cmds.button("renameFromClosest_button", label="Rename Targets!", command=renameFromClosest_button_OnClicked)

	cmds.showWindow("renameFromClosest_window")

	cmds.windowPref(enableAll=True)

def renameFromClosest():
	"""
	Launches the 'Rename From Closest' main window.
	"""

	renameFromClosest_window()

@stacksHandler
def IRenameFromClosest():
	"""
	Defines the renameFromClosest definition Interface.
	"""

	renameFromClosest()
