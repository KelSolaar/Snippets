#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**toAlembic.py**

**Platform:**
	Windows.

**Description:**
	This module exports given scene to Alembic using Maya.
	
	Usage::

		alias toAlembic 'setenv MAYA_LOCATION /software/maya/2013/linux.centos6.x86_64 && $MAYA_LOCATION/bin/mayapy "/usr/people/thomas-ma/Developement/Snippets/src/others/toAlembic.py"'
		
		toAlembic -i myFile.obj
		
**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import maya.standalone

maya.standalone.initialize(name="python")

import inspect
import maya.cmds as cmds
import optparse
import os
import re
import sys

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["ascendantsWalker" , "getRoot", "toAlembic", "getCommandLineParameters"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def ascendantsWalker(path, visitor=None):
	"""
	This definition returns the parents of given Dag path.
	
	:param path: Dag path. ( String )
	:param visitor: Visitor. ( Object )
	:return: Parent. ( String )
	"""

	parents = cmds.listRelatives(path, allParents=True, fullPath=True)
	if not parents:
		return
	
	for parent in parents:
		visitor and visitor(parent)
		yield parent
		for value in ascendantsWalker(parent):
			yield value

def getRoot(path):
	"""
	This definition returns the root path of given Dag path.
	
	:param path: Dag path. ( String )
	:return: Root path. ( String )
	"""

	parents = list(ascendantsWalker(path))
	return parents[-1] if parents else path
	
def toAlembic(parameters, arguments):
	"""
	This definition converts an Obj file to Alembic file.
	
	:param parameters: Command line parameters. ( Object )
	:param arguments: Command line arguments. ( Object )
	:return: Definition success. ( Boolean )
	"""

	inputFile = parameters.inputFile
	if inputFile is None:
		sys.stderr.write("!> {0} | No input file provided!\n".format(inspect.getmodulename(__file__)))
		return

	if not os.path.exists(inputFile):
		sys.stderr.write("!> {0} | '{1}' file doesn't exists'!\n".format(inspect.getmodulename(__file__), inputFile))
		return

	outputFile = os.path.abspath(parameters.outputFile if parameters.outputFile else re.sub(r"\.\w+$", ".abc", inputFile))

	exportAll = parameters.exportAll

	frameRange = parameters.frameRange
	try:
		frameIn, frameOut = frameRange.split("-")
	except ValueError:
		sys.stderr.write("!> {0} | The frame range format could not be determined!\n".format(inspect.getmodulename(__file__)))
		return
	
	not cmds.pluginInfo("AbcExport", q=True, loaded=True) and cmds.loadPlugin("AbcExport")	

	cmds.file(inputFile, o=True)

	# Processing ".obj" file normals.
	if re.search(r"\.obj$", inputFile, flags=re.IGNORECASE):
		for mesh in cmds.ls(type="mesh", long=True):
			cmds.polyNormalPerVertex(mesh, ufn=True)
			cmds.polySoftEdge(mesh, a=180, ch=False)

	if exportAll:
		jobCommand = "-frameRange {0} {1} -uvWrite -file {2}".format(frameIn, frameOut, outputFile)
	else:
		rootNodes = list(set([getRoot(mesh) for mesh in cmds.ls(type="mesh", long=True)]))
		rootFlags = " ".join(["-root {0}".format(rootNode) for rootNode in rootNodes])
		jobCommand = "-frameRange {0} {1} -uvWrite {2} -file {3}".format(frameIn, frameOut, rootFlags, outputFile)
	
	sys.stderr.write("{0} | Exporting to 'Alembic' with following job command: '{1}'\n".format(inspect.getmodulename(__file__), jobCommand))
	cmds.AbcExport(j=jobCommand)
	return True

def getCommandLineParameters(argv):
	"""
	This definition returns the command line parameters parser.

	:param argv: Command line parameters. ( String )
	:return: Settings, arguments ( Parser Instance )
	"""

	argv = argv or sys.argv[1:]

	parser = optparse.OptionParser(formatter=optparse.IndentedHelpFormatter (indent_increment=2, max_help_position=8, width=128, short_first=1), add_help_option=None)

	parser.add_option("-h", "--help", action="help", help="'Display this help message and exit.'")
	parser.add_option("-i", "--inputFile", action="store", type="string", dest="inputFile", help="'Input file.")
	parser.add_option("-o", "--outputFile", action="store", type="string", dest="outputFile", help="'Output file.")
	parser.add_option("-a", "--exportAll", action="store_true", dest="exportAll", default=False, help="Export all scene.")
	parser.add_option("-r", "--frameRange", action="store", type="string", dest="frameRange", default="1-5", help="Frame range ( '1-5' ).")

	parameters, args = parser.parse_args(argv)

	return parameters, args

if __name__ == "__main__":
	parameters, arguments = getCommandLineParameters(sys.argv)
	toAlembic(parameters, arguments)
