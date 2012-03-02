#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**active_QLabel.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Active_QLabel` class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QCursor
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QPixmap

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import snippets.ui.common
from snippets.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Active_QLabel"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Active_QLabel(QLabel):
	"""
	This class is a `QLabel <http://doc.qt.nokia.com/qlabel.html>`_ subclass providing
	a clickable label with hovering capabilities.
	"""

	# Custom signals definitions.
	clicked = pyqtSignal()
	"""
	This signal is emited by the :class:`Active_QLabel` class when it has been clicked. ( pyqtSignal )
	"""

	pressed = pyqtSignal()
	"""
	This signal is emited by the :class:`Active_QLabel` class when it has been pressed. ( pyqtSignal )
	"""

	released = pyqtSignal()
	"""
	This signal is emited by the :class:`Active_QLabel` class when it has been released. ( pyqtSignal )
	"""

	toggled = pyqtSignal(bool)
	"""
	This signal is emited by the :class:`Active_QLabel` class when it has been toggled. ( pyqtSignal )

	:return: Current checked state. ( Boolean )	
	"""

	@core.executionTrace
	def __init__(self,
				parent=None,
				defaultPixmap=None,
				hoverPixmap=None,
				activePixmap=None,
				checkable=False,
				checked=False):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		:param defaultPixmap: Label default pixmap. ( QPixmap )
		:param hoverPixmap: Label hover pixmap. ( QPixmap )
		:param activePixmap: Label active pixmap. ( QPixmap )
		:param checkable: Checkable state. ( Boolean )
		:param checked: Checked state. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QLabel.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__defaultPixmap = None
		self.defaultPixmap = defaultPixmap or QPixmap()
		self.__hoverPixmap = None
		self.hoverPixmap = hoverPixmap or QPixmap()
		self.__activePixmap = None
		self.activePixmap = activePixmap or QPixmap()

		self.__checkable = None
		self.checkable = checkable
		self.__checked = None
		self.checked = checked

		self.__menu = None

		self.__checked and self.setPixmap(self.__activePixmap) or self.setPixmap(self.__defaultPixmap)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def defaultPixmap(self):
		"""
		This method is the property for **self.__defaultPixmap** attribute.

		:return: self.__defaultPixmap. ( QPixmap )
		"""

		return self.__defaultPixmap

	@defaultPixmap.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultPixmap(self, value):
		"""
		This method is the setter method for **self.__defaultPixmap** attribute.

		:param value: Attribute value. ( QPixmap )
		"""

		if value is not None:
			assert type(value) is QPixmap, "'{0}' attribute: '{1}' type is not 'QPixmap'!".format("defaultPixmap", value)
		self.__defaultPixmap = value

	@defaultPixmap.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultPixmap(self):
		"""
		This method is the deleter method for **self.__defaultPixmap** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultPixmap"))

	@property
	def hoverPixmap(self):
		"""
		This method is the property for **self.__hoverPixmap** attribute.

		:return: self.__hoverPixmap. ( QPixmap )
		"""

		return self.__hoverPixmap

	@hoverPixmap.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def hoverPixmap(self, value):
		"""
		This method is the setter method for **self.__hoverPixmap** attribute.

		:param value: Attribute value. ( QPixmap )
		"""

		if value is not None:
			assert type(value) is QPixmap, "'{0}' attribute: '{1}' type is not 'QPixmap'!".format("hoverPixmap", value)
		self.__hoverPixmap = value

	@hoverPixmap.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def hoverPixmap(self):
		"""
		This method is the deleter method for **self.__hoverPixmap** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "hoverPixmap"))

	@property
	def activePixmap(self):
		"""
		This method is the property for **self.__activePixmap** attribute.

		:return: self.__activePixmap. ( QPixmap )
		"""

		return self.__activePixmap

	@activePixmap.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def activePixmap(self, value):
		"""
		This method is the setter method for **self.__activePixmap** attribute.

		:param value: Attribute value. ( QPixmap )
		"""

		if value is not None:
			assert type(value) is QPixmap, "'{0}' attribute: '{1}' type is not 'QPixmap'!".format("activePixmap", value)
		self.__activePixmap = value

	@activePixmap.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def activePixmap(self):
		"""
		This method is the deleter method for **self.__activePixmap** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "activePixmap"))

	@property
	def checkable(self):
		"""
		This method is the property for **self.__checkable** attribute.

		:return: self.__checkable. ( Boolean )
		"""

		return self.__checkable

	@checkable.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def checkable(self, value):
		"""
		This method is the setter method for **self.__checkable** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("checkable", value)
		self.__checkable = value

	@checkable.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def checkable(self):
		"""
		This method is the deleter method for **self.__checkable** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "checkable"))

	@property
	def checked(self):
		"""
		This method is the property for **self.__checked** attribute.

		:return: self.__checked. ( Boolean )
		"""

		return self.__checked

	@checked.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def checked(self, value):
		"""
		This method is the setter method for **self.__checked** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("checked", value)
		self.setChecked(value)

	@checked.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def checked(self):
		"""
		This method is the deleter method for **self.__checked** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "checked"))

	@property
	def menu(self):
		"""
		This method is the property for **self.__menu** attribute.

		:return: self.__menu. ( QMenu )
		"""

		return self.__menu

	@menu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menu(self, value):
		"""
		This method is the setter method for **self.__menu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "menu"))

	@menu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menu(self):
		"""
		This method is the deleter method for **self.__menu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "menu"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def enterEvent(self, event):
		"""
		This method reimplements the :meth:`QLabel.enterEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		if self.__checkable:
			not self.__checked and self.setPixmap(self.__hoverPixmap)
		else:
			self.setPixmap(self.__hoverPixmap)

	@core.executionTrace
	def leaveEvent(self, event):
		"""
		This method reimplements the :meth:`QLabel.leaveEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		if self.__checkable:
			not self.__checked and self.setPixmap(self.__defaultPixmap)
		else:
			self.setPixmap(self.__defaultPixmap)

	@core.executionTrace
	def mousePressEvent(self, event):
		"""
		This method reimplements the :meth:`QLabel.mousePressEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		self.setPixmap(self.__activePixmap)
		self.__menu and self.__menu.exec_(QCursor.pos())
		self.pressed.emit()

	@core.executionTrace
	def mouseReleaseEvent(self, event):
		"""
		This method reimplements the :meth:`QLabel.mouseReleaseEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		if self.underMouse():
			if self.__checkable:
				self.setChecked(True)
			else:
				self.setPixmap(self.__activePixmap)
			self.clicked.emit()
		else:
			self.setPixmap(self.__defaultPixmap)
			self.released.emit()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setChecked(self, state):
		"""
		This method sets the Widget checked state.

		:param state: New check state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.__checkable:
			return

		if state:
			self.__checked = True
			self.setPixmap(self.__activePixmap)
		else:
			self.__checked = False
			self.setPixmap(self.__defaultPixmap)
		self.toggled.emit(state)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def isChecked(self):
		"""
		This method returns the Widget checked state.

		:return: Checked state. ( Boolean )
		"""

		return self.__checked

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setMenu(self, menu):
		"""
		This method sets the Widget menu.

		:param menu: Menu. ( QMenu )
		:return: Method success. ( Boolean )
		"""

		self.__menu = menu

		if not self.parent():
			return

		parent = [parent for parent in snippets.ui.common.parentsWalker(self)].pop()
		for action in self.__menu.actions():
			not action.shortcut().isEmpty() and parent.addAction(action)
		return True
