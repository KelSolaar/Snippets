import maya.cmds as cmds

def stacksHandler(object_):
	"""
	This Decorator Is Used To Handle Various Maya Stacks.

	@param object_: Python Object ( Object )
	@return: Python Function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This Decorator Is Used To Handle Various Maya Stacks.

		@return: Python Object. ( Python )
		"""
		
		cmds.undoInfo(openChunk=True)
		value = object_(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya Produces A Weird Command Error If Not Wrapped Here.
		try:
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")"% (__name__, __name__, object_.__name__), addCommandLabel=object_.__name__)
		except:
			pass
		return value

	return stacksHandlerCall


def viewportSnapshot():
	"""
	This Definition Does A Viewport Snapshot.
	"""

	filter = "Tif Files (*.tif)"
	file = cmds.fileDialog2(fileFilter=filter, fm=0, dialogStyle=2)
    
	if file:
		imageFormat = cmds.getAttr("defaultRenderGlobals.imageFormat")
		cmds.setAttr("defaultRenderGlobals.imageFormat", 3)
		cmds.playblast(frame=[1], format="image", os=True, quality=100, p=100, cf=file[0])
		cmds.setAttr("defaultRenderGlobals.imageFormat", imageFormat)

@stacksHandler
def IViewportSnapshot():
	"""
	This Definition Is The viewportSnapshot Method Interface.
	"""

	viewportSnapshot()
