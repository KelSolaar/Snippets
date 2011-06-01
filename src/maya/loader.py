#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2009 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	loader.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***      	Loader Module.
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
import maya.cmds as cmds
import maya.mel as mel
import os
import platform
import re
import sys
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.io as io
import foundations.strings as strings
import libraries.common
import foundations.namespace as namespace
from foundations.walker import Walker
from globals.constants import Constants
from globals.runtimeConstants import RuntimeConstants
from globals.uiConstants import UiConstants

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

# Remove Existing Handlers.
del logging.root.handlers[:]

if LOGGER.handlers == []:
	consoleHandler = libraries.common.MayaLoggingHandler()
	consoleHandler.setFormatter(core.LOGGING_FORMATTER)
	LOGGER.addHandler(consoleHandler)

RuntimeConstants.loaderUiFile = os.path.join(os.path.dirname(__file__), UiConstants.loaderUiFile)
if os.path.exists(RuntimeConstants.loaderUiFile):
	Ui_Loader_Setup, Ui_Loader_Type = uic.loadUiType(RuntimeConstants.loaderUiFile)
else:
	ui.common.messageBox("Error", "Error", "'{0}' Ui File Is Not Available!" % UiConstants.loaderUiFile)

LIBRARIES = os.path.join(os.path.dirname(__file__), Constants.librariesPath)

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Interface(core.Structure):
	'''
	This Is The Interface Class.
	'''

	@core.executionTrace
	def __init__(self, **kwargs):
		'''
		This Method Initializes The Class.

		@param kwargs: name, module. ( Key / Value Pairs )
		'''

		core.Structure.__init__(self, **kwargs)

		# --- Setting Class Attributes. ---
		self.__dict__.update(kwargs)
class Module(object):
	'''
	This Class Is The Module Class.
	'''

	@core.executionTrace
	def __init__(self, name=None, path=None):
		'''
		This Method Initializes The Class.
		
		@param name: Name Of The Component. ( String )
		@param path: Path Of The Component. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		# --- Setting Class Attributes. ---
		self._name = None
		self.name = name
		self.path = None
		self._path = path
		
		self._import = None
		self._interfaces = None

	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def name(self):
		'''
		This Method Is The Property For The _name Attribute.

		@return: self._name. ( String )
		'''

		return self._name

	@name.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def name(self, value):
		'''
		This Method Is The Setter Method For The _name Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("name", value)
		self._name = value

	@name.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def name(self):
		'''
		This Method Is The Deleter Method For The _name Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("name"))

	@property
	def path(self):
		'''
		This Method Is The Property For The _path Attribute.

		@return: self._path. ( String )
		'''

		return self._path

	@path.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def path(self, value):
		'''
		This Method Is The Setter Method For The _path Attribute.
		
		@param value: Attribute Value. ( String )
		'''

		if value:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' Type Is Not 'str' or 'unicode'!".format("path", value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' Directory Doesn't Exists!".format("path", value)
		self._path = value

	@path.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def path(self):
		'''
		This Method Is The Deleter Method For The _path Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("path"))

	@property
	def import_(self):
		'''
		This Method Is The Property For The _import_ Attribute.

		@return: self._import. ( Module )
		'''

		return self._import

	@import_.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def import_(self, value):
		'''
		This Method Is The Setter Method For The _import_ Attribute.
		
		@param value: Attribute Value. ( Module )
		'''

		if value:
			assert type(value) is type(sys), "'{0}' Attribute: '{1}' Type Is Not 'module'!".format("import", value)
		self._import = value

	@import_.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def import_(self):
		'''
		This Method Is The Deleter Method For The _import_ Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("import"))

	@property
	def interfaces(self):
		'''
		This Method Is The Property For The _interfaces Attribute.

		@return: self._interfaces. ( Object )
		'''

		return self._interfaces

	@interfaces.setter
	def interfaces(self, value):
		'''
		This Method Is The Setter Method For The _interfaces Attribute.
		
		@param value: Attribute Value. ( Object )
		'''

		self._interfaces = value

	@interfaces.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def interfaces(self):
		'''
		This Method Is The Deleter Method For The _interfaces Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("interfaces"))

class Loader(Ui_Loader_Type, Ui_Loader_Setup):
	'''
	This Class Is The Main Class For Loader.
	'''

	#***************************************************************************************
	#***	Initialization.
	#***************************************************************************************

	@core.executionTrace
	def __init__(self, container=None):
		'''
		This Method Initializes The Class.

		@param identity: Current Reports Id. ( String )
		'''

		LOGGER.debug("> Initializing '{0}()' Class.".format(self.__class__.__name__))

		Ui_Loader_Type.__init__(self, container)
		Ui_Loader_Setup.__init__(self)

		self.setupUi(self)
		
		# --- Setting Class Attributes. ---
		self._modules = None

		# --- Setting Up UI. ---
		self.initializeUI()
		
		# -- Loader Signals / Slots. ---		
		self.connect(self.Execute_Snippet_pushButton, SIGNAL("clicked()"), self.Execute_Snippet_pushButton_OnClicked)
		self.connect(self.Methods_listWidget, SIGNAL("itemSelectionChanged()"), self.Methods_listWidget_ItemSelectionChanged )
	
	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def initializeUI(self):
		self.gatherLibraries()
		self.getInterfaces()
		for module in self._modules.values():
			if module.interfaces:
				for interface in module.interfaces:
					listWidgetItem = QListWidgetItem(strings.getNiceName(self.getMethodName(interface)))
					listWidgetItem._datas = Interface(name=interface, module=module)
					self.Methods_listWidget.addItem(listWidgetItem)
		self.Methods_listWidget.sortItems(Qt.AscendingOrder)
	
	@core.executionTrace
	def getMethodName(self, name):
		return "%s%s" % (name[1].lower(), name[2:])
	
	@core.executionTrace
	def gatherLibraries(self):
		walker = Walker(LIBRARIES)
		modules = walker.walk(filtersIn="%s$" % Constants.librariesExtension)
		
		self._modules = {}
		for name, path in modules.items():
			module = Module()
			module.name = namespace.getNamespace(name, rootOnly=True)
			module.path = os.path.dirname(path)
			self._modules[module.name] = module

	@core.executionTrace
	def getInterfaces(self):
		for module in self._modules.values():
			if module.path not in sys.path:
				sys.path.append(module.path)
			module.import_ = __import__(module.name)
			interfaces = [object_ for object_ in module.import_.__dict__.keys() if re.search("^I[A-Z]\w+", object_)]
			if interfaces:
				module.interfaces = interfaces
	@core.executionTrace
	def Execute_Snippet_pushButton_OnClicked(self):
		module = self.Methods_listWidget.currentItem()._datas.module
		method = self.Methods_listWidget.currentItem()._datas.name	
		module.import_.__dict__[method]()
	
	@core.executionTrace
	def Methods_listWidget_ItemSelectionChanged(self):
		content = """
				<h4><center>%s</center></h4>
				<p>
				<b>Module:</b> %s
				<br/>
				<b>Path:</b> %s
				<br/>
				<b>Interface:</b> %s
				<br/>
				</p>
				""" % (self.getMethodName(self.Methods_listWidget.currentItem()._datas.name), self.Methods_listWidget.currentItem()._datas.module.name, self.Methods_listWidget.currentItem()._datas.module.import_.__file__, self.Methods_listWidget.currentItem()._datas.name)
		self.Informations_textBrowser.setText(content)

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
