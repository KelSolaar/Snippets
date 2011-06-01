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
	ISelectNsidesFaces()
