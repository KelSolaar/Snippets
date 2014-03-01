#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`snippets.loader.Loader` class Models.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtCore import QAbstractListModel
from PyQt4.QtCore import QModelIndex
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.dataStructures
import foundations.exceptions
import foundations.verbose
from snippets.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"Categorie",
			"Interface",
			"InterfacesModel"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Categorie(foundations.dataStructures.Structure):
	"""
	This is the **Interface** class.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param kwargs: name. ( Key / Value pairs )
		"""

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class Interface(foundations.dataStructures.Structure):
	"""
	This is the **Interface** class.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param kwargs: name, attribute, module. ( Key / Value pairs )
		"""

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class InterfacesModel(QAbstractListModel):
	"""
	Defines a `QAbstractListModel <http://doc.qt.nokia.com/qabstractListmodel.html>`_ subclass.
	"""

	def __init__(self, parent=None, interfaces=None):
		"""
		Initializes the class.

		:param parent: Parent object. ( QObject )
		:param interfaces: InterfacesModel. ( List )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QAbstractListModel.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__interfaces = []
		self.interfaces = interfaces or self.__interfaces

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def interfaces(self):
		"""
		Property for **self.__interfaces** attribute.

		:return: self.__interfaces. ( List )
		"""

		return self.__interfaces

	@interfaces.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def interfaces(self, value):
		"""
		Setter for **self.__interfaces** attribute.

		:param value: Attribute value. ( List )
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("interfaces", value)
			for element in value:
				assert type(element) is Interface, "'{0}' attribute: '{1}' type is not 'Interface'!".format("interfaces", element)
		# TODO: Rollback to beginResetModel() whenever MPC changes it's PyQt version.	
		self.modelAboutToBeReset.emit()
		self.__interfaces = value
		# TODO: Rollback to endResetModel () whenever MPC changes it's PyQt version.
		self.modelReset.emit()

	@interfaces.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def interfaces(self):
		"""
		Deleter for **self.__interfaces** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "interfaces"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __getitem__(self, name):
		"""
		Reimplements the :meth:`object.__getitem__` method.
		
		:param name: Item name. ( String )
		:return: Item. ( Interface ) 
		"""

		for item in self.__interfaces:
			if item.name == name:
				return item

	def __iter__(self):
		"""
		Reimplements the :meth:`object.__iter__` method.

		:return: Interfaces iterator. ( Object )
		"""

		return iter(self.__interfaces)

	def __reversed__(self):
		"""
		Reimplements the :meth:`object.__reversed__` method.

		:return: Reverse interfaces iterator. ( Object )
		"""

		return reversed(self.__interfaces)

	def __contains__(self, name):
		"""
		Reimplements the :meth:`object.__contains__` method.

		:param name: Item name. ( String )
		:return: Item existence. ( Boolean )
		"""

		return self[name] and True or False

	def __len__(self):
		"""
		Reimplements the :meth:`object.__len__` method.

		:return: Interfaces count. ( Integer )
		"""

		return len(self.__interfaces)

	def rowCount(self, parent=QModelIndex()):
		"""
		Reimplements the :meth:`QAbstractListModel.rowCount` method.

		:param parent: Parent. ( QModelIndex )
		:return: Row count. ( Integer )
		"""

		return len(self.__interfaces)

	def data(self, index, role=Qt.DisplayRole):
		"""
		Reimplements the :meth:`QAbstractListModel.data` method.

		:param index: Index. ( QModelIndex )
		:param role: Role. ( Integer )
		:return: Data. ( QVariant )
		"""

		if not index.isValid():
			return QVariant()

		if role == Qt.DisplayRole:
			return QVariant(self.__interfaces[index.row()].name)
		return QVariant()

	def clear(self):
		"""
		Clears the Model.
		
		:return: Method success. ( Boolean )
		"""

		# TODO: Rollback to beginResetModel() whenever MPC changes it's PyQt version.
		self.modelAboutToBeReset.emit()
		self.__interfaces = []
		# TODO: Rollback to endResetModel () whenever MPC changes it's PyQt version.
		self.modelReset.emit()

	def sort(self, order=Qt.AscendingOrder):
		"""
		Sorts the Model interfaces.
		
		:param order: Order. ( Qt.SortOrder )
		:return: Method success. ( Boolean )
		"""

		# TODO: Rollback to beginResetModel() whenever MPC changes it's PyQt version.
		self.modelAboutToBeReset.emit()
		self.__interfaces = sorted(self.__interfaces, key=lambda x: (x.name), reverse=order)
		# TODO: Rollback to endResetModel () whenever MPC changes it's PyQt version.
		self.modelReset.emit()

	def getInterface(self, index):
		"""
		Returns the interface with given index.
		
		:param index: Interface index. ( QModelIndex )
		:return: Interface. ( Interface )
		"""

		return self.__interfaces[index.row()]

	def __registerCategorie(self, categorie):
		"""
		Registers given categorie.

		:param categorie: Categorie name. ( String )
		"""

		name = categorie[0]
		if not name in self:
			self.__interfaces.append(Categorie(name=name))

	def __unregisterCategorie(self, name):
		"""
		Unregisters categorie with given name.

		:param categorie: Categorie name. ( String )
		"""

		name = name[0]
		count = 0
		for item in reversed(self):
			if item.name.startswith(name):
				count += 1

			if item.name == name and count == 1:
				self.__interfaces.remove(self[name])

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def registerInterface(self, interface):
		"""
		Registers given interface.
		
		:param interface: Interface to register. ( Interface )
		:return: Method success. ( Boolean )
		"""

		name = interface.name
		if name in self:
			raise foundations.exceptions.ProgrammingError("{0} | An interface with '{1}' name is already registered!".format(
			self.__class__.__name__, name))

		LOGGER.debug("> Registering '{0}' interface.".format(name))

		self.__interfaces.append(interface)
		self.__registerCategorie(name)
		self.sort()
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def unregisterInterface(self, name):
		"""
		Unregisters interface with given name.
		
		:param name: Interface to unregister. ( String )
		:return: Method success. ( Boolean )
		"""

		if not name in self:
			raise foundations.exceptions.ProgrammingError("{0} | Interface with '{1}' name isn't registered!".format(
			self.__class__.__name__, name))

		LOGGER.debug("> Unregistering '{0}' interface.".format(name))

		for i, interface in enumerate(self):
			if not interface.name == name:
				continue

			del(self.__interfaces[i])
			self.__unregisterCategorie(name)
			self.sort()
			return True
