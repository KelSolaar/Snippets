#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**active_QLabel.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Active_QLabel` class.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QCursor
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap

import foundations.exceptions
import foundations.verbose
import snippets.ui.common

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Active_QLabel"]

LOGGER = foundations.verbose.install_logger()

class Active_QLabel(QLabel):
	"""
	Defines a `QLabel <http://doc.qt.nokia.com/qlabel.html>`_ subclass providing
	a clickable label with hovering capabilities.
	"""

	# Custom signals definitions.
	clicked = pyqtSignal()
	"""
	This signal is emited by the :class:`Active_QLabel` class when it has been clicked.
	"""

	pressed = pyqtSignal()
	"""
	This signal is emited by the :class:`Active_QLabel` class when it has been pressed.
	"""

	released = pyqtSignal()
	"""
	This signal is emited by the :class:`Active_QLabel` class when it has been released.
	"""

	toggled = pyqtSignal(bool)
	"""
	This signal is emited by the :class:`Active_QLabel` class when it has been toggled.

	:return: Current checked state.
	:rtype: bool
	"""

	def __init__(self,
				parent=None,
				default_pixmap=None,
				hover_pixmap=None,
				active_pixmap=None,
				checkable=False,
				checked=False):
		"""
		Initializes the class.

		:param parent: Widget parent.
		:type parent: QObject
		:param default_pixmap: Label default pixmap.
		:type default_pixmap: QPixmap
		:param hover_pixmap: Label hover pixmap.
		:type hover_pixmap: QPixmap
		:param active_pixmap: Label active pixmap.
		:type active_pixmap: QPixmap
		:param checkable: Checkable state.
		:type checkable: bool
		:param checked: Checked state.
		:type checked: bool
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QLabel.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__default_pixmap = None
		self.default_pixmap = default_pixmap or QPixmap()
		self.__hover_pixmap = None
		self.hover_pixmap = hover_pixmap or QPixmap()
		self.__active_pixmap = None
		self.active_pixmap = active_pixmap or QPixmap()

		self.__checkable = None
		self.checkable = checkable
		self.__checked = None
		self.checked = checked

		self.__menu = None

		if self.__checked:
			self.setPixmap(self.__active_pixmap)
		else:
			self.setPixmap(self.__default_pixmap)

	@property
	def default_pixmap(self):
		"""
		Property for **self.__default_pixmap** attribute.

		:return: self.__default_pixmap.
		:rtype: QPixmap
		"""

		return self.__default_pixmap

	@default_pixmap.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def default_pixmap(self, value):
		"""
		Setter for **self.__default_pixmap** attribute.

		:param value: Attribute value.
		:type value: QPixmap
		"""

		if value is not None:
			assert type(value) is QPixmap, "'{0}' attribute: '{1}' type is not 'QPixmap'!".format("default_pixmap", value)
		self.__default_pixmap = value

	@default_pixmap.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_pixmap(self):
		"""
		Deleter for **self.__default_pixmap** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_pixmap"))

	@property
	def hover_pixmap(self):
		"""
		Property for **self.__hover_pixmap** attribute.

		:return: self.__hover_pixmap.
		:rtype: QPixmap
		"""

		return self.__hover_pixmap

	@hover_pixmap.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def hover_pixmap(self, value):
		"""
		Setter for **self.__hover_pixmap** attribute.

		:param value: Attribute value.
		:type value: QPixmap
		"""

		if value is not None:
			assert type(value) is QPixmap, "'{0}' attribute: '{1}' type is not 'QPixmap'!".format("hover_pixmap", value)
		self.__hover_pixmap = value

	@hover_pixmap.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def hover_pixmap(self):
		"""
		Deleter for **self.__hover_pixmap** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "hover_pixmap"))

	@property
	def active_pixmap(self):
		"""
		Property for **self.__active_pixmap** attribute.

		:return: self.__active_pixmap.
		:rtype: QPixmap
		"""

		return self.__active_pixmap

	@active_pixmap.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def active_pixmap(self, value):
		"""
		Setter for **self.__active_pixmap** attribute.

		:param value: Attribute value.
		:type value: QPixmap
		"""

		if value is not None:
			assert type(value) is QPixmap, "'{0}' attribute: '{1}' type is not 'QPixmap'!".format("active_pixmap", value)
		self.__active_pixmap = value

	@active_pixmap.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def active_pixmap(self):
		"""
		Deleter for **self.__active_pixmap** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "active_pixmap"))

	@property
	def checkable(self):
		"""
		Property for **self.__checkable** attribute.

		:return: self.__checkable.
		:rtype: bool
		"""

		return self.__checkable

	@checkable.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def checkable(self, value):
		"""
		Setter for **self.__checkable** attribute.

		:param value: Attribute value.
		:type value: bool
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("checkable", value)
		self.__checkable = value

	@checkable.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def checkable(self):
		"""
		Deleter for **self.__checkable** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "checkable"))

	@property
	def checked(self):
		"""
		Property for **self.__checked** attribute.

		:return: self.__checked.
		:rtype: bool
		"""

		return self.__checked

	@checked.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def checked(self, value):
		"""
		Setter for **self.__checked** attribute.

		:param value: Attribute value.
		:type value: bool
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("checked", value)
		self.set_checked(value)

	@checked.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def checked(self):
		"""
		Deleter for **self.__checked** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "checked"))

	@property
	def menu(self):
		"""
		Property for **self.__menu** attribute.

		:return: self.__menu.
		:rtype: QMenu
		"""

		return self.__menu

	@menu.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def menu(self, value):
		"""
		Setter for **self.__menu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "menu"))

	@menu.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def menu(self):
		"""
		Deleter for **self.__menu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "menu"))

	def enterEvent(self, event):
		"""
		Reimplements the :meth:`QLabel.enterEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		if self.__checkable:
			not self.__checked and self.setPixmap(self.__hover_pixmap)
		else:
			self.setPixmap(self.__hover_pixmap)

	def leaveEvent(self, event):
		"""
		Reimplements the :meth:`QLabel.leaveEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		if self.__checkable:
			not self.__checked and self.setPixmap(self.__default_pixmap)
		else:
			self.setPixmap(self.__default_pixmap)

	def mousePressEvent(self, event):
		"""
		Reimplements the :meth:`QLabel.mousePressEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		self.setPixmap(self.__active_pixmap)
		self.__menu and self.__menu.exec_(QCursor.pos())
		self.pressed.emit()

	def mouseReleaseEvent(self, event):
		"""
		Reimplements the :meth:`QLabel.mouseReleaseEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		if self.underMouse():
			if self.__checkable:
				self.set_checked(not self.__checked)
			else:
				self.setPixmap(self.__active_pixmap)
		else:
			self.setPixmap(self.__default_pixmap)
		self.released.emit()
		self.clicked.emit()

	def set_checked(self, state):
		"""
		Sets the Widget checked state.

		:param state: New check state.
		:type state: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.__checkable:
			return False

		if state:
			self.__checked = True
			self.setPixmap(self.__active_pixmap)
		else:
			self.__checked = False
			self.setPixmap(self.__default_pixmap)
		self.toggled.emit(state)
		return True

	def set_menu(self, menu):
		"""
		Sets the Widget menu.

		:param menu: Menu.
		:type menu: QMenu
		:return: Method success.
		:rtype: bool
		"""

		self.__menu = menu

		if not self.parent():
			return False

		parent = [parent for parent in snippets.ui.common.parents_walker(self)].pop()
		for action in self.__menu.actions():
			not action.shortcut().isEmpty() and parent.addAction(action)
		return True