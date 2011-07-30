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

	@param object: Python object. ( Object )
	@return: Python function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This decorator is used to handle various Maya stacks.

		@return: Python object. ( Python )
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

def selectStarVertices():
	"""
	This definition selects star vertices.
	"""

	cmds.polySelectConstraint(m=3, t=1, order=True, orb=(5, 65535))
	cmds.polySelectConstraint(dis=True)

@stacksHandler
def ISelectStarVertices():
	"""
	This definition is the selectStarVertices definition Interface.
	"""

	selectStarVertices()

def selectTrianglesFaces():
	"""
	This definition selects triangles faces.
	"""

	cmds.polySelectConstraint(m=3, t=8, sz=1)
	cmds.polySelectConstraint(dis=True)

@stacksHandler
def ISelectTrianglesFaces():
	"""
	This definition is the selectTrianglesFaces definition Interface.
	"""

	selectTrianglesFaces()

def selectNsidesFaces():
	"""
	This definition selects nsides faces.
	"""

	cmds.polySelectConstraint(m=3, t=8, sz=3)
	cmds.polySelectConstraint(dis=True)

@stacksHandler
def ISelectNsidesFaces():
	"""
	This definition is the selectNsidesFaces definition Interface.
	"""

	selectNsidesFaces()

def selectBoundaryEdges(components):
	"""
	This definition selects selection boundaries edges.
	"""

	cmds.select(cmds.polyListComponentConversion(components, te=True, bo=True))

@stacksHandler
def ISelectBoundaryEdges():
	"""
	This definition is the selectBoundaryEdges definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and selectBoundaryEdges(selection)

def selectBorderEdges():
	"""
	This definition selects the border edges.
	"""

	cmds.polySelectConstraint(m=3, t=0x8000, w=1)
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectBorderEdges():
	"""
	This definition is the selectBorderEdges definition Interface.
	"""

	selectBorderEdges()

def selectCreasesEdges(object):
	"""
	This definition cleans Maya hierarchical polygonal conversion.

	@param object : Object to select creases edges. ( String )
	"""

	edges = cmds.ls(object +".e[0:" + str(cmds.polyEvaluate(object, edge=True)-1) + "]", fl = True)
	creaseEdges = [edge for edge in edges if cmds.polyCrease(edge, q=True, v=True)[0] > 0.0]
	if creaseEdges:
		cmds.select(creaseEdges)

@stacksHandler
def ISelectCreasesEdges():
	"""
	This definition is the selectCreasesEdges definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and selectCreasesEdges(selection[0])

def selectHardEdges():
	"""
	This definition selects the hard edges.
	"""

	cmds.polySelectConstraint(m=3, t=0x8000, sm=1)
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectHardEdges():
	"""
	This definition is the selectHardEdges definition Interface.
	"""

	selectHardEdges()

def selectNonManifoldVertices():
	"""
	This definition selects the non manifold vertices.
	"""

	cmds.polySelectConstraint(m=3, t=1, nonmanifold=True)
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectNonManifoldVertices():
	"""
	This definition is the selectNonManifoldVertices definition Interface.
	"""

	selectNonManifoldVertices()

def selectLaminaFaces():
	"""
	This definition selects the lamina faces.
	"""

	cmds.polySelectConstraint(m=3, t=8, tp=2)
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectLaminaFaces():
	"""
	This definition is the selectLaminaFaces definition Interface.
	"""

	selectLaminaFaces()

def selectZeroGeometryAreaFaces():
	"""
	This definition selects the zero geometry area faces.
	"""

	cmds.polySelectConstraint(m=3, t=8, ga=True, gab=(0, 0.001))
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectZeroGeometryAreaFaces():
	"""
	This definition is the selectZeroGeometryAreaFaces definition Interface.
	"""

	selectZeroGeometryAreaFaces()
