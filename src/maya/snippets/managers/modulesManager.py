#!/usr/bin/env python
# -*- coding: utf-8 -*-

#**********************************************************************************************************************
#
# Copyright (C) 2009 - 2012 - Thomas Mansencal - thomas.mansencal@gmail.com
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
import foundations.core as core
import foundations.exceptions
import foundations.namespace as namespace
from foundations.walkers import OsWalker
from snippets.globals.constants import Constants
from snippets.globals.runtimeGlobals import RuntimeGlobals
from snippets.globals.uiConstants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Module", "ModulesManager"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Module(object):
	"""
	This class is the **Module** class.
	"""

	@core.executionTrace
	def __init__(self, name=None, path=None):
		"""
		This method initializes the class.

		:param name: Name of the Component. ( String )
		:param path: Path of the Component. ( String )
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
		This method is the property for **self.___name** attribute.

		:return: self.__name. ( String )
		"""

		return self.__name

	@name.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def name(self, value):
		"""
		This method is the setter method for **self.___name** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' type is not 'str' or 'unicode'!".format("name",
																												value)
		self.__name = value

	@name.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def name(self):
		"""
		This method is the deleter method for **self.___name** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("name"))

	@property
	def path(self):
		"""
		This method is the property for **self.__paths** attribute.

		:return: self.__paths. ( String )
		"""

		return self.__paths

	@path.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def path(self, value):
		"""
		This method is the setter method for **self.__paths** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' Attribute: '{1}' type is not 'str' or 'unicode'!".format("path",
																												value)
			assert os.path.exists(value), "'{0}' Attribute: '{1}' directory doesn't exists!".format("path", value)
		self.__paths = value

	@path.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def path(self):
		"""
		This method is the deleter method for **self.__paths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("path"))

	@property
	def import_(self):
		"""
		This method is the property for **self.___import_** attribute.

		:return: self.__import. ( Module )
		"""

		return self.__import

	@import_.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def import_(self, value):
		"""
		This method is the setter method for **self.___import_** attribute.

		:param value: Attribute value. ( Module )
		"""

		if value is not None:
			assert type(value) is type(sys), "'{0}' Attribute: '{1}' type is not 'module'!".format("import", value)
		self.__import = value

	@import_.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def import_(self):
		"""
		This method is the deleter method for **self.___import_** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("import"))

	@property
	def interfaces(self):
		"""
		This method is the property for **self.__interfaces** attribute.

		:return: self.__interfaces. ( Object )
		"""

		return self.__interfaces

	@interfaces.setter
	def interfaces(self, value):
		"""
		This method is the setter method for **self.__interfaces** attribute.

		:param value: Attribute value. ( Object )
		"""

		self.__interfaces = value

	@interfaces.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def interfaces(self):
		"""
		This method is the deleter method for **self.__interfaces** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("interfaces"))

class ModulesManager(object):
	"""
	This class is the **ModulesManager** class.
	"""

	@core.executionTrace
	def __init__(self, paths=None):
		"""
		This method initializes the class.

		:param path: Paths of the modules. ( Tuple / List )
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
		This method is the property for **self.__paths** attribute.

		:return: self.__paths. ( List )
		"""

		return self.__paths

	@paths.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def paths(self, value):
		"""
		This method is the setter method for **self.__paths** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' Attribute: '{1}' type is not 'tuple' or 'list'!".format("paths", value)
			for path in value:
				assert os.path.exists(path), "'{0}' Attribute: '{1}' directory doesn't exists!".format("paths", value)
		self.__paths = value

	@paths.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def paths(self):
		"""
		This method is the deleter method for **self.__paths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("paths"))

	@property
	def modules(self):
		"""
		This method is the property for **self.__modules** attribute.

		:return: self.__modules. ( Dictionary )
		"""

		return self.__modules

	@modules.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def modules(self, value):
		"""
		This method is the setter method for **self.__modules** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' Attribute: '{1}' type is not 'dict'!".format("modules", value)
		self.__modules = value

	@modules.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modules(self):
		"""
		This method is the deleter method for **self.__modules** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Attribute is not deletable!".format("modules"))

	@property
	def libraryExtension(self):
		"""
		This method is the property for **self.__libraryExtension** attribute.

		:return: self.__libraryExtension. ( String )
		"""

		return self.__libraryExtension

	@libraryExtension.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def libraryExtension(self, value):
		"""
		This method is the setter method for **self.__libraryExtension** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "libraryExtension"))

	@libraryExtension.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def libraryExtension(self):
		"""
		This method is the deleter method for **self.__libraryExtension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "libraryExtension"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __getitem__(self, name):
		"""
		This method reimplements the :meth:`object.__getitem__` method.

		:param name: Module name. ( String )
		:return: Module. ( Module )
		"""

		for module in self.__modules.itervalues():
			if module.name == name:
				return module

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __iter__(self):
		"""
		This method reimplements the :meth:`object.__iter__` method.
		
		:return: Modules iterator. ( Object )
		"""

		return self.__modules.iteritems()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __contains__(self, name):
		"""
		This method reimplements the :meth:`object.__contains__` method.

		:param name: Module name. ( String )
		:return: Module existence. ( Boolean )
		"""

		return self[name] and True or False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __len__(self):
		"""
		This method reimplements the :meth:`object.__len__` method.

		:return: Modules count. ( Integer )
		"""

		return len(self.__modules)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listModules(self):
		"""
		This method lists the registered modules.

		:return: Modules list. ( List )
		"""

		return [module.name for module in self.iterkeys()]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def registerModule(self, name, path):
		"""
		This method registers given module.

		:param name: Module name. ( String )
		:param path: Module path. ( Layout )
		:return: Method success. ( Boolean )
		"""

		if name in self:
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' module is already registered!".format(
			self.__class__.__name__, name))

		name = namespace.getNamespace(name, rootOnly=True)
		self.__modules[name] = Module(name=name, path=os.path.dirname(path))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def unregisterModule(self, name):
		"""
		This method unregisters given module.

		:param name: Module name. ( String )
		:return: Method success. ( Boolean )
		"""

		if not name in self:
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' module is not registered!".format(
			self.__class__.__name__, name))

		del(self.__modules[name])
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def registerModules(self):
		"""
		This method gathers the modules.
		:return: Method success. ( Boolean )
		"""

		for directory in self.__paths:
			osWalker = OsWalker(directory)
			modules = osWalker.walk(filtersIn=(r"\.{0}$".format(self.__libraryExtension),))

			for name, path in modules.iteritems():
				self.registerModule(name, path)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, ImportError)
	def registerModuleInterfaces(self, module):
		"""
		This method instantiates given module interfaces.

		:param module: Module. ( Module )
		:return: Method success. ( Boolean )
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

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def registerInterfaces(self):
		"""
		This method registers modules interfaces.

		:return: Method success. ( Boolean )
		"""

		for name, module in self:
			self.registerModuleInterfaces(module)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def unregisterAll(self):
		"""
		This method unregisters modules and their interfaces.

		:return: Method success. ( Boolean )
		"""

		self.__modules = {}
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def registerAll(self):
		"""
		This method registers modules and their interfaces.

		:return: Method success. ( Boolean )
		"""

		self.registerModules()
		self.registerInterfaces()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def reloadAll(self):
		"""
		This method reloads all modules and their interfaces.

		:return: Method success. ( Boolean )
		"""

		self.unregisterAll()
		self.registerAll()
		return True
