#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2009 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	Common.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***      	UI Common Module.
***
***	Others:
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import logging
import platform
import maya.OpenMayaUI as OpenMayaUI
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sip

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
from globals.constants import Constants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger( Constants.logger )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
@core.executionTrace
def getMayaWindow():
	'''
	This Method Returns Maya Window As QObject.

	@return: Maya Window. ( QObject )
	'''

	pointer = OpenMayaUI.MQtUtil.mainWindow()
	return sip.wrapinstance( long( pointer ), QObject )

@core.executionTrace
def messageBox( messageType, title, message ):
	'''
	This Definition Provides A Fast GUI Message Box.
	
	@param messageType: Message Type. ( String )
	@param title: Message Box Title. ( String )
	@param message: Message Content. ( String )
	'''

	LOGGER.debug( "> Launching messageBox()." )
	LOGGER.debug( "> Message Type: '%s'.", messageType )
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
	'''
	This Definition Centers The Provided Widget Middle Of The Screen.
	
	@param widget: Current Widget. ( QWidget )
	'''

	widget.move( QApplication.desktop().width() / 2 - widget.width() / 2, QApplication.desktop().height() / 2 - widget.height() / 2 )

@core.executionTrace
def resizeWidget( widget, size_x, size_y ):
	'''
	This Definition Resize The Provided Widget.
	
	@param widget: Current Widget. ( QWidget )
	@param size_x: Size X. ( Integer )
	@param size_y: Size Y. ( Integer )
	'''

	widget.resize( int( size_x ), int( size_y ) )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
