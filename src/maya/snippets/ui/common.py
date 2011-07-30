#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2009 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**Common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	UI common Module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import platform
import maya.OpenMayaUI as OpenMayaUI
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sip

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
from snippets.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
def getMayaWindow():
	"""
	This method returns Maya window as QObject.

	@return: Maya window. ( QObject )
	"""

	pointer = OpenMayaUI.MQtUtil.mainWindow()
	return sip.wrapinstance( long( pointer ), QObject )

@core.executionTrace
def messageBox( messageType, title, message ):
	"""
	This definition provides a fast gui message box.

	@param messageType: Message type. ( String )
	@param title: Message box title. ( String )
	@param message: Message content. ( String )
	"""

	LOGGER.debug( "> Launching messagebox()." )
	LOGGER.debug( "> Message type: '%s'.", messageType )
	LOGGER.debug( "> Title: '%s'.", title )
	LOGGER.debug( "> Message: '%s'.", message )

	messageBox = QMessageBox()
	messageBox.setWindowTitle( "Message | " + title )
	messageBox.setText( message )

	if messageType == "Critical":
		messageBox.setIcon( QMessageBox.Critical )
		LOGGER.critical( "'%s'.", "MessageBox | " + message )
	elif messageType == "Error":
		messageBox.setIcon( QMessageBox.Critical )
		LOGGER.error( "'%s'.", "MessageBox | " + message )
	elif messageType == "Warning":
		messageBox.setIcon( QMessageBox.Warning )
		LOGGER.warning( "'%s'.", "MessageBox | " + message )
	elif messageType == "Information":
		messageBox.setIcon( QMessageBox.Information )
		LOGGER.info( "'%s'.", "MessageBox | " + message )

	messageBox.setWindowFlags( Qt.WindowStaysOnTopHint )

	if platform.system() == "Linux":
		messageBox.show()
		centerWidgetOnScreen( messageBox )

	messageBox.exec_()

@core.executionTrace
def centerWidgetOnScreen( widget ):
	"""
	This definition centers the provided Widget middle of the screen.

	@param widget: Current Widget. ( QWidget )
	"""

	widget.move( QApplication.desktop().width() / 2 - widget.width() / 2, QApplication.desktop().height() / 2 - widget.height() / 2 )

@core.executionTrace
def resizeWidget( widget, size_x, size_y ):
	"""
	This definition resize the provided Widget.

	@param widget: Current Widget. ( QWidget )
	@param size_x: Size x. ( Integer )
	@param size_y: Size y. ( Integer )
	"""

	widget.resize( int( size_x ), int( size_y ) )

