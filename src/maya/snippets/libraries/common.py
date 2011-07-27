#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2009 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

"""
**Common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Common Functions Module.

**Others:**

"""

#***********************************************************************************************
#***	Python Begin.
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports.
#***********************************************************************************************
import logging
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import re

#***********************************************************************************************
#***	Internal Imports.
#***********************************************************************************************
import foundations.core as core
from snippets.globals.constants import Constants

#***********************************************************************************************
#***	Global Variables.
#***********************************************************************************************
LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module Classes And Definitions.
#***********************************************************************************************
class MayaLoggingHandler(logging.Handler):
	"""
	This Class Provides A Maya Friendly Logging Handler.
	"""

	def emit(self, record):
		"""
		This Method Emits The Provided Record.

		@param record: Record. ( String )
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

#***********************************************************************************************
#***	Python End.
#***********************************************************************************************
