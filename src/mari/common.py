#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2009 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**loader.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Loader Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import inspect
import mari
import os
from PythonQt.QtCore import *
from PythonQt.QtGui import *

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["fillPaintBuffer", "projectColor", "projectBlack", "projectWhite"]

def fillPaintBuffer(color):
	"""
	This definition fills the paint buffer with provided color.
	
	:param color: Color. ( QColor )
	:return: Definition success. ( Boolean )
	"""

	paintBuffer = mari.canvases.paintBuffer()
	image = paintBuffer.getPaint()
	image.fill(color.rgba())
	paintBuffer.setPaint(image)
	return True

def projectColor(color):
	"""
	This definition projects the provided color.
	
	:param color: Color. ( QColor )
	:return: Definition success. ( Boolean )
	"""

	if fillPaintBuffer(color):
		mari.canvases.paintBuffer().bakeAndClear()
		return True

def projectBlack():
	"""
	This definition projects black color.

	:return: Definition success. ( Boolean )
	"""

	return projectColor(QColor(0, 0, 0,255))

def projectWhite():
	"""
	This definition projects white color.

	:return: Definition success. ( Boolean )
	"""

	return projectColor(QColor(255, 255, 255,255))

def getSelectedPatches():
	"""
	This definition returns current selected patches.

	:return: Selected patches. ( List )
	"""

	patches = []
	for patch in mari.geo.current().patches():
    		if patch.isSelected():
			patches.append(patch.name())
	return sorted(patches)

def displaySelectedPatches():
	"""
	This definition displays current selected patches.

	:return: Definition success. ( Boolean )
	"""
	
	patches = getSelectedPatches()
	print "%s | Current object: '%s'" % (inspect.getmodulename(__file__), mari.geo.current().name())
	print "%s | Selected patches: '%s'" % (inspect.getmodulename(__file__), patches)
	mari.utils.misc.message("Current object: '%s'\nSelected patches: '%s'" % (mari.geo.current().name(), ", ".join(patches)), title="Current Object Selected Patches")
	return True

mari.menus.addAction(mari.actions.create("Show Selected Patches ...", "import common;reload(common);common.displaySelectedPatches()"), "MainWindow/&MPC/")
mari.menus.addAction(mari.actions.create("Project Black", "import common;reload(common);common.projectBlack()"), "MainWindow/&MPC/")
mari.menus.addAction(mari.actions.create("Project White", "import common;reload(common);common.projectWhite()"), "MainWindow/&MPC/")
mari.menus.addAction(mari.actions.create("Clear History Queue ...", "mari.history.clear()"), "MainWindow/&MPC/")
