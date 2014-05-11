#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**********************************************************************************************************************
#
# Copyright (C) 2009 - 2014 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#**********************************************************************************************************************

"""
**loader.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`Loader` class.

**Others:**

"""

from __future__ import unicode_literals

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

import foundations.exceptions
import foundations.strings
import foundations.verbose
import snippets.ui.common
from foundations.environment import Environment
from snippets.globals.constants import Constants
from snippets.globals.runtime_globals import RuntimeGlobals
from snippets.globals.ui_constants import UiConstants
from snippets.ui.models import Interface
from snippets.ui.models import InterfacesModel
from snippets.ui.views import Interfaces_QListView
from snippets.ui.widgets.search_QLineEdit import Search_QLineEdit

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Ui_Loader_Setup", "Ui_Loader_Type", "Loader"]

LOGGER = foundations.verbose.install_logger()

RuntimeGlobals.loader_ui_file = snippets.ui.common.get_resource_path(UiConstants.loader_ui_file)
if foundations.common.path_exists(RuntimeGlobals.loader_ui_file):
    Ui_Loader_Setup, Ui_Loader_Type = uic.loadUiType(RuntimeGlobals.loader_ui_file)
else:
    error = "'{0}' Ui file is not available!".format(RuntimeGlobals.loader_ui_file)
    snippets.ui.common.message_box("Error", "Error", error)
    raise Exception(error)

class Loader(Ui_Loader_Type, Ui_Loader_Setup):
    """
    Defines the complex Maya Interfaces loader widget.
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

        Ui_Loader_Type.__init__(self, parent)
        Ui_Loader_Setup.__init__(self)

        self.setupUi(self)

        # --- Setting class attributes. ---
        self.__container = parent
        self.__modules_manager = modules_manager

        self.__model = None
        self.__view = None

        self.__default_text = "<center><br/><br/><h4>* * *</h4>Select a Snippet to display related informations!<h4>* * *</h4></center>"

        self.__linux_text_editors = ("gedit", "kwrite", "nedit", "mousepad")
        self.__linux_browsers = ("nautilus", "dolphin", "konqueror", "thunar")

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

    @property
    def view(self):
        """
        Property for **self.__view** attribute.

        :return: self.__view.
        :rtype: QWidget
        """

        return self.__view

    @view.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def view(self, value):
        """
        Setter for **self.__view** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

    @view.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def view(self):
        """
        Deleter for **self.__view** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

    @property
    def default_text(self):
        """
        Property for **self.__default_text** attribute.

        :return: self.__default_text.
        :rtype: str
        """

        return self.__default_text

    @default_text.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_text(self, value):
        """
        Setter for **self.__default_text** attribute.

        :param value: Attribute value.
        :type value: str
        """

        raise foundations.exceptions.ProgrammingError("'{0}' Attribute is read only!".format("default_text"))

    @default_text.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_text(self):
        """
        Deleter for **self.__default_text** attribute.
        """

        raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("default_text"))

    @property
    def linux_text_editors(self):
        """
        Property for **self.__linux_text_editors** attribute.

        :return: self.__linux_text_editors.
        :rtype: tuple
        """

        return self.__linux_text_editors

    @linux_text_editors.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def linux_text_editors(self, value):
        """
        Setter for **self.__linux_text_editors** attribute.

        :param value: Attribute value.
        :type value: tuple
        """

        raise foundations.exceptions.ProgrammingError("'{0}' Attribute is read only!".format("linux_text_editors"))

    @linux_text_editors.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def linux_text_editors(self):
        """
        Deleter for **self.__linux_text_editors** attribute.
        """

        raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("linux_text_editors"))

    @property
    def linux_browsers(self):
        """
        Property for **self.__linux_browsers** attribute.

        :return: self.__linux_browsers.
        :rtype: QObject
        """

        return self.__linux_browsers

    @linux_browsers.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def linux_browsers(self, value):
        """
        Setter for **self.__linux_browsers** attribute.

        :param value: Attribute value.
        :type value: QObject
        """

        raise foundations.exceptions.ProgrammingError("'{0}' Attribute is read only!".format("linux_browsers"))

    @linux_browsers.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def linux_browsers(self):
        """
        Deleter for **self.__linux_browsers** attribute.
        """

        raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("linux_browsers"))

    def __initialize_ui(self):
        """
        Initializes the Widget.
        """

        self.Search_lineEdit.setParent(None)
        self.Search_lineEdit = Search_QLineEdit(self)
        self.Search_lineEdit.setObjectName("Search_lineEdit")
        hasattr(self.Search_lineEdit, "setPlaceholderText") and \
        self.Search_lineEdit.setPlaceholderText("Enter Interface Name...")
        self.Search_horizontalLayout.addWidget(self.Search_lineEdit)

        self.__model = InterfacesModel(self)

        self.Interfaces_listView.setParent(None)
        self.Interfaces_listView = Interfaces_QListView(self, self.__model)
        self.Interfaces_listView.setObjectName("Interfaces_listView")
        self.Interfaces_frame_splitter.insertWidget(0, self.Interfaces_listView)
        self.__view = self.Interfaces_listView
        self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.__view_add_actions()

        self.Snippets_Loader_Logo_label.setPixmap(QPixmap(os.path.join(RuntimeGlobals.resources_directory,
                                                                    UiConstants.snippets_loader_logo)))

        self.Informations_textBrowser.setText(self.__default_text)

        self.Interfaces_frame_splitter.setSizes([16777215, 0])

        self.set_interfaces()

        # Signals / Slots.
        self.Execute_Snippet_pushButton.clicked.connect(self.__Execute_Snippet_pushButton__clicked)
        self.Reload_Snippets_pushButton.clicked.connect(self.__Reload_Snippets_pushButton__clicked)
        self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
        self.__view.doubleClicked.connect(self.__view__doubleClicked)
        self.Search_lineEdit.textChanged.connect(self.__Search_lineEdit__textChanged)

    def __view_add_actions(self):
        """
        Sets the View actions.
        """

        editSnippetAction = QAction("Edit Snippet", self.__view)
        editSnippetAction.triggered.connect(self.__view_editSnippetAction)
        self.__view.addAction(editSnippetAction)

        exploreSnippetFolderAction = QAction("Explore Snippet Folder", self.__view)
        exploreSnippetFolderAction.triggered.connect(self.__view_exploreSnippetFolderAction)
        self.__view.addAction(exploreSnippetFolderAction)

    def __view_editSnippetAction(self, checked):
        """
        Defines the slot triggered by **editSnippetAction** action.

        :param checked: Checked state.
        :type checked: bool
        """

        interface = self.get_selected_interface()
        if not interface:
            return

        self.edit_file(interface.module.import_.__file__.replace(
        Constants.library_compiled_extension, Constants.library_extension))

    def __view_exploreSnippetFolderAction(self, checked):
        """
        Defines the slot triggered by **exploreSnippetFolderAction** action.

        :param checked: Checked state.
        :type checked: bool
        """

        interface = self.get_selected_interface()
        if not interface:
            return

        self.explore_directory(os.path.dirname(interface.module.import_.__file__))

    def __Execute_Snippet_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Execute_Snippet_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.execute_interface()

    def __Reload_Snippets_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Reload_Snippets_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.__modules_manager.reload_all()
        self.set_interfaces()

    def __view_selectionModel__selectionChanged(self, selected_items, deselected_items):
        """
        Sets the **Informations_textBrowser** Widget.

        :param selected_items: Selected items.
        :type selected_items: QItemSelection
        :param deselected_items: Deselected items.
        :type deselected_items: QItemSelection
        """

        interface = self.get_selected_interface()
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
                        self.get_method_name(interface.attribute),
                        interface.attribute,
                        arguments.args,
                        arguments.defaults,
                        arguments.varargs,
                        arguments.keywords,
                        interface.module.import_.__dict__[interface.attribute].__doc__)
        else:
            content = self.__default_text

        LOGGER.debug("> Update 'Informations_textBrowser' Widget content: '{0}'.".format(content))
        self.Informations_textBrowser.setText(content)

    def __view__doubleClicked(self, index):
        """
        Defines the slot triggered by **Interfaces_listView** Widget when double clicked.

        :param index: Current index.
        :type index: QModelIndex
        """

        self.execute_interface()

    def __Search_lineEdit__textChanged(self, text):
        """
        Defines the slot triggered by **Search_lineEdit** Widget when text changed.

        :param text: Current text value.
        :type text: QString
        """

        self.set_interfaces(foundations.strings.to_string(text))

    def get_method_name(self, name):
        """
        Returns the method name from the Interface.

        :param name: Interface name.
        :type name: str
        :return: Method name.
        :rtype: str
        """

        return " ".join(map(lambda x: x.title(), name.split("_")))

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

        for name, module in self.__modules_manager:
            if not module.interfaces:
                continue

            for interface in module.interfaces:
                name = foundations.strings.get_nice_name(self.get_method_name(interface))
                if re.search(pattern, name):
                    self.__model.register_interface(Interface(name=name, attribute=interface, module=module))
        return True

    def get_selected_interface(self):
        """
        Returns the current selected Interface.

        :return: Selected interface.
        :rtype: Interface
        """

        items = [self.__model.get_interface(index) for index in self.__view.selectionModel().selectedIndexes()]
        return items and items[0]

    def execute_interface(self):
        """
        Triggers the selected Interface execution.

        :return: Method success.
        :rtype: bool
        """

        interface = self.get_selected_interface()
        if not interface:
            return

        module = interface.module
        method = interface.attribute

        LOGGER.info("{0} | Executing '{1}' Interface from '{2}' Module!".format(self.__class__.__name__,
                                                                            method,
                                                                            module.name))
        module.import_.__dict__[method]()
        return True

    def edit_file(self, file):
        """
        Provides editing capability.

        :param file: File to edit.
        :type file: str
        :return: Method success.
        :rtype: bool
        """

        edit_command = None

        file = os.path.normpath(file)
        if platform.system() == "Windows" or platform.system() == "Microsoft":
            LOGGER.info("{0} | Launching 'notepad.exe' with '{1}'.".format(self.__class__.__name__, file))
            edit_command = "notepad.exe \"{0}\"".format(file)
        elif platform.system() == "Darwin":
            LOGGER.info("{0} | Launching default text editor with '{1}'.".format(self.__class__.__name__, file))
            edit_command = "open -e \"{0}\"".format(file)
        elif platform.system() == "Linux":
            environment_variable = Environment("PATH")
            paths = environment_variable.get_value().split(":")

            editor_found = False
            for editor in self.__linux_text_editors:
                if not editor_found:
                    try:
                        for path in paths:
                            if os.path.exists(os.path.join(path, editor)):
                                LOGGER.info("{0} | Launching '{1}' text editor with '{2}'.".format(self.__class__.__name__, editor, file))
                                edit_command = "\"{0}\" \"{1}\"".format(editor, file)
                                editor_found = True
                                raise StopIteration
                    except StopIteration:
                        pass
                else:
                    break
        if edit_command:
            LOGGER.debug("> Current edit command: '{0}'.".format(edit_command))
            edit_process = QProcess()
            edit_process.startDetached(edit_command)
        return True

    def explore_directory(self, directory):
        """
        Provides directory exploring capability.

        :param directory: Folder to explore.
        :type directory: str
        :return: Method success.
        :rtype: bool
        """

        browser_command = None

        directory = os.path.normpath(directory)
        if platform.system() == "Windows" or platform.system() == "Microsoft":
            LOGGER.info("{0} | Launching 'explorer.exe' with '{1}'.".format(self.__class__.__name__, directory))
            browser_command = "explorer.exe \"{0}\"".format(directory)
        elif platform.system() == "Darwin":
            LOGGER.info("{0} | Launching 'Finder' with '{1}'.".format(self.__class__.__name__, directory))
            browser_command = "open \"{0}\"".format(directory)
        elif platform.system() == "Linux":
            environment_variable = Environment("PATH")
            paths = environment_variable.get_value().split(":")

            browser_found = False
            for browser in self.__linux_browsers:
                if not browser_found:
                    try:
                        for path in paths:
                            if os.path.exists(os.path.join(path, browser)):
                                LOGGER.info("{0} | Launching '{1}' file browser with '{1}'.".format(self.__class__.__name__,
                                                                                                    browser,
                                                                                                    directory))
                                browser_command = "\"{0}\" \"{1}\"".format(browser, directory)
                                browser_found = True
                                raise StopIteration
                    except StopIteration:
                        pass
                else:
                    break

        if browser_command:
            LOGGER.debug("> Current browser command: '{0}'.".format(browser_command))
            browser_process = QProcess()
            browser_process.startDetached(browser_command)
        return True
