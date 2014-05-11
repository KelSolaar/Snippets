#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**to_alembic.py**

**Platform:**
    Windows.

**Description:**
    Exports given scene to Alembic using Maya.

    Usage::

        alias to_alembic 'setenv MAYA_LOCATION /software/maya/2013/linux.centos6.x86_64 && $MAYA_LOCATION/bin/mayapy "/usr/people/thomas-ma/Developement/Snippets/src/others/to_alembic.py"'

        to_alembic -i myFile.obj

**Others:**

"""

from __future__ import unicode_literals

import maya.standalone

maya.standalone.initialize(name="python")

import inspect
import maya.cmds as cmds
import optparse
import os
import re
import sys

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["ascendants_walker", "get_root", "to_alembic", "get_command_line_parameters"]


def ascendants_walker(path, visitor=None):
    """
    Returns the parents of given Dag path.

    :param path: Dag path.
    :type path: str
    :param visitor: Visitor.
    :type visitor: object
    :return: Parent.
    :rtype: str
    """

    parents = cmds.listRelatives(path, allParents=True, fullPath=True)
    if not parents:
        return

    for parent in parents:
        visitor and visitor(parent)
        yield parent
        for value in ascendants_walker(parent):
            yield value


def get_root(path):
    """
    Returns the root path of given Dag path.

    :param path: Dag path.
    :type path: str
    :return: Root path.
    :rtype: str
    """

    parents = list(ascendants_walker(path))
    return parents[-1] if parents else path


def to_alembic(parameters, arguments):
    """
    Converts an Obj file to Alembic file.

    :param parameters: Command line parameters.
    :type parameters: object
    :param arguments: Command line arguments.
    :type arguments: object
    :return: Definition success.
    :rtype: bool
    """

    input_file = parameters.input_file
    if input_file is None:
        sys.stderr.write("!> {0} | No input file provided!\n".format(inspect.getmodulename(__file__)))
        return

    if not os.path.exists(input_file):
        sys.stderr.write("!> {0} | '{1}' file doesn't exists'!\n".format(inspect.getmodulename(__file__), input_file))
        return

    output_file = os.path.abspath(
        parameters.output_file if parameters.output_file else re.sub(r"\.\w+$", ".abc", input_file))

    export_all = parameters.export_all

    frame_range = parameters.frameRange
    try:
        frame_in, frame_out = frame_range.split("-")
    except ValueError:
        sys.stderr.write("!> {0} | The frame range format could not be determined!\n".format(
            inspect.getmodulename(__file__)))
        return

    not cmds.pluginInfo("AbcExport", q=True, loaded=True) and cmds.loadPlugin("AbcExport")

    cmds.file(input_file, o=True)

    # Processing ".obj" file normals.
    if re.search(r"\.obj$", input_file, flags=re.IGNORECASE):
        for mesh in cmds.ls(type="mesh", long=True):
            cmds.polyNormalPerVertex(mesh, ufn=True)
            cmds.polySoftEdge(mesh, a=180, ch=False)

    if export_all:
        job_command = "-frameRange {0} {1} -uvWrite -file {2}".format(frame_in, frame_out, output_file)
    else:
        root_nodes = list(set([get_root(mesh) for mesh in cmds.ls(type="mesh", long=True)]))
        root_flags = " ".join(["-root {0}".format(root_node) for root_node in root_nodes])
        job_command = "-frameRange {0} {1} -uvWrite {2} -file {3}".format(frame_in, frame_out, root_flags, output_file)

    sys.stderr.write("{0} | Exporting to 'Alembic' with following job command: '{1}'\n".format(
        inspect.getmodulename(__file__), job_command))
    cmds.AbcExport(j=job_command)
    return True


def get_command_line_parameters(argv):
    """
    Returns the command line parameters parser.

    :param argv: Command line parameters.
    :type argv: str
    :return: Settings, arguments
    :rtype: ParserInstance
    """

    argv = argv or sys.argv[1:]

    parser = optparse.OptionParser(formatter=optparse.IndentedHelpFormatter(
        indent_increment=2, max_help_position=8, width=128, short_first=1), add_help_option=None)

    parser.add_option("-h", "--help", action="help", help="'Display this help message and exit.'")
    parser.add_option("-i", "--input_file", action="store", type="string", dest="input_file", help="'Input file.")
    parser.add_option("-o", "--output_file", action="store", type="string", dest="output_file", help="'Output file.")
    parser.add_option("-a", "--export_all", action="store_true",
                      dest="export_all", default=False, help="Export all scene.")
    parser.add_option("-r", "--frameRange", action="store", type="string",
                      dest="frameRange", default="1-5", help="Frame range ( '1-5' ).")

    parameters, args = parser.parse_args(argv)

    return parameters, args


if __name__ == "__main__":
    parameters, arguments = get_command_line_parameters(sys.argv)
    to_alembic(parameters, arguments)
