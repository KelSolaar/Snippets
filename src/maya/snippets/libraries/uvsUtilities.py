import math
import maya.cmds as cmds
import pprint

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["DEFAULT_SCALE_MARGIN",
			"stacksHandler",
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
			"getComponentsUVsCenter",
			"printComponentsUvsCenterAsUvDims",
			"IPrintComponentsUvsCenterAsUvDims",
			"printComponentsUvsCenterAsMariPatch",
			"IPrintComponentsUvsCenterAsMariPatch",
			"scaleCenterComponentsUvs",
			"IScaleCenterComponentsUvs"]

DEFAULT_SCALE_MARGIN = 0.98

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

def getComponentUVDims(component):
	"""
	This definition returns the UVDims of the provided component.

	:param component: Component to retrieve the UVDims. ( String )
	:return: UVDims. ( Tuple )
	"""

	u, v = cmds.polyEditUV(component, q=True, uValue=True, vValue=True)
	return int(u), int(v)

def getMariPatchFromUVDims(uvDims):
	"""
	This definition returns the Mari patch of the provided component from UVDims.

	:param uvDims: UVDims to convert to Mari Patch. ( Tuple )
	:return: Mari patch. ( Integer )
	"""

	uDim, vDim = uvDims
	return 1000 + uDim + 1 + vDim *10

def getComponentsUVDims(components):
	"""
	This definition returns provided components UVDims.

	:param components: Components. ( Tuple / List )
	:return: Components UVDims. ( List )
	"""

	uvs = cmds.ls(cmds.polyListComponentConversion(components, toUV=True), fl=True)
	uvDims = []
	for uv in uvs:
		uDim, vDim = getComponentUVDims(uv)
		uvDims.append((uv, (uDim, vDim)))
	return uvDims

def getComponentsMariPatches(components):
	"""
	This definition returns provided components Mari patches.

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
	This definition returns provided components occupation as UVDims.

	:param components: Components. ( Tuple / List )
	:return: Components occupation. ( Tuple )
	"""

	shells = getComponentsUVDims(components)
	return tuple(set((shell[1] for shell in shells)))

def getComponentsOccupationAsMariPatches(components):
	"""
	This definition returns provided components occupation as Mari patches.

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
	This definition returns provided components Bounding Box.

	:param components: Components. ( Tuple / List )
	:return: Components Bounding Box. ( Tuple )
	"""
	
	uvs = cmds.ls(cmds.polyListComponentConversion(components, toUV=True), fl=True)
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
	This definition returns provided components UVs center.

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
def scaleCenterComponentsUvs(components, margin):
	"""
	This definition scales / centers provided components UVs.

	:param components: Components. ( Tuple / List )
	:return: Definition succes. ( Boolean )
	"""
	
	uvs = cmds.ls(cmds.polyListComponentConversion(components, toUV=True), fl=True)
	uMin, vMin, uMax, vMax = getComponentsBoundingBox(uvs)
	uCenter, vCenter = (uMin + uMax) / 2.0, (vMin + vMax) / 2.0
	uTargetCenter, vTargetCenter = math.floor(uCenter), math.floor(vCenter)
	cmds.polyEditUV(uvs, u=uTargetCenter - uCenter + 0.5, v=vTargetCenter - vCenter + 0.5)
	uScale = math.fabs(uMin - uMax)
	vScale = math.fabs(vMin - vMax)
	scaleFactor = 1 / max(uScale, vScale) * margin
	cmds.polyEditUV(uvs, pu=uTargetCenter + 0.5, pv=vTargetCenter + 0.5, su=scaleFactor, sv=scaleFactor)
	return True

@stacksHandler
def IScaleCenterComponentsUvs():
	"""
	This definition is the scaleCenterComponentsUVs definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and scaleCenterComponentsUvs(selection, DEFAULT_SCALE_MARGIN)
