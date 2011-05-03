# Vertex Paint Tool Massaging.
import maya.cmds as cmds
import maya.mel as mel

vtxs = [u'body.vtx[2111]', u'body.vtx[2114]', u'body.vtx[2117]', u'body.vtx[2120]', u'body.vtx[2143:2180]', u'body.vtx[2194:2208]', u'body.vtx[2211]', u'body.vtx[2216:2223]', u'body.vtx[2236:2237]', u'body.vtx[2239:2261]', u'body.vtx[2269:2299]', u'body.vtx[2302]', u'body.vtx[2305]', u'body.vtx[2308:2309]', u'body.vtx[2314:2317]', u'body.vtx[2321:2332]', u'body.vtx[2342:2353]', u'body.vtx[2355:2362]', u'body.vtx[2372:2386]', u'body.vtx[2388]', u'body.vtx[2393:2497]', u'body.vtx[2502:2513]', u'body.vtx[2518:2529]', u'body.vtx[2531:2556]', u'body.vtx[2561:2584]', u'body.vtx[2592]', u'body.vtx[2598:2624]', u'body.vtx[2630:2633]', u'body.vtx[2640:2699]', u'body.vtx[2704:2749]', u'body.vtx[2998:3001]', u'body.vtx[3003:3011]', u'body.vtx[3013:3015]', u'body.vtx[3067]', u'body.vtx[5089]', u'body.vtx[5092]', u'body.vtx[5095]', u'body.vtx[5098]', u'body.vtx[5121:5158]', u'body.vtx[5172:5186]', u'body.vtx[5189]', u'body.vtx[5194:5201]', u'body.vtx[5214:5215]', u'body.vtx[5217:5239]', u'body.vtx[5247:5277]', u'body.vtx[5280]', u'body.vtx[5283]', u'body.vtx[5286:5287]', u'body.vtx[5292:5295]', u'body.vtx[5299:5310]', u'body.vtx[5319:5330]', u'body.vtx[5332:5339]', u'body.vtx[5349:5363]', u'body.vtx[5365]', u'body.vtx[5370:5474]', u'body.vtx[5479:5490]', u'body.vtx[5495:5506]', u'body.vtx[5508:5533]', u'body.vtx[5538:5561]', u'body.vtx[5569]', u'body.vtx[5575:5601]', u'body.vtx[5607:5610]', u'body.vtx[5617:5676]', u'body.vtx[5680:5725]', u'body.vtx[5968:5971]', u'body.vtx[5973:5981]', u'body.vtx[5983:5985]', u'body.vtx[6037]', u'body.vtx[6098:6113]', u'body.vtx[6125:6156]', u'body.vtx[6168:6199]', u'body.vtx[6211:6242]', u'body.vtx[6254:6285]', u'body.vtx[6297:6328]', u'body.vtx[6340:6355]'] # 
body = cmds.ls( sl = True, l = True)[0]
cmds.polyColorPerVertex( body, r = 0, g =0, b = 0, a = 1, cdo = True )
for vtx in vtxs:
	cmds.polyColorPerVertex(vtx, r = 1, g =1, b = 1, a = 1, cdo = True )

pVtxTool = mel.eval( "artAttrColorPerVertexToolScript 4;")
cmds.artAttrPaintVertexCtx( pVtxTool, e = True, sao = "smooth" )
for i in range(5):
	cmds.artAttrPaintVertexCtx( pVtxTool, e = True, clear = True )
cmds.artAttrPaintVertexCtx( pVtxTool, e = True, exportfilesizex = 2048 )
cmds.artAttrPaintVertexCtx( pVtxTool, e = True, exportfilesizey = 2048 )
cmds.artAttrPaintVertexCtx( pVtxTool, e = True, exportfilesave = "D:\\Mask.tif" )


# Multiple Targets Vertices Positions Transfert.
import maya.cmds as cmds

def transfertVerticesPositions(source, targets, searchMethod=0):
	for target in targets:
	    cmds.transferAttributes(source, target, transferPositions=1, sampleSpace=0, searchMethod=3)
	    cmds.delete(target, ch=True)

selection = cmds.ls(sl=True, l=True)
transfertVerticesPositions(selection[0], selection[1:], 0)

# Select Boundary Edges.
def getBoundaryEdges(components):
    return cmds.polyListComponentConversion(components, te=True, bo=True)

cmds.select(getBoundaryEdges(cmds.ls(sl=True, l=True)))

import maya.cmds as cmds

for object in cmds.ls(sl=True, l=True):
	cmds.select(object)
	cmds.polySelectConstraint(m=3, t=0x8000, sm=1)
	hardEdges = cmds.ls(sl=True, l=True)
	cmds.polyBevel(hardEdges, offset=0.05, offsetAsFraction=True, autoFit=False, roundness=0, segments=1, worldSpace=True, uvAssignment=False, fillNgons=True, mergeVertices=True, mergeVertexTolerance=0.00005, smoothingAngle=30, miteringAngle=180, angleTolerance=180, ch=False)
