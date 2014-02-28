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
			"stacksHandler",
			"getShapes",
			"transfertVerticesPositionsInUvsSpace",
			"ITransfertVerticesPositionsInUvsSpace",
			"transfertVerticesPositionsInWorldSpace",
			"ITransfertVerticesPositionsInWorldSpace",
			"transfertUvsInTopologySpace",
			"ITransfertUvsInTopologySpace",
			"toggleSelectionHighlight",
			"IToggleSelectionHighlight",
			"toggleGeometriesVisibility",
			"IToggleGeometriesVisibility",
			"toggleGeometriesShadingOverride",
			"IToggleGeometriesShadingOverride",
			"isolateSelection",
			"IIsolateSelection",
			"splitRingMiddle",
			"ISplitRingMiddle",
			"symmetricalInstance",
			"ISymmetricalInstance",
			"pivotsIdentity",
			"IPivotsIdentity",
			"flattenHierarchy",
			"IFlattenHierarchy",
			"transfertSelection",
			"ITransfertSelection",
			"transfertSelectionToUserTarget",
			"pickTarget_button_OnClicked",
			"setUnsetContextHotkeys_button_OnClicked",
			"transfertSelection_button_OnClicked",
			"transfertSelectionToTarget_window",
			"transfertSelectionToTarget",
			"ITransfertSelectionToTarget"]

DEFAULTS_HOTKEYS = {}
TRANSFERT_SELECTION_HOTKEY = "t"

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

def transfertVerticesPositionsInUvsSpace(targets, source):
	"""
	This definition transferts vertices positions from source to targets object in UVs space.

	:param targets: Sources objects. ( List )
	:param source: Target object. ( String )
	"""

	for target in targets:
		cmds.transferAttributes(source, target, transferPositions=1, sampleSpace=3)
		cmds.delete(source, ch=True)

@stacksHandler
def ITransfertVerticesPositionsInUvsSpace():
	"""
	This definition is the transfertVerticesPositionsInUvsSpace definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and transfertVerticesPositionsInUvsSpace(selection[:-1], selection[-1])

def transfertVerticesPositionsInWorldSpace(targets, source, searchMethod=0):
	"""
	This definition transferts vertices positions from source to targets object in world space.

	:param targets: Sources objects. ( List )
	:param source: Target object. ( String )
	:param searchMethod: Current search method. ( Integer )
	"""

	for target in targets:
		cmds.transferAttributes(source, target, transferPositions=1, sampleSpace=0, searchMethod=3)
		cmds.delete(source, ch=True)

@stacksHandler
def ITransfertVerticesPositionsInWorldSpace():
	"""
	This definition is the transfertVerticesPositionsInWorldSpace definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and transfertVerticesPositionsInWorldSpace(selection[:-1], selection[-1], 0)

def transfertUvsInTopologySpace(targets, source):
	"""
	This definition transferts UVs from source to targets object in topology space.

	:param targets: Sources objects. ( List )
	:param source: Target object. ( String )
	"""

	for target in targets:
		cmds.transferAttributes(source, target, transferUVs=2, sampleSpace=5)
		cmds.delete(source, ch=True)

@stacksHandler
def ITransfertUvsInTopologySpace():
	"""
	This definition is the transfertUvsInTopologySpace definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and transfertUvsInTopologySpace(selection[:-1], selection[-1])

def toggleSelectionHighlight():
	"""
	This definition toggles active modeling panel selection highlight.
	"""

	panel = cmds.getPanel(withFocus=True)
	try:
		cmds.modelEditor(panel, e=True, sel=not cmds.modelEditor(panel, q=True, sel=True))
	except:
		pass

@stacksHandler
def IToggleSelectionHighlight():
	"""
	This definition is the toggleSelectionHighlight definition Interface.
	"""

	toggleSelectionHighlight()

def toggleGeometriesVisibility():
	"""
	This definition toggles active modeling panel geometries visibility highlight.
	"""

	panel = cmds.getPanel(withFocus=True)
	try:
		cmds.modelEditor(panel, e=True, nurbsCurves=not cmds.modelEditor(panel, q=True, nurbsCurves=True))
		cmds.modelEditor(panel, e=True, nurbsSurfaces=not cmds.modelEditor(panel, q=True, nurbsSurfaces=True))
		cmds.modelEditor(panel, e=True, polymeshes=not cmds.modelEditor(panel, q=True, polymeshes=True))
		cmds.modelEditor(panel, e=True, subdivSurfaces=not cmds.modelEditor(panel, q=True, subdivSurfaces=True))
	except:
		pass

@stacksHandler
def IToggleGeometriesVisibility():
	"""
	This definition is the toggleGeometriesVisibility definition Interface.
	"""

	toggleGeometriesVisibility()

def toggleGeometriesShadingOverride(nodes):
	"""
	This definition toggles geometries shading override.
	
	:param nodes: Nodes to toggle shading override on. ( List )
	"""

	for node in nodes:
		shape = getShapes(node, True)[0]
		cmds.setAttr("%s.overrideEnabled" % shape, 1)
		cmds.setAttr("%s.overrideShading" % shape, not cmds.getAttr("%s.overrideShading" % shape))

@stacksHandler
def IToggleGeometriesShadingOverride():
	"""
	This definition is the toggleGeometriesShadingOverride definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True, type="transform")
	selection and toggleGeometriesShadingOverride(selection)

def isolateSelection():
	"""
	This definition isolates current selection.
	"""

	panel = cmds.getPanel(withFocus=True)
	try:
		mel.eval("enableIsolateSelect {0} {1};".format(panel, str(not cmds.isolateSelect(panel, q=True, state=True)).lower()))
	except:
		pass

@stacksHandler
def IIsolateSelection():
	"""
	This definition is the isolateSelection definition Interface.
	"""

	isolateSelection()

def splitRingMiddle(nodes):
	"""
	This definition sets the polysplitring nodes weights to 0.5.

	:param nodes: Nodes to retrieve history from. ( List )
	"""

	for node in nodes:
		for historyNode in cmds.listHistory(node):
			if cmds.nodeType(historyNode) == "polySplitRing":
				cmds.setAttr(historyNode + ".weight", 0.5)

@stacksHandler
def ISplitRingMiddle():
	"""
	This definition is the splitRingMiddle definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and splitRingMiddle(selection)

def symmetricalInstance(object):
	"""
	This definition creates a symmetrical instance.

	:param object: Object to symmetrical instantiate. ( String )
	"""

	instance = cmds.instance(object)
	cmds.setAttr(object + ".sx", -1)

@stacksHandler
def ISymmetricalInstance():
	"""
	This definition is the symmetricalInstance definition Interface.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	for object in selection:
		symmetricalInstance(object)

def pivotsIdentity(transforms):
	"""
	This definition puts given transforms pivots to origin.

	:param transforms: Transforms to affect pivots. ( List )
	"""

	for transform in transforms:
		try:
			for pivotType in ("scalePivot", "rotatePivot"):
				cmds.move(0, 0, 0, transform + "." + pivotType)
		except:
			pass
@stacksHandler
def IPivotsIdentity():
	"""
	This definition is the pivotsIdentity definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True, type="transform")
	selection and pivotsIdentity(selection)


def flattenHierachy(object):
	"""
	This definition flattens given object hierarchy.
	
	:return: Definition succes. ( Boolean )
	"""

	relatives = cmds.listRelatives(object, allDescendents=True, fullPath=True)
	for relative in relatives:
		if not getShapes(relative):
			continue
		if cmds.listRelatives(relative, fullPath=True, parent=True)[0] != object:
			cmds.parent(relative, object)

	relatives = cmds.listRelatives(object, fullPath=True)
	if relatives:
		for relative in relatives:
			if not getShapes(relative):
				cmds.delete(relative)
	return True

@stacksHandler
def IFlattenHierachy():
	"""
	This definition is the flattenHierachy definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	for object in selection:
		flattenHierachy(object)

def transfertSelection():
	"""
	This definition transfers a component selection to another object.
	
	:return: Definition succes. ( Boolean )
	"""

	selection = cmds.ls(sl=True, long=True)

	targetObject = str()
	for item in selection:
		if "." not in item:
			targetObject = item
			break

	if targetObject != "":
		cmds.hilite(targetObject, replace=True)
		cmds.selectMode(component=True)
		nextSelection = []
		for item in selection:
			if item != targetObject:
				if "." in item:
					itemTokens = item.split(".")
					nextSelection.append(targetObject + "." + itemTokens[1])
		nextSelection and cmds.select(nextSelection)
	return True

@stacksHandler
def ITransfertSelection():
	"""
	This definition is the transfertSelection definition Interface.
	"""

	transfertSelection()

@stacksHandler
def transfertSelectionToUserTarget():
	"""
	This definition transfers a component selection to user target object.
	"""

	source = cmds.textField("target_textField", query=True, text=True)
	if not source:
		return

	if not cmds.ls(source):
		return

	cmds.select(source, add=True)
	return transfertSelection()

@stacksHandler
def pickTarget_button_OnClicked(state=None):
	"""
	This definition is triggered by the **pickTarget_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and cmds.textField("target_textField", edit=True, text=selection[0])

@stacksHandler
def setUnsetContextHotkeys():
	"""
	This definition sets / unsets context hotkeys.
	"""

	sequence = TRANSFERT_SELECTION_HOTKEY
	command = "python(\"import snippets.libraries.others as others; reload(others); others.transfertSelectionToUserTarget()\")"
	name = "transfertSelectionNamedCommand"
	if cmds.hotkey(sequence, query=True, name=True) != name:
		print("%s | Assigning '%s' hotkey to '%s' command!" % (__name__, sequence, name))
		DEFAULTS_HOTKEYS[sequence] = {"name" : cmds.hotkey(sequence, query=True, name=True),
								"releaseName" : cmds.hotkey(sequence, query=True, releaseName=True)}

		cmds.nameCommand(name, annotation="Transfert Selection", command=command)
		cmds.hotkey(k=sequence, rcr=True, name=name)
	else:
		hotkey = DEFAULTS_HOTKEYS.get(sequence)
		if hotkey:
			print("%s | Unassigning '%s' hotkey from '%s' command!" % (__name__, sequence, name))
			cmds.hotkey(k=sequence, name=hotkey.get("name"), releaseName=hotkey.get("releaseName"))
	return True

@stacksHandler
def transfertSelection_button_OnClicked(state=None):
	"""
	This definition is triggered by the **transfertSelection_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	transfertSelectionToUserTarget()

def transfertSelectionToTarget_window():
	"""
	This definition creates the 'Transfert Selection To Target' main window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("transfertSelectionToTarget_window", exists=True)):
		cmds.deleteUI("transfertSelectionToTarget_window")

	cmds.window("transfertSelectionToTarget_window",
		title="Transfert Selection To Target",
		width=320)

	spacing = 5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=(125, 150, 130), adjustableColumn=2, columnAlign=(2, "left"), columnAttach=[(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)])
	cmds.text(label="Target:")
	sources_textField = cmds.textField("target_textField")
	cmds.button("pickTarget_button", label="Pick Target!", command=pickTarget_button_OnClicked)
	cmds.setParent(topLevel=True)

	cmds.separator(style="single")

	cmds.button("transfertSelection_button", label="Transfert Selection!", command=transfertSelection_button_OnClicked)

	setUnsetContextHotkeys()
	scriptJob = cmds.scriptJob(uiDeleted=("transfertSelectionToTarget_window", setUnsetContextHotkeys), runOnce=True)

	cmds.showWindow("transfertSelectionToTarget_window")

	cmds.windowPref(enableAll=True)

@stacksHandler
def transfertSelectionToTarget():
	"""
	This definition launches the 'Transfert Selection To Target' main window.
	"""

	transfertSelectionToTarget_window()

@stacksHandler
def ITransfertSelectionToTarget():
	"""
	This definition is the transfertSelectionToTarget definition Interface.
	"""

	transfertSelectionToTarget()
