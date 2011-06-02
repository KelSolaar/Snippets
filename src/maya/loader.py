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
import inspect
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

RuntimeConstants.librariesDirectory = os.path.join(os.path.dirname(__file__), Constants.librariesDirectory)
RuntimeConstants.resourcesDirectory = os.path.join(os.path.dirname(__file__), Constants.resourcesDirectory)

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
		self._container = container
		self._modules = None
		self._Informations_textBrowser_defaultText  =  "<center><br/><br/><h4>* * *</h4>Select A Snippet To Display Related Informations!<h4>* * *</h4></center>"
		
		# --- Gathering Modules. ---
		self.getModules()

		# --- Setting Up UI. ---
		self.initializeUI()
		
		# -- Loader Signals / Slots. ---		
		self.connect(self.Execute_Snippet_pushButton, SIGNAL("clicked()"), self.Execute_Snippet_pushButton_OnClicked)
		self.connect(self.Reload_Snippets_pushButton, SIGNAL("clicked()"), self.Reload_Snippets_pushButton_OnClicked)
		self.connect(self.Methods_listWidget, SIGNAL("itemSelectionChanged()"), self.Methods_listWidget_OnItemSelectionChanged )
		self.connect(self.Methods_listWidget, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.Methods_listWidget_OnItemDoubleClicked )
		self.connect(self.Search_lineEdit, SIGNAL("textChanged( const QString & )"), self.Search_lineEdit_OnTextChanged )
	
	#***************************************************************************************
	#***	Attributes Properties
	#***************************************************************************************
	@property
	def container(self):
		'''
		This Method Is The Property For The _container Attribute.

		@return: self._container. ( QObject )
		'''

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		'''
		This Method Is The Setter Method For The _container Attribute.

		@param value: Attribute Value. ( QObject )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		'''
		This Method Is The Deleter Method For The _container Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("container"))

	@property
	def modules(self):
		'''
		This Method Is The Property For The _modules Attribute.

		@return: self._modules. ( Dictionary )
		'''

		return self._modules

	@modules.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def modules(self, value):
		'''
		This Method Is The Setter Method For The _modules Attribute.
		
		@param value: Attribute Value. ( Dictionary )
		'''

		if value:
			assert type(value) is dict, "'{0}' Attribute: '{1}' Type Is Not 'dict'!".format("modules", value)
		self._modules = value

	@modules.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modules(self):
		'''
		This Method Is The Deleter Method For The _modules Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("modules"))

	@property
	def Informations_textBrowser_defaultText(self):
		'''
		This Method Is The Property For The _Informations_textBrowser_defaultText Attribute.

		@return: self._Informations_textBrowser_defaultText. ( String )
		'''

		return self._Informations_textBrowser_defaultText

	@Informations_textBrowser_defaultText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Informations_textBrowser_defaultText(self, value):
		'''
		This Method Is The Setter Method For The _Informations_textBrowser_defaultText Attribute.

		@param value: Attribute Value. ( String )
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Read Only!".format("Informations_textBrowser_defaultText"))

	@Informations_textBrowser_defaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Informations_textBrowser_defaultText(self):
		'''
		This Method Is The Deleter Method For The _Informations_textBrowser_defaultText Attribute.
		'''

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute Is Not Deletable!".format("Informations_textBrowser_defaultText"))

	#***************************************************************************************
	#***	Class Methods
	#***************************************************************************************
	@core.executionTrace
	def getMethodName(self, name):
		'''
		This Definition Gets The Method Name From The Interface.
		
		@param name: Interface Name. ( String )
		@return: Method Name. ( String )
		'''

		return "%s%s" % (name[1].lower(), name[2:])
	
	@core.executionTrace
	def gatherLibraries(self):
		'''
		This Definition Gathers The Libraries.
		'''

		walker = Walker(RuntimeConstants.librariesDirectory)
		modules = walker.walk(filtersIn="%s$" % Constants.librariesExtension)
		
		self._modules = {}
		for name, path in modules.items():
			module = Module()
			module.name = namespace.getNamespace(name, rootOnly=True)
			module.path = os.path.dirname(path)
			self._modules[module.name] = module

	@core.executionTrace
	def getInterfaces(self):
		'''
		This Definition Gets The Interfaces.
		'''

		for module in self._modules.values():
			if module.path not in sys.path:
				sys.path.append(module.path)
			if module.name in sys.modules.keys():
				del(sys.modules[module.name])
			module.import_ = __import__(module.name)
			interfaces = [object_ for object_ in module.import_.__dict__.keys() if re.search("^I[A-Z]\w+", object_)]
			if interfaces:
				module.interfaces = interfaces
	
	@core.executionTrace
	def getModules(self):
		'''
		This Definition Gets The Modules.
		'''

		self.gatherLibraries()
		self.getInterfaces()

	@core.executionTrace
	def initializeUI(self):
		'''
		This Definition Triggers The Methods_listWidget Widget.
		'''

		self.Snippets_Loader_Logo_label.setPixmap(QPixmap(os.path.join(RuntimeConstants.resourcesDirectory, UiConstants.snippetsLoaderLogo)))
		self.Search_Icon_label.setPixmap(QPixmap(os.path.join(RuntimeConstants.resourcesDirectory, UiConstants.searchIcon)))
		
		self.Methods_listWidget_setWidget()
		
		self.Informations_textBrowser.setText(self._Informations_textBrowser_defaultText)
	
	@core.executionTrace
	def executeSnippet(self):
		'''
		This Definition Triggers The Selected Snippet Execution.
		'''

		listWidget = self.Methods_listWidget.currentItem()
		if hasattr(listWidget, "_datas"):
			module = listWidget._datas.module
			method = listWidget._datas.name	
			
			LOGGER.info( "%s | Executing '%s' Snippet From '%s' Module!" % (self.__class__.__name__, method, module.name))
			module.import_.__dict__[method]()		
	
	@core.executionTrace
	def Methods_listWidget_setWidget(self):
		'''
		This Definition Sets The Methods_listWidget Widget.
		'''
		
		if self._modules:
			self.Methods_listWidget.clear()
		
			listWidgetItems = set()
			for module in self._modules.values():
				if module.interfaces:
					for interface in module.interfaces:
						text = strings.getNiceName(self.getMethodName(interface))
						if re.search(str(self.Search_lineEdit.text()), text, flags=re.IGNORECASE):
							listWidgetItem = QListWidgetItem(text)
							listWidgetItem._datas = Interface(name=interface, module=module)
							listWidgetItems.add(listWidgetItem)
							listWidgetItems.add(text[0])

			for listWidgetItem in listWidgetItems:
				self.Methods_listWidget.addItem(listWidgetItem)
			
			self.Methods_listWidget.sortItems(Qt.AscendingOrder)

	@core.executionTrace
	def Execute_Snippet_pushButton_OnClicked(self):
		'''
		This Method Is Triggered When Execute_Snippet_pushButton Is Clicked.
		'''
	
		self.executeSnippet()

	@core.executionTrace
	def Reload_Snippets_pushButton_OnClicked(self):
		'''
		This Method Is Triggered When Reload_Snippets_pushButton Is Clicked.
		'''
			
		self.getModules()
		self.Methods_listWidget_setWidget()

	@core.executionTrace
	def Methods_listWidget_OnItemSelectionChanged(self):
		'''
		This Method Is Triggered When Methods_listWidget Selection Has Changed.
		'''
		
		if hasattr(self.Methods_listWidget.currentItem(), "_datas"):
			datas = self.Methods_listWidget.currentItem()._datas
			method = self.getMethodName(datas.name)
			arguments = inspect.getargspec(datas.module.import_.__dict__[method])
			content = """
					<h4><center>%s</center></h4>
					<p>
					<b>Module:</b> %s
					<br/>
					<b>Path:</b> %s
					</p>
					<p>
					<b>Method:</b> %s
					<br/>
					<b>Interface:</b> %s
					<br/>
					<b>Arguments:</b> %s
					<br/>
					<b>Defaults:</b> %s
					<br/>
					<b>Variable Arguments:</b> %s
					<br/>
					<b>Keywords:</b> %s
					</p>
					<p>
					<b>Documentation:</b> %s
					</p>
					""" % (strings.getNiceName(method), datas.module.name, datas.module.import_.__file__, method, datas.name, arguments.args, arguments.defaults, arguments.varargs, arguments.keywords, datas.module.import_.__dict__[method].__doc__)
		else:
			content = self._Informations_textBrowser_defaultText
		self.Informations_textBrowser.setText(content)
	
	@core.executionTrace
	def Methods_listWidget_OnItemDoubleClicked(self, listWidgetItem):
		'''
		This Method Is Triggered When Methods_listWidget Is Double Clicked.
		
		@param listWidgetItem: Selected QListWidgetItem. ( QListWidgetItem )
		'''
		
		self.executeSnippet()

	@core.executionTrace
	def Search_lineEdit_OnTextChanged(self, text):
		'''
		This Method Is Triggered When Search_lineEdit Text Changes.
		
		@param text: Current Text Value. ( QString )
		'''
		
		self.Methods_listWidget_setWidget()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
