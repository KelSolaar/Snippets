#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**search_QLineEdit.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Search_QLineEdit` class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import logging
import os
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QCompleter
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QToolButton

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import umbra.ui.common
from umbra.globals.constants import Constants
from umbra.ui.widgets.active_QLabel import Active_QLabel

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Search_QLineEdit"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Search_QLineEdit(QLineEdit):
	"""
	This class is a `QLineEdit <http://doc.qt.nokia.com/qlinedit.html>`_ subclass providing
	a search field with clearing capabilities.
	"""

	@core.executionTrace
	def __init__(self,
				parent=None,
				uiSearchImage=None,
				uiSearchClickedImage=None,
				uiClearImage=None,
				uiClearClickedImage=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		:param uiSearchImage: Search button image path. ( String )
		:param uiSearchClickedImage: Search button clicked image path. ( String )
		:param uiClearImage: Clear button image path. ( String )
		:param uiClearClickedImage: Clear button clicked image path. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QLineEdit.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__uiSearchImage = None
		self.uiSearchImage = uiSearchImage or umbra.ui.common.getResourcePath("images/Search_Glass.png")
		self.__uiSearchClickedImage = None
		self.uiSearchClickedImage = uiSearchClickedImage or umbra.ui.common.getResourcePath(
		"images/Search_Glass_Clicked.png")
		self.__uiClearImage = None
		self.uiClearImage = uiClearImage or umbra.ui.common.getResourcePath("images/Search_Clear.png")
		self.__uiClearClickedImage = None
		self.uiClearClickedImage = uiClearClickedImage or umbra.ui.common.getResourcePath(
		"images/Search_Clear_Clicked.png")

		self.__searchActiveLabel = Active_QLabel(self,
												QPixmap(self.__uiSearchImage),
												QPixmap(self.__uiSearchImage),
												QPixmap(self.__uiSearchClickedImage))
		self.__searchActiveLabel.setObjectName("Search_Field_activeLabel")

		self.__clearButton = QToolButton(self)
		self.__clearButton.setObjectName("Clear_Field_button")

		self.__completer = QCompleter()
		self.setCompleter(self.__completer)
		self.__completerVisibleItemsCount = 16

		Search_QLineEdit.__initializeUi(self)
		self.__setClearButtonVisibility(self.text())

		# Signals / Slots.
		self.__clearButton.clicked.connect(self.clear)
		self.textChanged.connect(self.__setClearButtonVisibility)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def uiSearchImage(self):
		"""
		This method is the property for **self.__uiSearchImage** attribute.

		:return: self.__uiSearchImage. ( String )
		"""

		return self.__uiSearchImage

	@uiSearchImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiSearchImage(self, value):
		"""
		This method is the setter method for **self.__uiSearchImage** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"uiSearchImage", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("uiSearchImage", value)
		self.__uiSearchImage = value

	@uiSearchImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchImage(self):
		"""
		This method is the deleter method for **self.__uiSearchImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiSearchImage"))

	@property
	def uiSearchClickedImage(self):
		"""
		This method is the property for **self.__uiSearchClickedImage** attribute.

		:return: self.__uiSearchClickedImage. ( String )
		"""

		return self.__uiSearchClickedImage

	@uiSearchClickedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiSearchClickedImage(self, value):
		"""
		This method is the setter method for **self.__uiSearchClickedImage** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"uiSearchClickedImage", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format(
			"uiSearchClickedImage", value)
		self.__uiSearchClickedImage = value

	@uiSearchClickedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchClickedImage(self):
		"""
		This method is the deleter method for **self.__uiSearchClickedImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiSearchClickedImage"))

	@property
	def uiClearImage(self):
		"""
		This method is the property for **self.__uiClearImage** attribute.

		:return: self.__uiClearImage. ( String )
		"""

		return self.__uiClearImage

	@uiClearImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiClearImage(self, value):
		"""
		This method is the setter method for **self.__uiClearImage** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"uiClearImage", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format(
			"uiClearImage", value)
		self.__uiClearImage = value

	@uiClearImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearImage(self):
		"""
		This method is the deleter method for **self.__uiClearImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiClearImage"))

	@property
	def uiClearClickedImage(self):
		"""
		This method is the property for **self.__uiClearClickedImage** attribute.

		:return: self.__uiClearClickedImage. ( String )
		"""

		return self.__uiClearClickedImage

	@uiClearClickedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiClearClickedImage(self, value):
		"""
		This method is the setter method for **self.__uiClearClickedImage** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"uiClearClickedImage", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format(
			"uiClearClickedImage", value)
		self.__uiClearClickedImage = value

	@uiClearClickedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedImage(self):
		"""
		This method is the deleter method for **self.__uiClearClickedImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiClearClickedImage"))

	@property
	def searchActiveLabel(self):
		"""
		This method is the property for **self.__searchActiveLabel** attribute.

		:return: self.__searchActiveLabel. ( QPushButton )
		"""

		return self.__searchActiveLabel

	@searchActiveLabel.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchActiveLabel(self, value):
		"""
		This method is the setter method for **self.__searchActiveLabel** attribute.

		:param value: Attribute value. ( QPushButton )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchActiveLabel"))

	@searchActiveLabel.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchActiveLabel(self):
		"""
		This method is the deleter method for **self.__searchActiveLabel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchActiveLabel"))

	@property
	def clearButton(self):
		"""
		This method is the property for **self.__clearButton** attribute.

		:return: self.__clearButton. ( QPushButton )
		"""

		return self.__clearButton

	@clearButton.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def clearButton(self, value):
		"""
		This method is the setter method for **self.__clearButton** attribute.

		:param value: Attribute value. ( QPushButton )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "clearButton"))

	@clearButton.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def clearButton(self):
		"""
		This method is the deleter method for **self.__clearButton** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "clearButton"))

	@property
	def completer(self):
		"""
		This method is the property for **self.__completer** attribute.

		:return: self.__completer. ( QCompleter )
		"""

		return self.__completer

	@completer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self, value):
		"""
		This method is the setter method for **self.__completer** attribute.

		:param value: Attribute value. ( QCompleter )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "completer"))

	@completer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self):
		"""
		This method is the deleter method for **self.__completer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "completer"))

	@property
	def completerVisibleItemsCount(self):
		"""
		This method is the property for **self.__completerVisibleItemsCount** attribute.

		:return: self.__completerVisibleItemsCount. ( Integer )
		"""

		return self.__completerVisibleItemsCount

	@completerVisibleItemsCount.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completerVisibleItemsCount(self, value):
		"""
		This method is the setter method for **self.__completerVisibleItemsCount** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "completerVisibleItemsCount"))

	@completerVisibleItemsCount.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completerVisibleItemsCount(self):
		"""
		This method is the deleter method for **self.__completerVisibleItemsCount** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "completerVisibleItemsCount"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def resizeEvent(self, event):
		"""
		This method reimplements the :meth:`QLineEdit.QResizeEvent` method.

		:param event: Resize event. ( QResizeEvent )
		"""

		frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
		searchActiveLabelSize = self.__searchActiveLabel.sizeHint()
		self.__searchActiveLabel.move(self.rect().left() + frameWidth,
		(self.rect().bottom() - searchActiveLabelSize.height()) / 2 + frameWidth / 2)
		clearButtonSize = self.__clearButton.sizeHint()
		self.__clearButton.move(self.rect().right() - frameWidth - clearButtonSize.width(),
		(self.rect().bottom() - clearButtonSize.height()) / 2 + frameWidth / 2)

	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.__clearButton.setCursor(Qt.ArrowCursor)
		if self.__uiClearImage and self.__uiClearClickedImage:
			pixmap = QPixmap(self.__uiClearImage)
			clickedPixmap = QPixmap(self.__uiClearClickedImage)
			self.__clearButton.setStyleSheet("QToolButton { border: none; padding: 0px; }")
			self.__clearButton.setIcon(QIcon(pixmap))
			self.__clearButton.setMaximumSize(pixmap.size())

			# Signals / Slots.
			self.__clearButton.pressed.connect(functools.partial(self.__clearButton.setIcon, QIcon(clickedPixmap)))
			self.__clearButton.released.connect(functools.partial(self.__clearButton.setIcon, QIcon(pixmap)))
		else:
			self.__clearButton.setText("Clear")

		frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
		self.setStyleSheet(QString("QLineEdit {{ padding-left: {0}px; padding-right: {1}px; }}".format(
		self.__searchActiveLabel.sizeHint().width() + frameWidth, self.__clearButton.sizeHint().width() + frameWidth)))

		self.setMinimumSize(max(self.minimumSizeHint().width(), self.__clearButton.sizeHint().height() + frameWidth * 2),
		 					max(self.minimumSizeHint().height(), self.__clearButton.sizeHint().height() + frameWidth * 2))

		self.__completer.setCaseSensitivity(Qt.CaseInsensitive)
		self.__completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
		self.__completer.setMaxVisibleItems(self.__completerVisibleItemsCount)

	@core.executionTrace
	def __setClearButtonVisibility(self, text):
		"""
		This method sets the clear button visibility.

		:param text: Current field text. ( QString )
		"""

		if text:
			self.__clearButton.show()
		else:
			self.__clearButton.hide()
