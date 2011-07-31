import maya.cmds as cmds

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

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
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")"% (__name__, __name__, object.__name__), addCommandLabel=object.__name__)
		except:
			pass
		return value

	return stacksHandlerCall

@stacksHandler
def cleanupHierarchicalSubdivisionConversion(object):
	"""
	This definition cleans Maya hierarchical polygonal conversion.

	:param object: Object to cleanup. ( String )
	"""

	cmds.select(object)
	cmds.polySelectConstraint(m=3, t=8, sz=3)
	cmds.polySelectConstraint(dis=True)
	nsidesFaces = cmds.ls(sl=True, l=True, fl=True)
	cmds.select(nsidesFaces)
	cmds.polySelectConstraint(m=3, t=1, order=True, orb=(3, 3))
	cmds.polySelectConstraint(dis=True)
	nsideVertices = cmds.ls(sl=True, l=True, fl=True)
	offendingEdges = []
	for vertice in nsideVertices:
		faces = cmds.ls(cmds.polyListComponentConversion(vertice, fv=True, tf=True), fl=True, l=True)
		faces = [face for face in faces if not face in nsidesFaces]
		if len(faces) == 2:
			faceEdgesA = cmds.ls(cmds.polyListComponentConversion(faces[0], ff=True, te=True), fl=True, l=True)
			faceEdgesB = cmds.ls(cmds.polyListComponentConversion(faces[1], ff=True, te=True), fl=True, l=True)
			sharedEdge = list(set(faceEdgesA).intersection(faceEdgesB))
			offendingEdges.append(sharedEdge[0])
	cmds.polySelectSp(offendingEdges, loop=True)
	cmds.polyDelEdge(cmds.ls(sl=True), cv=True, ch=True)
	cmds.select(object)

def ICleanupHierarchicalSubdivisionConversion():
	"""
	This definition is the cleanupHierarchicalSubdivisionConversion definition Interface.
	"""

	for object in cmds.ls(sl=True, l=True):
		cleanupHierarchicalSubdivisionConversion(object)
