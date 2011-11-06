import maya.cmds as cmds
import maya.mel as mel

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacksHandler",
			"getShapes",
			"transfertVerticesPositionsInUvSpace",
			"ITransfertVerticesPositionsInUvSpace",
			"transfertVerticesPositionsInWorldSpace",
			"ITransfertVerticesPositionsInWorldSpace",
			"toggleSelectionHighlight",
			"IToggleSelectionHighlight",
			"toggleGeometriesVisibility",
			"IToggleGeometriesVisibility",
			"toggleGeometriesShadingOverride",
			"IToggleGeometriesShadingOverride",
			"splitRingMiddle",
			"ISplitRingMiddle",
			"symmetricalInstance",
			"ISymmetricalInstance",
			"pivotsIdentity",
			"IPivotsIdentity",
			"flattenHierarchy",
			"IFlattenHierarchy"]

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

def transfertVerticesPositionsInUvSpace(sources, target):
	"""
	This definition transferts vertices positions from sources to target object in UVs space.

	:param sources: Sources objects. ( List )
	:param target: Target object. ( String )
	:param searchMethod: Current search method. ( Integer )
	"""

	for source in sources:
		cmds.transferAttributes(target, source, transferPositions=1, sampleSpace=3)
		cmds.delete(target, ch=True)

@stacksHandler
def ITransfertVerticesPositionsInUvSpace():
	"""
	This definition is the transfertVerticesPositionsInUvSpace definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and transfertVerticesPositionsInUvSpace(selection[:-1], selection[-1])

def transfertVerticesPositionsInWorldSpace(sources, target, searchMethod=0):
	"""
	This definition transferts vertices positions from sources to target object in world space.

	:param sources: Sources objects. ( List )
	:param target: Target object. ( String )
	:param searchMethod: Current search method. ( Integer )
	"""

	for source in sources:
		cmds.transferAttributes(target, source, transferPositions=1, sampleSpace=0, searchMethod=3)
		cmds.delete(target, ch=True)

@stacksHandler
def ITransfertVerticesPositionsInWorldSpace():
	"""
	This definition is the transfertVerticesPositionsInWorldSpace definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and transfertVerticesPositionsInWorldSpace(selection[:-1], selection[-1], 0)

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
	selection = toggleGeometriesShadingOverride(selection)

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
