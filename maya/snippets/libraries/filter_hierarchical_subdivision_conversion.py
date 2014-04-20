import maya.cmds as cmds

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["stacks_handler",
           "filter_hierarchical_subdivision_conversion",
           "filter_selected_hierarchical_subdivision_conversion_objects"]

__interfaces__ = ["filter_selected_hierarchical_subdivision_conversion_objects"]

def stacks_handler(object):
	"""
	Handles Maya stacks.

	:param object: Python object.
	:type object: object
	:return: Python function.
	:rtype: object
	"""

	def stacks_handler_wrapper(*args, **kwargs):
		"""
		Handles Maya stacks.

		:return: Python object.
		:rtype: object
		"""

		cmds.undoInfo(openChunk=True)
		value = object(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya produces a weird command error if not wrapped here.
		try:
			cmds.repeatLast(addCommand="python(\"import {0}; {1}.{2}()\")".format(__name__, __name__, object.__name__), addCommandLabel=object.__name__)
		except:
			pass
		return value

	return stacks_handler_wrapper

@stacks_handler
def filter_hierarchical_subdivision_conversion(object):
	"""
	Filters hierarchical subdivision conversion to polygons.

	:param object: Object to filter.
	:type object: unicode
	"""

	cmds.select(object)
	cmds.polySelectConstraint(m=3, t=8, sz=3)
	cmds.polySelectConstraint(dis=True)
	nsides_faces = cmds.ls(sl=True, l=True, fl=True)
	cmds.select(nsides_faces)
	cmds.polySelectConstraint(m=3, t=1, order=True, orb=(3, 3))
	cmds.polySelectConstraint(dis=True)
	nside_vertices = cmds.ls(sl=True, l=True, fl=True)
	offending_edges = []
	for vertice in nside_vertices:
		faces = cmds.ls(cmds.polyListComponentConversion(vertice, fv=True, tf=True), fl=True, l=True)
		faces = [face for face in faces if not face in nsides_faces]
		if len(faces) == 2:
			face_edges_a = cmds.ls(cmds.polyListComponentConversion(faces[0], ff=True, te=True), fl=True, l=True)
			face_edges_b = cmds.ls(cmds.polyListComponentConversion(faces[1], ff=True, te=True), fl=True, l=True)
			shared_edge = list(set(face_edges_a).intersection(face_edges_b))
			offending_edges.append(shared_edge[0])
	cmds.polySelectSp(offending_edges, loop=True)
	cmds.polyDelEdge(cmds.ls(sl=True), cv=True, ch=True)
	cmds.select(object)

@stacks_handler
def filter_selected_hierarchical_subdivision_conversion_objects():
	"""
	Filters selectied hierarchical subdivision conversion objects to polygons.
	"""

	for object in cmds.ls(sl=True, l=True):
		filter_hierarchical_subdivision_conversion(object)
