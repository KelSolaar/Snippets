import maya.cmds as cmds

# Select Star Vertices.
def selectStarVertices():
	cmds.polySelectConstraint(m=3, t=1, order=True, orb=(5, 65535))
	cmds.polySelectConstraint(dis=True)

def ISelectStarVertices():
	selectStarVertices()

# Select Triangles Faces.
def selectTrianglesFaces():
	cmds.polySelectConstraint(m=3, t=8, sz=1)
	cmds.polySelectConstraint(dis=True)

def ISelectTrianglesFaces():
	selectTrianglesFaces()
	
# Select NSides Faces.
def selectNsidesFaces():
	cmds.polySelectConstraint(m=3, t=8, sz=3)
	cmds.polySelectConstraint(dis=True)

def ISelectNsidesFaces():
	selectNsidesFaces()
	
# Select Boundary Edges.
def selectBoundaryEdges(components):
	cmds.select(cmds.polyListComponentConversion(components, te=True, bo=True))

def ISelectBoundaryEdges():
	selectBoundaryEdges(cmds.ls(sl=True, l=True))

# Select Border Edges.
def selectBorderEdges():
	cmds.polySelectConstraint(m=3, t=0x8000, w=1)
	cmds.polySelectConstraint(m=0)

def ISelectBorderEdges():
	selectBorderEdges()
	
# Select Creases Edges.
def selectCreasesEdges(object):
	'''
	This Definition Cleans Maya Hierarchical Polygonal Conversion.

	@param object : Object To Select Creases Edges. (String)
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
