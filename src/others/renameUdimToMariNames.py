#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**renameUdimToMariNames.py**

**Platform:**
	Windows.

**Description:**
	Combines UVs shells siblings images.

**Others:**
	TODO: Refactor _get'Nuke'Node using \*\*kwargs for optional arguments.
"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import glob
import inspect
import os
import optparse
import sys
import re

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["UDIM_FILTER" , "getMariPatchNumberFromUdim", "getCommandLineParametersParser", "renameUdimToMariNames"]

UDIM_FILTER = "u\d+_v\d+"

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
def getMariPatchNumberFromUdim(udim):
	"""
	This definition gets Mari patch number from Udim.

	:param udim: Udim to convert. ( String )
	:return: Mari patch. ( Integer )
	"""

	u, v = (int(value[1:]) for value in udim.split("_"))
	return 1000 + u + 1 + v *10

def getCommandLineParametersParser():
	"""
	This definition returns the command line parameters parser.

	:return: Parser. ( Parser )
	"""

	parser = optparse.OptionParser(formatter=optparse.IndentedHelpFormatter (indent_increment=2, max_help_position=8, width=128, short_first=1), add_help_option=None)

	parser.add_option("-h", "--help", action="help", help="'Display this help message and exit.'")
	parser.add_option("-f", "--filesExtensions", action="store", type="string", dest="filesExtensions", default="psd", help="'Files extensions to rename'.")
	parser.add_option("-s", "--sourceDirectory", action="store", type="string", dest="sourceDirectory", default=os.getcwd(), help="'Source directory.")
	parser.add_option("-r", "--renamePrefix", action="store", type="string", dest="renamePrefix", help="'Rename prefix.")
	
	return parser

def renameUdimToMariNames(parameters, arguments):
	"""
	This definition renames Udim matched files to Mari patch number files.

	:param udim: Udim to convert. ( String )
	:param parameters: Command line parameters. ( Object )
	:param arguments: Command line arguments. ( Object )
	:return: Definition success. ( Boolean )
	"""

	if os.path.exists(parameters.sourceDirectory):
		files = glob.glob("{0}/*{1}".format(parameters.sourceDirectory, parameters.filesExtensions))
		for file in files:
			search = re.search(r"({0})".format(UDIM_FILTER), file)
			if not search:
				continue
			patchNumber = getMariPatchNumberFromUdim(search.group(0))
			if parameters.renamePrefix:
				name = "{0}{1}.{2}".format(parameters.renamePrefix, str(patchNumber), parameters.filesExtensions)
			else:
				name = re.sub(r"({0})".format(UDIM_FILTER), str(patchNumber), file)
			
			print("'{0}' | Rename '{1}' file to '{2}'.".format(inspect.getmodulename(__file__),file, name))
			os.rename(file, name)
		return True

#***********************************************************************************************
#*** Launcher.
#***********************************************************************************************
if __name__ == "__main__":
	parameters, arguments = getCommandLineParametersParser().parse_args(sys.argv)
	renameUdimToMariNames(parameters, arguments)
