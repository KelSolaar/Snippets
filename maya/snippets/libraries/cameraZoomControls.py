import maya.cmds as cmds
import maya.mel as mel

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacksHandler",
			"getActiveCamera",
			"overscan_floatSliderGrp_OnValueChanged",
			"horizontalOffset_floatSliderGrp_OnValueChanged",
			"verticalOffset_floatSliderGrp_OnValueChanged",
			"resetZoomControls_button_OnClicked",
			"cameraZoomControls_window",
			"cameraZoomControls",
			"ICameraZoomControls"]

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

def getActiveCamera():
	"""
	This definition returns the current active camera.

	:return: Active camera. ( String )
	"""

	try :
		activePanel = cmds.getPanel(withFocus=True)
		activeCamera = cmds.modelPanel(activePanel, query=True, camera=True)
		return activeCamera
	except :
		pass

def overscan_floatSliderGrp_OnValueChanged(value):
	"""
	This definition is triggered by the 'overscan_floatSliderGrp' slider when its value changed.

	:param value: Value. ( Float )
	"""

	activeCamera = getActiveCamera()
	if activeCamera != None :
		currentOverscanSliderValue = cmds.floatSliderGrp("overscan_floatSliderGrp", query=True, value=True)
		try :
			cmds.setAttr(activeCamera + ".overscan", currentOverscanSliderValue)
		except :
			print("Warning \"Current Camera \".overscan\" Attribute Is Locked !\"")

def horizontalOffset_floatSliderGrp_OnValueChanged(value):
	"""
	This definition is triggered by the 'horizontalOffset_floatSliderGrp' slider when its value changed.

	:param value: Value. ( Float )
	"""

	activeCamera = getActiveCamera()
	if activeCamera != None :
		currentOverscanSliderValue = cmds.floatSliderGrp("horizontalOffset_floatSliderGrp", query=True, value=True)
		try :
			cmds.setAttr(activeCamera + ".horizontalFilmOffset", currentOverscanSliderValue)
		except :
			print("Warning \"Current Camera \".horizontalFilmOffset\" Attribute Is Locked !\"")

def verticalOffset_floatSliderGrp_OnValueChanged(value):
	"""
	This definition is triggered by the 'verticalOffset_floatSliderGrp' slider when its value changed.

	:param value: Value. ( Float )
	"""

	activeCamera = getActiveCamera()
	if activeCamera != None :
		currentOverscanSliderValue = cmds.floatSliderGrp("verticalOffset_floatSliderGrp", query=True, value=True)
		try :
			cmds.setAttr(activeCamera + ".verticalFilmOffset", currentOverscanSliderValue)
		except :
			print("Warning \"Current Camera \".verticalFilmOffset\" Attribute Is Locked !\"")

def resetZoomControls_button_OnClicked(state=None):
	"""
	This definition is triggered by the **resetZoomControls_button** button when clicked.

	:param state: Button state. ( Boolean )
	"""

	cmds.floatSliderGrp("overscan_floatSliderGrp", edit=True, value=1)
	cmds.floatSliderGrp("horizontalOffset_floatSliderGrp", edit=True, value=0)
	cmds.floatSliderGrp("verticalOffset_floatSliderGrp", edit=True, value=0)
	activeCamera = getActiveCamera()
	try :
		cmds.setAttr(activeCamera + ".overscan", 1)
		cmds.setAttr(activeCamera + ".horizontalFilmOffset", 0)
		cmds.setAttr(activeCamera + ".verticalFilmOffset", 0)
	except :
		pass

def cameraZoomControls_window():
	"""
	This definition creates the 'Camera Zoom Controls' main window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("cameraZoomControls_window", exists=True)):
		cmds.deleteUI("cameraZoomControls_window")

	cmds.window("cameraZoomControls_window",
		title="Camera Zoom Controls",
		sizeable=True,
		width=320)

	spacing = 5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.floatSliderGrp("overscan_floatSliderGrp", label="Overscan", field=True, min=0.01, max=2.5, value=1, sliderStep=0.001, dragCommand=overscan_floatSliderGrp_OnValueChanged)

	cmds.floatSliderGrp("horizontalOffset_floatSliderGrp", label="Horizontal Offset", field=True, min=-2.5, max=2.5, value=0, sliderStep=0.001, dragCommand=horizontalOffset_floatSliderGrp_OnValueChanged)

	cmds.floatSliderGrp("verticalOffset_floatSliderGrp", label="Vertical Offset", field=True, min=-2.5, max=2.5, value=0, sliderStep=0.001, dragCommand=verticalOffset_floatSliderGrp_OnValueChanged)

	cmds.button("resetZoomCtrls_button", label="Reset Zoom Controls", command=resetZoomControls_button_OnClicked)

	cmds.showWindow("cameraZoomControls_window")
	cmds.windowPref(enableAll=True);
	
def cameraZoomControls():
	"""
	This definition launches the 'Camera Zoom Controls' main window.
	"""

	cameraZoomControls_window()

@stacksHandler
def ICameraZoomControls():
	"""
	This definition is the cameraZoomControls definition Interface.
	"""

	cameraZoomControls()
