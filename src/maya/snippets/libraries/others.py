import maya.cmds as cmds
import maya.mel as mel

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

def transfertVerticesPositionsInUvSpace(sources, target, searchMethod=0):
	"""
	This Definition Transferts Vertices Positions From Sources To Target Object In UVs Space.

	@param sources: Sources Objects. ( List )
	@param target: Target Object. ( String )
	@param searchMethod: Current Search Method. ( Integer )
	"""

	for source in sources:
	    cmds.transferAttributes(target, source, transferPositions=1, sampleSpace=3)
	    cmds.delete(target, ch=True)

@stacksHandler
def ITransfertVerticesPositionsInUvSpace():
	"""
	This Definition Is The transfertVerticesPositions Method Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and transfertVerticesPositionsInUvSpace(selection[:-1], selection[-1], 0)

def transfertVerticesPositionsInWorldSpace(sources, target, searchMethod=0):
	"""
	This Definition Transferts Vertices Positions From Sources To Target Object In World Space.

	@param sources: Sources Objects. ( List )
	@param target: Target Object. ( String )
	@param searchMethod: Current Search Method. ( Integer )
	"""

	for source in sources:
	    cmds.transferAttributes(target, source, transferPositions=1, sampleSpace=0, searchMethod=3)
	    cmds.delete(target, ch=True)

@stacksHandler
def ITransfertVerticesPositionsInWorldSpace():
	"""
	This Definition Is The transfertVerticesPositions Method Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	selection and transfertVerticesPositionsInWorldSpace(selection[:-1], selection[-1], 0)

def toggleSelectionHighlight():
	"""
	This Definition Toggles Active Modeling Panel Selection Highlight.
	"""

	panel = cmds.getPanel(withFocus=True)
	try:
		cmds.modelEditor(panel, e=True, sel=not cmds.modelEditor(panel, q=True, sel=True))
	except:
		pass
@stacksHandler
def IToggleSelectionHighlight():
	"""
	This Definition Is The toggleSelectionHighlight Method Interface.
	"""

	toggleSelectionHighlight()

def toggleGeometriesVisibility():
	'''
	This Definition Toggles Active Modeling Panel Geometries Visibility Highlight.
	'''

	panel = cmds.getPanel(withFocus=True)
	try:
		cmds.modelEditor(panel, e=True, nurbsCurves=not cmds.modelEditor(panel, q=True, nurbsCurves=True))
		cmds.modelEditor(panel, e=True, nurbsSurfaces=not cmds.modelEditor(panel, q=True, nurbsSurfaces=True))
		cmds.modelEditor(panel, e=True, polymeshes=not cmds.modelEditor(panel, q=True, polymeshes=True))
		cmds.modelEditor(panel, e=True, subdivSurfaces=not cmds.modelEditor(panel, q=True, subdivSurfaces=True))
	except:
		pass
@stacksHandler
def IToggleGeometriesVisibility():
	'''
	This Definition Is The toggleGeometriesVisibility Method Interface.
	'''

	toggleGeometriesVisibility()

def splitRingMiddle(nodes):
	"""
	This Definition Sets The polySplitRing Nodes Weights To 0.5.

	@param nodes: Nodes To Retrieve History From. ( List )
	"""

	for node in nodes:
		for historyNode in cmds.listHistory(node):
			if cmds.nodeType(historyNode) == "polySplitRing":
				cmds.setAttr(historyNode + ".weight", 0.5)

@stacksHandler
def ISplitRingMiddle():
	"""
	This Definition Is The splitRingMiddle Method Interface.
	"""

	selection = cmds.ls(sl=True, l=True)
	splitRingMiddle(selection)

def symmetricalInstance(object):
	"""
	This Definition Creates A Symmetrical Instance.

	@param object: Object To Symmetrical Instantiate. ( String )
	"""

	instance = cmds.instance(object)
	cmds.setAttr(object + ".sx", -1)

@stacksHandler
def ISymmetricalInstance():
	"""
	This Definition Is The symmetricalInstance Method Interface.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	for object in selection:
		symmetricalInstance(object)


def pivotsIdentity(transforms):
	"""
	This Definition Puts Provided Transforms Pivots To Origin.

	@param transforms: Transforms To Affect Pivots. ( List )
	"""


	for transform in transforms:
		try:
			for pivotType in ("scalePivot", "rotatePivot"):
				cmds.move( 0, 0, 0, transform + "." + pivotType)
		except:
			pass
@stacksHandler
def IPivotsIdentity():
	"""
	This Definition Is The pivotsIdentity Method Interface.
	"""

	selection = cmds.ls(sl=True, l=True, type="transform")
	selection and pivotsIdentity(selection)

# Vertex Paint Tool Massaging.
# def vertexPaintToolMassaging():
# 	vtxs = [u'body.vtx[2111]', u'body.vtx[2114]', u'body.vtx[2117]', u'body.vtx[2120]', u'body.vtx[2143:2180]', u'body.vtx[2194:2208]', u'body.vtx[2211]', u'body.vtx[2216:2223]', u'body.vtx[2236:2237]', u'body.vtx[2239:2261]', u'body.vtx[2269:2299]', u'body.vtx[2302]', u'body.vtx[2305]', u'body.vtx[2308:2309]', u'body.vtx[2314:2317]', u'body.vtx[2321:2332]', u'body.vtx[2342:2353]', u'body.vtx[2355:2362]', u'body.vtx[2372:2386]', u'body.vtx[2388]', u'body.vtx[2393:2497]', u'body.vtx[2502:2513]', u'body.vtx[2518:2529]', u'body.vtx[2531:2556]', u'body.vtx[2561:2584]', u'body.vtx[2592]', u'body.vtx[2598:2624]', u'body.vtx[2630:2633]', u'body.vtx[2640:2699]', u'body.vtx[2704:2749]', u'body.vtx[2998:3001]', u'body.vtx[3003:3011]', u'body.vtx[3013:3015]', u'body.vtx[3067]', u'body.vtx[5089]', u'body.vtx[5092]', u'body.vtx[5095]', u'body.vtx[5098]', u'body.vtx[5121:5158]', u'body.vtx[5172:5186]', u'body.vtx[5189]', u'body.vtx[5194:5201]', u'body.vtx[5214:5215]', u'body.vtx[5217:5239]', u'body.vtx[5247:5277]', u'body.vtx[5280]', u'body.vtx[5283]', u'body.vtx[5286:5287]', u'body.vtx[5292:5295]', u'body.vtx[5299:5310]', u'body.vtx[5319:5330]', u'body.vtx[5332:5339]', u'body.vtx[5349:5363]', u'body.vtx[5365]', u'body.vtx[5370:5474]', u'body.vtx[5479:5490]', u'body.vtx[5495:5506]', u'body.vtx[5508:5533]', u'body.vtx[5538:5561]', u'body.vtx[5569]', u'body.vtx[5575:5601]', u'body.vtx[5607:5610]', u'body.vtx[5617:5676]', u'body.vtx[5680:5725]', u'body.vtx[5968:5971]', u'body.vtx[5973:5981]', u'body.vtx[5983:5985]', u'body.vtx[6037]', u'body.vtx[6098:6113]', u'body.vtx[6125:6156]', u'body.vtx[6168:6199]', u'body.vtx[6211:6242]', u'body.vtx[6254:6285]', u'body.vtx[6297:6328]', u'body.vtx[6340:6355]'] #
# 	body = cmds.ls( sl = True, l = True)[0]
# 	cmds.polyColorPerVertex( body, r = 0, g =0, b = 0, a = 1, cdo = True )
# 	for vtx in vtxs:
# 		cmds.polyColorPerVertex(vtx, r = 1, g =1, b = 1, a = 1, cdo = True )
#
# 	pVtxTool = mel.eval( "artAttrColorPerVertexToolScript 4;")
# 	cmds.artAttrPaintVertexCtx( pVtxTool, e = True, sao = "smooth" )
# 	for i in range(5):
# 		cmds.artAttrPaintVertexCtx( pVtxTool, e = True, clear = True )
# 	cmds.artAttrPaintVertexCtx( pVtxTool, e = True, exportfilesizex = 2048 )
# 	cmds.artAttrPaintVertexCtx( pVtxTool, e = True, exportfilesizey = 2048 )
# 	cmds.artAttrPaintVertexCtx( pVtxTool, e = True, exportfilesave = "D:\\Mask.tif" )
