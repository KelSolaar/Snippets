#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**********************************************************************************************************************
#
# Copyright (C) 2009 - 2012 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#**********************************************************************************************************************

"""
**RuntimeGlobals.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Snippets runtime globals Module.

**Others:**

"""

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RuntimeGlobals"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RuntimeGlobals():
	"""
	This class is the runtime globals class.
	"""

	loaderUiFile = None
	popupUiFile = None

	modulesManager = None

	librariesDirectory = None
	resourcesDirectory = None

	popupPattern = None
