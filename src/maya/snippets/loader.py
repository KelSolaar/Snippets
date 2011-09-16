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
#***	Dependencies globals manipulation.
#***********************************************************************************************
import foundations.globals.constants
from snippets.globals.constants import Constants

def _overrideDependenciesGlobals():
	"""
	This definition overrides dependencies globals.

	:return: Definition success. ( Boolean )
	"""

	foundations.globals.constants.Constants.logger = Constants.logger
	return True

_overrideDependenciesGlobals()

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.io as io
import foundations.strings as strings
import foundations.namespace as namespace
import snippets.libraries.common
from foundations.environment import Environment
from foundations.walkers import OsWalker
from snippets.globals.runtimeGlobals import RuntimeGlobals
from snippets.globals.uiConstants import UiConstants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Ui_Loader_Setup", "Ui_Loader_Type", "Interface", "Module", "Loader"]

LOGGER = logging.getLogger(Constants.logger)

# Remove existing handlers.
del logging.root.handlers[:]

if LOGGER.handlers == []:
	consoleHandler = snippets.libraries.common.MayaLoggingHandler()
	consoleHandler.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
	LOGGER.addHandler(consoleHandler)

RuntimeGlobals.loaderUiFile = os.path.join(os.path.dirname(__file__), UiConstants.loaderUiFile)
if os.path.exists(RuntimeGlobals.loaderUiFile):
	Ui_Loader_Setup, Ui_Loader_Type = uic.loadUiType(RuntimeGlobals.loaderUiFile)
else:
	ui.common.messageBox("Error", "Error", "'%s' Ui file is not available!" % UiConstants.loaderUiFile)

RuntimeGlobals.librariesDirectory = os.path.join(os.path.dirname(__file__), Constants.librariesDirectory)
RuntimeGlobals.resourcesDirectory = os.path.join(os.path.dirname(__file__), Constants.resourcesDirectory)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Interface(core.Structure):
	"""
	This is the **Interface** class.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param kwargs: name, module. ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

class Module(object):
	"""
	This class is the **Module** class.
	"""

	@core.executionTrace
	def __init__(self, name=None, path=None):
		"""
		This method initializes the class.

		:param name: Name of the Component. ( String )
		:param path: Path of the Component. ( String )
		"""

		LOGGER.debug("> Initializing '%s()' class." % (self.__class__.__name__))

		# --- Setting class attributes. ---
		self._name = None
		self.name = name
		self.path = None
		self._path = path

		self._import = None
		self._interfaces = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def name(self):
		"""
		This method is the property for **self.__name** attribute.

		:return: self._name. ( String )
		"""

		return self._name

	@name.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def name(self, value):
		"""
		This method is the setter method for **self.__name** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'%s' Attribute: '%s' type is not 'str' or 'unicode'!" % ("name", value)
		self._name = value

	@name.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def name(self):
		"""
		This method is the deleter method for **self.__name** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is not deletable!" % "name")

	@property
	def path(self):
		"""
		This method is the property for **self.__path** attribute.

		:return: self._path. ( String )
		"""

		return self._path

	@path.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def path(self, value):
		"""
		This method is the setter method for **self.__path** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'%s' Attribute: '%s' type is not 'str' or 'unicode'!" % ("path", value)
			assert os.path.exists(value), "'%s' Attribute: '%s' directory doesn't exists!" % ("path", value)
		self._path = value

	@path.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def path(self):
		"""
		This method is the deleter method for **self.__path** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is not deletable!" % "path")

	@property
	def import_(self):
		"""
		This method is the property for **self.__import_** attribute.

		:return: self._import. ( Module )
		"""

		return self._import

	@import_.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def import_(self, value):
		"""
		This method is the setter method for **self.__import_** attribute.

		:param value: Attribute value. ( Module )
		"""

		if value:
			assert type(value) is type(sys), "'%s' Attribute: '%s' type is not 'module'!" % ("import", value)
		self._import = value

	@import_.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def import_(self):
		"""
		This method is the deleter method for **self.__import_** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is not deletable!" % "import")

	@property
	def interfaces(self):
		"""
		This method is the property for **self.__interfaces** attribute.

		:return: self._interfaces. ( Object )
		"""

		return self._interfaces

	@interfaces.setter
	def interfaces(self, value):
		"""
		This method is the setter method for **self.__interfaces** attribute.

		:param value: Attribute value. ( Object )
		"""

		self._interfaces = value

	@interfaces.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def interfaces(self):
		"""
		This method is the deleter method for **self.__interfaces** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is not deletable!" % "interfaces")

class Loader(Ui_Loader_Type, Ui_Loader_Setup):
	"""
	This class is the Main class for loader.
	"""

	#***********************************************************************************************
	#***	Initialization..
	#***********************************************************************************************

	@core.executionTrace
	def __init__(self, container=None):
		"""
		This method initializes the class.

		:param identity: Current reports id. ( String )
		"""

		LOGGER.debug("> Initializing '%s()' class." % (self.__class__.__name__))

		Ui_Loader_Type.__init__(self, container)
		Ui_Loader_Setup.__init__(self)

		self.setupUi(self)

		# --- Setting class attributes. ---
		self._container = container
		self._modules = None

		self._Informations_textBrowser_defaultText = "<center><br/><br/><h4>* * *</h4>Select a Snippet to display related informations!<h4>* * *</h4></center>"

		self._linuxTextEditors = ("gedit", "kwrite", "nedit", "mousepad")
		self._linuxBrowsers = ("nautilus", "dolphin", "konqueror", "thunar")

		# --- Gathering modules. ---
		self.getModules()

		# --- Setting up ui. ---
		self.initializeUI()

		# -- Loader Signals / Slots. ---
		self.connect(self.Execute_Snippet_pushButton, SIGNAL("clicked()"), self.Execute_Snippet_pushButton_OnClicked)
		self.connect(self.Reload_Snippets_pushButton, SIGNAL("clicked()"), self.Reload_Snippets_pushButton_OnClicked)
		self.connect(self.Methods_listWidget, SIGNAL("itemSelectionChanged()"), self.Methods_listWidget_OnItemSelectionChanged)
		self.connect(self.Methods_listWidget, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.Methods_listWidget_OnItemDoubleClicked)
		self.connect(self.Search_lineEdit, SIGNAL("textChanged( const QString & )"), self.Search_lineEdit_OnTextChanged)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self._container. ( QObject )
		"""

		return self._container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is read only!" % "container")

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is not deletable!" % "container")

	@property
	def modules(self):
		"""
		This method is the property for **self.__modules** attribute.

		:return: self._modules. ( Dictionary )
		"""

		return self._modules

	@modules.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def modules(self, value):
		"""
		This method is the setter method for **self.__modules** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'%s' Attribute: '%s' type is not 'dict'!" % ("modules", value)
		self._modules = value

	@modules.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modules(self):
		"""
		This method is the deleter method for **self.__modules** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is not deletable!" % "modules")

	@property
	def Informations_textBrowser_defaultText(self):
		"""
		This method is the property for **self.__Informations_textBrowser_defaultText** attribute.

		:return: self._Informations_textBrowser_defaultText. ( String )
		"""

		return self._Informations_textBrowser_defaultText

	@Informations_textBrowser_defaultText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Informations_textBrowser_defaultText(self, value):
		"""
		This method is the setter method for **self.__Informations_textBrowser_defaultText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is read only!" % "Informations_textBrowser_defaultText")

	@Informations_textBrowser_defaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Informations_textBrowser_defaultText(self):
		"""
		This method is the deleter method for **self.__Informations_textBrowser_defaultText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is not deletable!" % "Informations_textBrowser_defaultText")

	@property
	def linuxTextEditors(self):
		"""
		This method is the property for **self.__linuxTextEditors** attribute.

		:return: self._linuxTextEditors. ( Tuple )
		"""

		return self._linuxTextEditors

	@linuxTextEditors.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxTextEditors(self, value):
		"""
		This method is the setter method for **self.__linuxTextEditors** attribute.

		:param value: Attribute value. ( Tuple )
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is read only!" % "linuxTextEditors")

	@linuxTextEditors.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxTextEditors(self):
		"""
		This method is the deleter method for **self.__linuxTextEditors** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is not deletable!" % "linuxTextEditors")

	@property
	def linuxBrowsers(self):
		"""
		This method is the property for **self.__linuxBrowsers** attribute.

		:return: self._linuxBrowsers. ( QObject )
		"""

		return self._linuxBrowsers

	@linuxBrowsers.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxBrowsers(self, value):
		"""
		This method is the setter method for **self.__linuxBrowsers** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is read only!" % "linuxBrowsers")

	@linuxBrowsers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxBrowsers(self):
		"""
		This method is the deleter method for **self.__linuxBrowsers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is not deletable!" % "linuxBrowsers")

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def initializeUI(self):
		"""
		This method triggers the **Methods_listWidget** Widget.
		"""

		self.Methods_listWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.Methods_listWidget_setActions()

		self.Snippets_Loader_Logo_label.setPixmap(QPixmap(os.path.join(RuntimeGlobals.resourcesDirectory, UiConstants.snippetsLoaderLogo)))
		self.Search_Icon_label.setPixmap(QPixmap(os.path.join(RuntimeGlobals.resourcesDirectory, UiConstants.searchIcon)))

		self.Methods_listWidget_setWidget()

		self.Informations_textBrowser.setText(self._Informations_textBrowser_defaultText)

		self.Loader_splitter.setSizes([16777215, 0])

	@core.executionTrace
	def Methods_listWidget_setWidget(self):
		"""
		This method sets the **Methods_listWidget** Widget.
		"""

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
							LOGGER.debug("> Adding QListWidgetItem with text: '%s'." % text)
							listWidgetItems.add(listWidgetItem)
							listWidgetItems.add(text[0])

			for listWidgetItem in listWidgetItems:
				self.Methods_listWidget.addItem(listWidgetItem)

			self.Methods_listWidget.sortItems(Qt.AscendingOrder)

	@core.executionTrace
	def Methods_listWidget_setActions(self):
		"""
		This method sets the **Methods_listWidget** Widget actions.
		"""

		editSnippetAction = QAction("Edit Snippet", self.Methods_listWidget)
		self.connect(editSnippetAction, SIGNAL("triggered()"), self.Methods_listWidget_editSnippetAction)
		self.Methods_listWidget.addAction(editSnippetAction)

		exploreSnippetFolderAction = QAction("Explore Snippet Folder", self.Methods_listWidget)
		self.connect(exploreSnippetFolderAction, SIGNAL("triggered()"), self.Methods_listWidget_exploreSnippetFolderAction)
		self.Methods_listWidget.addAction(exploreSnippetFolderAction)

	@core.executionTrace
	def Methods_listWidget_editSnippetAction(self):
		"""
		This method is triggered by **editSnippet** action.
		"""
		listWidget = self.Methods_listWidget.currentItem()
		if hasattr(listWidget, "_datas"):
			module = listWidget._datas.module
			self.editProvidedfile(module.import_.__file__.replace(Constants.librariesCompiledExtension, Constants.librariesExtension))

	@core.executionTrace
	def Methods_listWidget_exploreSnippetFolderAction(self):
		"""
		This method is triggered by **exploreSnippetFolder** action.
		"""

		listWidget = self.Methods_listWidget.currentItem()
		if hasattr(listWidget, "_datas"):
			module = listWidget._datas.module
			self.exploreProvidedFolder(os.path.dirname(module.import_.__file__))

	@core.executionTrace
	def Execute_Snippet_pushButton_OnClicked(self):
		"""
		This method is triggered when **Execute_Snippet_pushButton** is clicked.
		"""

		if hasattr(self.Methods_listWidget.currentItem(), "_datas"):
			self.executeSnippet()

	@core.executionTrace
	def Reload_Snippets_pushButton_OnClicked(self):
		"""
		This method is triggered when **Reload_Snippets_pushButton** is clicked.
		"""

		self.getModules()
		self.Methods_listWidget_setWidget()

	@core.executionTrace
	def Methods_listWidget_OnItemSelectionChanged(self):
		"""
		This method is triggered when **Methods_listWidget** selection has changed.
		"""

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
					<b>Variable arguments:</b> %s
					<br/>
					<b>Keywords:</b> %s
					</p>
					<p>
					<b>Documentation:</b> %s
					</p>
					""" % (strings.getNiceName(method), datas.module.name, os.path.normpath(datas.module.import_.__file__), method, datas.name, arguments.args, arguments.defaults, arguments.varargs, arguments.keywords, datas.module.import_.__dict__[method].__doc__)
		else:
			content = self._Informations_textBrowser_defaultText

		LOGGER.debug("> Update 'Informations_textBrowser' Widget content: '%s'." % content)
		self.Informations_textBrowser.setText(content)

	@core.executionTrace
	def Methods_listWidget_OnItemDoubleClicked(self, listWidgetItem):
		"""
		This method is triggered when **Methods_listWidget** is double clicked.

		:param listWidgetItem: Selected QListWidgetItem. ( QListWidgetItem )
		"""

		self.executeSnippet()

	@core.executionTrace
	def Search_lineEdit_OnTextChanged(self, text):
		"""
		This method is triggered when **Search_lineEdit** text changes.

		:param text: Current text value. ( QString )
		"""

		self.Methods_listWidget_setWidget()

	@core.executionTrace
	def getMethodName(self, name):
		"""
		This method gets the method name from the Interface.

		:param name: Interface name. ( String )
		:return: Method name. ( String )
		"""

		return "%s%s" % (name[1].lower(), name[2:])

	@core.executionTrace
	def gatherLibraries(self):
		"""
		This method gathers the libraries.
		"""

		osWalker = OsWalker(RuntimeGlobals.librariesDirectory)
		modules = osWalker.walk(filtersIn=("\.%s$" % Constants.librariesExtension,))

		self._modules = {}
		for name, path in modules.items():
			module = Module()
			module.name = namespace.getNamespace(name, rootOnly=True)
			module.path = os.path.dirname(path)
			self._modules[module.name] = module

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, ImportError)
	def getInterfaces(self):
		"""
		This method gets the interfaces.
		"""

		for module in self._modules.values():
			if module.path not in sys.path:
				sys.path.append(module.path)
			if module.name in sys.modules.keys():
				del(sys.modules[module.name])

			module.import_ = __import__(module.name)

			interfaces = [object_ for object_ in module.import_.__dict__.keys() if re.search("^I[A-Z]\w+", object_)]
			if interfaces:
				LOGGER.info("%s | Registering '%s' Interfaces from '%s' Module!" % (self.__class__.__name__, interfaces, module.name))
				module.interfaces = interfaces

	@core.executionTrace
	def getModules(self):
		"""
		This method gets the Modules.
		"""

		self.gatherLibraries()
		self.getInterfaces()

	@core.executionTrace
	def executeSnippet(self):
		"""
		This method triggers the selected Snippet execution.
		"""

		listWidget = self.Methods_listWidget.currentItem()
		if hasattr(listWidget, "_datas"):
			module = listWidget._datas.module
			method = listWidget._datas.name

			LOGGER.info("%s | Executing '%s' Snippet from '%s' Module!" % (self.__class__.__name__, method, module.name))
			module.import_.__dict__[method]()

	@core.executionTrace
	def editProvidedfile(self, file):
		"""
		This method provides editing capability.

		:param file: File to edit. ( String )
		"""

		editCommand = None

		file = os.path.normpath(file)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			LOGGER.info("%s | Launching 'notepad.exe' with '%s'." % (self.__class__.__name__, file))
			editCommand = "notepad.exe \"%s\"" % file
		elif platform.system() == "Darwin":
			LOGGER.info("%s | Launching default text editor with '%s'." % (self.__class__.__name__, file))
			editCommand = "open -e \"%s\"" % file
		elif platform.system() == "Linux":
			environmentVariable = Environment("PATH")
			paths = environmentVariable.getValue().split(":")

			editorFound = False
			for editor in self._linuxTextEditors:
				if not editorFound:
					try:
						for path in paths:
							if os.path.exists(os.path.join(path, editor)):
								LOGGER.info("%s | Launching '%s' text editor with '%s'." % (self.__class__.__name__, editor, file))
								editCommand = "\"%s\" \"%s\"" % (editor, file)
								editorFound = True
								raise StopIteration
					except StopIteration:
						pass
				else:
					break
		if editCommand:
			LOGGER.debug("> Current edit command: '%s'." % editCommand)
			editProcess = QProcess()
			editProcess.startDetached(editCommand)

	@core.executionTrace
	def exploreProvidedFolder(self, folder):
		"""
		This method provides folder exploring capability.

		:param folder: Folder to explore. ( String )
		"""

		browserCommand = None

		folder = os.path.normpath(folder)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			LOGGER.info("%s | Launching 'explorer.exe' with '%s'." % (self.__class__.__name__, folder))
			browserCommand = "explorer.exe \"%s\"" % folder
		elif platform.system() == "Darwin":
			LOGGER.info("%s | Launching 'Finder' with '%s'." % (self.__class__.__name__, folder))
			browserCommand = "open \"%s\"" % folder
		elif platform.system() == "Linux":
			environmentVariable = Environment("PATH")
			paths = environmentVariable.getValue().split(":")

			browserFound = False
			for browser in self._linuxBrowsers:
				if not browserFound:
					try:
						for path in paths:
							if os.path.exists(os.path.join(path, browser)):
								LOGGER.info("%s | Launching '%s' file browser with '%s'." % (self.__class__.__name__, browser, folder))
								browserCommand = "\"%s\" \"%s\"" % (browser, folder)
								browserFound = True
								raise StopIteration
					except StopIteration:
						pass
				else:
					break

		if browserCommand:
			LOGGER.debug("> Current browser command: '%s'." % browserCommand)
			browserProcess = QProcess()
			browserProcess.startDetached(browserCommand)
