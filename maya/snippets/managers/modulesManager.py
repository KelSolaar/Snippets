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
	Libraries manager module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import re
import sys

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.namespace
import foundations.strings
import foundations.verbose
import foundations.walkers
from snippets.globals.constants import Constants
from snippets.globals.runtimeGlobals import RuntimeGlobals
from snippets.globals.uiConstants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Module", "ModulesManager"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Module(object):
	"""
	Defines the **Module** class.
	"""

	def __init__(self, name=None, path=None):
		"""
		Initializes the class.

		:param name: Name of the Component.
		:type name: str
		:param path: Path of the Component.
		:type path: str
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__name = None
		self.name = name
		self.paths = None
		self.__paths = path

		self.__import = None
		self.__interfaces = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def name(self):
		"""
		Property for **self.___name** attribute.

		:return: self.__name.
		:rtype: str
		"""

		return self.__name

	@name.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def name(self, value):
		"""
		Setter for **self.___name** attribute.

		:param value: Attribute value.
		:type value: str
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' type is not 'str' or 'unicode'!".format("name",
																												value)
		self.__name = value

	@name.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def name(self):
		"""
		Deleter for **self.___name** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("name"))

	@property
	def path(self):
		"""
		Property for **self.__paths** attribute.

		:return: self.__paths.
		:rtype: str
		"""

		return self.__paths

	@path.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def path(self, value):
		"""
		Setter for **self.__paths** attribute.

		:param value: Attribute value.
		:type value: str
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' type is not 'str' or 'unicode'!".format("path",
																												value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' directory doesn't exists!".format("path", value)
		self.__paths = value

	@path.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def path(self):
		"""
		Deleter for **self.__paths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("path"))

	@property
	def import_(self):
		"""
		Property for **self.___import_** attribute.

		:return: self.__import.
		:rtype: ModuleType
		"""

		return self.__import

	@import_.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def import_(self, value):
		"""
		Setter for **self.___import_** attribute.

		:param value: Attribute value.
		:type value: ModuleType
		"""

		if value is not None:
			assert type(value) is type(sys), "'{0}' Attribute: '{1}' type is not 'module'!".format("import", value)
		self.__import = value

	@import_.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def import_(self):
		"""
		Deleter for **self.___import_** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("import"))

	@property
	def interfaces(self):
		"""
		Property for **self.__interfaces** attribute.

		:return: self.__interfaces.
		:rtype: object
		"""

		return self.__interfaces

	@interfaces.setter
	def interfaces(self, value):
		"""
		Setter for **self.__interfaces** attribute.

		:param value: Attribute value.
		:type value: object
		"""

		self.__interfaces = value

	@interfaces.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def interfaces(self):
		"""
		Deleter for **self.__interfaces** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("interfaces"))

class ModulesManager(object):
	"""
	Defines the **ModulesManager** class.
	"""

	def __init__(self, paths=None):
		"""
		Initializes the class.

		:param path: Paths of the modules.
		:type path: tuple or list
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.paths = None
		self.__paths = paths

		self.__modules = {}
		self.__libraryExtension = Constants.libraryExtension

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def paths(self):
		"""
		Property for **self.__paths** attribute.

		:return: self.__paths.
		:rtype: list
		"""

		return self.__paths

	@paths.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def paths(self, value):
		"""
		Setter for **self.__paths** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' Attribute: '{1}' type is not 'tuple' or 'list'!".format("paths", value)
			for path in value:
				assert os.path.exists(path), "'{0}' Attribute: '{1}' directory doesn't exists!".format("paths", value)
		self.__paths = value

	@paths.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def paths(self):
		"""
		Deleter for **self.__paths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("paths"))

	@property
	def modules(self):
		"""
		Property for **self.__modules** attribute.

		:return: self.__modules.
		:rtype: dict
		"""

		return self.__modules

	@modules.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def modules(self, value):
		"""
		Setter for **self.__modules** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' Attribute: '{1}' type is not 'dict'!".format("modules", value)
		self.__modules = value

	@modules.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def modules(self):
		"""
		Deleter for **self.__modules** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("modules"))

	@property
	def libraryExtension(self):
		"""
		Property for **self.__libraryExtension** attribute.

		:return: self.__libraryExtension.
		:rtype: str
		"""

		return self.__libraryExtension

	@libraryExtension.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def libraryExtension(self, value):
		"""
		Setter for **self.__libraryExtension** attribute.

		:param value: Attribute value.
		:type value: str
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "libraryExtension"))

	@libraryExtension.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def libraryExtension(self):
		"""
		Deleter for **self.__libraryExtension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "libraryExtension"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __getitem__(self, name):
		"""
		Reimplements the :meth:`object.__getitem__` method.

		:param name: Module name.
		:type name: str
		:return: Module.
		:rtype: ModuleType
		"""

		for module in self.__modules.itervalues():
			if module.name == name:
				return module

	def __iter__(self):
		"""
		Reimplements the :meth:`object.__iter__` method.
		
		:return: Modules iterator.
		:rtype: object
		"""

		return self.__modules.iteritems()

	def __contains__(self, name):
		"""
		Reimplements the :meth:`object.__contains__` method.

		:param name: Module name.
		:type name: str
		:return: Module existence.
		:rtype: bool
		"""

		return self[name] and True or False

	def __len__(self):
		"""
		Reimplements the :meth:`object.__len__` method.

		:return: Modules count.
		:rtype: int
		"""

		return len(self.__modules)

	def listModules(self):
		"""
		Lists the registered modules.

		:return: Modules list.
		:rtype: list
		"""

		return [module.name for module in self.iterkeys()]

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def registerModule(self, name, path):
		"""
		Registers given module.

		:param name: Module name.
		:type name: str
		:param path: Module path.
		:type path: Layout
		:return: Method success.
		:rtype: bool
		"""

		if name in self:
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' module is already registered!".format(
			self.__class__.__name__, name))

		self.__modules[name] = Module(name=name, path=os.path.dirname(path))
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def unregisterModule(self, name):
		"""
		Unregisters given module.

		:param name: Module name.
		:type name: str
		:return: Method success.
		:rtype: bool
		"""

		if not name in self:
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' module is not registered!".format(
			self.__class__.__name__, name))

		del(self.__modules[name])
		return True

	def registerModules(self):
		"""
		Gathers the modules.
		:return: Method success.
		:rtype: bool
		"""

		for directory in self.__paths:
			for path in foundations.walkers.filesWalker(directory, filtersIn=(r"\.{0}$".format(self.__libraryExtension),)):
				self.registerModule(foundations.strings.getSplitextBasename(path), path)
		return True

	def registerModuleInterfaces(self, module):
		"""
		Instantiates given module interfaces.

		:param module: Module.
		:type module: ModuleType
		:return: Method success.
		:rtype: bool
		"""

		if module.path not in sys.path:
			sys.path.append(module.path)

		if module.name in sys.modules:
			del(sys.modules[module.name])

		module.import_ = __import__(module.name)

		interfaces = [attribute for attribute in module.import_.__dict__ if re.search(r"^I[A-Z]\w+", attribute)]
		if interfaces:
			LOGGER.info("{0} | Registering '{1}' Interfaces from '{2}' Module!".format(self.__class__.__name__,
																						interfaces, module.name))
			module.interfaces = interfaces
			return True

	def registerInterfaces(self):
		"""
		Registers modules interfaces.

		:return: Method success.
		:rtype: bool
		"""

		for name, module in self:
			self.registerModuleInterfaces(module)
		return True

	def unregisterAll(self):
		"""
		Unregisters modules and their interfaces.

		:return: Method success.
		:rtype: bool
		"""

		self.__modules = {}
		return True

	def registerAll(self):
		"""
		Registers modules and their interfaces.

		:return: Method success.
		:rtype: bool
		"""

		self.registerModules()
		self.registerInterfaces()
		return True

	def reloadAll(self):
		"""
		Reloads all modules and their interfaces.

		:return: Method success.
		:rtype: bool
		"""

		self.unregisterAll()
		self.registerAll()
		return True
