#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**********************************************************************************************************************
#
# Copyright (C) 2009 - 2014 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#**********************************************************************************************************************

"""
**Common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	UI common Module.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import platform
import maya.OpenMayaUI as OpenMayaUI
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sip

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.verbose
from snippets.globals.constants import Constants
from snippets.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getResourcePath(name):
	"""
	Returns the resource file path matching the given name.

	:param name: Resource name.
	:type name: str
	:return: Resource path.
	:rtype: str
	"""

	if not foundations.common.pathExists(RuntimeGlobals.resourcesDirectory):
		return

	path = os.path.join(RuntimeGlobals.resourcesDirectory, name)
	if foundations.common.pathExists(path):
		LOGGER.debug("> '{0}' resource path: '{1}'.".format(name, path))
		return path

def parentsWalker(object):
	"""
	Defines a generator used to retrieve the chain of parents of the given :class:`QObject` instance.

	:param object: Provided path.
	:type object: QObject
	:yield: Object parent. ( QObject )
	"""

	while object.parent():
		object = object.parent()
		yield object

def getMayaWindow():
	"""
	Returns Maya window as QObject.

	:return: Maya window.
	:rtype: QObject
	"""

	pointer = OpenMayaUI.MQtUtil.mainWindow()
	return sip.wrapinstance(long(pointer), QObject)

def messageBox(messageType, title, message):
	"""
	Provides a fast gui message box.

	:param messageType: Message type.
	:type messageType: str
	:param title: Message box title.
	:type title: str
	:param message: Message content.
	:type message: str
	"""

	LOGGER.debug("> Launching messagebox().")
	LOGGER.debug("> Message type: '%s'.", messageType)
	LOGGER.debug("> Title: '%s'.", title)
	LOGGER.debug("> Message: '%s'.", message)

	messageBox = QMessageBox()
	messageBox.setWindowTitle("Message | " + title)
	messageBox.setText(message)

	if messageType == "Critical":
		messageBox.setIcon(QMessageBox.Critical)
		LOGGER.critical("'%s'.", "MessageBox | " + message)
	elif messageType == "Error":
		messageBox.setIcon(QMessageBox.Critical)
		LOGGER.error("'%s'.", "MessageBox | " + message)
	elif messageType == "Warning":
		messageBox.setIcon(QMessageBox.Warning)
		LOGGER.warning("'%s'.", "MessageBox | " + message)
	elif messageType == "Information":
		messageBox.setIcon(QMessageBox.Information)
		LOGGER.info("'%s'.", "MessageBox | " + message)

	messageBox.setWindowFlags(Qt.WindowStaysOnTopHint)

	if platform.system() == "Linux":
		messageBox.show()
		centerWidgetOnScreen(messageBox)

	messageBox.exec_()

def centerWidgetOnScreen(widget):
	"""
	Centers given Widget middle of the screen.

	:param widget: Current Widget.
	:type widget: QWidget
	"""

	widget.move(QApplication.desktop().width() / 2 - widget.width() / 2, QApplication.desktop().height() / 2 - widget.height() / 2)

def resizeWidget(widget, sizeX, sizeY):
	"""
	Resize given Widget.

	:param widget: Current Widget.
	:type widget: QWidget
	:param sizeX: Size x.
	:type sizeX: int
	:param sizeY: Size y.
	:type sizeY: int
	"""

	widget.resize(int(sizeX), int(sizeY))
