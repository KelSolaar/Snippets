#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**********************************************************************************************************************
#
# Copyright (C) 2009 - 2012 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#**********************************************************************************************************************

"""
**loader.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Loader Module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
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

#**********************************************************************************************************************
#***	Dependencies globals manipulation.
#**********************************************************************************************************************
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

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
import foundations.io as io
import foundations.strings as strings
import foundations.namespace as namespace
import snippets.libraries.common
import snippets.ui.common
from foundations.environment import Environment
from foundations.walkers import OsWalker
from snippets.globals.runtimeGlobals import RuntimeGlobals
from snippets.globals.uiConstants import UiConstants
from snippets.ui.models import Interface
from snippets.ui.models import InterfacesModel
from snippets.ui.views import Interfaces_QListView

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Ui_Loader_Setup", "Ui_Loader_Type", "Module", "Loader"]

LOGGER = logging.getLogger(Constants.logger)

# Remove existing handlers.
del logging.root.handlers[:]

if LOGGER.handlers == []:
	consoleHandler = snippets.libraries.common.MayaLoggingHandler()
	consoleHandler.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
	LOGGER.addHandler(consoleHandler)

RuntimeGlobals.librariesDirectory = os.path.join(os.path.dirname(__file__), Constants.librariesDirectory)
RuntimeGlobals.resourcesDirectory = os.path.join(os.path.dirname(__file__), Constants.resourcesDirectory)

RuntimeGlobals.loaderUiFile = os.path.join(os.path.join(RuntimeGlobals.resourcesDirectory, UiConstants.loaderUiFile))
if os.path.exists(RuntimeGlobals.loaderUiFile):
	Ui_Loader_Setup, Ui_Loader_Type = uic.loadUiType(RuntimeGlobals.loaderUiFile)
else:
	error = "'%s' Ui file is not available!" % RuntimeGlobals.loaderUiFile
	snippets.ui.common.messageBox("Error", "Error", error)
	raise Exception(error)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
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
		self.__name = None
		self.name = name
		self.path = None
		self.__path = path

		self._import = None
		self.__interfaces = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def name(self):
		"""
		This method is the property for **self.___name** attribute.

		:return: self.__name. ( String )
		"""

		return self.__name

	@name.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def name(self, value):
		"""
		This method is the setter method for **self.___name** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'%s' Attribute: '%s' type is not 'str' or 'unicode'!" % ("name", value)
		self.__name = value

	@name.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def name(self):
		"""
		This method is the deleter method for **self.___name** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is not deletable!" % "name")

	@property
	def path(self):
		"""
		This method is the property for **self.___path** attribute.

		:return: self.__path. ( String )
		"""

		return self.__path

	@path.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def path(self, value):
		"""
		This method is the setter method for **self.___path** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'%s' Attribute: '%s' type is not 'str' or 'unicode'!" % ("path", value)
			assert os.path.exists(value), "'%s' Attribute: '%s' directory doesn't exists!" % ("path", value)
		self.__path = value

	@path.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def path(self):
		"""
		This method is the deleter method for **self.___path** attribute.
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

		if value is not None:
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

		:return: self.__interfaces. ( Object )
		"""

		return self.__interfaces

	@interfaces.setter
	def interfaces(self, value):
		"""
		This method is the setter method for **self.__interfaces** attribute.

		:param value: Attribute value. ( Object )
		"""

		self.__interfaces = value

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

	#******************************************************************************************************************
	#***	Initialization..
	#******************************************************************************************************************

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
		self.__container = container
		self.__modules = None

		self.__model = None
		self.__view = None

		self.__defaultText = "<center><br/><br/><h4>* * *</h4>Select a Snippet to display related informations!<h4>* * *</h4></center>"

		self.__linuxTextEditors = ("gedit", "kwrite", "nedit", "mousepad")
		self.__linuxBrowsers = ("nautilus", "dolphin", "konqueror", "thunar")

		# --- Gathering modules. ---
		self.getModules()

		# --- Initialize Ui. ---
		self.__initializeUI()

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

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

		:return: self.__modules. ( Dictionary )
		"""

		return self.__modules

	@modules.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def modules(self, value):
		"""
		This method is the setter method for **self.__modules** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value is not None:
			assert type(value) is dict, "'%s' Attribute: '%s' type is not 'dict'!" % ("modules", value)
		self.__modules = value

	@modules.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modules(self):
		"""
		This method is the deleter method for **self.__modules** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is not deletable!" % "modules")

	@property
	def model(self):
		"""
		This method is the property for **self.__model** attribute.

		:return: self.__model. ( TemplatesModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for **self.__model** attribute.

		:param value: Attribute value. ( TemplatesModel )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This method is the deleter method for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

	@property
	def view(self):
		"""
		This method is the property for **self.__view** attribute.

		:return: self.__view. ( QWidget )
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		This method is the setter method for **self.__view** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		This method is the deleter method for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def defaultText(self):
		"""
		This method is the property for **self.__defaultText** attribute.

		:return: self.__defaultText. ( String )
		"""

		return self.__defaultText

	@defaultText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultText(self, value):
		"""
		This method is the setter method for **self.__defaultText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is read only!" % "defaultText")

	@defaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultText(self):
		"""
		This method is the deleter method for **self.__defaultText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'%s' Attribute is not deletable!" % "defaultText")

	@property
	def linuxTextEditors(self):
		"""
		This method is the property for **self.__linuxTextEditors** attribute.

		:return: self.__linuxTextEditors. ( Tuple )
		"""

		return self.__linuxTextEditors

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

		:return: self.__linuxBrowsers. ( QObject )
		"""

		return self.__linuxBrowsers

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

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __initializeUI(self):
		"""
		This method triggers the **Methods_listWidget** Widget.
		"""

		self.__model = InterfacesModel(self)
		self.setInterfaces(unicode())

		self.Interfaces_listView.setParent(None)
		self.Interfaces_listView = Interfaces_QListView(self, self.__model)
		self.Interfaces_listView.setObjectName("Interfaces_listView")
		self.Interfaces_frame_splitter.insertWidget(0, self.Interfaces_listView)
#		self.Methods_frame_gridLayout.addWidget(self.Interfaces_listView, 1, 0)
		self.__view = self.Interfaces_listView
		self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
#		self.__view_addActions()

#		self.Methods_listWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
#		self.__view_setActions()

		self.Snippets_Loader_Logo_label.setPixmap(QPixmap(os.path.join(RuntimeGlobals.resourcesDirectory, UiConstants.snippetsLoaderLogo)))
		self.Search_Icon_label.setPixmap(QPixmap(os.path.join(RuntimeGlobals.resourcesDirectory, UiConstants.searchIcon)))

		self.Informations_textBrowser.setText(self.__defaultText)

		self.Interfaces_frame_splitter.setSizes([16777215, 0])

		# Signals / Slots.
		# TODO: New SS mechanism.
		self.Execute_Snippet_pushButton.clicked.connect(self.__Execute_Snippet_pushButton__clicked)
		self.Reload_Snippets_pushButton.clicked.connect(self.__Reload_Snippets_pushButton__clicked)
#		self.connect(self.Methods_listWidget, SIGNAL("itemSelectionChanged()"), self.__view__itemSelectionChanged)
#		self.connect(self.Methods_listWidget, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.__view__itemDoubleClicked)
		self.connect(self.Search_lineEdit, SIGNAL("textChanged( const QString & )"), self.__Search_lineEdit__textChanged)

	@core.executionTrace
	def __view_setActions(self):
		"""
		This method sets the **Methods_listWidget** Widget actions.
		"""

		editSnippetAction = QAction("Edit Snippet", self.Methods_listWidget)
		self.connect(editSnippetAction, SIGNAL("triggered()"), self.__view_editSnippetAction)
		self.Methods_listWidget.addAction(editSnippetAction)

		exploreSnippetFolderAction = QAction("Explore Snippet Folder", self.Methods_listWidget)
		self.connect(exploreSnippetFolderAction, SIGNAL("triggered()"), self.__view_exploreSnippetFolderAction)
		self.Methods_listWidget.addAction(exploreSnippetFolderAction)

	@core.executionTrace
	def __view_editSnippetAction(self):
		"""
		This method is triggered by **editSnippet** action.
		"""
		listWidget = self.Methods_listWidget.currentItem()
		if hasattr(listWidget, "_data"):
			module = listWidget._data.module
			self.editFile(module.import_.__file__.replace(Constants.librariesCompiledExtension, Constants.librariesExtension))

	@core.executionTrace
	def __view_exploreSnippetFolderAction(self):
		"""
		This method is triggered by **exploreSnippetFolder** action.
		"""

		listWidget = self.Methods_listWidget.currentItem()
		if hasattr(listWidget, "_data"):
			module = listWidget._data.module
			self.exploreDirectory(os.path.dirname(module.import_.__file__))

	@core.executionTrace
	def __Execute_Snippet_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Execute_Snippet_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		if hasattr(self.Methods_listWidget.currentItem(), "_data"):
			self.executeSnippet()

	@core.executionTrace
	def __Reload_Snippets_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Reload_Snippets_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.getModules()
		self.setInterfaces(unicode())

	@core.executionTrace
	def __view__itemSelectionChanged(self):
		"""
		This method is triggered when **Methods_listWidget** Widget selection has changed.
		"""

		if hasattr(self.Methods_listWidget.currentItem(), "_data"):
			data = self.Methods_listWidget.currentItem()._data
			method = self.getMethodName(data.name)
			arguments = inspect.getargspec(data.module.import_.__dict__[method])
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
					""" % (strings.getNiceName(method), data.module.name, os.path.normpath(data.module.import_.__file__), method, data.name, arguments.args, arguments.defaults, arguments.varargs, arguments.keywords, data.module.import_.__dict__[method].__doc__)
		else:
			content = self.__defaultText

		LOGGER.debug("> Update 'Informations_textBrowser' Widget content: '%s'." % content)
		self.Informations_textBrowser.setText(content)

	@core.executionTrace
	def __view__itemDoubleClicked(self, listWidgetItem):
		"""
		This method is triggered when **Methods_listWidget** Widget is double clicked.

		:param listWidgetItem: Selected QListWidgetItem. ( QListWidgetItem )
		"""

		self.executeSnippet()

	@core.executionTrace
	def __Search_lineEdit__textChanged(self, text):
		"""
		This method is triggered when **Search_lineEdit** Widget text changes.

		:param text: Current text value. ( QString )
		"""

		self.setInterfaces(strings.encode(self.Search_lineEdit.text()))

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

		self.__modules = {}
		for name, path in modules.items():
			module = Module()
			module.name = namespace.getNamespace(name, rootOnly=True)
			module.path = os.path.dirname(path)
			self.__modules[module.name] = module

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, ImportError)
	def getInterfaces(self):
		"""
		This method gets the interfaces.

		:return: Method success. ( Boolean )
		"""

		for module in self.__modules.values():
			if module.path not in sys.path:
				sys.path.append(module.path)
			if module.name in sys.modules:
				del(sys.modules[module.name])

			module.import_ = __import__(module.name)

			interfaces = [object_ for object_ in module.import_.__dict__ if re.search(r"^I[A-Z]\w+", object_)]
			if interfaces:
				LOGGER.info("%s | Registering '%s' Interfaces from '%s' Module!" % (self.__class__.__name__, interfaces, module.name))
				module.interfaces = interfaces
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getModules(self):
		"""
		This method gets the Modules.
	
		:return: Method success. ( Boolean )
		"""

		self.gatherLibraries()
		self.getInterfaces()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setInterfaces(self, pattern, flags=re.IGNORECASE):
		"""
		This method sets the Model interfaces.

		:param pattern: Interface name. ( String )
		:param flags: Regex filtering flags. ( Integer )
		:return: Method success. ( Boolean )
		"""

		try:
			pattern = re.compile(pattern, flags)
		except Exception:
			return

		self.__model.clear()

		for module in self.__modules.values():
			if not module.interfaces:
				continue

			for interface in module.interfaces:
				name = strings.getNiceName(self.getMethodName(interface))
				if re.search(pattern, name):
					self.__model.registerInterface(Interface(name=name, attribute=interface, module=module))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def executeSnippet(self):
		"""
		This method triggers the selected Snippet execution.
		
		:return: Method success. ( Boolean )
		"""

		listWidget = self.Methods_listWidget.currentItem()
		if hasattr(listWidget, "_data"):
			module = listWidget._data.module
			method = listWidget._data.name

			LOGGER.info("%s | Executing '%s' Snippet from '%s' Module!" % (self.__class__.__name__, method, module.name))
			module.import_.__dict__[method]()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def editFile(self, file):
		"""
		This method provides editing capability.

		:param file: File to edit. ( String )
		:return: Method success. ( Boolean )
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
			for editor in self.__linuxTextEditors:
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
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def exploreDirectory(self, directory):
		"""
		This method provides directory exploring capability.

		:param directory: Folder to explore. ( String )
		:return: Method success. ( Boolean )
		"""

		browserCommand = None

		directory = os.path.normpath(directory)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			LOGGER.info("%s | Launching 'explorer.exe' with '%s'." % (self.__class__.__name__, directory))
			browserCommand = "explorer.exe \"%s\"" % directory
		elif platform.system() == "Darwin":
			LOGGER.info("%s | Launching 'Finder' with '%s'." % (self.__class__.__name__, directory))
			browserCommand = "open \"%s\"" % directory
		elif platform.system() == "Linux":
			environmentVariable = Environment("PATH")
			paths = environmentVariable.getValue().split(":")

			browserFound = False
			for browser in self.__linuxBrowsers:
				if not browserFound:
					try:
						for path in paths:
							if os.path.exists(os.path.join(path, browser)):
								LOGGER.info("%s | Launching '%s' file browser with '%s'." % (self.__class__.__name__, browser, directory))
								browserCommand = "\"%s\" \"%s\"" % (browser, directory)
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
		return True
