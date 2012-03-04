#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**********************************************************************************************************************
#
# Copyright (C) 2009 - 2012 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#**********************************************************************************************************************

"""
**popup.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Popup module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import maya.cmds as cmds
import maya.mel as mel
import re
from PyQt4 import uic
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QStringListModel

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import snippets.ui.common
from snippets.globals.constants import Constants
from snippets.globals.runtimeGlobals import RuntimeGlobals
from snippets.globals.uiConstants import UiConstants
from snippets.ui.models import Interface
from snippets.ui.models import InterfacesModel
from snippets.ui.widgets.search_QLineEdit import Search_QLineEdit

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Ui_Popup_Type", "Ui_Popup_Setup", "Popup"]

LOGGER = logging.getLogger(Constants.logger)

print RuntimeGlobals.resourcesDirectory
RuntimeGlobals.popupUiFile = snippets.ui.common.getResourcePath(UiConstants.popupUiFile)
if foundations.common.pathExists(RuntimeGlobals.popupUiFile):
	Ui_Popup_Setup, Ui_Popup_Type = uic.loadUiType(RuntimeGlobals.popupUiFile)
else:
	error = "'{0}' Ui file is not available!".format(RuntimeGlobals.popupUiFile)
	snippets.ui.common.messageBox("Error", "Error", error)
	raise Exception(error)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Popup(Ui_Popup_Type, Ui_Popup_Setup):
	"""
	"""

	@core.executionTrace
	def __init__(self, parent=None, modulesManager=RuntimeGlobals.modulesManager):
		"""
		This method initializes the class.
		
		:param parent: Parent object. ( QObject )
		:param modulesManager: Modules Manager. ( ModulesManager )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		Ui_Popup_Type.__init__(self, parent)
		Ui_Popup_Setup.__init__(self)

		self.setupUi(self)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__modulesManager = modulesManager

		self.__model = None
		self.__view = None

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

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def show(self):
		"""
		This method reimplements the :meth:`QWidget.show` method.
		"""

		super(Popup, self).show()
		self.Interfaces_lineEdit.setText(RuntimeGlobals.popupPattern or QString())
		self.Interfaces_lineEdit.setFocus()

	@core.executionTrace
	def __initializeUI(self):
		"""
		This method triggers the **Methods_listWidget** Widget.
		"""

		self.setWindowFlags(Qt.Popup)
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.__model = InterfacesModel(self)

		self.Interfaces_lineEdit.setParent(None)
		self.Interfaces_lineEdit = Search_QLineEdit(self)
		self.Interfaces_lineEdit.setObjectName("Interfaces_lineEdit")
		# self.Interfaces_lineEdit.setPlaceholderText("Enter Interface Name...")
		self.Popup_Form_gridLayout.addWidget(self.Interfaces_lineEdit)

		self.setInterfaces()

		# Signals / Slots.
		self.Interfaces_lineEdit.returnPressed.connect(self.__Interfaces_lineEdit__returnPressed)

	@core.executionTrace
	def __Interfaces_lineEdit__returnPressed(self):
		"""
		This method is triggered when **Interfaces_lineEdit** Widget when return is pressed.
		"""

		pattern = RuntimeGlobals.popupPattern = self.Interfaces_lineEdit.text()
		interface = self.getInterface(strings.encode("^{0}$".format(pattern)))
		if not interface:
			return

		self.executeInterface(interface)
		self.close()

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

		interfaces = []
		for name, module in self.__modulesManager:
			if not module.interfaces:
				continue

			for interface in module.interfaces:
				name = strings.getNiceName(self.getMethodName(interface))
				if re.search(pattern, name):
					interfaces.append(name)
					self.__model.registerInterface(Interface(name=name, attribute=interface, module=module))
		self.Interfaces_lineEdit.completer.setModel(QStringListModel(sorted(interfaces)))
		return True

	@core.executionTrace
	def getMethodName(self, name):
		"""
		This method gets the method name from the Interface.

		:param name: Interface name. ( String )
		:return: Method name. ( String )
		"""

		return "{0}{1}".format(name[1].lower(), name[2:])

	@core.executionTrace
	def getInterface(self, pattern):
		"""
		This method returns the Interface with given name.

		:param pattern: Interface name. ( String )
		:param flags: Regex filtering flags. ( Integer )
		:return: Method success. ( Boolean )
		"""

		for interface in self.__model:
			if not hasattr(interface, "attribute"):
				continue

			if re.search(pattern, interface.name):
				return interface

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def executeInterface(self, interface):
		"""
		This method executes the object associated with given Interface.
		
		:param interface: Interface. ( interface )
		:return: Method success. ( Boolean )
		"""

		if not interface:
			return

		module = interface.module
		method = interface.attribute

		LOGGER.info("{0} | Executing '{1}' Interface from '{2}' Module!".format(self.__class__.__name__,
																			method,
																			module.name))
		module.import_.__dict__[method]()
		return True
