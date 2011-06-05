import maya.cmds as cmds

def selectStarVertices():
	'''
	This Definition Selects Star Vertices.
	'''
	
	cmds.polySelectConstraint(m=3, t=1, order=True, orb=(5, 65535))
	cmds.polySelectConstraint(dis=True)

def ISelectStarVertices():
	'''
	This Definition Is The selectStarVertices Method Interface.
	'''
	
	selectStarVertices()

def selectTrianglesFaces():
	'''
	This Definition Selects Triangles Faces.
	'''

	cmds.polySelectConstraint(m=3, t=8, sz=1)
	cmds.polySelectConstraint(dis=True)

def ISelectTrianglesFaces():
	'''
	This Definition Is The selectTrianglesFaces Method Interface.
	'''

	selectTrianglesFaces()
	
def selectNsidesFaces():
	'''
	This Definition Selects NSides Faces.
	'''
	
	cmds.polySelectConstraint(m=3, t=8, sz=3)
	cmds.polySelectConstraint(dis=True)

def ISelectNsidesFaces():
	'''
	This Definition Is The selectNsidesFaces Method Interface.
	'''

	selectNsidesFaces()
	
def selectBoundaryEdges(components):
	'''
	This Definition Selects Selection Boundaries Edges.
	'''
	
	cmds.select(cmds.polyListComponentConversion(components, te=True, bo=True))

def ISelectBoundaryEdges():
	'''
	This Definition Is The selectBoundaryEdges Method Interface.
	'''

	selection = cmds.ls(sl=True, l=True)
	selection and selectBoundaryEdges(selection)

def selectBorderEdges():
	'''
	This Definition Selects The Border Edges.
	'''
	
	cmds.polySelectConstraint(m=3, t=0x8000, w=1)
	cmds.polySelectConstraint(m=0)

def ISelectBorderEdges():
	'''
	This Definition Is The selectNsidesFaces Method Interface.
	'''

	selectBorderEdges()
	
def selectCreasesEdges(object):
	'''
	This Definition Cleans Maya Hierarchical Polygonal Conversion.

	@param object : Object To Select Creases Edges. ( String )
	'''

	edges = cmds.ls(object +".e[0:" + str(cmds.polyEvaluate(object, edge=True)-1) + "]", fl = True)
	creaseEdges = [edge for edge in edges if cmds.polyCrease(edge, q=True, v=True)[0] > 0.0]
	if creaseEdges:
		cmds.select(creaseEdges)

def ISelectCreasesEdges():
	'''
	This Definition Is The selectCreasesEdges Method Interface.
	'''
	
	selection = cmds.ls(sl=True, l=True)
	selection and selectCreasesEdges(selection[0])
