#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**rename_textures.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :def:`get_textures_names` and :def:`rename_textures` definitions and other related objects.

**Others:**
"""

from __future__ import unicode_literals

import doctest
import glob
import inspect
import os
import optparse
import sys
import re

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["UDIM_PATTERN",
           "PATCH_PATTERN",
           "get_patch_from_udim",
           "get_udim_from_patch",
           "get_textures_names",
           "get_command_line_parameters_parser",
           "rename_textures"]

UDIM_PATTERN = "u\d+_v\d+"
PATCH_PATTERN = "\d{4,}"


def get_patch_from_udim(udim):
    """
    Returns the patch from given udim.

    Usage::

        >>> get_patch_from_udim((0, 0)) # doctest: +NORMALIZE_WHITESPACE
        1001
        >>> get_patch_from_udim((9, 0))
        1010
        >>> get_patch_from_udim((0, 1))
        1011
        >>> get_patch_from_udim((9, 1))
        1020
        >>> get_patch_from_udim((9, 9))
        1100

    :param udim: Udim to convert.
    :type udim: tuple
    :return: Patch.
    :rtype: int
    """

    return 1000 + udim[0] + 1 + udim[1] * 10


def get_udim_from_patch(patch):
    """
    Returns the udim from given patch.

    Usage::

        >>> get_udim_from_patch(1001) # doctest: +NORMALIZE_WHITESPACE
        (0, 0)
        >>> get_udim_from_patch(1010)
        (9, 0)
        >>> get_udim_from_patch(1011)
        (0, 1)
        >>> get_udim_from_patch(1020)
        (9, 1)
        >>> get_udim_from_patch(1100)
        (9, 9)

    :param udim: Patch to convert.
    :type udim: int
    :return: Udim.
    :rtype: str
    """

    u = (patch - 1000) % 10
    v = (patch - 1000) / 10
    return 9 if u == 0 else u - 1, v - 1 if u % 10 == 0 else v


def get_textures_names(textures, input="zbrush", output="mari", prefix=None):
    """
    Renames given textures.

    Usage::

        >>> get_textures_names(["Diffuse_u0_v0.exr", "Diffuse_u9_v0.exr"]) # doctest: +NORMALIZE_WHITESPACE
        [(u'Diffuse_u0_v0.exr', u'Diffuse_1001.exr'), (u'Diffuse_u9_v0.exr', u'Diffuse_1010.exr')]
        >>> get_textures_names(["Diffuse_u0_v0.exr", "Diffuse_u9_v0.exr"], "zbrush", "mudbox")
        [(u'Diffuse_u9_v0.exr', u'Diffuse_u10_v1.exr'), (u'Diffuse_u0_v0.exr', u'Diffuse_u1_v1.exr')]
        >>> get_textures_names(["Diffuse_1001.exr", "Diffuse_1010.exr"], "mari", "zbrush")
        [(u'Diffuse_1001.exr', u'Diffuse_u0_v0.exr'), (u'Diffuse_1010.exr', u'Diffuse_u9_v0.exr')]
        >>> get_textures_names(["Diffuse_1001.exr", "Diffuse_1010.exr"], "mari", "mudbox")
        [(u'Diffuse_1001.exr', u'Diffuse_u1_v1.exr'), (u'Diffuse_1010.exr', u'Diffuse_u10_v1.exr')]
        >>> get_textures_names(["Diffuse_u0_v0.exr", "Diffuse_u9_v0.exr"], prefix="")
        [(u'Diffuse_u0_v0.exr', u'1001.exr'), (u'Diffuse_u9_v0.exr', u'1010.exr')]
        >>> get_textures_names(["Diffuse_u0_v0.exr", "Diffuse_u9_v0.exr"], prefix="Color_")
        [(u'Diffuse_u0_v0.exr', u'Color_1001.exr'), (u'Diffuse_u9_v0.exr', u'Color_1010.exr')]

    :param textures: Textures.
    :type textures: list
    :param input: Input format ( "mari", "mudbox", "zbrush" ).
    :type input: str
    :param output: Output format ( "mari", "mudbox", "zbrush" ).
    :type output: str
    :param prefix: Rename prefix.
    :type prefix: str
    :return: Converted textures names.
    :rtype: list
    """

    input_method = "udim" if input in ("mudbox", "zbrush") else "patch"
    output_method = "udim" if output in ("mudbox", "zbrush") else "patch"
    pattern = UDIM_PATTERN if input_method == "udim" else PATCH_PATTERN

    offset_udim = lambda x, y: (x[0] + y, x[1] + y)

    if input == "zbrush" and output == "mudbox":
        textures = reversed(textures)

    textures_mapping = []
    for texture in textures:
        basename = os.path.basename(texture)
        search = re.search(r"({0})".format(pattern), basename)
        if not search:
            print("'{0}' | '{1}' file doesn't match '{2}' pattern!".format(inspect.getmodulename(__file__),
                                                                           texture,
                                                                           input_method.title()))
            continue

        if input_method == "udim":
            udim = [int(value[1:]) for value in search.group(0).split("_")]
        elif input_method == "patch":
            udim = get_udim_from_patch(int(search.group(0)))

        udim = offset_udim(udim, -1) if input == "mudbox" else udim
        udim = offset_udim(udim, 1) if output == "mudbox" else udim

        if output_method == "udim":
            output_affix = "u{0}_v{1}".format(*udim)
        elif output_method == "patch":
            output_affix = get_patch_from_udim(udim)

        if prefix is not None:
            path = os.path.join(os.path.dirname(texture), "{0}{1}{2}".format(prefix,
                                                                             output_affix,
                                                                             os.path.splitext(texture)[-1]))
        else:
            path = os.path.join(os.path.dirname(texture), re.sub(
                r"({0})".format(pattern), str(output_affix), basename))

        textures_mapping.append((texture, path))

    return textures_mapping


def get_command_line_parameters_parser():
    """
    Returns the command line parameters parser.

    :return: Parser.
    :rtype: Parser
    """

    parser = optparse.OptionParser(formatter=optparse.IndentedHelpFormatter(indent_increment=2,
                                                                            max_help_position=8,
                                                                            width=128,
                                                                            short_first=1),
                                   add_help_option=None)

    parser.add_option("-h",
                      "--help",
                      action="help",
                      help="'Display this help message and exit.'")
    parser.add_option("-i",
                      "--input",
                      action="store",
                      type="string",
                      dest="input",
                      default="zbrush",
                      help="'Input textures format ( mari, zbrush, mudbox )'.")
    parser.add_option("-o",
                      "--output",
                      action="store",
                      type="string",
                      dest="output",
                      default="mari",
                      help="'Output textures format ( mari, zbrush, mudbox )'.")
    parser.add_option("-n",
                      "--name",
                      action="store",
                      type="string",
                      dest="name",
                      help="'Name prefix ( \"\" to strip name ).")
    parser.add_option("-p",
                      "--preview",
                      action="store_true",
                      default=False,
                      dest="preview",
                      help="'Preview changes only.")

    return parser


def rename_textures(textures, input="zbrush", output="mari", prefix=None, preview=False):
    """
    Renames given textures.

    :param textures: Textures.
    :type textures: list
    :param input: Input format ( "mari", "mudbox", "zbrush" ).
    :type input: str
    :param output: Output format ( "mari", "mudbox", "zbrush" ).
    :type output: str
    :param prefix: Rename prefix.
    :type prefix: str
    :param preview: Only preview changes.
    :type preview: bool
    :return: Definition success.
    :rtype: bool
    """

    for source, target in get_textures_names(textures, input, output, prefix):
        if not os.path.exists(source):
            print("'{0}' | '{1}' file doesn't exists!".format(inspect.getmodulename(__file__), source))
            continue

        print("'{0}' | {1} '{2}' texture to '{3}'.".format(
            inspect.getmodulename(__file__), "Rename ('Preview')" if preview else "Rename", source, target))
        not preview and os.rename(source, target)

    return True


if __name__ == "__main__":
    if "*" in sys.argv[-1]:
        sys.argv[-1:] = glob.glob(sys.argv[-1])

    parameters, arguments = get_command_line_parameters_parser().parse_args(sys.argv)
    rename_textures([os.path.join(os.getcwd(), texture) for texture in arguments[1:]],
                    parameters.input.lower(),
                    parameters.output.lower(),
                    parameters.name,
                    parameters.preview)