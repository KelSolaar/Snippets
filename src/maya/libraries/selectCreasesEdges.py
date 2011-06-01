import maya.cmds as cmds

# Select Creases Edges.
def selectCreasesEdges(object):
	'''
	This Definition Cleans Maya Hierarchical Polygonal Conversion.

	@param object : Object To Select Creases Edges. (String)
	'''
	edges = cmds.ls(object +".e[0:" + str(cmds.polyEvaluate(object, edge=True)-1) + "]", fl = True)
	creaseEdges = [edge for edge in edges if cmds.polyCrease(edge, q=True, v=True)[0] > 0.0]
	cmds.select(creaseEdges)

def ISelectCreasesEdges():
	'''
	This Definition Is The selectCreasesEdges Method Interface.
	'''

	selectCreasesEdges(cmds.ls(sl=True, l=True)[0])
