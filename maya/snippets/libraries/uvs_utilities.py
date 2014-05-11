# Uvs area calculation code by Naughty Nathan: http://forums.cgsociety.org/showpost.php?p=6522248&postcount=4
import math
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import os
import pprint
import re

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RESOURCES_DIRECTORY",
           "CHECKER_IMAGE",
           "DEFAULT_SCALE_COVERAGE",
           "MARI_NAME_FORMAT",
           "stacks_handler",
           "anchor_selection",
           "get_first_item",
           "get_shapes",
           "get_node",
           "is_geometry",
           "get_connections",
           "get_attached_shaders",
           "get_uvs_from_components",
           "get_faces_per_patches",
           "get_object_uvs_area",
           "get_component_uv_dims",
           "get_mari_patch_from_uv_dims",
           "get_components_uv_dims",
           "get_components_mari_patches",
           "get_components_occupation_as_uv_dims",
           "get_components_occupation_as_mari_patches",
           "print_components_occupation_as_uv_dims",
           "print_components_occupation_as_mari_patches",
           "get_components_bounding_box",
           "get_components_uvs_center",
           "print_components_uvs_center_as_uv_dims",
           "print_components_uvs_center_as_mari_patch",
           "scale_components_uvs",
           "center_components_uvs",
           "scale_center_components_uvs",
           "rotate_components_uvs",
           "move_components_uvs",
           "mirror_components_uvs",
           "stack_objects_uvs",
           "prescale_uvs_shells",
           "auto_ratio_uvs_areas",
           "add_uvs_checker",
           "remove_uvs_checker",
           "set_uvs_checker_repeats",
           "get_patch_shader_tree",
           "assign_mari_shadersToObject",
           "assign_mari_shaders",
           "get_mari_affixes",
           "get_preview_mari_textures_branches",
           "assign_mari_preview_textures",
           "flip_uvs_button__on_clicked",
           "move_up_uvs_button__on_clicked",
           "flop_uvs_button__on_clicked",
           "move_left_uvs_button__on_clicked",
           "fit_uvs_button__on_clicked",
           "move_right_uvs_button__on_clicked",
           "center_uvs_button__on_clicked",
           "move_down_uvs_button__on_clicked",
           "scale_uvs_button__on_clicked",
           "rotate_counter_clock_wise_uvs_button__on_clicked",
           "rotate_clock_wise_uvs_button__on_clicked",
           "stack_uvs_on_u_bottom_button__on_clicked",
           "stack_uvs_on_u_center_button__on_clicked",
           "stack_uvs_on_u_top_button__on_clicked",
           "stack_uvs_on_v_left_button__on_clicked",
           "stack_uvs_on_v_center_button__on_clicked",
           "stack_uvs_on_v_right_button__on_clicked",
           "auto_ratio_uvs_areas_button__on_clicked",
           "add_uvs_checker_button__on_clicked",
           "remove_uvs_checker_button__on_clicked",
           "u_repeat_float_field__on_changed",
           "v_repeat_float_field__on_changed",
           "unfolding_tools_window",
           "unfolding_tools"]

__interfaces__ = ["print_components_occupation_as_uv_dims",
                  "print_components_occupation_as_mari_patches",
                  "print_components_uvs_center_as_uv_dims",
                  "print_components_uvs_center_as_mari_patch",
                  "assign_mari_shaders_on_selected_objects",
                  "assign_mari_preview_textures",
                  "unfolding_tools"]

RESOURCES_DIRECTORY = os.path.join(os.path.dirname("__file__" in locals() and __file__ or ""), "../resources")
CHECKER_IMAGE = "images/Checker.jpg"

DEFAULT_SCALE_COVERAGE = 0.98

MARI_NAME_FORMAT = "_%s"


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
            cmds.repeatLast(addCommand="python(\"import {0}; {1}.{2}()\")".format(
                __name__, __name__, object.__name__), addCommandLabel=object.__name__)
        except:
            pass
        return value

    return stacks_handler_wrapper


def anchor_selection(object):
    """
    Anchors current selection.

    :param object: Python object.
    :type object: object
    :return: Python function.
    :rtype: object
    """

    def function(*args, **kwargs):
        """
        Anchors current selection.

        :return: Python object.
        :rtype: object
        """

        selection = cmds.ls(sl=True, l=True)
        value = object(*args, **kwargs)
        cmds.select(selection)
        return value

    return function


def get_first_item(iterable, default=None):
    """
    Returns the first item of given iterable.

    :param iterable: Iterable.
    :type iterable: object
    :param default: Default value.
    :type default: object
    :return: First iterable item.
    :rtype: object
    """

    if not iterable:
        return default

    for item in iterable:
        return item


def get_shapes(object, full_path=False, no_intermediate=True):
    """
    Returns shapes of the given object.

    :param object: Current object.
    :type object: str
    :param full_path: Current full path state.
    :type full_path: bool
    :param noIntermediate: Current no intermediate state.
    :type noIntermediate: bool
    :return: Objects shapes.
    :rtype: list
    """

    object_shapes = []
    shapes = cmds.listRelatives(object, fullPath=full_path, shapes=True, noIntermediate=no_intermediate)
    if shapes != None:
        object_shapes = shapes

    return object_shapes


def get_node(node):
    """
    Returns given node if it exists or **None**.

    :param node: Current node to retrun.
    :type node: str
    :return: Node.
    :rtype: str
    """

    try:
        return cmds.ls(node, l=True)[0]
    except:
        pass


def is_geometry(object):
    """
    Returns if a node is a geometry.

    :param object: Current object to check.
    :type object: str
    :return: Geometry object state.
    :rtype: bool
    """

    if cmds.nodeType(object) == "mesh" or cmds.nodeType(object) == "nurbsSurface" or cmds.nodeType(object) == "subdiv":
        return True
    else:
        return False


def get_connections(node):
    """
    Returns the connections of given node.

    :param node: Node.
    :type node: str
    :return: Connections.
    :rtype: list
    """

    connections = cmds.listConnections(node, c=True)
    return [(connections[i + 1], connections[i]) for i in range(0, len(connections), 2)]


def get_attached_shaders(object):
    """
    Returns the shaders attached to given objects.

    :param object: Current object.
    :type object: str
    :return: Attached shaders.
    :rtype: list
    """

    shape = get_first_item(get_shapes(object))
    if not shape:
        return tuple()

    shading_engine = get_first_item(cmds.listConnections(shape, t="shadingEngine"))
    if not shading_engine:
        return tuple()

    shader = get_first_item(filter(lambda x: re.search("\.surfaceShader$", x[1]), get_connections(shading_engine)))
    if not shader:
        return tuple()

    return (get_first_item(shader),)


def get_uvs_from_components(components, flatten=True):
    """
    Returns the uvs from given components.

    :param components: Components.
    :type components: list
    :param flatten: Flatten components list.
    :type flatten: bool
    :return: Components Uvs.
    :rtype: list
    """

    pattern = re.compile(r"map\[\d+\]")
    for component in components:
        if not re.search(pattern, component):
            return cmds.ls(cmds.polyListComponentConversion(components, toUV=True), fl=flatten)
    return components


def get_faces_per_patches(object):
    """
    Returns the faces per patches from given object.

    :param object: Object.
    :type object: str
    :return: Faces per patches.
    :rtype: dict
    """

    faces = cmds.ls("%s.f[0:%s]" % (object, cmds.polyEvaluate(object, face=True)), fl=True)
    faces_per_patches = {}
    for face in faces:
        map, patch = get_components_mari_patches(face)[0]
        if not patch in faces_per_patches:
            faces_per_patches[patch] = [face]
            continue

        faces_per_patches[patch].append(face)
    return faces_per_patches


def get_object_uvs_area(object):
    """
    Returns given object Uvs area.

    :param object: Object to retrieve Uvs area.
    :type object: str
    :return: Uvs area.
    :rtype: int
    """

    mselection_list = OpenMaya.MSelectionList()
    mselection_list.add(object)
    mselection_listIterator = OpenMaya.MItSelectionList(mselection_list)
    mdag_path = OpenMaya.MDagPath()
    mselection_listIterator.getDagPath(mdag_path, OpenMaya.MObject())
    mesh_polygon_iterator = OpenMaya.MItMeshPolygon(mdag_path)
    mscript_util = OpenMaya.MScriptUtil()
    mscript_util.createFromDouble(0.0)
    area_pointer = mscript_util.asDoublePtr()
    uvs_area = 0
    while not mesh_polygon_iterator.isDone():
        mesh_polygon_iterator.getUVArea(area_pointer)
        uvs_area += OpenMaya.MScriptUtil().getDouble(area_pointer)
        mesh_polygon_iterator.next()
    return uvs_area


def get_component_uv_dims(component):
    """
    Returns the UVDims of the given component.

    :param component: Component to retrieve the UVDims.
    :type component: str
    :return: UVDims.
    :rtype: tuple
    """

    u, v = cmds.polyEditUV(component, q=True, uValue=True, vValue=True)
    return int(u), int(v)


def get_mari_patch_from_uv_dims(uv_dims):
    """
    Returns the Mari patch of the given component from UVDims.

    :param uv_dims: UVDims to convert to Mari Patch.
    :type uv_dims: tuple
    :return: Mari patch.
    :rtype: int
    """

    u_dim, v_dim = uv_dims
    return 1000 + u_dim + 1 + v_dim * 10


def get_components_uv_dims(components):
    """
    Returns given components UVDims.

    :param components: Components.
    :type components: tuple or list
    :return: Components UVDims.
    :rtype: list
    """

    uvs = get_uvs_from_components(components)
    uv_dims = []
    for uv in uvs:
        u_dim, v_dim = get_component_uv_dims(uv)
        uv_dims.append((uv, (u_dim, v_dim)))
    return uv_dims


def get_components_mari_patches(components):
    """
    Returns given components Mari patches.

    :param components: Components.
    :type components: tuple or list
    :return: Components Mari patches.
    :rtype: list
    """

    uv_dims = get_components_uv_dims(components)
    mari_patches = []
    for uv, uv_dims in uv_dims:
        mari_patches.append((uv, get_mari_patch_from_uv_dims(uv_dims)))
    return mari_patches


def get_components_occupation_as_uv_dims(components):
    """
    Returns given components occupation as UVDims.

    :param components: Components.
    :type components: tuple or list
    :return: Components occupation.
    :rtype: tuple
    """

    shells = get_components_uv_dims(components)
    return tuple(set((shell[1] for shell in shells)))


def get_components_occupation_as_mari_patches(components):
    """
    Returns given components occupation as Mari patches.

    :param components: Components.
    :type components: tuple or list
    :return: Components occupation.
    :rtype: tuple
    """

    mari_patches = get_components_mari_patches(components)
    return tuple(set((patch[1] for patch in mari_patches)))


def print_components_occupation_as_uv_dims():
    """
    Prints selected components occupation as UVDims.
    """

    selection = cmds.ls(sl=True, l=True)
    selection and pprint.pprint(sorted(get_components_occupation_as_uv_dims(selection)))


def print_components_occupation_as_mari_patches():
    """
    Prints selected components occupation as Mari patches.
    """

    selection = cmds.ls(sl=True, l=True)
    selection and pprint.pprint(sorted(get_components_occupation_as_mari_patches(selection)))


def get_components_bounding_box(components):
    """
    Returns given components Bounding Box.

    :param components: Components.
    :type components: tuple or list
    :return: Components Bounding Box.
    :rtype: tuple
    """

    uvs = get_uvs_from_components(components)
    u_min, v_min, u_max, v_max = 2 ** 8, 2 ** 8, -2 ** 8, -2 ** 8
    for uv in uvs:
        u, v = cmds.polyEditUV(uv, q=True, uValue=True, vValue=True)
        u_min = min(u, u_min)
        u_max = max(u, u_max)
        v_min = min(v, v_min)
        v_max = max(v, v_max)
    return u_min, v_min, u_max, v_max


def get_components_uvs_center(components):
    """
    Returns given components Uvs center.

    :param components: Components.
    :type components: tuple or list
    :return: Components Uvs center.
    :rtype: tuple
    """

    u_min, v_min, u_max, v_max = get_components_bounding_box(components)
    return (u_min + u_max) / 2.0, (v_min + v_max) / 2.0


def print_components_uvs_center_as_uv_dims():
    """
    Prints selected components Uvs center as UVDims
    """

    selection = cmds.ls(sl=True, l=True)
    selection and pprint.pprint(tuple([int(value) for value in get_components_uvs_center(selection)]))


def print_components_uvs_center_as_mari_patch():
    """
    Prints selected components Uvs center as Mari Patch.
    """

    selection = cmds.ls(sl=True, l=True)
    selection and pprint.pprint(get_mari_patch_from_uv_dims(
        (int(value) for value in get_components_uvs_center(selection))))


@stacks_handler
def scale_components_uvs(components, su=1, sv=1):
    """
    Scales given components Uvs.

    :param components: Components.
    :type components: tuple or list
    :param su: Scale U value.
    :type su: float
    :param sv: Scale V value.
    :type sv: float
    :return: Definition succes.
    :rtype: bool
    """

    if su == 0.0:
        su = 1e-15
    if sv == 0.0:
        sv = 1e-15
    uvs = get_uvs_from_components(components)
    u_center, v_center = get_components_uvs_center(uvs)
    cmds.polyEditUV(uvs, pu=u_center, pv=v_center, su=su, sv=sv)
    return True


@stacks_handler
def center_components_uvs(components):
    """
    Centers given components Uvs.

    :param components: Components.
    :type components: tuple or list
    :return: Definition succes.
    :rtype: bool
    """

    uvs = get_uvs_from_components(components)
    u_min, v_min, u_max, v_max = get_components_bounding_box(uvs)
    u_center, v_center = (u_min + u_max) / 2.0, (v_min + v_max) / 2.0
    u_target_center, v_target_center = math.floor(u_center), math.floor(v_center)
    cmds.polyEditUV(uvs, u=u_target_center - u_center + 0.5, v=v_target_center - v_center + 0.5)
    return True


@stacks_handler
def scale_center_components_uvs(components, coverage=DEFAULT_SCALE_COVERAGE):
    """
    Scales / centers given components Uvs.

    :param components: Components.
    :type components: tuple or list
    :return: Definition succes.
    :rtype: bool
    """

    uvs = get_uvs_from_components(components)
    u_min, v_min, u_max, v_max = get_components_bounding_box(uvs)
    u_center, v_center = (u_min + u_max) / 2.0, (v_min + v_max) / 2.0
    u_target_center, v_target_center = math.floor(u_center), math.floor(v_center)
    cmds.polyEditUV(uvs, u=u_target_center - u_center + 0.5, v=v_target_center - v_center + 0.5)
    u_scale = math.fabs(u_min - u_max)
    v_scale = math.fabs(v_min - v_max)
    scale_factor = 1 / max(u_scale, v_scale) * coverage
    cmds.polyEditUV(uvs, pu=u_target_center + 0.5, pv=v_target_center + 0.5, su=scale_factor, sv=scale_factor)
    return True


@stacks_handler
def rotate_components_uvs(components, value, clock_wise=True):
    """
    Rotates given components Uvs.

    :param components: Components.
    :type components: tuple or list
    :param value: Rotation value.
    :type value: float
    :param clock_wise: Rotation direction.
    :type clock_wise: bool
    :return: Definition succes.
    :rtype: bool
    """

    uvs = get_uvs_from_components(components)
    u_center, v_center = get_components_uvs_center(uvs)
    if not clock_wise:
        value = -value
    cmds.polyEditUV(uvs, pu=u_center, pv=v_center, a=-value)
    return True


@stacks_handler
@anchor_selection
def poly_rotate_components_uvs(components, value, clock_wise=True):
    """
    Rotates given components Uvs using Maya "polyRotateUvs" melscript ( Ugly but sadly faster ).

    :param components: Components.
    :type components: tuple or list
    :param value: Rotation value.
    :type value: float
    :param clock_wise: Rotation direction.
    :type clock_wise: bool
    :return: Definition succes.
    :rtype: bool
    """

    if clock_wise:
        value = -value

    mel.eval("polyRotateUvs %s" % value)
    return True


@stacks_handler
def move_components_uvs(components, u=0, v=0):
    """
    Moves given components Uvs.

    :param components: Components.
    :type components: tuple or list
    :param u: U value.
    :type u: float
    :param v: V value.
    :type v: float
    :return: Definition succes.
    :rtype: bool
    """

    uvs = get_uvs_from_components(components, flatten=False)
    cmds.polyEditUV(uvs, u=u, v=v)
    return True


@stacks_handler
def mirror_components_uvs(components, horizontal=True):
    """
    Mirrors given components Uvs.

    :param components: Components.
    :type components: tuple or list
    :param horizontal: Horizontal mirror.
    :type horizontal: bool
    :return: Definition succes.
    :rtype: bool
    """

    uvs = get_uvs_from_components(components)
    u_center, v_center = (math.floor(value) for value in get_components_uvs_center(uvs))
    if horizontal:
        cmds.polyEditUV(uvs, pu=u_center + 0.5, pv=v_center + 0.5, su=-1)
    else:
        cmds.polyEditUV(uvs, pu=u_center + 0.5, pv=v_center + 0.5, sv=-1)
    return True


@stacks_handler
def stack_objects_uvs(objects, alignement="center", horizontal=True, margin=0):
    """
    Stacks given objects Uvs.

    :param objects: Objects.
    :type objects: tuple or list
    :param alignement: Alignement ( "bottom", "top", "left", "right", "center" ).
    :type alignement: str
    :param horizontal: Horizontal stack.
    :type horizontal: bool
    :return: Definition succes.
    :rtype: bool
    """

    if not objects:
        return

    uvs = get_uvs_from_components(objects.pop(0))
    u_center, v_center = get_components_uvs_center(uvs)
    u_min, v_min, u_max, v_max = get_components_bounding_box(uvs)
    u_border = u_max - u_min + u_min
    v_border = v_max - v_min + v_min
    for object in objects:
        uvs = get_uvs_from_components(object)
        current_u_min, current_v_min, current_u_max, current_v_max = get_components_bounding_box(uvs)
        if horizontal:
            offset_u = u_border - current_u_min + margin
            if alignement == "bottom":
                offset_v = v_min - current_v_min
            elif alignement == "center":
                offset_v = (v_min - current_v_min) / 2 + (v_max - current_v_max) / 2
            elif alignement == "top":
                offset_v = v_max - current_v_max
            u_border = u_border + current_u_max - current_u_min + margin
        else:
            offset_v = v_border - current_v_min + margin
            if alignement == "left":
                offset_u = u_min - current_u_min
            elif alignement == "center":
                offset_u = (u_min - current_u_min) / 2 + (u_max - current_u_max) / 2
            elif alignement == "right":
                offset_u = u_max - current_u_max
            v_border = v_border + current_v_max - current_v_min + margin
        cmds.polyEditUV(uvs, u=offset_u, v=offset_v)
    return True


@stacks_handler
def prescale_uvs_shells(object):
    """
    Prescales object Uvs shells.

    :param objects: Object.
    :type objects: str
    :return: Definition succes.
    :rtype: bool
    """

    uvs = get_uvs_from_components(object)
    u_min, v_min, u_max, v_max = get_components_bounding_box(uvs)
    u_center, v_center = (u_min + u_max) / 2.0, (v_min + v_max) / 2.0
    width, height = u_max - u_min, v_max - v_min
    scale = max(width, height)

    cmds.polyMultiLayoutUV(object, lm=0, sc=1, rbf=0, fr=False, ps=0.2, l=2, psc=True)

    current_u_min, current_v_min, current_u_max, current_v_max = get_components_bounding_box(uvs)
    current_u_center, current_v_center = (current_u_min + current_u_max) / 2.0, (current_v_min + current_v_max) / 2.0
    current_width, current_height = current_u_max - current_u_min, current_v_max - current_v_min
    current_scale = max(current_width, current_height)

    scale_factor = scale / current_scale

    cmds.polyEditUV(uvs, u=u_center - current_u_center, v=v_center - current_v_center)
    scale_components_uvs(uvs, su=scale_factor, sv=scale_factor)
    return True


@stacks_handler
def auto_ratio_uvs_areas(objects):
    """
    Scales objects Uvs depending their worldspace areas.

    :param objects: Objects.
    :type objects: tuple or list
    :return: Definition succes.
    :rtype: bool
    """

    if not objects:
        return

    base_object = objects.pop(0)
    area = cmds.polyEvaluate(base_object, worldArea=True)
    uvs_area = get_object_uvs_area(base_object)

    for object in objects:
        current_area = cmds.polyEvaluate(object, worldArea=True)
        current_uvs_area = get_object_uvs_area(object)
        scale_factor = math.sqrt(((current_area * uvs_area) / current_uvs_area) / area)
        scale_components_uvs(object, su=scale_factor, sv=scale_factor)
    return True


def get_connections(node):
    """
    Returns the connections of given node.

    :param node: Node.
    :type node: str
    :return: Connections.
    :rtype: list
    """

    connections = cmds.listConnections(node, c=True)
    return [(connections[i + 1], connections[i]) for i in range(0, len(connections), 2)]


def get_attached_shaders(object):
    """
    Returns the shaders attached to given objects.

    :param object: Current object.
    :type object: str
    :return: Attached shaders.
    :rtype: list
    """

    shape = get_first_item(get_shapes(object))
    if not shape:
        return tuple()

    shading_engine = get_first_item(cmds.listConnections(shape, t="shadingEngine"))
    if not shading_engine:
        return tuple()

    shader = get_first_item(filter(lambda x: re.search("\.surfaceShader$", x[1]), get_connections(shading_engine)))
    if not shader:
        return tuple()

    return (get_first_item(shader),)


@stacks_handler
def add_uvs_checker(objects, u_repeats=4, v_repeats=4):
    """
    Applies Uvs checkers onto given geometry objects.

    :param objects: Current objects list.
    :type objects: list
    :param u_repeats: U checker repeats.
    :type u_repeats: float
    :param v_repeats: V checker repeats.
    :type v_repeats: float
    :return: Definition succes.
    :rtype: bool
    """

    for object in objects:
        for shader in get_attached_shaders(object):
            file = get_first_item(filter(lambda x: re.search("\.color$", x[1]), get_connections(shader)))
            if file is not None:
                if "UvsChecker" in get_first_item(file):
                    continue

            file = cmds.shadingNode("file", asTexture=True)
            cmds.setAttr("{0}.fileTextureName".format(file), os.path.normpath(
                os.path.join(RESOURCES_DIRECTORY, CHECKER_IMAGE)), type="string")
            place_2d_texture = cmds.shadingNode("place2dTexture", asUtility=True)
            cmds.setAttr("{0}.repeatU".format(place_2d_texture), u_repeats)
            cmds.setAttr("{0}.repeatV".format(place_2d_texture), v_repeats)
            for uv_attribute in (
                    "coverage", "translateFrame", "rotateFrame", "mirrorU", "mirrorV", "stagger", "wrapU", "wrapV",
                    "repeatUV",
                    "vertexUvOne", "vertexUvTwo", "vertexUvThree", "vertexCameraOne", "noiseUV", "offset", "rotateUV"):
                cmds.connectAttr("{0}.{1}".format(place_2d_texture, uv_attribute),
                                 "{0}.{1}".format(file, uv_attribute), force=True)

            cmds.connectAttr("{0}.outColor".format(file), "{0}.color".format(shader), force=True)
            cmds.rename(file, "UvsChecker_{0}_file".format(shader))
            cmds.rename(place_2d_texture, "UvsChecker_{0}_place2dTexture".format(shader))
    return True


@stacks_handler
def remove_uvs_checker(objects):
    """
    :param objects: Current objects list.
    :type objects: list
    :return: Definition succes.
    :rtype: bool
    """

    for object in objects:
        for shader in get_attached_shaders(object):
            file = get_first_item(filter(lambda x: re.search("\.color$", x[1]), get_connections(shader)))
            if file is not None:
                file = get_first_item(file)
                "UvsChecker" in file and cmds.delete(cmds.listHistory(file))
    return True


@stacks_handler
def set_uvs_checker_repeats(u_repeats=None, v_repeats=None):
    """
    Sets Uvs checkers repeats.

    :param u_repeats: U checker repeats.
    :type u_repeats: float
    :param v_repeats: V checker repeats.
    :type v_repeats: float
    :return: Definition succes.
    :rtype: bool
    """

    for file in cmds.ls("UvsChecker_*_place2dTexture"):
        u_repeats and cmds.setAttr("{0}.repeatU".format(file), u_repeats)
        v_repeats and cmds.setAttr("{0}.repeatV".format(file), v_repeats)
    return True


@stacks_handler
def get_patch_shader_tree(patch, prefix):
    """
    Builds the patch shader tree of given patch.

    :param patch: Patch.
    :type patch: int
    :param prefix: Name prefix.
    :type prefix: str
    :return: Tree shading engine.
    :rtype: str
    """

    name = "{0}{1}".format(prefix, patch)
    shading_engine = get_node("{0}SG".format(name))
    if not shading_engine:
        lambert = cmds.shadingNode("lambert", asShader=True)
        shading_engine = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
        cmds.connectAttr("{0}.outColor".format(lambert), "{0}.surfaceShader".format(shading_engine), f=True)

        cmds.rename(lambert, name)
        shading_engine = cmds.rename(shading_engine, "{0}SG".format(name))
    return shading_engine


@stacks_handler
def assign_mari_shadersToObject(object, prefix):
    """
    Assigns the Mari shaders to given object.

    :param prefix: Shader prefix name.
    :type prefix: str
    :param object: Object.
    :type object: str
    :return: Definition success.
    :rtype: bool
    """

    patches = get_components_occupation_as_mari_patches(object)
    if len(patches) == 1:
        patch = patches[0]
        shading_engine = get_patch_shader_tree(patch, prefix)
        cmds.sets(object, e=True, forceElement=shading_engine)
    else:
        for patch, faces in get_faces_per_patches(object).items():
            shading_engine = get_patch_shader_tree(patch, prefix)
            cmds.sets(faces, e=True, forceElement=shading_engine)
    return True


@stacks_handler
def assign_mari_shaders(objects, prefix):
    """
    Assigns the Mari shaders to given objects.

    :param objects: Objects.
    :type objects: list
    :param prefix: Shader prefix name.
    :type prefix: str
    :return: Definition success.
    :rtype: bool
    """

    main_progress_bar = mel.eval('$tmp = $gMainProgressBar')
    cmds.progressBar(main_progress_bar, edit=True, beginProgress=True, isInterruptable=True,
                     status="Assigning Mari shaders ...", maxValue=len(objects))

    success = True
    for object in objects:
        if cmds.progressBar(main_progress_bar, query=True, isCancelled=True):
            break

        cmds.progressBar(
            main_progress_bar, edit=True, status="Assigning Mari shaders to '{0}' ...".format(object), step=1)
        success *= assign_mari_shadersToObject(object, prefix)

    cmds.progressBar(main_progress_bar, edit=True, endProgress=True)

    return success


@stacks_handler
def assign_mari_shaders_on_selected_objects():
    """
    Assigns the Mari shaders to selected objects.
    """

    selection = cmds.ls(sl=True, l=True)
    if not selection:
        return

    relatives = cmds.listRelatives(selection, allDescendents=True, full_path=True, type="mesh")

    project_name = os.path.basename(os.path.dirname(cmds.workspace(q=True, fullName=True)))
    result = cmds.promptDialog(title="Mari Shaders Prefix", message="Enter Prefix:", text=project_name, button=[
        "OK", "Cancel"], defaultButton="OK", cancelButton="Cancel", dismissString="Cancel")
    if result == "OK":
        prefix = cmds.promptDialog(query=True, text=True)
        prefix and assign_mari_shaders(relatives, prefix)


def get_mari_affixes(name):
    """
    Returns given name Mari affixes.

    :param name: Name.
    :type name: str
    :return: Affixes.
    :rtype: tuple
    """

    prefix, suffix = os.path.splitext(os.path.basename(name))
    prefix = re.match(r"([\w\.]+)\d{4}", prefix)
    return prefix.groups()[0] if prefix else "", suffix.replace(".", "")


@stacks_handler
def get_preview_mari_textures_branches(directory, prefix, extension, shader="lambert"):
    """
    Creates Mari preview textures branches.

    :param directory: Source directory.
    :type directory: str
    :param prefix: Files prefix.
    :type prefix: str
    :param extension: Files extension.
    :type extension: str
    :param shader: Shader type.
    :type shader: str
    :return: Definition success.
    :rtype: bool
    """

    for shader in filter(lambda x: re.search(r"\w+[0-9]{4}", x), cmds.ls(type=shader)):
        texture_name = os.path.join(
            directory, "{0}{1}.{2}".format(prefix, re.search(r"[0-9]{4}", shader).group(0), extension))
        if not os.path.exists(texture_name):
            print("'{0}' file doesn't exists!".format(texture_name))
            continue

        file_node = cmds.shadingNode("file", asTexture=True)
        cmds.setAttr("{0}.fileTextureName".format(file_node), texture_name, type="string")
        cmds.connectAttr("{0}.outColor".format(file_node), "{0}.color".format(shader), force=True)
        cmds.rename(file_node, "{0}_file".format(shader))
    return True


@stacks_handler
def assign_mari_preview_textures():
    """
    Assigns the Mari preview textures.

    :return: Definition success.
    :rtype: bool
    """

    file = cmds.fileDialog2(fileFilter="All files (*.*)", fm=1, dialogStyle=2)
    file = file and file[0] or None
    if not file:
        return

    prefix, suffix = get_mari_affixes(file)
    if not suffix:
        return

    directory = os.path.dirname(file)
    return get_preview_mari_textures_branches(directory, prefix, suffix)


@stacks_handler
def flip_uvs_button__on_clicked(state=None):
    """
    Defines the slot triggered by **flip_uvs_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and mirror_components_uvs(selection)


@stacks_handler
def move_up_uvs_button__on_clicked(state=None):
    """
    Defines the slot triggered by **move_up_uvs_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and move_components_uvs(selection, v=cmds.floatField("move_factor_floatField", q=True, value=True))


@stacks_handler
def flop_uvs_button__on_clicked(state=None):
    """
    Defines the slot triggered by **flop_uvs_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and mirror_components_uvs(selection, horizontal=False)


@stacks_handler
def move_left_uvs_button__on_clicked(state=None):
    """
    Defines the slot triggered by **move_left_uvs_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and move_components_uvs(selection, u=-cmds.floatField("move_factor_floatField", q=True, value=True))


@stacks_handler
def fit_uvs_button__on_clicked(state=None):
    """
    Defines the slot triggered by **fit_uvs_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and scale_center_components_uvs(
        selection, float(cmds.intField("coverage_intField", q=True, value=True)) / 100)


@stacks_handler
def move_right_uvs_button__on_clicked(state=None):
    """
    Defines the slot triggered by **move_right_uvs_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and move_components_uvs(selection, u=cmds.floatField("move_factor_floatField", q=True, value=True))


@stacks_handler
def center_uvs_button__on_clicked(state=None):
    """
    Defines the slot triggered by **center_uvs_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and center_components_uvs(selection)


@stacks_handler
def move_down_uvs_button__on_clicked(state=None):
    """
    Defines the slot triggered by **move_down_uvs_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and move_components_uvs(selection, v=-cmds.floatField("move_factor_floatField", q=True, value=True))


@stacks_handler
def scale_uvs_button__on_clicked(state=None):
    """
    Defines the slot triggered by **scale_uvs_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and scale_components_uvs(selection, su=cmds.floatField(
        "u_scale_floatField", q=True, value=True), sv=cmds.floatField("v_scale_floatField", q=True, value=True))


@stacks_handler
def rotate_counter_clock_wise_uvs_button__on_clicked(state=None):
    """
    Defines the slot triggered by **rotate_counter_clock_wise_uvs_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and poly_rotate_components_uvs(
        selection, cmds.floatField("rotation_floatField", q=True, value=True), clock_wise=False)


@stacks_handler
def rotate_clock_wise_uvs_button__on_clicked(state=None):
    """
    Defines the slot triggered by **rotate_clock_wise_uvs_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and poly_rotate_components_uvs(selection, cmds.floatField("rotation_floatField", q=True, value=True))


@stacks_handler
def stack_uvs_on_u_bottom_button__on_clicked(state=None):
    """
    Defines the slot triggered by **stack_uvs_on_u_bottom_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and stack_objects_uvs(
        selection, alignement="bottom", margin=cmds.floatField("margin_floatField", q=True, value=True))


@stacks_handler
def stack_uvs_on_u_center_button__on_clicked(state=None):
    """
    Defines the slot triggered by **stack_uvs_on_u_center_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and stack_objects_uvs(
        selection, alignement="center", margin=cmds.floatField("margin_floatField", q=True, value=True))


@stacks_handler
def stack_uvs_on_u_top_button__on_clicked(state=None):
    """
    Defines the slot triggered by **stack_uvs_on_u_top_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and stack_objects_uvs(
        selection, alignement="top", margin=cmds.floatField("margin_floatField", q=True, value=True))


@stacks_handler
def stack_uvs_on_v_left_button__on_clicked(state=None):
    """
    Defines the slot triggered by **stack_uvs_on_v_left_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and stack_objects_uvs(
        selection, alignement="left", horizontal=False, margin=cmds.floatField("margin_floatField", q=True, value=True))


@stacks_handler
def stack_uvs_on_v_center_button__on_clicked(state=None):
    """
    Defines the slot triggered by **stack_uvs_on_v_center_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and stack_objects_uvs(
        selection, alignement="center", horizontal=False,
        margin=cmds.floatField("margin_floatField", q=True, value=True))


@stacks_handler
def stack_uvs_on_v_right_button__on_clicked(state=None):
    """
    Defines the slot triggered by **stack_uvs_on_v_right_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and stack_objects_uvs(
        selection, alignement="right", horizontal=False,
        margin=cmds.floatField("margin_floatField", q=True, value=True))


@stacks_handler
def prescale_uvs_shells_button__on_clicked(state=None):
    """
    Defines the slot triggered by **prescale_uvs_shells_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    for object in selection:
        prescale_uvs_shells(object)


@stacks_handler
def auto_ratio_uvs_areas_button__on_clicked(state=None):
    """
    Defines the slot triggered by **auto_ratio_uvs_areas_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and auto_ratio_uvs_areas(selection)


@stacks_handler
def add_uvs_checker_button__on_clicked(state=None):
    """
    Defines the slot triggered by **add_uvs_checker_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and add_uvs_checker(selection)


@stacks_handler
def remove_uvs_checker_button__on_clicked(state=None):
    """
    Defines the slot triggered by **remove_uvs_checker_button** button when clicked.

    :param state: Button state.
    :type state: bool
    """

    selection = cmds.ls(sl=True, l=True)
    selection and remove_uvs_checker(selection)


@stacks_handler
def u_repeat_float_field__on_changed(value=None):
    """
    Defines the slot triggered by **u_repeat_floatField** button when changed.

    :param value: Field value.
    :type value: float
    """

    set_uvs_checker_repeats(u_repeats=value)


@stacks_handler
def v_repeat_float_field__on_changed(value=None):
    """
    Defines the slot triggered by **v_repeat_floatField** button when changed.

    :param value: Field value.
    :type value: float
    """

    set_uvs_checker_repeats(v_repeats=value)


def unfolding_tools_window():
    """
    Creates the 'Unfolding Tools' main window.
    """

    cmds.windowPref(enableAll=False)

    if (cmds.window("unfolding_tools_window", exists=True)):
        cmds.deleteUI("unfolding_tools_window")

    cmds.window("unfolding_tools_window",
                title="Unfolding Tools",
                width=320)

    spacing = 0

    columnsWidth = (106, 106, 106)
    columnsAttach = [(1, "both", spacing), (2, "both", spacing), (3, "both", spacing)]

    cmds.columnLayout()

    cmds.frameLayout(label="Uvs Move / Scale", collapsable=True, borderStyle="etchedIn")

    cmds.columnLayout()

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.button("flip_uvs_button", label="Flip", command=flip_uvs_button__on_clicked)
    cmds.button("move_up_uvs_button", label="Move Up", command=move_up_uvs_button__on_clicked)
    cmds.button("flop_uvs_button", label="Flop", command=flop_uvs_button__on_clicked)
    cmds.setParent(upLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.button("move_left_uvs_button", label="Move Left", command=move_left_uvs_button__on_clicked)
    cmds.button("fit_uvs_button", label="Fit", command=fit_uvs_button__on_clicked)
    cmds.button("move_right_uvs_button", label="Move Right", command=move_right_uvs_button__on_clicked)
    cmds.setParent(upLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.button("center_uvs_button", label="Center", command=center_uvs_button__on_clicked)
    cmds.button("move_down_uvs_button", label="Move Down", command=move_down_uvs_button__on_clicked)
    cmds.button("scale_uvs_button", label="Scale", command=scale_uvs_button__on_clicked)
    cmds.setParent(upLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.text(label="Coverage %:")
    cmds.intField("coverage_intField", minValue=0, maxValue=100, value=98)
    cmds.setParent(upLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.text(label="Move Factor:")
    cmds.floatField("move_factor_floatField", minValue=0, maxValue=10, value=1)
    cmds.setParent(upLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.text(label="Scale U / V:")
    cmds.floatField("u_scale_floatField", minValue=-10, maxValue=10, value=1)
    cmds.floatField("v_scale_floatField", minValue=-10, maxValue=10, value=1)
    cmds.setParent(upLevel=True)

    cmds.setParent(upLevel=True)
    cmds.setParent(upLevel=True)

    cmds.frameLayout(label="Uvs Rotation", collapsable=True, borderStyle="etchedIn")

    cmds.columnLayout()

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.button("rotate_counter_clock_wise_uvs_button", label="Rotate CCWZ",
                command=rotate_counter_clock_wise_uvs_button__on_clicked)
    cmds.button(label="", enable=False)
    cmds.button("rotate_clock_wise_uvs_button", label="Rotate CWZ", command=rotate_clock_wise_uvs_button__on_clicked)
    cmds.setParent(upLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.text(label="Angle:")
    cmds.floatField("rotation_floatField", minValue=-360, maxValue=360, value=45)
    cmds.setParent(upLevel=True)

    cmds.setParent(upLevel=True)
    cmds.setParent(upLevel=True)

    cmds.frameLayout(label="Uvs Alignement", collapsable=True, borderStyle="etchedIn")

    cmds.columnLayout()

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.button(label="", enable=False)
    cmds.button("align_uvs_maximum_v_button", label="Align Max. V", command=lambda state: mel.eval("alignUV 0 0 1 0;"))
    cmds.button(label="", enable=False)
    cmds.setParent(upLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.button("align_uvs_minimum_u_button", label="Align Min. U", command=lambda state: mel.eval("alignUV 1 1 0 0;"))
    cmds.button("straighten_uvs_button", label="Straigthen",
                command=lambda state: mel.eval("warning \"Not implemented yet!\";"))
    cmds.button("align_uvs_maximum_u_button", label="Align Max. U", command=lambda state: mel.eval("alignUV 1 0 0 0;"))
    cmds.setParent(upLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.button(label="", enable=False)
    cmds.button("align_uvs_minimum_v_button", label="Align Min. V", command=lambda state: mel.eval("alignUV 0 0 1 1;"))
    cmds.button(label="", enable=False)
    cmds.setParent(upLevel=True)

    cmds.setParent(upLevel=True)
    cmds.setParent(upLevel=True)

    cmds.frameLayout(label="Uvs Stacks", collapsable=True, borderStyle="etchedIn")

    cmds.columnLayout()

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.button("stack_uvs_on_u_bottom_button", label="Stack On U Bottom",
                command=stack_uvs_on_u_bottom_button__on_clicked)
    cmds.button("stack_uvs_on_u_center_button", label="Stack On U Center",
                command=stack_uvs_on_u_center_button__on_clicked)
    cmds.button("stack_uvs_on_u_top_button", label="Stack On U Top", command=stack_uvs_on_u_top_button__on_clicked)
    cmds.setParent(upLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.button("stack_uvs_on_v_left_button", label="Stack On V Left", command=stack_uvs_on_v_left_button__on_clicked)
    cmds.button("stack_uvs_on_v_center_button", label="Stack On V Center",
                command=stack_uvs_on_v_center_button__on_clicked)
    cmds.button("stack_uvs_on_v_right_button", label="Stack On V Right",
                command=stack_uvs_on_v_right_button__on_clicked)
    cmds.setParent(upLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.text(label="Margin:")
    cmds.floatField("margin_floatField", minValue=0, maxValue=10, value=0.001)
    cmds.setParent(upLevel=True)

    cmds.setParent(upLevel=True)
    cmds.setParent(upLevel=True)

    cmds.frameLayout(label="Uvs Auto Ratio", collapsable=True, borderStyle="etchedIn")

    cmds.columnLayout()

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.button("prescale_uvs_shells_button", label="Prescale Shells", command=prescale_uvs_shells_button__on_clicked)
    cmds.button(label="", enable=False)
    cmds.button("auto_ratio_uvs_areas_button", label="Auto Ratio", command=auto_ratio_uvs_areas_button__on_clicked)
    cmds.setParent(upLevel=True)

    cmds.setParent(upLevel=True)
    cmds.setParent(upLevel=True)

    cmds.frameLayout(label="Uvs Verbose", collapsable=True, borderStyle="etchedIn")

    cmds.columnLayout()

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.button("print_uvs_uvdims_button", label="Print UVDims",
                command=lambda state: print_components_occupation_as_uv_dims())
    cmds.button(label="", enable=False)
    cmds.button("print_uvs_mari_patches_button", label="Print Mari Patches",
                command=lambda state: print_components_occupation_as_mari_patches())
    cmds.setParent(upLevel=True)

    cmds.setParent(upLevel=True)
    cmds.setParent(upLevel=True)

    cmds.frameLayout(label="Uvs Checker", collapsable=True, borderStyle="etchedIn")

    cmds.columnLayout()

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.button("add_uvs_checker_button", label="Add Checker", command=add_uvs_checker_button__on_clicked)
    cmds.button(label="", enable=False)
    cmds.button("remove_uvs_checker_button", label="Remove Checker", command=remove_uvs_checker_button__on_clicked)
    cmds.setParent(upLevel=True)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=columnsWidth, columnAttach=columnsAttach)
    cmds.text(label="Repeat U / V:")
    cmds.floatField("u_repeat_floatField", minValue=0.01, maxValue=256, value=4,
                    step=0.25, changeCommand=u_repeat_float_field__on_changed)
    cmds.floatField("v_repeat_floatField", minValue=0.01, maxValue=256, value=4,
                    step=0.25, changeCommand=v_repeat_float_field__on_changed)
    cmds.setParent(upLevel=True)

    cmds.setParent(upLevel=True)
    cmds.setParent(upLevel=True)

    cmds.showWindow("unfolding_tools_window")

    cmds.windowPref(enableAll=True)


def unfolding_tools():
    """
    Launches the 'Unfolding Tools' main window.
    """

    unfolding_tools_window()
