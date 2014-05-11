#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**********************************************************************************************************************
#
# Copyright (C) 2009 - 2014 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#**********************************************************************************************************************

"""
**runtime_globals.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Snippets runtime globals Module.

**Others:**

"""

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RuntimeGlobals"]

class RuntimeGlobals():
	"""
	Defines the runtime globals class.
	"""

	loader_ui_file = None
	popup_ui_file = None

	modules_manager = None

	libraries_directory = None
	resources_directory = None

	popup_pattern = None
