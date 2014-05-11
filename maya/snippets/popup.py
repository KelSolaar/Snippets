#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**********************************************************************************************************************
#
# Copyright (C) 2009 - 2014 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#**********************************************************************************************************************

"""
**popup.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`Popup` class.

**Others:**

"""

from __future__ import unicode_literals

import logging
import maya.cmds as cmds
import maya.mel as mel
import re
from PyQt4 import uic
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QStringListModel
from PyQt4.QtGui import QCursor

import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import snippets.ui.common
from snippets.globals.constants import Constants
from snippets.globals.runtime_globals import RuntimeGlobals
from snippets.globals.ui_constants import UiConstants
from snippets.ui.models import Interface
from snippets.ui.models import InterfacesModel
from snippets.ui.widgets.search_QLineEdit import Search_QLineEdit

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Ui_Popup_Type", "Ui_Popup_Setup", "Popup"]

LOGGER = foundations.verbose.install_logger()

RuntimeGlobals.popup_ui_file = snippets.ui.common.get_resource_path(UiConstants.popup_ui_file)
if foundations.common.path_exists(RuntimeGlobals.popup_ui_file):
    Ui_Popup_Setup, Ui_Popup_Type = uic.loadUiType(RuntimeGlobals.popup_ui_file)
else:
    error = "'{0}' Ui file is not available!".format(RuntimeGlobals.popup_ui_file)
    snippets.ui.common.message_box("Error", "Error", error)
    raise Exception(error)

class Popup(Ui_Popup_Type, Ui_Popup_Setup):
    """
    Defines the simple Maya Interfaces loader widget.
    """

    def __init__(self, parent=None, modules_manager=RuntimeGlobals.modules_manager):
        """
        Initializes the class.

        :param parent: Parent object.
        :type parent: QObject
        :param modules_manager: Modules Manager.
        :type modules_manager: ModulesManager
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        Ui_Popup_Type.__init__(self, parent)
        Ui_Popup_Setup.__init__(self)

        self.setupUi(self)

        # --- Setting class attributes. ---
        self.__container = parent
        self.__modules_manager = modules_manager

        self.__model = None
        self.__view = None

        # --- Initialize Ui. ---
        self.__initialize_ui()

    @property
    def container(self):
        """
        Property for **self.__container** attribute.

        :return: self.__container.
        :rtype: QObject
        """

        return self.__container

    @container.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def container(self, value):
        """
        Setter for **self.__container** attribute.

        :param value: Attribute value.
        :type value: QObject
        """

        raise foundations.exceptions.ProgrammingError("'{0}' Attribute is read only!".format("container"))

    @container.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def container(self):
        """
        Deleter for **self.__container** attribute.
        """

        raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("container"))

    @property
    def modules_manager(self):
        """
        Property for **self.__modules_manager** attribute.

        :return: self.__modules_manager.
        :rtype: QObject
        """

        return self.__modules_manager

    @modules_manager.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def modules_manager(self, value):
        """
        Setter for **self.__modules_manager** attribute.

        :param value: Attribute value.
        :type value: QObject
        """

        raise foundations.exceptions.ProgrammingError("'{0}' Attribute is read only!".format("modules_manager"))

    @modules_manager.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def modules_manager(self):
        """
        Deleter for **self.__modules_manager** attribute.
        """

        raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("modules_manager"))

    @property
    def model(self):
        """
        Property for **self.__model** attribute.

        :return: self.__model.
        :rtype: TemplatesModel
        """

        return self.__model

    @model.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def model(self, value):
        """
        Setter for **self.__model** attribute.

        :param value: Attribute value.
        :type value: TemplatesModel
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

    @model.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def model(self):
        """
        Deleter for **self.__model** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

    def show(self):
        """
        Reimplements the :meth:`QWidget.show` method.
        """

        self.move(QCursor.pos().x() - self.width() / 2, QCursor.pos().y() - self.height() / 2)
        self.Interfaces_lineEdit.setText(RuntimeGlobals.popup_pattern or QString())
        self.Interfaces_lineEdit.setFocus()
        super(Popup, self).show()

    def __initialize_ui(self):
        """
        Triggers the **Methods_listWidget** Widget.
        """

        self.setWindowFlags(Qt.Popup)

        self.__model = InterfacesModel(self)

        self.Interfaces_lineEdit.setParent(None)
        self.Interfaces_lineEdit = Search_QLineEdit(self)
        self.Interfaces_lineEdit.setObjectName("Interfaces_lineEdit")
        # self.Interfaces_lineEdit.setPlaceholderText("Enter Interface Name...")
        self.Popup_Form_gridLayout.addWidget(self.Interfaces_lineEdit)

        self.set_interfaces()

        # Signals / Slots.
        self.Interfaces_lineEdit.returnPressed.connect(self.__Interfaces_lineEdit__returnPressed)

    def __Interfaces_lineEdit__returnPressed(self):
        """
        Defines the slot triggered by **Interfaces_lineEdit** Widget when return pressed.
        """

        self.__triggerInterface(self.Interfaces_lineEdit.text())

    def __triggerInterface(self, name):
        """
        Triggers the Interface with given name execution.

        :param name: Interface name.
        :type name: str
        """

        pattern = RuntimeGlobals.popup_pattern = name
        interface = self.get_interface(foundations.strings.to_string("^{0}$".format(pattern)))
        if not interface:
            return

        self.execute_interface(interface)
        self.close()

    def set_interfaces(self, pattern=".*", flags=re.IGNORECASE):
        """
        Sets the Model interfaces.

        :param pattern: Interface name.
        :type pattern: str
        :param flags: Regex filtering flags.
        :type flags: int
        :return: Method success.
        :rtype: bool
        """

        try:
            pattern = re.compile(pattern, flags)
        except Exception:
            return

        self.__model.clear()

        interfaces = []
        for name, module in self.__modules_manager:
            if not module.interfaces:
                continue

            for interface in module.interfaces:
                name = foundations.strings.get_nice_name(self.get_method_name(interface))
                if re.search(pattern, name):
                    interfaces.append(name)
                    self.__model.register_interface(Interface(name=name, attribute=interface, module=module))
        self.Interfaces_lineEdit.completer.setModel(QStringListModel(sorted(interfaces)))
        return True

    def get_method_name(self, name):
        """
        Gets the method name from the Interface.

        :param name: Interface name.
        :type name: str
        :return: Method name.
        :rtype: str
        """

        return " ".join(map(lambda x: x.title(), name.split("_")))

    def get_interface(self, pattern):
        """
        Returns the Interface with given name.

        :param pattern: Interface name.
        :type pattern: str
        :param flags: Regex filtering flags.
        :type flags: int
        :return: Method success.
        :rtype: bool
        """

        for interface in self.__model:
            if not hasattr(interface, "attribute"):
                continue

            if re.search(pattern, interface.name):
                return interface

    def execute_interface(self, interface):
        """
        Executes the object associated with given interface.

        :param interface: Interface.
        :type interface: Interface
        :return: Method success.
        :rtype: bool
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
