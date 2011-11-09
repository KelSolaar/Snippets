#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**combineImagesWithUVsShellsIdentifiers.py**

**Platform:**
	Windows.

**Description:**
	Combines UVs shells siblings images.

**Others:**
	TODO: Refactor _get'Nuke'Node using \*\*kwargs for optional arguments.
"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import glob
import nuke
import os
import sys
import re

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["GLOB_FILTER", "OUTPUT_FILE_FORMAT", "SHELLS_FILTER", "getSplitextBasename", "getUVsShellsSiblingsTrees", "combineImagesWithUVsShellsIdentifiers"]

GLOB_FILTER = "tif"
OUTPUT_FILE_FORMAT = "tif"
SHELLS_FILTER = "u[0-9]+_v[0-9]+"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def _getUVsShellsSiblings(elements, filter=SHELLS_FILTER):
	"""
	This definition gets UVs shells siblings from given elements.

	:param elements: Elements to filter. ( List )
	:param filter: Shells identifier regex filter. ( String )
	:return: UVs shells siblings. ( Dictionary )
	"""

	uvsShellsSiblings = {}
	for element in elements:
		search = re.search(r"({0})".format(filter), element)
		if not search:
			continue

		uvShell = search.group(0)
		name = getSplitextBasename(element)
		if uvShell not in uvsShellsSiblings.keys():
			uvsShellsSiblings[uvShell] = {name:element}
		else:
			uvsShellsSiblings[uvShell][name] = element
	return uvsShellsSiblings

def _getReadNode(name="", file=None):
	"""
	This definition gets a Nuke **Read** node.

	:param name: Node name. ( String )
	:param file: Node file parameter. ( String )
	:return: Read node. ( Node )
	"""

	return nuke.nodes.Read(file=file, name="{0}_Read".format(name))

def _getMerge2Node(name="", nodes=None, useMask=True):
	"""
	This definition gets a Nuke **Merge2** node.

	:param name: Node name. ( String )
	:param nodes: Inputs nodes list. ( List )
	:param useMask: Input mask slot will be connected. ( Boolean )
	:return: Merge2 node. ( Node )
	"""

	merge = nuke.nodes.Merge2(name="{0}_Merge".format(name))

	nodes = not nodes and [] or list(nodes)
	not useMask and len(nodes) >= 2 and nodes.insert(2, None)
	for i, node in enumerate(nodes):
		merge.setInput(i, node)
	return merge

def _getWriteNode(name="", file=None, node=None):
	"""
	This definition gets a Nuke **Write** node.

	:param name: Node name. ( String )
	:param file: Node file parameter. ( String )
	:param node: Input node. ( Node )
	:return: Write node. ( Node )
	"""

	write = nuke.nodes.Write(file=file, name="{0}_Write".format(name))
	write.setInput(0, node)
	return write

def getSplitextBasename(path):
	"""
	This definition gets the basename of a path without its extension.

	:param path: Path to extract the basename without extension. ( String )
	:return: Splitext basename. ( String )
	"""

	basename = os.path.splitext(os.path.basename(os.path.normpath(path)))[0]
	return basename

def getUVsShellsSiblingsTrees(elements, outputDirectory, outputFileFormat, outputPrefix=""):
	"""
	This gets UVs shells siblings trees.

	:param elements: Elements to get UVs shells trees siblings from. ( List )
	:param outputDirectory: Write nodes output directory. ( String )
	:param outputFileFormat: Write nodes output format. ( String )
	:param outputPrefix: Write nodes output prefix. ( String )
	:return: Write nodes. ( List )
	"""

	writes = []
	for shell, siblings in _getUVsShellsSiblings(elements).items():
		files = []
		for name, sibling in siblings.items():
			files.append(_getReadNode(name, sibling))

		merge = _getMerge2Node(shell, files, useMask=False)
		writes.append(_getWriteNode(shell, os.path.join(outputDirectory, "{0}{1}.{2}".format(outputPrefix, shell, outputFileFormat)), merge))
	return writes

def combineImagesWithUVsShellsIdentifiers():
	"""
	This definition combines images with UVs shells identifiers.

	:return: Definition success. ( Boolean )
	"""

	directory = nuke.getFilename("Choose a directory containing images with UVs shells identifiers to combine!", multiple=False)
	if not directory: return
	if not os.path.exists(directory): return

	directory = os.path.isfile(directory) and os.path.dirname(directory) or directory
	files = glob.glob("{0}/*{1}".format(directory, GLOB_FILTER))

	return getUVsShellsSiblingsTrees(files, directory, OUTPUT_FILE_FORMAT) and True or False
