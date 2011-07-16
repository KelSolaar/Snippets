# Credits: Zananick (Unknown).
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya

ALIGNEMENT_ANCHORS = None

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

def getMVector(vector):
	"""
	This Definition Returns An MVector.

	@param vector: Vector. ( List )
	@return: MVector ( MVector )
	"""
	
	return OpenMaya.MVector(vector[0], vector[1], vector[2])

def normalize(vector):
	"""
	This Definition Returns The Normalized Vector.

	@param vector: Vector. ( List )
	@return: Normalized Vector ( Tuple )
	"""
	
	mVector = getMVector(vector)
	mVector.normalize()
	return (mVector.x, mVector.y, mVector.z)

def alignComponentsBetweenAnchors(anchorA, anchorB, components, axis=("X", "Y", "Z")):
	"""
	This Definition Aligns Provided Components BetweenThe Two Anchors.

	@param anchorA: Anchor A. ( String )
	@param anchorB: Anchor B. ( String )
	@param components: Components To Align. ( List )
	@param axis: Collapse Axis. ( Tuple )
	"""
	
	vertices = cmds.ls(cmds.polyListComponentConversion(components, toVertex=True), fl=True)

	pointA = cmds.xform(anchorA, q=True, t=True, ws=True)
	pointB = cmds.xform(anchorB, q=True, t=True, ws=True)
	vectorA = normalize([pointB_ - pointA_ for pointA_, pointB_ in zip(pointA, pointB)])
	
	for vertex in vertices:
		pointC = cmds.xform(vertex, q=True, ws=True, t=True)
		vectorB = [pointC_ - pointA_ for pointA_, pointC_ in zip(pointA, pointC)]
		mVectorA = getMVector(vectorA)
		mVectorB = getMVector(vectorB)
		dot = mVectorB*mVectorA
		mVectorA *= dot
		offset = mVectorB - mVectorA

		xValue = "X" in axis and -offset.x or 0
		yValue = "Y" in axis and -offset.y or 0
		zValue = "Z" in axis and -offset.z or 0

		cmds.xform(vertex, ws=True, r=True, t=(xValue, yValue, zValue))

@stacksHandler
def selectAnchors_Button_OnClicked(state=None):
	"""
	This Definition Is Triggered By The selectAnchors_Button Button When Clicked.
	
	@param state: Button State. ( Boolean )
	"""

	global ALIGNEMENT_ANCHORS

	selection = cmds.ls(sl=True, l=True, fl=True)
	if len(selection) == 2:
		ALIGNEMENT_ANCHORS = (selection[0], selection[1])
	else:
		mel.eval("warning(\"%s | Failed To Retrieve Anchors, You Need To Select Exactly Two Objects Or Components!\")" % __name__)

@stacksHandler
def alignSelection_Button_OnClicked(state=None):
	"""
	This Definition Is Triggered By The alignSelection Button When Clicked.
	
	@param state: Button State. ( Boolean )
	"""

	if ALIGNEMENT_ANCHORS:
		selection = cmds.ls(sl=True, l=True)
		selection and alignComponentsBetweenAnchors(ALIGNEMENT_ANCHORS[0], ALIGNEMENT_ANCHORS[1], selection)

@stacksHandler
def alignSelectionOnXAxis_Button_OnClicked(state=None):
	"""
	This Definition Is Triggered By The alignSelectionOnXAxis Button When Clicked.
	
	@param state: Button State. ( Boolean )
	"""

	if ALIGNEMENT_ANCHORS:
		selection = cmds.ls(sl=True, l=True)
		selection and alignComponentsBetweenAnchors(ALIGNEMENT_ANCHORS[0], ALIGNEMENT_ANCHORS[1], selection, axis=("X"))

@stacksHandler
def alignSelectionOnYAxis_Button_OnClicked(state=None):
	"""
	This Definition Is Triggered By The alignSelectionOnYAxis Button When Clicked.
	
	@param state: Button State. ( Boolean )
	"""

	if ALIGNEMENT_ANCHORS:
		selection = cmds.ls(sl=True, l=True)
		selection and alignComponentsBetweenAnchors(ALIGNEMENT_ANCHORS[0], ALIGNEMENT_ANCHORS[1], selection, axis=("Y"))

@stacksHandler
def alignSelectionOnZAxis_Button_OnClicked(state=None):
	"""
	This Definition Is Triggered By The alignSelectionOnZAxis Button When Clicked.
	
	@param state: Button State. ( Boolean )
	"""

	if ALIGNEMENT_ANCHORS:
		selection = cmds.ls(sl=True, l=True)
		selection and alignComponentsBetweenAnchors(ALIGNEMENT_ANCHORS[0], ALIGNEMENT_ANCHORS[1], selection, axis=("Z"))

def alignComponents_Window():
	"""
	This Definition Creates The Align Components Main Window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("alignComponents_Window", exists=True)):
		cmds.deleteUI("alignComponents_Window")

	cmds.window("alignComponents_Window",
		title="Align Components",
		width=320)
	
	spacing=5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.button("selectAnchors_Button", label="Select Anchors!", command=selectAnchors_Button_OnClicked)

	cmds.separator(height=10, style="singleDash")
	
	cmds.button("alignSelection_Button", label="Align Selection!", command=alignSelection_Button_OnClicked)

	cmds.separator(height=10, style="singleDash")
	
	cmds.button("alignSelectionOnXAxis_Button", label="Align Selection On X!", command=alignSelectionOnXAxis_Button_OnClicked)
	cmds.button("alignSelectionOnYAxis_Button", label="Align Selection On Y!", command=alignSelectionOnYAxis_Button_OnClicked)
	cmds.button("alignSelectionOnZAxis_Button", label="Align Selection On Z!", command=alignSelectionOnZAxis_Button_OnClicked)
	
	cmds.showWindow("alignComponents_Window")

	cmds.windowPref(enableAll=True)

def alignComponents():
	"""
	This Definition Launches The Align Components Main Window.
	"""
	
	alignComponents_Window()

@stacksHandler
def IAlignComponents():
	"""
	This Definition Is The alignComponents Method Interface.
	"""

	alignComponents()
