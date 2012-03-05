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
	This module defines the :class:`Loader` class.

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
from PyQt4 import uic
from PyQt4.QtCore import QProcess
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QPixmap

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import snippets.ui.common
from foundations.environment import Environment
from snippets.globals.constants import Constants
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

__all__ = ["LOGGER", "Ui_Loader_Setup", "Ui_Loader_Type", "Loader"]

LOGGER = logging.getLogger(Constants.logger)

RuntimeGlobals.loaderUiFile = snippets.ui.common.getResourcePath(UiConstants.loaderUiFile)
if foundations.common.pathExists(RuntimeGlobals.loaderUiFile):
	Ui_Loader_Setup, Ui_Loader_Type = uic.loadUiType(RuntimeGlobals.loaderUiFile)
else:
	error = "'{0}' Ui file is not available!".format(RuntimeGlobals.loaderUiFile)
	snippets.ui.common.messageBox("Error", "Error", error)
	raise Exception(error)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Loader(Ui_Loader_Type, Ui_Loader_Setup):
	"""
	This class defines the complex Maya Interfaces loader widget.
	"""

	@core.executionTrace
	def __init__(self, parent=None, modulesManager=RuntimeGlobals.modulesManager):
		"""
		This method initializes the class.
		
		:param parent: Parent object. ( QObject )
		:param modulesManager: Modules Manager. ( ModulesManager )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		Ui_Loader_Type.__init__(self, parent)
		Ui_Loader_Setup.__init__(self)

		self.setupUi(self)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__modulesManager = modulesManager

		self.__model = None
		self.__view = None

		self.__defaultText = "<center><br/><br/><h4>* * *</h4>Select a Snippet to display related informations!<h4>* * *</h4></center>"

		self.__linuxTextEditors = ("gedit", "kwrite", "nedit", "mousepad")
		self.__linuxBrowsers = ("nautilus", "dolphin", "konqueror", "thunar")

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
	def modulesManager(self):
		"""
		This method is the property for **self.__modulesManager** attribute.

		:return: self.__modulesManager. ( QObject )
		"""

		return self.__modulesManager

	@modulesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modulesManager(self, value):
		"""
		This method is the setter method for **self.__modulesManager** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is read only!".format("modulesManager"))

	@modulesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modulesManager(self):
		"""
		This method is the deleter method for **self.__modulesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("modulesManager"))

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

		self.Interfaces_listView.setParent(None)
		self.Interfaces_listView = Interfaces_QListView(self, self.__model)
		self.Interfaces_listView.setObjectName("Interfaces_listView")
		self.Interfaces_frame_splitter.insertWidget(0, self.Interfaces_listView)
		self.__view = self.Interfaces_listView
		self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__view_addActions()

		self.Snippets_Loader_Logo_label.setPixmap(QPixmap(os.path.join(RuntimeGlobals.resourcesDirectory,
																	UiConstants.snippetsLoaderLogo)))
		self.Search_Icon_label.setPixmap(QPixmap(os.path.join(RuntimeGlobals.resourcesDirectory,
															UiConstants.searchIcon)))

		self.Informations_textBrowser.setText(self.__defaultText)

		self.Interfaces_frame_splitter.setSizes([16777215, 0])

		self.setInterfaces(unicode())

		# Signals / Slots.
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
			self.executeInterface()

	@core.executionTrace
	def __Reload_Snippets_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Reload_Snippets_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.setInterfaces()

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

		self.executeInterface()

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
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setInterfaces(self, pattern=".*", flags=re.IGNORECASE):
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

		for name, module in self.__modulesManager:
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
	def executeInterface(self):
		"""
		This method triggers the selected Interface execution.
		
		:return: Method success. ( Boolean )
		"""

		interface = self.getSelectedInterface()
		if not interface:
			return

		module = interface.module
		method = interface.attribute

		LOGGER.info("{0} | Executing '{1}' Interface from '{2}' Module!".format(self.__class__.__name__,
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
