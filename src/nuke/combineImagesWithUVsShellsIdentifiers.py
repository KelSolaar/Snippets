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
# The Following Code Is Protected By GNU GPL V3 Licence.
#

"""
**combineImagesWithUVsShellsIdentifiers.py**

**Platform:**
	Windows.

**Description:**
	Combines UVs Shells Siblings Images.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin.
#***********************************************************************************************
#***********************************************************************************************
#***	External Imports.
#***********************************************************************************************
import nuke
import glob
import os
import sys
import re

#***********************************************************************************************
#***	Internal Imports.
#***********************************************************************************************

#***********************************************************************************************
#***	Global Variables.
#***********************************************************************************************
GLOB_FILTER = "tif"
OUTPUT_FILE_FORMAT = "tif"
SHELLS_FILTER = "u[0-9]+_v[0-9]+"
NAMESPACE_SPLITTER = "|"

#***********************************************************************************************
#***	Main Python Code.
#***********************************************************************************************

#***********************************************************************************************
#***	Module Classes And Definitions.
#***********************************************************************************************
def _getUVsShellsSiblings(elements, filter=SHELLS_FILTER):
	"""
	This Definition Gets UVs Shells Siblings From Provided Elements.
	@param elements: Elements To Filter. ( List )
	@param filter: Shells Identifier Regex Filter. ( String )
	@return: UVs Shells Siblings. ( Dictionary )
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
	This Definition Gets A Nuke Read Node.
	@param name: Node Name. ( String )
	@param file: Node File Parameter. ( String )
	@return: Read Node. ( Node )
	"""

	return nuke.nodes.Read(file=file, name="{0}_Read".format(name))

def _getMerge2Node(name="", nodes=None, useMask=True):
	"""
	This Definition Gets A Nuke Merge2 Node.
	@param name: Node Name. ( String )
	@param nodes: Inputs Nodes List. ( List )
	@param useMask: Input Mask Slot Will Be Connected. ( Boolean )
	@return: Merge2 Node. ( Node )
	"""

	merge = nuke.nodes.Merge2(name="{0}_Merge".format(name))

	nodes = not nodes and [] or nodes
	not useMask and len(nodes) >= 2 and nodes.insert(2, None)
	for i, node in enumerate(nodes):
		merge.setInput(i, node)
	return merge

def _getWriteNode(name="", file=None, node=None):
	"""
	This Definition Gets A Nuke Read Node.
	@param name: Node Name. ( String )
	@param file: Node File Parameter. ( String )
	@param node: Input Node. ( Node )
	@return: Write Node. ( Node )
	"""

	write = nuke.nodes.Write(file=file, name="{0}_Write".format(name))
	write.setInput(0, node)
	return write

def getSplitextBasename(path):
	"""
	This Definition Get The Basename Of A Path Without Its Extension.

	@param path: Path To Extract The Basename Without Extension. ( String )
	@return: Splitext Basename. ( String )
	"""

	basename = os.path.splitext(os.path.basename(os.path.normpath(path)))[0]
	return basename

def getUVsShellsSiblingsTrees(elements, outputDirectory, outputFileFormat, outputPrefix=""):
	"""
	This Gets UVs Shells Siblings Trees.
	
	@param elements: Elements To Get UVS Shells Trees Siblings From. ( List )
	@param outputPrefix: Write Nodes Output Prefix. ( String )
	@param outputDirectory: Write Nodes Output Directory. ( String )
	@param outputFileFormat: Write Nodes Output Format. ( String )
	@return: Write Nodes. ( List )
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
	This Definition Combines Images With UVs Shells Identifiers.
	
	@return: Definition Success. ( List )
	"""

	directory = nuke.getFilename("Choose A Directory Containing Images With UVs Shells Identifiers To Combine!", multiple=False)
	if not directory: return
	if not os.path.exists(directory): return

	directory = os.path.isfile(directory) and os.path.dirname(directory) or directory
	files = glob.glob("{0}/*{1}".format(directory, GLOB_FILTER))

	return getUVsShellsSiblingsTrees(files, directory, OUTPUT_FILE_FORMAT) and True or False

#***********************************************************************************************
#***	Python End.
#***********************************************************************************************

