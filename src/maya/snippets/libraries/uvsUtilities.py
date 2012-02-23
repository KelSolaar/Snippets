# UVs area calculation code by Naughty Nathan: http://forums.cgsociety.org/showpost.php?p=6522248&postcount=4
import math
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import os
import pprint
import re

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY", 
				"CHECKER_IMAGE",
				"DEFAULT_SCALE_COVERAGE = 0.98",
				"MARI_NAME_FORMAT",
				"stacksHandler",
				"getNode",
				"isGeometry",
				"getUVsFromComponents",
				"getFacesPerPatches",
				"getObjectUVsArea",
				"getComponentUVDims",
				"getMariPatchFromUVDims",
				"getComponentsUVDims",
				"getComponentsMariPatches",
				"getComponentsOccupationAsUVDims",
				"getComponentsOccupationAsMariPatches",
				"printComponentsOccupationAsUvDims",
				"IPrintComponentsOccupationAsUvDims",
				"printComponentsOccupationAsMariPatches",
				"IPrintComponentsOccupationAsMariPatches",
				"getComponentsBoundingBox",
				"getComponentsUVsCenter",
				"printComponentsUvsCenterAsUvDims",
				"IPrintComponentsUvsCenterAsUvDims",
				"printComponentsUvsCenterAsMariPatch",
				"IPrintComponentsUvsCenterAsMariPatch",
				"scaleComponentsUVs",
				"centerComponentsUVs",
				"scaleCenterComponentsUVs",
				"rotateComponentsUVs",
				"moveComponentsUVs",
				"mirrorComponentsUVs",
				"stackObjectsUVs",
				"prescaleUVsShells",
				"autoRatioUVsAreas",
				"addUVsChecker",
				"removeUVsChecker",
				"setUVsCheckerRepeats",
				"getPatchShaderTree",
				"assignMariShadersToObject",
				"assignMariShaders",
				"IAssignMariShaders",
				"flipUVs_button_OnClicked",
				"moveUpUVs_button_OnClicked",
				"flopUVs_button_OnClicked",
				"moveLeftUVs_button_OnClicked",
				"fitUVs_button_OnClicked",
				"moveRightUVs_button_OnClicked",
				"centerUVs_button_OnClicked",
				"moveDownUVs_button_OnClicked",
				"scaleUVs_button_OnClicked",
				"rotateCounterClockWiseUVs_button_OnClicked",
				"rotateClockWiseUVs_button_OnClicked",
				"stackUVsOnUBottom_button_OnClicked",
				"stackUVsOnUCenter_button_OnClicked",
				"stackUVsOnUTop_button_OnClicked",
				"stackUVsOnVLeft_button_OnClicked",
				"stackUVsOnVCenter_button_OnClicked",
				"stackUVsOnVRight_button_OnClicked",
				"autoRatioUVsAreas_button_OnClicked",
				"addUVsChecker_button_OnClicked",
				"uRepeat_floatField_OnChanged",
				"vRepeat_floatField_OnChanged",
				"unfoldingTools_window",
				"unfoldingTools",
				"IUvsTools"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname("__file__" in locals() and __file__ or str()), "../resources")
CHECKER_IMAGE = "images/Checker.jpg"

DEFAULT_SCALE_COVERAGE = 0.98

MARI_NAME_FORMAT = "_%s"

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

def anchorSelection(object):
	"""
	This decorator is used to anchor current selection.

	:param object: Python object. ( Object )
	:return: Python function. ( Function )
	"""

	def function(*args, **kwargs):
		"""
		This decorator is used to anchor current selection.

		:return: Python object. ( Python )
		"""

		selection = cmds.ls(sl=True, l=True)
		value = object(*args, **kwargs)
		cmds.select(selection)
		return value

	return function

def getNode(node):
	"""
	This definition returns given node if it exists or **None**.

	:param node: Current node to retrun. ( String )
	:return: Node. ( String )
	"""

	try:
		return cmds.ls(node, l=True)[0]
	except:
		pass

def isGeometry(object):
	"""
	This definition returns if a node is a geometry.

	:param object: Current object to check. ( String )
	:return: Geometry object state. ( Boolean )
	"""

	if cmds.nodeType(object) == "mesh" or cmds.nodeType(object) == "nurbsSurface" or cmds.nodeType(object) == "subdiv":
		return True
	else:
		return False

def getUVsFromComponents(components, flatten=True):
	"""
	This definition returns the uvs from given components.

	:param components: Components. ( List )
	:param flatten: Flatten components list. ( Boolean )
	:return: Components UVs. ( List )
	"""
    	
	pattern = re.compile(r"map\[\d+\]")
   	for component in components:
		if not re.search(pattern, component):
			return cmds.ls(cmds.polyListComponentConversion(components, toUV=True), fl=flatten)
	return components        

def getFacesPerPatches(object):
	"""
	This definition returns the faces per patches from given object.

	:param object: Object. ( String )
	:return: Faces per patches. ( Dictionary )
	"""

	faces = cmds.ls("%s.f[0:%s]" % (object, cmds.polyEvaluate(object, face=True)), fl=True)
	facesPerPatches = {}
	for face in faces:
		map, patch = getComponentsMariPatches(face)[0]
		if not patch in facesPerPatches:
			facesPerPatches[patch] = [face]
			continue
        
		facesPerPatches[patch].append(face)
	return facesPerPatches

def getObjectUVsArea(object):
	"""
	This definition returns given object UVs area.

	:param object: Object to retrieve UVs area. ( String )
	:return: UVs area. ( Integer )
	"""

	selectionList = OpenMaya.MSelectionList()
	selectionList.add(object)
	selectionListIterator = OpenMaya.MItSelectionList(selectionList)
	dagPath = OpenMaya.MDagPath()
	selectionListIterator.getDagPath(dagPath, OpenMaya.MObject())
	meshPolygonIterator = OpenMaya.MItMeshPolygon(dagPath)
	scriptUtil = OpenMaya.MScriptUtil()
	scriptUtil.createFromDouble(0.0)
	areaPointer = scriptUtil.asDoublePtr() 
	uvsArea = 0
	while not meshPolygonIterator.isDone():
		meshPolygonIterator.getUVArea(areaPointer)
		uvsArea += OpenMaya.MScriptUtil(areaPointer).asDouble()
		meshPolygonIterator.next()
	return uvsArea

def getComponentUVDims(component):
	"""
	This definition returns the UVDims of the given component.

	:param component: Component to retrieve the UVDims. ( String )
	:return: UVDims. ( Tuple )
	"""

	u, v = cmds.polyEditUV(component, q=True, uValue=True, vValue=True)
	return int(u), int(v)

def getMariPatchFromUVDims(uvDims):
	"""
	This definition returns the Mari patch of the given component from UVDims.

	:param uvDims: UVDims to convert to Mari Patch. ( Tuple )
	:return: Mari patch. ( Integer )
	"""

	uDim, vDim = uvDims
	return 1000 + uDim + 1 + vDim *10

def getComponentsUVDims(components):
	"""
	This definition returns given components UVDims.

	:param components: Components. ( Tuple / List )
	:return: Components UVDims. ( List )
	"""

	uvs = getUVsFromComponents(components)
	uvDims = []
	for uv in uvs:
		uDim, vDim = getComponentUVDims(uv)
		uvDims.append((uv, (uDim, vDim)))
	return uvDims

def getComponentsMariPatches(components):
	"""
	This definition returns given components Mari patches.

	:param components: Components. ( Tuple / List )
	:return: Components Mari patches. ( List )
	"""

	uvDims = getComponentsUVDims(components)
	mariPatches = []
	for uv, uvDims in uvDims:
		mariPatches.append((uv, getMariPatchFromUVDims(uvDims)))
	return mariPatches

def getComponentsOccupationAsUVDims(components):
	"""
	This definition returns given components occupation as UVDims.

	:param components: Components. ( Tuple / List )
	:return: Components occupation. ( Tuple )
	"""

	shells = getComponentsUVDims(components)
	return tuple(set((shell[1] for shell in shells)))

def getComponentsOccupationAsMariPatches(components):
	"""
	This definition returns given components occupation as Mari patches.

	:param components: Components. ( Tuple / List )
	:return: Components occupation. ( Tuple )
	"""

	mariPatches = getComponentsMariPatches(components)
	return tuple(set((patch[1] for patch in mariPatches)))

def printComponentsOccupationAsUvDims():
	"""
	This definition prints selected components occupation as UVDims.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and pprint.pprint(sorted(getComponentsOccupationAsUVDims(selection)))

def IPrintComponentsOccupationAsUvDims():
	"""
	This definition is the printComponentsOccupationAsUvDims definition Interface.
	"""

	printComponentsOccupationAsUvDims()

def printComponentsOccupationAsMariPatches():
	"""
	This definition prints selected components occupation as Mari patches.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and pprint.pprint(sorted(getComponentsOccupationAsMariPatches(selection)))

def IPrintComponentsOccupationAsMariPatches():
	"""
	This definition is the printComponentsOccupationAsMariPatches definition Interface.
	"""

	printComponentsOccupationAsMariPatches()

def getComponentsBoundingBox(components):
	"""
	This definition returns given components Bounding Box.

	:param components: Components. ( Tuple / List )
	:return: Components Bounding Box. ( Tuple )
	"""
	
	uvs = getUVsFromComponents(components)
	uMin, vMin, uMax, vMax = 2**8, 2**8, -2**8, -2**8
	for uv in uvs:	
		u, v = cmds.polyEditUV(uv, q=True, uValue=True, vValue=True)
		uMin = min(u, uMin)
		uMax = max(u, uMax)
		vMin = min(v, vMin)
		vMax = max(v, vMax)
	return uMin, vMin, uMax, vMax

def getComponentsUVsCenter(components):
	"""
	This definition returns given components UVs center.

	:param components: Components. ( Tuple / List )
	:return: Components UVs center. ( Tuple )
	"""
	
	uMin, vMin, uMax, vMax = getComponentsBoundingBox(components)
	return (uMin + uMax) / 2.0, (vMin + vMax) / 2.0

def printComponentsUvsCenterAsUvDims():
	"""
	This definition prints selected components Uvs center as UVDims
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and pprint.pprint(tuple([int(value) for value in getComponentsUVsCenter(selection)]))

def IPrintComponentsUvsCenterAsUvDims():
	"""
	This definition is the printComponentsUvsCenterAsUvDims definition Interface.
	"""

	printComponentsUvsCenterAsUvDims()

def printComponentsUvsCenterAsMariPatch():
	"""
	This definition prints selected components Uvs center as Mari Patch.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and pprint.pprint(getMariPatchFromUVDims((int(value) for value in getComponentsUVsCenter(selection))))

def IPrintComponentsUvsCenterAsMariPatch():
	"""
	This definition is the printComponentsUvsCenterAsMariPatch definition Interface.
	"""

	printComponentsUvsCenterAsMariPatch()

@stacksHandler
def scaleComponentsUVs(components, su=1, sv=1):
	"""
	This definition scales given components UVs.

	:param components: Components. ( Tuple / List )
	:param su: Scale U value. ( Float )
	:param sv: Scale V value. ( Float )
	:return: Definition succes. ( Boolean )
	"""
	
	if su == 0.0:
		su = 1e-15
	if sv == 0.0:
		sv = 1e-15
	uvs = getUVsFromComponents(components)
	uCenter, vCenter = getComponentsUVsCenter(uvs)
	cmds.polyEditUV(uvs, pu=uCenter, pv=vCenter, su=su, sv=sv)
	return True

@stacksHandler
def centerComponentsUVs(components):
	"""
	This definition centers given components UVs.

	:param components: Components. ( Tuple / List )
	:return: Definition succes. ( Boolean )
	"""
	
	uvs = getUVsFromComponents(components)
	uMin, vMin, uMax, vMax = getComponentsBoundingBox(uvs)
	uCenter, vCenter = (uMin + uMax) / 2.0, (vMin + vMax) / 2.0
	uTargetCenter, vTargetCenter = math.floor(uCenter), math.floor(vCenter)
	cmds.polyEditUV(uvs, u=uTargetCenter - uCenter + 0.5, v=vTargetCenter - vCenter + 0.5)
	return True

@stacksHandler
def scaleCenterComponentsUVs(components, coverage=DEFAULT_SCALE_COVERAGE):
	"""
	This definition scales / centers given components UVs.

	:param components: Components. ( Tuple / List )
	:return: Definition succes. ( Boolean )
	"""
	
	uvs = getUVsFromComponents(components)
	uMin, vMin, uMax, vMax = getComponentsBoundingBox(uvs)
	uCenter, vCenter = (uMin + uMax) / 2.0, (vMin + vMax) / 2.0
	uTargetCenter, vTargetCenter = math.floor(uCenter), math.floor(vCenter)
	cmds.polyEditUV(uvs, u=uTargetCenter - uCenter + 0.5, v=vTargetCenter - vCenter + 0.5)
	uScale = math.fabs(uMin - uMax)
	vScale = math.fabs(vMin - vMax)
	scaleFactor = 1 / max(uScale, vScale) * coverage
	cmds.polyEditUV(uvs, pu=uTargetCenter + 0.5, pv=vTargetCenter + 0.5, su=scaleFactor, sv=scaleFactor)
	return True

@stacksHandler
def rotateComponentsUVs(components, value, clockWise=True):
	"""
	This definition rotates given components UVs.

	:param components: Components. ( Tuple / List )
	:param value: Rotation value. ( Float )
	:param clockWise: Rotation direction. ( Boolean )
	:return: Definition succes. ( Boolean )
	"""
	
	uvs = getUVsFromComponents(components)
	uCenter, vCenter = getComponentsUVsCenter(uvs)
	if not clockWise:
		value = -value
	cmds.polyEditUV(uvs, pu=uCenter, pv=vCenter, a=-value)		
	return True

@stacksHandler
@anchorSelection
def polyRotateComponentsUVs(components, value, clockWise=True):
	"""
	This definition rotates given components UVs using Maya "polyRotateUVs" melscript ( Ugly but sadly faster ).

	:param components: Components. ( Tuple / List )
	:param value: Rotation value. ( Float )
	:param clockWise: Rotation direction. ( Boolean )
	:return: Definition succes. ( Boolean )
	"""
	
	if clockWise:
		value = -value	
	
	mel.eval("polyRotateUVs %s" % value)
	return True

@stacksHandler
def moveComponentsUVs(components, u=0, v=0):
	"""
	This definition moves given components UVs.

	:param components: Components. ( Tuple / List )
	:param u: U value. ( Float )
	:param v: V value. ( Float )
	:return: Definition succes. ( Boolean )
	"""

	uvs = getUVsFromComponents(components, flatten=False)
	cmds.polyEditUV(uvs, u=u, v=v)	
	return True

@stacksHandler
def mirrorComponentsUVs(components, horizontal=True):
	"""
	This definition mirrors given components UVs.

	:param components: Components. ( Tuple / List )
	:param horizontal: Horizontal mirror. ( Boolean )
	:return: Definition succes. ( Boolean )
	"""

	uvs = getUVsFromComponents(components)
	uCenter, vCenter = (math.floor(value) for value in getComponentsUVsCenter(uvs))
	if horizontal:
		cmds.polyEditUV(uvs, pu=uCenter + 0.5, pv=vCenter + 0.5, su=-1)	
	else:
		cmds.polyEditUV(uvs, pu=uCenter + 0.5, pv=vCenter + 0.5, sv=-1)	
	return True


@stacksHandler
def stackObjectsUVs(objects, alignement="center", horizontal=True, margin=0):
	"""
	This definition stacks given objects UVs.

	:param objects: Objects. ( Tuple / List )
	:param alignement: Alignement ( "bottom", "top", "left", "right", "center" ). ( String )
	:param horizontal: Horizontal stack. ( Boolean )
	:return: Definition succes. ( Boolean )
	"""
	
	if not objects:
		return

	uvs = getUVsFromComponents(objects.pop(0))	
	uCenter, vCenter = getComponentsUVsCenter(uvs)
	uMin, vMin, uMax, vMax = getComponentsBoundingBox(uvs)
	uBorder = uMax - uMin + uMin
	vBorder = vMax - vMin + vMin
	for object in objects:
		uvs = getUVsFromComponents(object)		
		currentUMin, currentVMin, currentUMax, currentVMax = getComponentsBoundingBox(uvs)
		if horizontal:
			offsetU = uBorder - currentUMin + margin
			if alignement == "bottom":
				offsetV = vMin - currentVMin
			elif alignement == "center":
				offsetV = (vMin - currentVMin) / 2 + (vMax - currentVMax) / 2
			elif alignement == "top":
				offsetV = vMax - currentVMax
			uBorder = uBorder + currentUMax - currentUMin + margin
		else:
			offsetV = vBorder - currentVMin + margin
			if alignement == "left":
				offsetU = uMin - currentUMin
			elif alignement == "center":
				offsetU = (uMin - currentUMin) / 2 + (uMax - currentUMax) / 2
			elif alignement == "right":
				offsetU = uMax - currentUMax
			vBorder = vBorder + currentVMax - currentVMin + margin
		cmds.polyEditUV(uvs, u=offsetU, v=offsetV)	
	return True

@stacksHandler
def prescaleUVsShells(object):
	"""
	This definition prescales object UVs shells.

	:param objects: Object. ( String )
	:return: Definition succes. ( Boolean )
	"""
	
	uvs = getUVsFromComponents(object)	
	uMin, vMin, uMax, vMax = getComponentsBoundingBox(uvs)
	uCenter, vCenter = (uMin + uMax) / 2.0, (vMin + vMax) / 2.0
	width, height = uMax - uMin, vMax - vMin
	scale = max(width, height)
	
	cmds.polyMultiLayoutUV(object, lm=0, sc=1, rbf=0, fr=False, ps=0.2, l=2, psc=True)

	currentUMin, currentVMin, currentUMax, currentVMax = getComponentsBoundingBox(uvs)
	currentUCenter, currentVCenter = (currentUMin + currentUMax) / 2.0, (currentVMin + currentVMax) / 2.0
	currentWidth, currentHeight = currentUMax - currentUMin, currentVMax - currentVMin
	currentScale = max(currentWidth, currentHeight)
	
	scaleFactor = scale / currentScale

	cmds.polyEditUV(uvs, u=uCenter - currentUCenter, v=vCenter - currentVCenter)		
	scaleComponentsUVs(uvs, su=scaleFactor, sv=scaleFactor)
	return True

@stacksHandler
def autoRatioUVsAreas(objects):
	"""
	This definition scales objects UVs depending their worldspace areas.

	:param objects: Objects. ( Tuple / List )
	:return: Definition succes. ( Boolean )
	"""
	
	if not objects:
		return
	baseObject = objects.pop(0)
	area = cmds.polyEvaluate(baseObject, worldArea=True)
	uvsArea = getObjectUVsArea(baseObject)

	for object in objects:
		currentArea = cmds.polyEvaluate(object, worldArea=True)
		currentUVsArea = getObjectUVsArea(object)
		scaleFactor = math.sqrt(((currentArea * uvsArea) / currentUVsArea) / area)
		scaleComponentsUVs(object, su=scaleFactor, sv=scaleFactor)
	return True

@stacksHandler
def addUVsChecker(items, uRepeats=4, vRepeats=4):
	"""
	This definition applies UVs checkers onto given geometry objects.

	:param items: Current items list. ( List )
	:param uRepeats: U checker repeats. ( Float )
	:param vRepeats: V checker repeats. ( Float )
	:return: Definition succes. ( Boolean )
	"""

	# Removing previous UVs checkers shaders.
	removeUVsChecker()

	lambertSE = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
	lambert = cmds.shadingNode("lambert", asShader=True)
	cmds.connectAttr(lambert + ".outColor", lambertSE + ".surfaceShader", force=True)

	file = cmds.shadingNode("file", asTexture=True)
	cmds.setAttr(file + ".fileTextureName", os.path.normpath(os.path.join(RESOURCES_DIRECTORY, CHECKER_IMAGE)), type="string")
	place2dTexture = cmds.shadingNode("place2dTexture", asUtility=True)
	cmds.setAttr(place2dTexture + ".repeatU", uRepeats)
	cmds.setAttr(place2dTexture + ".repeatV", vRepeats)
	uvAttributes = ("coverage", "translateFrame", "rotateFrame", "mirrorU", "mirrorV", "stagger", "wrapU", "wrapV" , "repeatUV" , "vertexUvOne" , "vertexUvTwo" , "vertexUvThree" , "vertexCameraOne", "noiseUV", "offset", "rotateUV")
	for uvAttribute in uvAttributes:
		cmds.connectAttr(place2dTexture + "." + uvAttribute, file + "." + uvAttribute, force=True)

	cmds.connectAttr(file + ".outColor", lambert + ".color", force=True)

	for item in items:
		if "." in item:
			continue
		cmds.sets(item, edit=True, forceElement=lambertSE)

	cmds.rename(lambert, "UVsChecker_Lambert")
	cmds.rename(lambertSE, "UVsChecker_ShadingEngine")
	cmds.rename(file, "UVsChecker_File")
	cmds.rename(place2dTexture, "UVsChecker_Place2dTexture")
	return True

@stacksHandler
def removeUVsChecker():
	"""
	This definition removes UVs checkers from the scene.
	:return: Definition succes. ( Boolean )
	"""

	if cmds.objExists("UVsChecker_ShadingEngine"):
		connections = cmds.listHistory("UVsChecker_ShadingEngine")

		for connection in connections:
			if isGeometry(connection):
				cmds.sets(connection, edit=True, forceElement="initialShadingGroup")

		cmds.delete("UVsChecker_ShadingEngine")

	if cmds.objExists("UVsChecker_Lambert"):
		cmds.delete("UVsChecker_Lambert")

	if cmds.objExists("UVsChecker_File"):
		cmds.delete("UVsChecker_File")

	if cmds.objExists("UVsChecker_Place2dTexture"):
		cmds.delete("UVsChecker_Place2dTexture")
	return True	

@stacksHandler
def setUVsCheckerRepeats(uRepeats=None, vRepeats=None):
	"""
	This definition sets UVs checkers repeats.

	:param uRepeats: U checker repeats. ( Float )
	:param vRepeats: V checker repeats. ( Float )
	:return: Definition succes. ( Boolean )
	"""

	if not cmds.objExists("UVsChecker_Place2dTexture"):
		return
	
	uRepeats and cmds.setAttr("UVsChecker_Place2dTexture.repeatU", uRepeats)
	vRepeats and cmds.setAttr("UVsChecker_Place2dTexture.repeatV", vRepeats)
	return True

@stacksHandler
def getPatchShaderTree(patch, prefix):
	"""
	This definition builds the patch shader tree of given patch.

	:param patch: Patch. ( Integer )
	:param prefix: Name prefix. ( String )
	:return: Tree shading engine. ( String )
	"""

	name = "%s%s" % (prefix, patch)
	shadingEngine = getNode("%sSG" % name)
	if not shadingEngine:
		lambert = cmds.shadingNode("lambert", asShader=True)
		shadingEngine = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
		cmds.connectAttr("%s.outColor" % lambert, "%s.surfaceShader" % shadingEngine, f=True)
       
		cmds.rename(lambert, name)
		shadingEngine = cmds.rename(shadingEngine, "%sSG" % name)
	return shadingEngine

@stacksHandler
def assignMariShadersToObject(object, prefix):
	"""
	This definition assigns the Mari shaders to given object.

	:param prefix: Shader prefix name. ( String )
	:param object: Object. ( String )
	:return: Definition success. ( Boolean )
	"""

	patches = getComponentsOccupationAsMariPatches(object)
	if len(patches) == 1:
		patch = patches[0]
		shadingEngine = getPatchShaderTree(patch, prefix)
		cmds.sets(object, e=True, forceElement=shadingEngine)
	else:
		for patch, faces in getFacesPerPatches(object).items():
			shadingEngine = getPatchShaderTree(patch, prefix)
			cmds.sets(faces, e=True, forceElement=shadingEngine)
	return True

@stacksHandler
def assignMariShaders(objects, prefix):
	"""
	This definition assigns the Mari shaders to given objects.

	:param objects: Objects. ( List )
	:param prefix: Shader prefix name. ( String )
	:return: Definition success. ( Boolean )
	"""

	mainProgressBar = mel.eval('$tmp = $gMainProgressBar')
	cmds.progressBar(mainProgressBar, edit=True, beginProgress=True, isInterruptable=True, status="Assigning Mari shaders ...", maxValue=len(objects))
	
	success = True
	for object in objects:
		if cmds.progressBar(mainProgressBar, query=True, isCancelled=True):
                	break

        	cmds.progressBar(mainProgressBar, edit=True, status="Assigning Mari shaders to '%s' ..." % object, step=1)

		success *= assignMariShadersToObject(object, prefix)
	
	cmds.progressBar(mainProgressBar, edit=True, endProgress=True)

	return success

@stacksHandler
def IAssignMariShaders():
	"""
	This definition is the assignMariShaders definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	if not selection:
		return

	projectName = os.path.basename(os.path.dirname(cmds.workspace(q=True, fullName=True)))
	result = cmds.promptDialog(title="Mari Shaders Prefix", message="Enter Prefix:", text=projectName, button=["OK", "Cancel"], defaultButton="OK", cancelButton="Cancel", dismissString="Cancel")
	if result == "OK":
		prefix = cmds.promptDialog(query=True, text=True)
		prefix and assignMariShaders(selection, prefix)

@stacksHandler
def flipUVs_button_OnClicked(state=None):
	"""
	This definition is triggered by the **flipUVs_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and mirrorComponentsUVs(selection)

@stacksHandler
def moveUpUVs_button_OnClicked(state=None):
	"""
	This definition is triggered by the **moveUpUVs_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and moveComponentsUVs(selection, v=cmds.floatField("moveFactor_floatField", q=True, value=True))

@stacksHandler
def flopUVs_button_OnClicked(state=None):
	"""
	This definition is triggered by the **flopUVs_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and mirrorComponentsUVs(selection, horizontal=False)

@stacksHandler
def moveLeftUVs_button_OnClicked(state=None):
	"""
	This definition is triggered by the **moveLeftUVs_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and moveComponentsUVs(selection, u=-cmds.floatField("moveFactor_floatField", q=True, value=True))

@stacksHandler
def fitUVs_button_OnClicked(state=None):
	"""
	This definition is triggered by the **fitUVs_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and scaleCenterComponentsUVs(selection, float(cmds.intField("coverage_intField", q=True, value=True)) / 100)

@stacksHandler
def moveRightUVs_button_OnClicked(state=None):
	"""
	This definition is triggered by the **moveRightUVs_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and moveComponentsUVs(selection, u=cmds.floatField("moveFactor_floatField", q=True, value=True))

@stacksHandler
def centerUVs_button_OnClicked(state=None):
	"""
	This definition is triggered by the **centerUVs_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and centerComponentsUVs(selection)

@stacksHandler
def moveDownUVs_button_OnClicked(state=None):
	"""
	This definition is triggered by the **moveDownUVs_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and moveComponentsUVs(selection, v=-cmds.floatField("moveFactor_floatField", q=True, value=True))

@stacksHandler
def scaleUVs_button_OnClicked(state=None):
	"""
	This definition is triggered by the **scaleUVs_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and scaleComponentsUVs(selection, su=cmds.floatField("uScale_floatField", q=True, value=True), sv=cmds.floatField("vScale_floatField", q=True, value=True))

@stacksHandler
def rotateCounterClockWiseUVs_button_OnClicked(state=None):
	"""
	This definition is triggered by the **rotateCounterClockWiseUVs_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and polyRotateComponentsUVs(selection, cmds.floatField("rotation_floatField", q=True, value=True), clockWise=False)

@stacksHandler
def rotateClockWiseUVs_button_OnClicked(state=None):
	"""
	This definition is triggered by the **rotateClockWiseUVs_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and polyRotateComponentsUVs(selection, cmds.floatField("rotation_floatField", q=True, value=True))

@stacksHandler
def stackUVsOnUBottom_button_OnClicked(state=None):
	"""
	This definition is triggered by the **stackUVsOnUBottom_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and stackObjectsUVs(selection, alignement="bottom", margin=cmds.floatField("margin_floatField", q=True, value=True))

@stacksHandler
def stackUVsOnUCenter_button_OnClicked(state=None):
	"""
	This definition is triggered by the **stackUVsOnUCenter_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and stackObjectsUVs(selection, alignement="center", margin=cmds.floatField("margin_floatField", q=True, value=True))

@stacksHandler
def stackUVsOnUTop_button_OnClicked(state=None):
	"""
	This definition is triggered by the **stackUVsOnUTop_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and stackObjectsUVs(selection, alignement="top", margin=cmds.floatField("margin_floatField", q=True, value=True))
@stacksHandler
def stackUVsOnVLeft_button_OnClicked(state=None):
	"""
	This definition is triggered by the **stackUVsOnVLeft_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and stackObjectsUVs(selection, alignement="left", horizontal=False, margin=cmds.floatField("margin_floatField", q=True, value=True))

@stacksHandler
def stackUVsOnVCenter_button_OnClicked(state=None):
	"""
	This definition is triggered by the **stackUVsOnVCenter_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and stackObjectsUVs(selection, alignement="center", horizontal=False, margin=cmds.floatField("margin_floatField", q=True, value=True))

@stacksHandler
def stackUVsOnVRight_button_OnClicked(state=None):
	"""
	This definition is triggered by the **stackUVsOnVRight_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and stackObjectsUVs(selection, alignement="right", horizontal=False, margin=cmds.floatField("margin_floatField", q=True, value=True))

@stacksHandler
def prescaleUVsShells_button_OnClicked(state=None):
	"""
	This definition is triggered by the **prescaleUVsShells_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	for object in selection:
		prescaleUVsShells(object)

@stacksHandler
def autoRatioUVsAreas_button_OnClicked(state=None):
	"""
	This definition is triggered by the **autoRatioUVsAreas_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and autoRatioUVsAreas(selection)

@stacksHandler
def addUVsChecker_button_OnClicked(state=None):
	"""
	This definition is triggered by the **addUVsChecker_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and addUVsChecker(selection)

@stacksHandler
def uRepeat_floatField_OnChanged(value=None):
	"""
	This definition is triggered by the **uRepeat_floatField** button when changed.

	:param value: Field value. ( Float )
	"""
		
	setUVsCheckerRepeats(uRepeats=value)

@stacksHandler
def vRepeat_floatField_OnChanged(value=None):
	"""
	This definition is triggered by the **vRepeat_floatField** button when changed.

	:param value: Field value. ( Float )
	"""
		
	setUVsCheckerRepeats(vRepeats=value)

def unfoldingTools_window():
	"""
	This definition creates the 'Unfolding Tools' main window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("unfoldingTools_window", exists=True)):
		cmds.deleteUI("unfoldingTools_window")

	cmds.window("unfoldingTools_window",
		title="Unfolding Tools",
		width=320)

	spacing = 0
	
	columnsWidth = (106, 106, 106)
	columnsAttach = [(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)]
	
	cmds.columnLayout()

	cmds.frameLayout(label="UVs Move / Scale", collapsable=True, borderStyle="etchedIn")

	cmds.columnLayout()
	
	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button("flipUVs_button", label="Flip", command=flipUVs_button_OnClicked)
	cmds.button("moveUpUVs_button", label="Move Up", command=moveUpUVs_button_OnClicked)
	cmds.button("flopUVs_button", label="Flop", command=flopUVs_button_OnClicked)
	cmds.setParent(upLevel=True)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button("moveLeftUVs_button", label="Move Left", command=moveLeftUVs_button_OnClicked)
	cmds.button("fitUVs_button", label="Fit", command=fitUVs_button_OnClicked)
	cmds.button("moveRightUVs_button", label="Move Right", command=moveRightUVs_button_OnClicked)
	cmds.setParent(upLevel=True)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button("centerUVs_button", label="Center", command=centerUVs_button_OnClicked)
	cmds.button("moveDownUVs_button", label="Move Down", command=moveDownUVs_button_OnClicked)
	cmds.button("scaleUVs_button", label="Scale", command=scaleUVs_button_OnClicked)
	cmds.setParent(upLevel=True)
	
	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.text(label="Coverage %:")
	cmds.intField("coverage_intField", minValue=0, maxValue=100, value=98)
	cmds.setParent(upLevel=True)
	
	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.text(label="Move Factor:")
	cmds.floatField("moveFactor_floatField", minValue=0, maxValue=10, value=1)
	cmds.setParent(upLevel=True)
	
	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.text(label="Scale U / V:")
	cmds.floatField("uScale_floatField", minValue=-10, maxValue=10, value=1)
	cmds.floatField("vScale_floatField", minValue=-10, maxValue=10, value=1)
	cmds.setParent(upLevel=True)

	cmds.setParent(upLevel=True)
	cmds.setParent(upLevel=True)

	cmds.frameLayout(label="UVs Rotation", collapsable=True, borderStyle="etchedIn")
	
	cmds.columnLayout()

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button("rotateCounterClockWiseUVs_button", label="Rotate CCWZ", command=rotateCounterClockWiseUVs_button_OnClicked)
	cmds.button(label="", enable=False)
	cmds.button("rotateClockWiseUVs_button", label="Rotate CWZ", command=rotateClockWiseUVs_button_OnClicked)
	cmds.setParent(upLevel=True)
	
	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.text(label="Angle:")
	cmds.floatField("rotation_floatField", minValue=-360, maxValue=360, value=45)
	cmds.setParent(upLevel=True)
	
	cmds.setParent(upLevel=True)
	cmds.setParent(upLevel=True)

	cmds.frameLayout(label="UVs Alignement", collapsable=True, borderStyle="etchedIn")
	
	cmds.columnLayout()

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button(label="", enable=False)
	cmds.button("alignUVsMaximumV_button", label="Align Max. V", command=lambda state: mel.eval("alignUV 0 0 1 0;"))
	cmds.button(label="", enable=False)
	cmds.setParent(upLevel=True)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button("alignUVsMinimumU_button", label="Align Min. U", command=lambda state: mel.eval("alignUV 1 1 0 0;"))
	cmds.button("straightenUVs_button", label="Straigthen", command=lambda state: mel.eval("warning \"Not implemented yet!\";"))
	cmds.button("alignUVsMaximumU_button", label="Align Max. U", command=lambda state: mel.eval("alignUV 1 0 0 0;"))
	cmds.setParent(upLevel=True)
	
	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button(label="", enable=False)
	cmds.button("alignUVsMinimumV_button", label="Align Min. V", command=lambda state: mel.eval("alignUV 0 0 1 1;"))	
	cmds.button(label="", enable=False)
	cmds.setParent(upLevel=True)

	cmds.setParent(upLevel=True)
	cmds.setParent(upLevel=True)

	cmds.frameLayout(label="UVs Stacks", collapsable=True, borderStyle="etchedIn")
	
	cmds.columnLayout()

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button("stackUVsOnUBottom_button", label="Stack On U Bottom", command=stackUVsOnUBottom_button_OnClicked)
	cmds.button("stackUVsOnUCenter_button", label="Stack On U Center", command=stackUVsOnUCenter_button_OnClicked)
	cmds.button("stackUVsOnUTop_button", label="Stack On U Top", command=stackUVsOnUTop_button_OnClicked)
	cmds.setParent(upLevel=True)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button("stackUVsOnVLeft_button", label="Stack On V Left", command=stackUVsOnVLeft_button_OnClicked)
	cmds.button("stackUVsOnVCenter_button", label="Stack On V Center", command=stackUVsOnVCenter_button_OnClicked)
	cmds.button("stackUVsOnVRight_button", label="Stack On V Right", command=stackUVsOnVRight_button_OnClicked)
	cmds.setParent(upLevel=True)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.text(label="Margin:")
	cmds.floatField("margin_floatField", minValue= 0, maxValue=10, value=0.001)
	cmds.setParent(upLevel=True)

	cmds.setParent(upLevel=True)
	cmds.setParent(upLevel=True)

	cmds.frameLayout(label="UVs Auto Ratio", collapsable=True, borderStyle="etchedIn")
	
	cmds.columnLayout()

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button("prescaleUVsShells_button", label="Prescale Shells", command=prescaleUVsShells_button_OnClicked)
	cmds.button(label="", enable=False)
	cmds.button("autoRatioUVsAreas_button", label="Auto Ratio", command=autoRatioUVsAreas_button_OnClicked)
	cmds.setParent(upLevel=True)

	cmds.setParent(upLevel=True)
	cmds.setParent(upLevel=True)

	cmds.frameLayout(label="UVs Verbose", collapsable=True, borderStyle="etchedIn")
	
	cmds.columnLayout()

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button("printUVsUVdims_button", label="Print UVDims", command=lambda state: printComponentsOccupationAsUvDims())
	cmds.button(label="", enable=False)
	cmds.button("printUVsMariPatches_button", label="Print Mari Patches", command=lambda state: printComponentsOccupationAsMariPatches())
	cmds.setParent(upLevel=True)

	cmds.setParent(upLevel=True)
	cmds.setParent(upLevel=True)

	cmds.frameLayout(label="UVs Checker", collapsable=True, borderStyle="etchedIn")
	
	cmds.columnLayout()

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button("addUVsChecker_button", label="Add Checker", command=addUVsChecker_button_OnClicked)
	cmds.button(label="", enable=False)
	cmds.button("removeUVsChecker_button", label="Remove Checker", command=lambda state: removeUVsChecker())
	cmds.setParent(upLevel=True)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.text(label="Repeat U / V:")
	cmds.floatField("uRepeat_floatField", minValue=0.01, maxValue=256, value=4, step=0.25, changeCommand=uRepeat_floatField_OnChanged)
	cmds.floatField("vRepeat_floatField", minValue=0.01, maxValue=256, value=4, step=0.25, changeCommand=vRepeat_floatField_OnChanged)
	cmds.setParent(upLevel=True)


	cmds.setParent(upLevel=True)
	cmds.setParent(upLevel=True)

	cmds.showWindow("unfoldingTools_window")

	cmds.windowPref(enableAll=True)

def unfoldingTools():
	"""
	This definition launches the 'Unfolding Tools' main window.
	"""

	unfoldingTools_window()

@stacksHandler
def IUnfoldingTools():
	"""
	This definition is the unfoldingTools definition Interface.
	"""

	unfoldingTools()
