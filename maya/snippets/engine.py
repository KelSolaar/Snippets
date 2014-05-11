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
    Engine module.

**Others:**

"""

from __future__ import unicode_literals

import logging
import os

import foundations.globals.constants
from snippets.globals.constants import Constants


def _override_dependencies_globals():
    """
    Overrides dependencies globals.

    :return: Definition success.
    :rtype: bool
    """

    foundations.globals.constants.Constants.logger = Constants.logger
    return True


_override_dependencies_globals()

import foundations.verbose
import snippets.libraries.common
from snippets.globals.runtime_globals import RuntimeGlobals
from snippets.managers.modules_manager import ModulesManager

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Ui_Loader_Setup", "Ui_Loader_Type", "Loader"]

LOGGER = foundations.verbose.install_logger()

# Remove existing handlers.
del logging.root.handlers[:]

foundations.verbose.get_logging_console_handler()


def _set_modules_manager():
    """
    Sets the global modules manager instance.
    """

    if not isinstance(RuntimeGlobals.modules_manager, ModulesManager):
        RuntimeGlobals.modules_manager = ModulesManager([RuntimeGlobals.libraries_directory])
        RuntimeGlobals.modules_manager.register_all()


def run():
    """
    Starts the Application.

    :return: Definition success.
    :rtype: bool
    """

    RuntimeGlobals.libraries_directory = os.path.join(os.path.dirname(__file__), Constants.libraries_directory)
    RuntimeGlobals.resources_directory = os.path.join(os.path.dirname(__file__), Constants.resources_directory)

    _set_modules_manager()
