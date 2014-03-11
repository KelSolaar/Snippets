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

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os

#**********************************************************************************************************************
#***	Dependencies globals manipulation.
#**********************************************************************************************************************
import foundations.globals.constants
from snippets.globals.constants import Constants

def _overrideDependenciesGlobals():
	"""
	Overrides dependencies globals.

	:return: Definition success.
	:rtype: bool
	"""

	foundations.globals.constants.Constants.logger = Constants.logger
	return True

_overrideDependenciesGlobals()

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose
import snippets.libraries.common
from snippets.globals.runtimeGlobals import RuntimeGlobals
from snippets.managers.modulesManager import ModulesManager

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Ui_Loader_Setup", "Ui_Loader_Type", "Loader"]

LOGGER = foundations.verbose.installLogger()

# Remove existing handlers.
del logging.root.handlers[:]

foundations.verbose.getLoggingConsoleHandler()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def _setModulesManager():
	"""
	Sets the global modules manager instance.
	"""

	if not isinstance(RuntimeGlobals.modulesManager, ModulesManager):
		RuntimeGlobals.modulesManager = ModulesManager([RuntimeGlobals.librariesDirectory])
		RuntimeGlobals.modulesManager.registerAll()

def run():
	"""
	Starts the Application.

	:return: Definition success.
	:rtype: bool
	"""

	RuntimeGlobals.librariesDirectory = os.path.join(os.path.dirname(__file__), Constants.librariesDirectory)
	RuntimeGlobals.resourcesDirectory = os.path.join(os.path.dirname(__file__), Constants.resourcesDirectory)

	_setModulesManager()
