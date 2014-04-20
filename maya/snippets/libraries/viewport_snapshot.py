import maya.cmds as cmds

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacks_handler", "viewport_snapshot"]

__interfaces__ = ["viewport_snapshot"]

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

def viewport_snapshot():
	"""
	Does a viewport snapshot.
	"""

	filter = "Tif files (*.tif)"
	file = cmds.fileDialog2(fileFilter=filter, fm=0, dialogStyle=2)

	if file:
		image_format = cmds.getAttr("defaultRenderGlobals.image_format")
		cmds.setAttr("defaultRenderGlobals.image_format", 3)
		cmds.playblast(frame=[cmds.getAttr("time1.outTime")], format="image", os=True, quality=100, p=100, cf=file[0])
		cmds.setAttr("defaultRenderGlobals.image_format", image_format)
