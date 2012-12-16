#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**renameTextures.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**

**Others:**
"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
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
__copyright__ = "Copyright (C) 2010 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["UDIM_PATTERN", "PATCH_PATTERN", "getPatchFromUdim", "getCommandLineParametersParser", "renameTextures"]

UDIM_PATTERN = "u\d+_v\d+"
PATCH_PATTERN = "\d{4,}"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getPatchFromUdim(udim):
	"""
	This definition returns the patch from given udim.

	:param udim: Udim to convert. ( String )
	:return: Patch. ( Integer )
	"""

	return 1000 + udim[0] + 1 + udim[1] * 10 

def getUdimFromPatch(patch):
	"""
	This definition returns the udim from given patch.

	:param udim: Patch to convert. ( Integer )
	:return: Udim. ( String )
	"""

	u = (patch - 1000) % 10
	u = 10 if u == 0 else u
	v = (patch - 1000) / 10
	return u - 1, v

def getCommandLineParametersParser():
	"""
	This definition returns the command line parameters parser.

	:return: Parser. ( Parser )
	"""

	parser = optparse.OptionParser(formatter=optparse.IndentedHelpFormatter (indent_increment=2, max_help_position=8, width=128, short_first=1), add_help_option=None)

	parser.add_option("-h", "--help", action="help", help="'Display this help message and exit.'")
	parser.add_option("-i", "--input", action="store", type="string", dest="input", default="zbrush", help="'Input format'.")
	parser.add_option("-o", "--output", action="store", type="string", dest="output", default="mari", help="'Output format'.")
	parser.add_option("-n", "--name", action="store", type="string", dest="name", help="'Name prefix.")
	parser.add_option("-p", "--preview", action="store_true", default=False, dest="preview", help="'Preview changes only.")
	
	return parser

def renameTextures(files, input="zbrush", output="mari", prefix=None, preview=False):
	"""
	This definition renames given textures.

	:param files: Files. ( List )
	:param input: Input format ( "mari", "mudbox", "zbrush" ). ( List )
	:param output: Output format ( "mari", "mudbox", "zbrush" ). ( List )
	:param prefix: Rename prefix. ( String )
	:param preview: Only preview changes. ( Boolean )
	:return: Definition success. ( Boolean )
	"""

	inputMethod = "udim" if input in ("mudbox", "zbrush") else "patch"
	outputMethod = "udim" if output in ("mudbox", "zbrush") else "patch"
	pattern = UDIM_PATTERN if inputMethod == "udim" else PATCH_PATTERN

	offsetUdim = lambda x, y: (x[0] + y, x[1] + y)

	if input == "zbrush" and output == "mudbox":
		files = reversed(files)

	for file in files:
		if not os.path.exists(file):
			print("'{0}' | '{1}' file doesn't exists!".format(inspect.getmodulename(__file__), file))
			continue

		search = re.search(r"({0})".format(pattern), file)
		if not search:
			print("'{0}' | '{1}' file doesn't match '{2}' pattern!".format(inspect.getmodulename(__file__), file, inputMethod.title()))
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
		 	path = os.path.join(os.path.dirname(file), "{0}{1}{2}".format(prefix, outputAffix, os.path.splitext(file)[-1]))
		else:
			path = re.sub(r"({0})".format(pattern), str(outputAffix), file)
		
		print("'{0}' | {1} '{2}' file to '{3}'.".format(
		inspect.getmodulename(__file__), "Rename ('Preview')" if preview else "Rename", file, path,))
		not preview and os.rename(file, path)
	return True

#**********************************************************************************************************************
#*** Launcher.
#**********************************************************************************************************************
if __name__ == "__main__":
	parameters, arguments = getCommandLineParametersParser().parse_args(sys.argv)
	renameTextures([os.path.join(os.getcwd(), file) for file in arguments[1:]],
					parameters.input.lower(),
					parameters.output.lower(),
					parameters.name,
					parameters.preview)
