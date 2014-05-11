#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**********************************************************************************************************************
#
# Copyright (C) 2009 - 2014 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#**********************************************************************************************************************

"""
**Constants.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Snippets constants Module.

**Others:**

"""

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["Constants"]


class Constants():
    """
    Defines the **Constants** class.
    """

    logger = "Snippets_Logger"
    verbosity_level = 3
    logging_separators = "*" * 96

    library_extension = "py"
    library_compiled_extension = "pyc"

    libraries_directory = "libraries"
    resources_directory = "resources"

    null_object = "None"
