#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`snippets.loader.Loader` class Models.

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
from PyQt4.QtCore import QAbstractListModel
from PyQt4.QtCore import QModelIndex
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.data_structures
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

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Categorie(foundations.data_structures.Structure):
	"""
	This is the **Interface** class.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param kwargs: name.
		:type kwargs: dict
		"""

		foundations.data_structures.Structure.__init__(self, **kwargs)

class Interface(foundations.data_structures.Structure):
	"""
	This is the **Interface** class.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param kwargs: name, attribute, module.
		:type kwargs: dict
		"""

		foundations.data_structures.Structure.__init__(self, **kwargs)

class InterfacesModel(QAbstractListModel):
	"""
	Defines a `QAbstractListModel <http://doc.qt.nokia.com/qabstractListmodel.html>`_ subclass.
	"""

	def __init__(self, parent=None, interfaces=None):
		"""
		Initializes the class.

		:param parent: Parent object.
		:type parent: QObject
		:param interfaces: InterfacesModel.
		:type interfaces: list
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

		:return: self.__interfaces.
		:rtype: list
		"""

		return self.__interfaces

	@interfaces.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def interfaces(self, value):
		"""
		Setter for **self.__interfaces** attribute.

		:param value: Attribute value.
		:type value: list
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
		
		:param name: Item name.
		:type name: str
		:return: Item.
		:rtype: Interface
		"""

		for item in self.__interfaces:
			if item.name == name:
				return item

	def __iter__(self):
		"""
		Reimplements the :meth:`object.__iter__` method.

		:return: Interfaces iterator.
		:rtype: object
		"""

		return iter(self.__interfaces)

	def __reversed__(self):
		"""
		Reimplements the :meth:`object.__reversed__` method.

		:return: Reverse interfaces iterator.
		:rtype: object
		"""

		return reversed(self.__interfaces)

	def __contains__(self, name):
		"""
		Reimplements the :meth:`object.__contains__` method.

		:param name: Item name.
		:type name: str
		:return: Item existence.
		:rtype: bool
		"""

		return self[name] and True or False

	def __len__(self):
		"""
		Reimplements the :meth:`object.__len__` method.

		:return: Interfaces count.
		:rtype: int
		"""

		return len(self.__interfaces)

	def rowCount(self, parent=QModelIndex()):
		"""
		Reimplements the :meth:`QAbstractListModel.rowCount` method.

		:param parent: Parent.
		:type parent: QModelIndex
		:return: Row count.
		:rtype: int
		"""

		return len(self.__interfaces)

	def data(self, index, role=Qt.DisplayRole):
		"""
		Reimplements the :meth:`QAbstractListModel.data` method.

		:param index: Index.
		:type index: QModelIndex
		:param role: Role.
		:type role: int
		:return: Data.
		:rtype: QVariant
		"""

		if not index.isValid():
			return QVariant()

		if role == Qt.DisplayRole:
			return QVariant(self.__interfaces[index.row()].name)
		return QVariant()

	def clear(self):
		"""
		Clears the Model.
		
		:return: Method success.
		:rtype: bool
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
		:return: Method success.
		:rtype: bool
		"""

		# TODO: Rollback to beginResetModel() whenever MPC changes it's PyQt version.
		self.modelAboutToBeReset.emit()
		self.__interfaces = sorted(self.__interfaces, key=lambda x: (x.name), reverse=order)
		# TODO: Rollback to endResetModel () whenever MPC changes it's PyQt version.
		self.modelReset.emit()

	def get_interface(self, index):
		"""
		Returns the interface with given index.
		
		:param index: Interface index.
		:type index: QModelIndex
		:return: Interface.
		:rtype: Interface
		"""

		return self.__interfaces[index.row()]

	def __register_categorie(self, categorie):
		"""
		Registers given categorie.

		:param categorie: Categorie name.
		:type categorie: str
		"""

		name = categorie[0]
		if not name in self:
			self.__interfaces.append(Categorie(name=name))

	def __unregister_categorie(self, name):
		"""
		Unregisters categorie with given name.

		:param categorie: Categorie name.
		:type categorie: str
		"""

		name = name[0]
		count = 0
		for item in reversed(self):
			if item.name.startswith(name):
				count += 1

			if item.name == name and count == 1:
				self.__interfaces.remove(self[name])

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def register_interface(self, interface):
		"""
		Registers given interface.
		
		:param interface: Interface to register.
		:type interface: Interface
		:return: Method success.
		:rtype: bool
		"""

		name = interface.name
		if name in self:
			raise foundations.exceptions.ProgrammingError("{0} | An interface with '{1}' name is already registered!".format(
			self.__class__.__name__, name))

		LOGGER.debug("> Registering '{0}' interface.".format(name))

		self.__interfaces.append(interface)
		self.__register_categorie(name)
		self.sort()
		return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def unregister_interface(self, name):
		"""
		Unregisters interface with given name.
		
		:param name: Interface to unregister.
		:type name: str
		:return: Method success.
		:rtype: bool
		"""

		if not name in self:
			raise foundations.exceptions.ProgrammingError("{0} | Interface with '{1}' name isn't registered!".format(
			self.__class__.__name__, name))

		LOGGER.debug("> Unregistering '{0}' interface.".format(name))

		for i, interface in enumerate(self):
			if not interface.name == name:
				continue

			del(self.__interfaces[i])
			self.__unregister_categorie(name)
			self.sort()
			return True
