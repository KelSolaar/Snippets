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
	Common functions Module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import re

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
from snippets.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "MayaLoggingHandler"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class MayaLoggingHandler(logging.Handler):
	"""
	Defines a Maya friendly logging handler.
	"""

	def emit(self, record):
		"""
		Emits the given record.

		:param record: Record. ( String )
		"""

		if record.levelno > logging.INFO:
			message = record.getMessage()
		else:
			message = self.format(record)

		if record.levelno > logging.ERROR:
			OpenMaya.MGlobal.displayError(message)
		elif record.levelno > logging.WARNING:
			OpenMaya.MGlobal.displayError(message)
		elif record.levelno > logging.INFO:
			OpenMaya.MGlobal.displayWarning(message)
		elif record.levelno <= logging.DEBUG:
			OpenMaya.MGlobal.displayInfo(message)
		else:
			OpenMaya.MGlobal.displayInfo(message)
