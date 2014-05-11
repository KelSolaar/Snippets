#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**********************************************************************************************************************
#
# Copyright (C) 2009 - 2014 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#**********************************************************************************************************************

"""
**Common.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    UI common Module.

**Others:**

"""

from __future__ import unicode_literals

import os
import platform
import maya.OpenMayaUI as OpenMayaUI
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sip

import foundations.common
import foundations.verbose
from snippets.globals.constants import Constants
from snippets.globals.runtime_globals import RuntimeGlobals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

LOGGER = foundations.verbose.install_logger()


def get_resource_path(name):
    """
    Returns the resource file path matching the given name.

    :param name: Resource name.
    :type name: str
    :return: Resource path.
    :rtype: str
    """

    if not foundations.common.path_exists(RuntimeGlobals.resources_directory):
        return

    path = os.path.join(RuntimeGlobals.resources_directory, name)
    if foundations.common.path_exists(path):
        LOGGER.debug("> '{0}' resource path: '{1}'.".format(name, path))
        return path


def parents_walker(object):
    """
    Defines a generator used to retrieve the chain of parents of the given :class:`QObject` instance.

    :param object: Provided path.
    :type object: QObject
    :yield: Object parent. ( QObject )
    """

    while object.parent():
        object = object.parent()
        yield object


def get_maya_window():
    """
    Returns Maya window as QObject.

    :return: Maya window.
    :rtype: QObject
    """

    pointer = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(pointer), QObject)


def message_box(message_type, title, message):
    """
    Provides a fast gui message box.

    :param message_type: Message type.
    :type message_type: str
    :param title: Message box title.
    :type title: str
    :param message: Message content.
    :type message: str
    """

    LOGGER.debug("> Launching messagebox().")
    LOGGER.debug("> Message type: '%s'.", message_type)
    LOGGER.debug("> Title: '%s'.", title)
    LOGGER.debug("> Message: '%s'.", message)

    message_box = QMessageBox()
    message_box.setWindowTitle("Message | " + title)
    message_box.setText(message)

    if message_type == "Critical":
        message_box.setIcon(QMessageBox.Critical)
        LOGGER.critical("'%s'.", "MessageBox | " + message)
    elif message_type == "Error":
        message_box.setIcon(QMessageBox.Critical)
        LOGGER.error("'%s'.", "MessageBox | " + message)
    elif message_type == "Warning":
        message_box.setIcon(QMessageBox.Warning)
        LOGGER.warning("'%s'.", "MessageBox | " + message)
    elif message_type == "Information":
        message_box.setIcon(QMessageBox.Information)
        LOGGER.info("'%s'.", "MessageBox | " + message)

    message_box.setWindowFlags(Qt.WindowStaysOnTopHint)

    if platform.system() == "Linux":
        message_box.show()
        center_widget_on_screen(message_box)

    message_box.exec_()


def center_widget_on_screen(widget):
    """
    Centers given Widget middle of the screen.

    :param widget: Current Widget.
    :type widget: QWidget
    """

    widget.move(QApplication.desktop().width() / 2 - widget.width() / 2,
                QApplication.desktop().height() / 2 - widget.height() / 2)


def resize_widget(widget, size_x, size_y):
    """
    Resize given Widget.

    :param widget: Current Widget.
    :type widget: QWidget
    :param size_x: Size x.
    :type size_x: int
    :param size_y: Size y.
    :type size_y: int
    """

    widget.resize(int(size_x), int(size_y))
