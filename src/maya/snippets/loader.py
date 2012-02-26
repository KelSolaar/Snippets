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
from snippets.modulesManager import ModulesManager
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
	error = "'{0}' Ui file is not available!".format(RuntimeGlobals.loaderUiFile)
	snippets.ui.common.messageBox("Error", "Error", error)
	raise Exception(error)

RuntimeGlobals.modulesManager = ModulesManager([RuntimeGlobals.librariesDirectory])
RuntimeGlobals.modulesManager.registerModules()
RuntimeGlobals.modulesManager.registerInterfaces()

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

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

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
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' type is not 'str' or 'unicode'!".format("name",
																												value)
		self.__name = value

	@name.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def name(self):
		"""
		This method is the deleter method for **self.___name** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("name"))

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
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' type is not 'str' or 'unicode'!".format("path",
																												value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' directory doesn't exists!".format("path", value)
		self.__path = value

	@path.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def path(self):
		"""
		This method is the deleter method for **self.___path** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("path"))

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
			assert type(value) is type(sys), "'{0}' Attribute: '{1}' type is not 'module'!".format("import", value)
		self._import = value

	@import_.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def import_(self):
		"""
		This method is the deleter method for **self.__import_** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("import"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("interfaces"))

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

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

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

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("container"))

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
			assert type(value) is dict, "'{0}' Attribute: '{1}' type is not 'dict'!".format("modules", value)
		self.__modules = value

	@modules.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modules(self):
		"""
		This method is the deleter method for **self.__modules** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("modules"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is read only!".format("defaultText"))

	@defaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultText(self):
		"""
		This method is the deleter method for **self.__defaultText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("defaultText"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is read only!".format("linuxTextEditors"))

	@linuxTextEditors.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxTextEditors(self):
		"""
		This method is the deleter method for **self.__linuxTextEditors** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("linuxTextEditors"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is read only!".format("linuxBrowsers"))

	@linuxBrowsers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def linuxBrowsers(self):
		"""
		This method is the deleter method for **self.__linuxBrowsers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("linuxBrowsers"))

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
		self.__view = self.Interfaces_listView
		self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__view_addActions()

		self.Snippets_Loader_Logo_label.setPixmap(QPixmap(os.path.join(RuntimeGlobals.resourcesDirectory, UiConstants.snippetsLoaderLogo)))
		self.Search_Icon_label.setPixmap(QPixmap(os.path.join(RuntimeGlobals.resourcesDirectory, UiConstants.searchIcon)))

		self.Informations_textBrowser.setText(self.__defaultText)

		self.Interfaces_frame_splitter.setSizes([16777215, 0])

		# Signals / Slots.
		# TODO: New SS mechanism.
		self.Execute_Snippet_pushButton.clicked.connect(self.__Execute_Snippet_pushButton__clicked)
		self.Reload_Snippets_pushButton.clicked.connect(self.__Reload_Snippets_pushButton__clicked)
		self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
		self.__view.doubleClicked.connect(self.__view__doubleClicked)
		self.Search_lineEdit.textChanged.connect(self.__Search_lineEdit__textChanged)

	@core.executionTrace
	def __view_addActions(self):
		"""
		This method sets the View actions.
		"""

		editSnippetAction = QAction("Edit Snippet", self.__view)
		self.connect(editSnippetAction, SIGNAL("triggered()"), self.__view_editSnippetAction)
		self.__view.addAction(editSnippetAction)

		exploreSnippetFolderAction = QAction("Explore Snippet Folder", self.__view)
		self.connect(exploreSnippetFolderAction, SIGNAL("triggered()"), self.__view_exploreSnippetFolderAction)
		self.__view.addAction(exploreSnippetFolderAction)

	@core.executionTrace
	def __view_editSnippetAction(self):
		"""
		This method is triggered by **editSnippetAction** action.
		"""

		interface = self.getSelectedInterface()
		if not interface:
			return

		self.editFile(interface.module.import_.__file__.replace(
		Constants.libraryCompiledExtension, Constants.libraryExtension))

	@core.executionTrace
	def __view_exploreSnippetFolderAction(self):
		"""
		This method is triggered by **exploreSnippetFolderAction** action.
		"""

		interface = self.getSelectedInterface()
		if not interface:
			return

		self.exploreDirectory(os.path.dirname(interface.module.import_.__file__))

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
	def __view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method sets the **Informations_textBrowser** Widget.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		interface = self.getSelectedInterface()
		if not interface:
			return

		if hasattr(interface, "attribute"):
			arguments = inspect.getargspec(interface.module.import_.__dict__[interface.attribute])
			content = """
					<h4><center>{0}</center></h4>
					<p>
					<b>Module:</b> {1}
					<br/>
					<b>Path:</b> {2}
					</p>
					<p>
					<b>Method:</b> {3}
					<br/>
					<b>Interface:</b> {4}
					<br/>
					<b>Arguments:</b> {5}
					<br/>
					<b>Defaults:</b> {6}
					<br/>
					<b>Variable arguments:</b> {7}
					<br/>
					<b>Keywords:</b> {8}
					</p>
					<p>
					<b>Documentation:</b> {9}
					</p>
					""".format(interface.name,
						interface.module.name,
						os.path.normpath(interface.module.import_.__file__),
						self.getMethodName(interface.attribute),
						interface.attribute,
						arguments.args,
						arguments.defaults,
						arguments.varargs,
						arguments.keywords,
						interface.module.import_.__dict__[interface.attribute].__doc__)
		else:
			content = self.__defaultText

		LOGGER.debug("> Update 'Informations_textBrowser' Widget content: '{0}'.".format(content))
		self.Informations_textBrowser.setText(content)

	@core.executionTrace
	def __view__doubleClicked(self, index):
		"""
		This method is triggered when **Interfaces_listView** Widget is double clicked.

		:param index: Current index. ( QModelIndex )
		"""

		self.executeSnippet()

	@core.executionTrace
	def __Search_lineEdit__textChanged(self, text):
		"""
		This method is triggered when **Search_lineEdit** Widget text changes.

		:param text: Current text value. ( QString )
		"""

		self.setInterfaces(strings.encode(text))

	@core.executionTrace
	def getMethodName(self, name):
		"""
		This method gets the method name from the Interface.

		:param name: Interface name. ( String )
		:return: Method name. ( String )
		"""

		return "{0}{1}".format(name[1].lower(), name[2:])

	@core.executionTrace
	def gatherLibraries(self):
		"""
		This method gathers the libraries.
		"""

		osWalker = OsWalker(RuntimeGlobals.librariesDirectory)
		modules = osWalker.walk(filtersIn=(r"\.{0}$".format(Constants.libraryExtension),))

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
				LOGGER.info("{0} | Registering '{1}' Interfaces from '{2}' Module!".format(self.__class__.__name__,
																							interfaces, module.name))
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
	def getSelectedInterface(self):
		"""
		This method returns the current selected Interface.

		:return: Selected interface. ( Interface )
		"""

		items = [self.__model.getInterface(index) for index in self.__view.selectionModel().selectedIndexes()]
		return items and items[0]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def executeSnippet(self):
		"""
		This method triggers the selected Snippet execution.
		
		:return: Method success. ( Boolean )
		"""

		interface = self.getSelectedInterface()
		if not interface:
			return

		module = interface.module
		method = interface.attribute

		LOGGER.info("{0} | Executing '{1}' Snippet from '{2}' Module!".format(self.__class__.__name__,
																			method,
																			module.name))
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
			LOGGER.info("{0} | Launching 'notepad.exe' with '{1}'.".format(self.__class__.__name__, file))
			editCommand = "notepad.exe \"{}\"".format(file)
		elif platform.system() == "Darwin":
			LOGGER.info("{0} | Launching default text editor with '{1}'.".format(self.__class__.__name__, file))
			editCommand = "open -e \"{0}\"".format(file)
		elif platform.system() == "Linux":
			environmentVariable = Environment("PATH")
			paths = environmentVariable.getValue().split(":")

			editorFound = False
			for editor in self.__linuxTextEditors:
				if not editorFound:
					try:
						for path in paths:
							if os.path.exists(os.path.join(path, editor)):
								LOGGER.info("{0} | Launching '{1}' text editor with '{2}'.".format(self.__class__.__name__, editor, file))
								editCommand = "\"{0}\" \"{1}\"".format(editor, file)
								editorFound = True
								raise StopIteration
					except StopIteration:
						pass
				else:
					break
		if editCommand:
			LOGGER.debug("> Current edit command: '{0}'.".format(editCommand))
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
			LOGGER.info("{0} | Launching 'explorer.exe' with '{1}'.".format(self.__class__.__name__, directory))
			browserCommand = "explorer.exe \"{0}\"".format(directory)
		elif platform.system() == "Darwin":
			LOGGER.info("{0} | Launching 'Finder' with '{1}'.".format(self.__class__.__name__, directory))
			browserCommand = "open \"{0}\"".format(directory)
		elif platform.system() == "Linux":
			environmentVariable = Environment("PATH")
			paths = environmentVariable.getValue().split(":")

			browserFound = False
			for browser in self.__linuxBrowsers:
				if not browserFound:
					try:
						for path in paths:
							if os.path.exists(os.path.join(path, browser)):
								LOGGER.info("{0} | Launching '{1}' file browser with '{1}'.".format(self.__class__.__name__,
																									browser,
																									directory))
								browserCommand = "\"{0}\" \"{1}\"".format(browser, directory)
								browserFound = True
								raise StopIteration
					except StopIteration:
						pass
				else:
					break

		if browserCommand:
			LOGGER.debug("> Current browser command: '{}'.".format(browserCommand))
			browserProcess = QProcess()
			browserProcess.startDetached(browserCommand)
		return True
