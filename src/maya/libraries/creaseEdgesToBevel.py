import maya.cmds as cmds

def creaseEdgesToBevel(object):
    edges = cmds.ls(object +".e[0:" + str(cmds.polyEvaluate(object, edge=True)-1) + "]", fl = True)
    creaseEdges = [edge for edge in edges if cmds.polyCrease(edge, q=True, v=True)[0] > 0.0]
    cmds.select(creaseEdges)
    
def ICreaseEdgesToBevel():
	creaseEdgesToBevel(cmds.ls(sl=True, l=True)[0])
