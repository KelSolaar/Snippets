# Select Star Vertices.
import maya.cmds as cmds
cmds.polySelectConstraint(m=3, t=1, order=True, orb=(5, 65535))
cmds.polySelectConstraint(dis=True)

# Select Triangles Faces.
import maya.cmds as cmds
cmds.polySelectConstraint(m=3, t=8, sz=1)
cmds.polySelectConstraint(dis=True)

# Select NSides Faces.
import maya.cmds as cmds
cmds.polySelectConstraint(m=3, t=8, sz=3)
cmds.polySelectConstraint(dis=True)