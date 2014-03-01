#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**renameTextures.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :def:`getTexturesNames` and :def:`renameTextures` definitions and other related objects.

**Others:**
"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import doctest
import glob
import inspect
import os
import optparse
import sys
import re

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["UDIM_PATTERN",
		"PATCH_PATTERN",
		"getPatchFromUdim",
		"getUdimFromPatch",
		"getTexturesNames",
		"getCommandLineParametersParser",
		"renameTextures"]

UDIM_PATTERN = "u\d+_v\d+"
PATCH_PATTERN = "\d{4,}"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getPatchFromUdim(udim):
	"""
	Returns the patch from given udim.

	Usage::

		>>> getPatchFromUdim((0, 0)) # doctest: +NORMALIZE_WHITESPACE
		1001	
		>>> getPatchFromUdim((9, 0))
		1010
		>>> getPatchFromUdim((0, 1))
		1011
		>>> getPatchFromUdim((9, 1))
		1020
		>>> getPatchFromUdim((9, 9))
		1100

	:param udim: Udim to convert. ( Tuple )
	:return: Patch. ( Integer )
	"""

	return 1000 + udim[0] + 1 + udim[1] * 10

def getUdimFromPatch(patch):
	"""
	Returns the udim from given patch.

	Usage::

		>>> getUdimFromPatch(1001) # doctest: +NORMALIZE_WHITESPACE
		(0, 0)
		>>> getUdimFromPatch(1010)
		(9, 0)
		>>> getUdimFromPatch(1011)
		(0, 1)
		>>> getUdimFromPatch(1020)
		(9, 1)
		>>> getUdimFromPatch(1100)
		(9, 9)

	:param udim: Patch to convert. ( Integer )
	:return: Udim. ( String )
	"""

	u = (patch - 1000) % 10
	v = (patch - 1000) / 10
	return 9 if u == 0 else u - 1, v - 1 if u % 10 == 0 else v

def getTexturesNames(textures, input="zbrush", output="mari", prefix=None):
	"""
	Renames given textures.

	Usage::

		>>> getTexturesNames(["Diffuse_u0_v0.exr", "Diffuse_u9_v0.exr"]) # doctest: +NORMALIZE_WHITESPACE
		[('Diffuse_u0_v0.exr', 'Diffuse_1001.exr'), ('Diffuse_u9_v0.exr', 'Diffuse_1010.exr')]
		>>> getTexturesNames(["Diffuse_u0_v0.exr", "Diffuse_u9_v0.exr"], "zbrush", "mudbox")
		[('Diffuse_u9_v0.exr', 'Diffuse_u10_v1.exr'), ('Diffuse_u0_v0.exr', 'Diffuse_u1_v1.exr')]
		>>> getTexturesNames(["Diffuse_1001.exr", "Diffuse_1010.exr"], "mari", "zbrush")
		[('Diffuse_1001.exr', 'Diffuse_u0_v0.exr'), ('Diffuse_1010.exr', 'Diffuse_u9_v0.exr')]
		>>> getTexturesNames(["Diffuse_1001.exr", "Diffuse_1010.exr"], "mari", "mudbox")
		[('Diffuse_1001.exr', 'Diffuse_u1_v1.exr'), ('Diffuse_1010.exr', 'Diffuse_u10_v1.exr')]
		>>> getTexturesNames(["Diffuse_u0_v0.exr", "Diffuse_u9_v0.exr"], prefix=str())
		[('Diffuse_u0_v0.exr', '1001.exr'), ('Diffuse_u9_v0.exr', '1010.exr')]
		>>> getTexturesNames(["Diffuse_u0_v0.exr", "Diffuse_u9_v0.exr"], prefix="Color_")
		[('Diffuse_u0_v0.exr', 'Color_1001.exr'), ('Diffuse_u9_v0.exr', 'Color_1010.exr')]

	:param textures: Textures. ( List )
	:param input: Input format ( "mari", "mudbox", "zbrush" ). ( String )
	:param output: Output format ( "mari", "mudbox", "zbrush" ). ( String )
	:param prefix: Rename prefix. ( String )
	:return: Converted textures names. ( List )
	"""

	inputMethod = "udim" if input in ("mudbox", "zbrush") else "patch"
	outputMethod = "udim" if output in ("mudbox", "zbrush") else "patch"
	pattern = UDIM_PATTERN if inputMethod == "udim" else PATCH_PATTERN

	offsetUdim = lambda x, y: (x[0] + y, x[1] + y)

	if input == "zbrush" and output == "mudbox":
		textures = reversed(textures)

	texturesMapping = []
	for texture in textures:
		basename = os.path.basename(texture)
		search = re.search(r"({0})".format(pattern), basename)
		if not search:
			print("'{0}' | '{1}' file doesn't match '{2}' pattern!".format(inspect.getmodulename(__file__),
																		texture,
																		inputMethod.title()))
	 		continue

		if inputMethod == "udim":
		 	udim = [int(value[1:]) for value in search.group(0).split("_")]
		elif inputMethod == "patch":
			udim = getUdimFromPatch(int(search.group(0)))

		udim = offsetUdim(udim, -1) if input == "mudbox" else udim
		udim = offsetUdim(udim, 1) if output == "mudbox" else udim

		if outputMethod == "udim":
		 	outputAffix = "u{0}_v{1}".format(*udim)
		elif outputMethod == "patch":
			outputAffix = getPatchFromUdim(udim)

		if prefix is not None:
		 	path = os.path.join(os.path.dirname(texture), "{0}{1}{2}".format(prefix,
																			outputAffix,
																			os.path.splitext(texture)[-1]))
		else:			
			path = os.path.join(os.path.dirname(texture), re.sub(r"({0})".format(pattern), str(outputAffix), basename))

		texturesMapping.append((texture, path))

	return texturesMapping

def getCommandLineParametersParser():
	"""
	Returns the command line parameters parser.

	:return: Parser. ( Parser )
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

def renameTextures(textures, input="zbrush", output="mari", prefix=None, preview=False):
	"""
	Renames given textures.

	:param textures: Textures. ( List )
	:param input: Input format ( "mari", "mudbox", "zbrush" ). ( String )
	:param output: Output format ( "mari", "mudbox", "zbrush" ). ( String )
	:param prefix: Rename prefix. ( String )
	:param preview: Only preview changes. ( Boolean )
	:return: Definition success. ( Boolean )
	"""

	for source, target in getTexturesNames(textures, input, output, prefix):
		if not os.path.exists(source):
			print("'{0}' | '{1}' file doesn't exists!".format(inspect.getmodulename(__file__), source))
			continue

		print("'{0}' | {1} '{2}' texture to '{3}'.".format(
		inspect.getmodulename(__file__), "Rename ('Preview')" if preview else "Rename", source, target))
		not preview and os.rename(source, target)

	return True

#**********************************************************************************************************************
#*** Launcher.
#**********************************************************************************************************************
if __name__ == "__main__":
	if "*" in sys.argv[-1]:
		sys.argv[-1:] = glob.glob(sys.argv[-1])

	parameters, arguments = getCommandLineParametersParser().parse_args(sys.argv)
	renameTextures([os.path.join(os.getcwd(), texture) for texture in arguments[1:]],
					parameters.input.lower(),
					parameters.output.lower(),
					parameters.name,
					parameters.preview)
