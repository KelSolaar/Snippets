import maya.cmds as cmds

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

def selectStarVertices():
	"""
	This Definition Selects Star Vertices.
	"""

	cmds.polySelectConstraint(m=3, t=1, order=True, orb=(5, 65535))
	cmds.polySelectConstraint(dis=True)

@stacksHandler
def ISelectStarVertices():
	"""
	This Definition Is The selectStarVertices Method Interface.
	"""

	selectStarVertices()

def selectTrianglesFaces():
	"""
	This Definition Selects Triangles Faces.
	"""

	cmds.polySelectConstraint(m=3, t=8, sz=1)
	cmds.polySelectConstraint(dis=True)

@stacksHandler
def ISelectTrianglesFaces():
	"""
	This Definition Is The selectTrianglesFaces Method Interface.
	"""

	selectTrianglesFaces()

def selectNsidesFaces():
	"""
	This Definition Selects NSides Faces.
	"""

	cmds.polySelectConstraint(m=3, t=8, sz=3)
	cmds.polySelectConstraint(dis=True)

@stacksHandler
def ISelectNsidesFaces():
	"""
	This Definition Is The selectNsidesFaces Method Interface.
	"""

	selectNsidesFaces()

def selectBoundaryEdges(components):
	"""
	This Definition Selects Selection Boundaries Edges.
	"""

	cmds.select(cmds.polyListComponentConversion(components, te=True, bo=True))

@stacksHandler
def ISelectBoundaryEdges():
	"""
	This Definition Is The selectBoundaryEdges Method Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and selectBoundaryEdges(selection)

def selectBorderEdges():
	"""
	This Definition Selects The Border Edges.
	"""

	cmds.polySelectConstraint(m=3, t=0x8000, w=1)
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectBorderEdges():
	"""
	This Definition Is The selectNsidesFaces Method Interface.
	"""

	selectBorderEdges()

def selectCreasesEdges(object):
	"""
	This Definition Cleans Maya Hierarchical Polygonal Conversion.

	@param object : Object To Select Creases Edges. ( String )
	"""

	edges = cmds.ls(object +".e[0:" + str(cmds.polyEvaluate(object, edge=True)-1) + "]", fl = True)
	creaseEdges = [edge for edge in edges if cmds.polyCrease(edge, q=True, v=True)[0] > 0.0]
	if creaseEdges:
		cmds.select(creaseEdges)

@stacksHandler
def ISelectCreasesEdges():
	"""
	This Definition Is The selectCreasesEdges Method Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and selectCreasesEdges(selection[0])

def selectNonManifoldVertices():
	"""
	This Definition Selects The Non Manifold Vertices.
	"""

	cmds.polySelectConstraint(m=3, t=1, nonmanifold=True)
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectNonManifoldVertices():
	"""
	This Definition Is The selectNonManifoldVertices Method Interface.
	"""

	selectNonManifoldVertices()

def selectLaminaFaces():
	"""
	This Definition Selects The Lamina Faces.
	"""

	cmds.polySelectConstraint(m=3, t=8, tp=2)
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectLaminaFaces():
	"""
	This Definition Is The selectLaminaFaces Method Interface.
	"""

	selectLaminaFaces()

def selectZeroGeometryAreaFaces():
	"""
	This Definition Selects The Zero Geometry Area Faces.
	"""

	cmds.polySelectConstraint(m=3, t=8, ga=True, gab=(0, 0.001))
	cmds.polySelectConstraint(m=0)

@stacksHandler
def ISelectZeroGeometryAreaFaces():
	"""
	This Definition Is The selectZeroGeometryAreaFaces Method Interface.
	"""

	selectZeroGeometryAreaFaces()
