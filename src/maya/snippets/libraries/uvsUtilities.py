import math
import maya.cmds as cmds
import maya.mel as mel
import pprint

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["DEFAULT_SCALE_COVERAGE = 0.98",
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
				"getComponentsBoundingBox",
				"getComponentsUVsCenter",
				"printComponentsUvsCenterAsUvDims",
				"IPrintComponentsUvsCenterAsUvDims",
				"printComponentsUvsCenterAsMariPatch",
				"IPrintComponentsUvsCenterAsMariPatch",
				"scaleComponentsUVs",
				"centerComponentsUVs",
				"scaleCenterComponentsUvs",
				"IScaleCenterComponentsUvs",
				"rotateComponentsUVs",
				"moveComponentsUVs",
				"mirrorComponentsUVs",
				"stackObjectsUVs",
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
				"stackUVsOnU_button_OnClicked",
				"stackUVsOnV_button_OnClicked",
				"uvsTools_window",
				"uvsTools",
				"IUvsTools"]

DEFAULT_SCALE_COVERAGE = 0.98

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
def scaleComponentsUVs(components, su=1, sv=1):
	"""
	This definition scales provided components UVs.

	:param components: Components. ( Tuple / List )
	:param su: Scale U value. ( Float )
	:param sv: Scale V value. ( Float )
	:return: Definition succes. ( Boolean )
	"""
	if su == 0.0:
		su = 1e-15
	if sv == 0.0:
		sv = 1e-15
	uvs = cmds.ls(cmds.polyListComponentConversion(components, toUV=True), fl=True)
	uCenter, vCenter = getComponentsUVsCenter(uvs)
	cmds.polyEditUV(uvs, pu=uCenter, pv=vCenter, su=su, sv=sv)
	return True

@stacksHandler
def centerComponentsUVs(components):
	"""
	This definition centers provided components UVs.

	:param components: Components. ( Tuple / List )
	:return: Definition succes. ( Boolean )
	"""
	
	uvs = cmds.ls(cmds.polyListComponentConversion(components, toUV=True), fl=True)
	uMin, vMin, uMax, vMax = getComponentsBoundingBox(uvs)
	uCenter, vCenter = (uMin + uMax) / 2.0, (vMin + vMax) / 2.0
	uTargetCenter, vTargetCenter = math.floor(uCenter), math.floor(vCenter)
	cmds.polyEditUV(uvs, u=uTargetCenter - uCenter + 0.5, v=vTargetCenter - vCenter + 0.5)
	return True

@stacksHandler
def scaleCenterComponentsUvs(components, coverage):
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
	scaleFactor = 1 / max(uScale, vScale) * coverage
	cmds.polyEditUV(uvs, pu=uTargetCenter + 0.5, pv=vTargetCenter + 0.5, su=scaleFactor, sv=scaleFactor)
	return True

@stacksHandler
def IScaleCenterComponentsUvs():
	"""
	This definition is the scaleCenterComponentsUVs definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and scaleCenterComponentsUvs(selection, DEFAULT_SCALE_COVERAGE)

@stacksHandler
def rotateComponentsUVs(components, value, clockWise=True):
	"""
	This definition rotates provided components UVs.

	:param components: Components. ( Tuple / List )
	:param value: Rotation value. ( Float )
	:param clockWise: Rotation direction. ( Boolean )
	:return: Definition succes. ( Boolean )
	"""
	
	uvs = cmds.ls(cmds.polyListComponentConversion(components, toUV=True), fl=True)
	uCenter, vCenter = getComponentsUVsCenter(uvs)
	if not clockWise:
		value = -value
	print value
	cmds.polyEditUV(uvs, pu=uCenter, pv=vCenter, a=-value)		
	return True

@stacksHandler
def moveComponentsUVs(components, u=0, v=0):
	"""
	This definition moves provided components UVs.

	:param components: Components. ( Tuple / List )
	:param u: U value. ( Float )
	:param v: V value. ( Float )
	:return: Definition succes. ( Boolean )
	"""

	uvs = cmds.ls(cmds.polyListComponentConversion(components, toUV=True), fl=True)
	cmds.polyEditUV(uvs, u=u, v=v)	
	return True

@stacksHandler
def mirrorComponentsUVs(components, horizontal=True):
	"""
	This definition mirrors provided components UVs.

	:param components: Components. ( Tuple / List )
	:param horizontal: Horizontal mirror. ( Boolean )
	:return: Definition succes. ( Boolean )
	"""

	uvs = cmds.ls(cmds.polyListComponentConversion(components, toUV=True), fl=True)
	uCenter, vCenter = (math.floor(value) for value in getComponentsUVsCenter(uvs))
	if horizontal:
		cmds.polyEditUV(uvs, pu=uCenter + 0.5, pv=vCenter + 0.5, su=-1)	
	else:
		cmds.polyEditUV(uvs, pu=uCenter + 0.5, pv=vCenter + 0.5, sv=-1)	
	return True


@stacksHandler
def stackObjectsUVs(objects, horizontal=True, margin=0):
	"""
	This definition stacks provided objects UVs.

	:param components: Components. ( Tuple / List )
	:param horizontal: Horizontal stack. ( Boolean )
	:return: Definition succes. ( Boolean )
	"""
	
	if not objects:
		return

	uvs = cmds.ls(cmds.polyListComponentConversion(objects.pop(0), toUV=True), fl=True)	
	uCenter, vCenter = getComponentsUVsCenter(uvs)
	uMin, vMin, uMax, vMax = getComponentsBoundingBox(uvs)
	uBorder = uMax - uMin + uMin
	vBorder = vMax - vMin + vMin
	for i, object in enumerate(objects):
		uvs = cmds.ls(cmds.polyListComponentConversion(object, toUV=True), fl=True)		
		currentUMin, currentVMin, currentUMax, currentVMax = getComponentsBoundingBox(uvs)
		if horizontal:
			offsetU = uBorder - currentUMin + margin
			offsetV = vMin - currentVMin
			uBorder = uBorder + currentUMax - currentUMin + margin
		else:
			offsetU = uMin - currentUMin
			offsetV = vBorder - currentVMin + margin
			vBorder = vBorder + currentVMax - currentVMin + margin
		cmds.polyEditUV(uvs, u=offsetU, v=offsetV)	
	return True
	
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
	selection and scaleCenterComponentsUvs(selection, float(cmds.intField("coverage_intField", q=True, value=True)) / 100)

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
	selection and rotateComponentsUVs(selection, cmds.floatField("rotation_floatField", q=True, value=True), clockWise=False)

@stacksHandler
def rotateClockWiseUVs_button_OnClicked(state=None):
	"""
	This definition is triggered by the **rotateClockWiseUVs_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and rotateComponentsUVs(selection, cmds.floatField("rotation_floatField", q=True, value=True))

@stacksHandler
def stackUVsOnU_button_OnClicked(state=None):
	"""
	This definition is triggered by the **stackUVsOnU_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and stackObjectsUVs(selection, margin=cmds.floatField("margin_floatField", q=True, value=True))

@stacksHandler
def stackUVsOnV_button_OnClicked(state=None):
	"""
	This definition is triggered by the **stackUVsOnV_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and stackObjectsUVs(selection, horizontal=False, margin=cmds.floatField("margin_floatField", q=True, value=True))

def uvsTools_window():
	"""
	This definition creates the 'UVs Tools' main window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("uvsTools_window", exists=True)):
		cmds.deleteUI("uvsTools_window")

	cmds.window("uvsTools_window",
		title="UVs Tools",
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
	cmds.intField("coverage_intField", minValue= 0, maxValue=100, value=98)
	cmds.setParent(upLevel=True)
	
	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.text(label="Move Factor:")
	cmds.floatField("moveFactor_floatField", minValue= 0, maxValue=10, value=1)
	cmds.setParent(upLevel=True)
	
	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.text(label="Scale U / V:")
	cmds.floatField("uScale_floatField", minValue= -10, maxValue=10, value=1)
	cmds.floatField("vScale_floatField", minValue= -10, maxValue=10, value=1)
	cmds.setParent(upLevel=True)

	cmds.setParent(topLevel=True)

	cmds.frameLayout(label="UVs Rotation", collapsable=True, borderStyle="etchedIn")
	
	cmds.columnLayout()

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button("rotateCounterClockWiseUVs_button", label="Rotate CCWZ", command=rotateCounterClockWiseUVs_button_OnClicked)
	cmds.button(label="", enable=False)
	cmds.button("rotateClockWiseUVs_button", label="Rotate CWZ", command=rotateClockWiseUVs_button_OnClicked)
	cmds.setParent(upLevel=True)
	
	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.text(label="Angle:")
	cmds.floatField("rotation_floatField", minValue= -360, maxValue=360, value=45)
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
	cmds.button("straightenUVs_button", label="Straigthen")
	cmds.button("alignUVsMaximumU_button", label="Align Max. U", command=lambda state: mel.eval("alignUV 1 0 0 0;"))
	cmds.setParent(upLevel=True)
	
	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button(label="", enable=False)
	cmds.button("alignUVsMinimumV_button", label="Align Min. V", command=lambda state: mel.eval("alignUV 0 0 1 1;"))	
	cmds.button(label="", enable=False)
	cmds.setParent(upLevel=True)

	cmds.setParent(topLevel=True)

	cmds.frameLayout(label="UVs Stacks", collapsable=True, borderStyle="etchedIn")
	
	cmds.columnLayout()

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.button("stackUVsOnU_button", label="Stack On U", command=stackUVsOnU_button_OnClicked)
	cmds.button(label="", enable=False)
	cmds.button("stackUVsOnV_button", label="Stack On V", command=stackUVsOnV_button_OnClicked)
	cmds.setParent(upLevel=True)

	cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
	cmds.text(label="Margin:")
	cmds.floatField("margin_floatField", minValue= 0, maxValue=10, value=0.001)
	cmds.setParent(upLevel=True)

	cmds.setParent(topLevel=True)

	cmds.showWindow("uvsTools_window")

	cmds.windowPref(enableAll=True)

def uvsTools():
	"""
	This definition launches the 'UVs Tools' main window.
	"""

	uvsTools_window()

@stacksHandler
def IUvsTools():
	"""
	This definition is the uvsTools definition Interface.
	"""

	uvsTools()
