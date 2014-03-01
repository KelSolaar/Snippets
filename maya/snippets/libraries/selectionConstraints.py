import maya.cmds as cmds
import operator

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacksHandler",
			"selectStarVertices",
			"ISelectStarVertices",
			"selectTrianglesFaces",
			"ISelectTrianglesFaces",
			"selectNsidesFaces",
			"ISelectNsidesFaces",
			"selectBoundaryEdges",
			"ISelectBoundaryEdges",
			"selectBorderEdges",
			"ISelectBorderEdges",
			"selectCreasesEdges",
			"ISelectCreasesEdges",
			"selectHardEdges",
			"ISelectHardEdges",
			"selectNonManifoldVertices",
			"ISelectNonManifoldVertices",
			"selectIsolatedVertices",
			"ISelectIsolatedVertices",
			"selectLaminaFaces",
			"ISelectLaminaFaces",
			"selectZeroGeometryAreaFaces",
			"ISelectZeroGeometryAreaFaces",
			"selectSideVertices",
			"selectLeftVertices",
			"ISelectLeftVertices",
			"selectRightVertices",
			"ISelectRightVertices"]

def stacksHandler(object):
	"""
	Handles Maya stacks.

	:param object: Python object. ( Object )
	:return: Python function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		Handles Maya stacks.

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

def selectStarVertices():
	"""
	Selects star vertices.
	"""

	cmds.polySelectConstraint(m=3, t=1, order=True, orb=(5, 65535))
	cmds.polySelectConstraint(dis=True)

@stacksHandler
def ISelectStarVertices():
	"""
	Defines the selectStarVertices definition Interface.
	"""

	selectStarVertices()

def selectTrianglesFaces():
	"""
	Selects triangles faces.
	"""

	cmds.polySelectConstraint(m=3, t=8, sz=1)
	cmds.polySelectConstraint(dis=True)

@stacksHandler
def ISelectTrianglesFaces():
	"""
	Defines the selectTrianglesFaces definition Interface.
	"""

	selectTrianglesFaces()

def selectNsidesFaces():
	"""
	Selects nsides faces.
	"""

	cmds.polySelectConstraint(m=3, t=8, sz=3)
	cmds.polySelectConstraint(dis=True)

@stacksHandler
def ISelectNsidesFaces():
	"""
	Defines the selectNsidesFaces definition Interface.
	"""

	selectNsidesFaces()

def selectBoundaryEdges(components):
	"""
	Selects selection boundaries edges.
	"""

	cmds.select(cmds.polyListComponentConversion(components, te=True, bo=True))

@stacksHandler
def ISelectBoundaryEdges():
	"""
	Defines the selectBoundaryEdges definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and selectBoundaryEdges(selection)

def selectBorderEdges():
	"""
	Selects the border edges.
	"""

	cmds.polySelectConstraint(m=3, t=0x8000, w=1)
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectBorderEdges():
	"""
	Defines the selectBorderEdges definition Interface.
	"""

	selectBorderEdges()

def selectCreasesEdges(object):
	"""
	Cleans Maya hierarchical polygonal conversion.

	:param object: Object to select creases edges. ( String )
	"""

	edges = cmds.ls(object + ".e[0:" + str(cmds.polyEvaluate(object, edge=True) - 1) + "]", fl=True)
	creaseEdges = [edge for edge in edges if cmds.polyCrease(edge, q=True, v=True)[0] > 0.0]
	if creaseEdges:
		cmds.select(creaseEdges)

@stacksHandler
def ISelectCreasesEdges():
	"""
	Defines the selectCreasesEdges definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and selectCreasesEdges(selection[0])

def selectHardEdges():
	"""
	Selects the hard edges.
	"""

	cmds.polySelectConstraint(m=3, t=0x8000, sm=1)
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectHardEdges():
	"""
	Defines the selectHardEdges definition Interface.
	"""

	selectHardEdges()

def selectNonManifoldVertices():
	"""
	Selects the non manifold vertices.
	"""

	cmds.polySelectConstraint(m=3, t=1, nonmanifold=True)
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectNonManifoldVertices():
	"""
	Defines the selectNonManifoldVertices definition Interface.
	"""

	selectNonManifoldVertices()

def selectIsolatedVertices(components):
	"""
	Selects the isolated vertices.
	"""

	cmds.select(cl=True)
	isolatedVertices = []
	vertices = cmds.ls(cmds.polyListComponentConversion(components, toVertex=True), fl=True)
	for vertex in vertices:
		edges = cmds.ls(cmds.polyListComponentConversion(vertex, toEdge=True), flatten=True)
		if len(edges) == 2:
			if len(cmds.ls(cmds.polyListComponentConversion(edges, toFace=True), flatten=True)) == 1:
				continue

			isolatedVertices.append(vertex)
	isolatedVertices and cmds.select(isolatedVertices)

@stacksHandler
def ISelectIsolatedVertices():
	"""
	Defines the selectIsolatedVertices definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and selectIsolatedVertices(selection)

def selectLaminaFaces():
	"""
	Selects the lamina faces.
	"""

	cmds.polySelectConstraint(m=3, t=8, tp=2)
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectLaminaFaces():
	"""
	Defines the selectLaminaFaces definition Interface.
	"""

	selectLaminaFaces()

def selectZeroGeometryAreaFaces():
	"""
	Selects the zero geometry area faces.
	"""

	cmds.polySelectConstraint(m=3, t=8, ga=True, gab=(0, 0.001))
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectZeroGeometryAreaFaces():
	"""
	Defines the selectZeroGeometryAreaFaces definition Interface.
	"""

	selectZeroGeometryAreaFaces()

def selectSideVertices(object, positive=True):
	"""
	Selects given side geometry vertices.
	
	:param object: Object to select vertices. ( String )
	:param positive: Select positive vertices. ( Boolean )
	"""

	comparison = positive and operator.gt or operator.lt
	verticesCount = cmds.polyEvaluate(object, vertex=True)
	vertices = cmds.ls(object + ".vtx[0:{0}]".format(str(verticesCount - 1)), fl=True, l=True)
	cmds.select(filter(lambda x: comparison(cmds.xform(x, q=True, t=True, ws=True)[0], 0), vertices))

def selectLeftVertices(object):
	"""
	Selects left side geometry vertices.
	
	:param object: Object to select left vertices. ( String )
	"""

	selectSideVertices(object)

@stacksHandler
def ISelectLeftVertices():
	"""
	Defines the selectLeftVertices definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and selectLeftVertices(selection[0])

def selectRightVertices(object):
	"""
	Selects right side geometry vertices.
	
	:param object: Object to select right vertices. ( String )
	"""

	selectSideVertices(object, positive=False)

@stacksHandler
def ISelectRightVertices():
	"""
	Defines the selectRightVertices definition Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and selectRightVertices(selection[0])
