import maya.cmds as cmds
import maya.mel as mel

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacks_handler",
			"get_active_camera",
			"overscan_floatSliderGrp__on_value_changed",
			"horizontal_offset_floatSliderGrp__on_value_changed",
			"vertical_offset_floatSliderGrp__on_value_changed",
			"reset_zoom_controls_button__on_clicked",
			"camera_zoom_controls_window",
			"camera_zoom_controls"]

__interfaces__ = ["camera_zoom_controls"]

def stacks_handler(object):
	"""
	Handles Maya stacks.

	:param object: Python object.
	:type object: object
	:return: Python function.
	:rtype: object
	"""

	def stacks_handler_wrapper(*args, **kwargs):
		"""
		Handles Maya stacks.

		:return: Python object.
		:rtype: object
		"""

		cmds.undoInfo(openChunk=True)
		value = object(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya produces a weird command error if not wrapped here.
		try:
			cmds.repeatLast(addCommand="python(\"import {0}; {1}.{2}()\")".format(__name__, __name__, object.__name__), addCommandLabel=object.__name__)
		except:
			pass
		return value

	return stacks_handler_wrapper

def get_active_camera():
	"""
	Returns the current active camera.

	:return: Active camera.
	:rtype: str
	"""

	try :
		active_panel = cmds.getPanel(withFocus=True)
		active_camera = cmds.modelPanel(active_panel, query=True, camera=True)
		return active_camera
	except :
		pass

@stacks_handler
def overscan_floatSliderGrp__on_value_changed(value):
	"""
	Defines the slot triggered by 'overscan_floatSliderGrp' slider when value changed.

	:param value: Value.
	:type value: float
	"""

	active_camera = get_active_camera()
	if active_camera != None :
		current_overscan_slider_value = cmds.floatSliderGrp("overscan_floatSliderGrp", query=True, value=True)
		try :
			cmds.setAttr("{0}.overscan".format(active_camera), current_overscan_slider_value)
		except :
			print("Warning \"Current Camera \".overscan\" Attribute Is Locked !\"")

@stacks_handler
def horizontal_offset_floatSliderGrp__on_value_changed(value):
	"""
	Defines the slot triggered by 'horizontal_offset_floatSliderGrp' slider when value changed.

	:param value: Value.
	:type value: float
	"""

	active_camera = get_active_camera()
	if active_camera != None :
		current_overscan_slider_value = cmds.floatSliderGrp("horizontal_offset_floatSliderGrp", query=True, value=True)
		try :
			cmds.setAttr("{0}.horizontalFilmOffset".format(active_camera), current_overscan_slider_value)
		except :
			print("Warning \"Current Camera \".horizontalFilmOffset\" Attribute Is Locked !\"")

@stacks_handler
def vertical_offset_floatSliderGrp__on_value_changed(value):
	"""
	Defines the slot triggered by 'vertical_offset_floatSliderGrp' slider when value changed.

	:param value: Value.
	:type value: float
	"""

	active_camera = get_active_camera()
	if active_camera != None :
		current_overscan_slider_value = cmds.floatSliderGrp("vertical_offset_floatSliderGrp", query=True, value=True)
		try :
			cmds.setAttr("{0}.verticalFilmOffset".format(active_camera), current_overscan_slider_value)
		except :
			print("Warning \"Current Camera \".verticalFilmOffset\" Attribute Is Locked !\"")

@stacks_handler
def reset_zoom_controls_button__on_clicked(state=None):
	"""
	Defines the slot triggered by **reset_zoom_controls_button** button when clicked.

	:param state: Button state.
	:type state: bool
	"""

	cmds.floatSliderGrp("overscan_floatSliderGrp", edit=True, value=1)
	cmds.floatSliderGrp("horizontal_offset_floatSliderGrp", edit=True, value=0)
	cmds.floatSliderGrp("vertical_offset_floatSliderGrp", edit=True, value=0)
	active_camera = get_active_camera()
	try :
		cmds.setAttr("{0}.overscan".format(active_camera), 1)
		cmds.setAttr("{0}.horizontalFilmOffset".format(active_camera), 0)
		cmds.setAttr("{0}.verticalFilmOffset".format(active_camera), 0)
	except :
		pass

def camera_zoom_controls_window():
	"""
	Creates the 'Camera Zoom Controls' main window.
	"""

	cmds.windowPref(enableAll=False)

	if (cmds.window("camera_zoom_controls_window", exists=True)):
		cmds.deleteUI("camera_zoom_controls_window")

	cmds.window("camera_zoom_controls_window",
		title="Camera Zoom Controls",
		sizeable=True,
		width=320)

	spacing = 5

	cmds.columnLayout(adjustableColumn=True, rowSpacing=spacing)

	cmds.floatSliderGrp("overscan_floatSliderGrp", label="Overscan", field=True, min=0.01, max=2.5, value=1, sliderStep=0.001, dragCommand=overscan_floatSliderGrp__on_value_changed)

	cmds.floatSliderGrp("horizontal_offset_floatSliderGrp", label="Horizontal Offset", field=True, min= -2.5, max=2.5, value=0, sliderStep=0.001, dragCommand=horizontal_offset_floatSliderGrp__on_value_changed)

	cmds.floatSliderGrp("vertical_offset_floatSliderGrp", label="Vertical Offset", field=True, min= -2.5, max=2.5, value=0, sliderStep=0.001, dragCommand=vertical_offset_floatSliderGrp__on_value_changed)

	cmds.button("reset_zoom_controls_button", label="Reset Zoom Controls", command=reset_zoom_controls_button__on_clicked)

	cmds.showWindow("camera_zoom_controls_window")
	cmds.windowPref(enableAll=True);

def camera_zoom_controls():
	"""
	Launches the 'Camera Zoom Controls' main window.
	"""

	camera_zoom_controls_window()
