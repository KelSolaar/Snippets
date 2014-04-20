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
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["GLOB_FILTER", "OUTPUT_FILE_FORMAT", "SHELLS_FILTER", "get_splitext_basename", "getUVsShellsSiblingsTrees", "combineImagesWithUVsShellsIdentifiers"]

GLOB_FILTER = "tif"
OUTPUT_FILE_FORMAT = "tif"
SHELLS_FILTER = "u[0-9]+_v[0-9]+"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def _getUVsShellsSiblings(elements, filter=SHELLS_FILTER):
	"""
	Gets UVs shells siblings from given elements.

	:param elements: Elements to filter.
	:type elements: list
	:param filter: Shells identifier regex filter.
	:type filter: str
	:return: UVs shells siblings.
	:rtype: dict
	"""

	uvsShellsSiblings = {}
	for element in elements:
		search = re.search(r"({0})".format(filter), element)
		if not search:
			continue

		uvShell = search.group(0)
		name = get_splitext_basename(element)
		if uvShell not in uvsShellsSiblings:
			uvsShellsSiblings[uvShell] = {name:element}
		else:
			uvsShellsSiblings[uvShell][name] = element
	return uvsShellsSiblings

def _getReadNode(name="", file=None):
	"""
	Gets a Nuke **Read** node.

	:param name: Node name.
	:type name: str
	:param file: Node file parameter.
	:type file: str
	:return: Read node.
	:rtype: Node
	"""

	return nuke.nodes.Read(file=file, name="{0}_Read".format(name))

def _getMerge2Node(name="", nodes=None, useMask=True):
	"""
	Gets a Nuke **Merge2** node.

	:param name: Node name.
	:type name: str
	:param nodes: Inputs nodes list.
	:type nodes: list
	:param useMask: Input mask slot will be connected.
	:type useMask: bool
	:return: Merge2 node.
	:rtype: Node
	"""

	merge = nuke.nodes.Merge2(name="{0}_Merge".format(name))

	nodes = not nodes and [] or list(nodes)
	not useMask and len(nodes) >= 2 and nodes.insert(2, None)
	for i, node in enumerate(nodes):
		merge.setInput(i, node)
	return merge

def _getWriteNode(name="", file=None, node=None):
	"""
	Gets a Nuke **Write** node.

	:param name: Node name.
	:type name: str
	:param file: Node file parameter.
	:type file: str
	:param node: Input node.
	:type node: Node
	:return: Write node.
	:rtype: Node
	"""

	write = nuke.nodes.Write(file=file, name="{0}_Write".format(name))
	write.setInput(0, node)
	return write

def get_splitext_basename(path):
	"""
	Gets the basename of a path without its extension.

	:param path: Path to extract the basename without extension.
	:type path: str
	:return: Splitext basename.
	:rtype: str
	"""

	basename = os.path.splitext(os.path.basename(os.path.normpath(path)))[0]
	return basename

def getUVsShellsSiblingsTrees(elements, output_directory, output_fileFormat, outputPrefix=""):
	"""
	This gets UVs shells siblings trees.

	:param elements: Elements to get UVs shells trees siblings from.
	:type elements: list
	:param output_directory: Write nodes output directory.
	:type output_directory: str
	:param output_fileFormat: Write nodes output format.
	:type output_fileFormat: str
	:param outputPrefix: Write nodes output prefix.
	:type outputPrefix: str
	:return: Write nodes.
	:rtype: list
	"""

	writes = []
	for shell, siblings in _getUVsShellsSiblings(elements).items():
		files = []
		for name, sibling in siblings.items():
			files.append(_getReadNode(name, sibling))

		merge = _getMerge2Node(shell, files, useMask=False)
		writes.append(_getWriteNode(shell, os.path.join(output_directory, "{0}{1}.{2}".format(outputPrefix, shell, output_fileFormat)), merge))
	return writes

def combineImagesWithUVsShellsIdentifiers():
	"""
	Combines images with UVs shells identifiers.

	:return: Definition success.
	:rtype: bool
	"""

	directory = nuke.getFilename("Choose a directory containing images with UVs shells identifiers to combine!", multiple=False)
	if not directory: return
	if not os.path.exists(directory): return

	directory = os.path.isfile(directory) and os.path.dirname(directory) or directory
	files = glob.glob("{0}/*{1}".format(directory, GLOB_FILTER))

	return getUVsShellsSiblingsTrees(files, directory, OUTPUT_FILE_FORMAT) and True or False
