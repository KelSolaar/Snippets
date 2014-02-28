import maya.cmds as cmds

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacksHandler", "viewportSnapshot", "IViewportSnapshot"]

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

def viewportSnapshot():
	"""
	This definition does a viewport snapshot.
	"""

	filter = "Tif files (*.tif)"
	file = cmds.fileDialog2(fileFilter=filter, fm=0, dialogStyle=2)

	if file:
		imageFormat = cmds.getAttr("defaultRenderGlobals.imageFormat")
		cmds.setAttr("defaultRenderGlobals.imageFormat", 3)
		cmds.playblast(frame=[cmds.getAttr("time1.outTime")], format="image", os=True, quality=100, p=100, cf=file[0])
		cmds.setAttr("defaultRenderGlobals.imageFormat", imageFormat)

@stacksHandler
def IViewportSnapshot():
	"""
	This definition is the viewportSnapshot definition Interface.
	"""

	viewportSnapshot()
