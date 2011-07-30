#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The following code is protected by GNU GPL V3 Licence.
#

"""
**combineImagesWithUVsShellsIdentifiers.py**

**Platform:**
	Windows.

**Description:**
	Combines UVs shells siblings images.

**Others:**

"""

#***********************************************************************************************
#***	Python begin.
#***********************************************************************************************
#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import nuke
import glob
import os
import sys
import re

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************

#***********************************************************************************************
#***	Global variables.
#***********************************************************************************************
GLOB_FILTER = "tif"
OUTPUT_FILE_FORMAT = "tif"
SHELLS_FILTER = "u[0-9]+_v[0-9]+"
NAMESPACE_SPLITTER = "|"

#***********************************************************************************************
#***	Main Python code.
#***********************************************************************************************

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
def _getUVsShellsSiblings(elements, filter=SHELLS_FILTER):
	"""
	This definition gets UVs shells siblings from provided elements.
	@param elements: Elements to filter. ( List )
	@param filter: Shells identifier regex filter. ( String )
	@return: UVs shells siblings. ( Dictionary )
	"""

	uvsShellsSiblings = {}
	for element in elements:
		search = re.search("({0})".format(filter), element)
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
	This definition gets a Nuke read node.
	@param name: Node name. ( String )
	@param file: Node file parameter. ( String )
	@return: Read node. ( Node )
	"""

	return nuke.nodes.Read(file=file, name="{0}_Read".format(name))

def _getMerge2Node(name="", nodes=None, useMask=True):
	"""
	This definition gets a Nuke merge2 node.
	@param name: Node name. ( String )
	@param nodes: Inputs nodes list. ( List )
	@param useMask: Input mask slot will be connected. ( Boolean )
	@return: Merge2 node. ( Node )
	"""

	merge = nuke.nodes.Merge2(name="{0}_Merge".format(name))

	nodes = not nodes and [] or nodes
	not useMask and len(nodes) >= 2 and nodes.insert(2, None)
	for i, node in enumerate(nodes):
		merge.setInput(i, node)
	return merge

def _getWriteNode(name="", file=None, node=None):
	"""
	This definition gets a Nuke read node.
	@param name: Node name. ( String )
	@param file: Node file parameter. ( String )
	@param node: Input node. ( Node )
	@return: Write node. ( Node )
	"""

	write = nuke.nodes.Write(file=file, name="{0}_Write".format(name))
	write.setInput(0, node)
	return write

def getSplitextBasename(path):
	"""
	This definition get the basename of a path without its extension.

	@param path: Path to extract the basename without extension. ( String )
	@return: Splitext basename. ( String )
	"""

	basename = os.path.splitext(os.path.basename(os.path.normpath(path)))[0]
	return basename

def getUVsShellsSiblingsTrees(elements, outputDirectory, outputFileFormat, outputPrefix=""):
	"""
	This gets UVs shells siblings trees.

	@param elements: Elements to get UVs shells trees siblings from. ( List )
	@param outputPrefix: Write nodes output prefix. ( String )
	@param outputDirectory: Write nodes output directory. ( String )
	@param outputFileFormat: Write nodes output format. ( String )
	@return: Write nodes. ( List )
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

	@return: Definition success. ( List )
	"""

	directory = nuke.getFilename("Choose a directory containing images with UVs shells identifiers to combine!", multiple=False)
	if not directory: return
	if not os.path.exists(directory): return

	directory = os.path.isfile(directory) and os.path.dirname(directory) or directory
	files = glob.glob("{0}/*{1}".format(directory, GLOB_FILTER))

	return getUVsShellsSiblingsTrees(files, directory, OUTPUT_FILE_FORMAT) and True or False

#***********************************************************************************************
#***	Python end.
#***********************************************************************************************

