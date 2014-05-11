#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**search_QLineEdit.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Search_QLineEdit` class.

**Others:**

"""

from __future__ import unicode_literals

import functools
import os
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QCompleter
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QToolButton

import foundations.exceptions
import foundations.verbose
import snippets.ui.common
from snippets.ui.widgets.active_QLabel import Active_QLabel

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Search_QLineEdit"]

LOGGER = foundations.verbose.install_logger()

class Search_QLineEdit(QLineEdit):
	"""
	Defines a `QLineEdit <http://doc.qt.nokia.com/qlinedit.html>`_ subclass providing
	a search field with clearing capabilities.
	"""

	def __init__(self,
				parent=None,
				ui_search_image=None,
				ui_search_clicked_image=None,
				ui_clear_image=None,
				ui_clear_clicked_image=None):
		"""
		Initializes the class.

		:param parent: Widget parent.
		:type parent: QObject
		:param ui_search_image: Search button image path.
		:type ui_search_image: unicode
		:param ui_search_clicked_image: Search button clicked image path.
		:type ui_search_clicked_image: unicode
		:param ui_clear_image: Clear button image path.
		:type ui_clear_image: unicode
		:param ui_clear_clicked_image: Clear button clicked image path.
		:type ui_clear_clicked_image: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QLineEdit.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__ui_search_image = None
		self.ui_search_image = ui_search_image or snippets.ui.common.get_resource_path("images/Search_Glass.png")
		self.__ui_search_clicked_image = None
		self.ui_search_clicked_image = ui_search_clicked_image or snippets.ui.common.get_resource_path(
		"images/Search_Glass_Clicked.png")
		self.__ui_clear_image = None
		self.ui_clear_image = ui_clear_image or snippets.ui.common.get_resource_path("images/Search_Clear.png")
		self.__ui_clear_clicked_image = None
		self.ui_clear_clicked_image = ui_clear_clicked_image or snippets.ui.common.get_resource_path(
		"images/Search_Clear_Clicked.png")

		self.__search_active_label = Active_QLabel(self,
												QPixmap(self.__ui_search_image),
												QPixmap(self.__ui_search_image),
												QPixmap(self.__ui_search_clicked_image))
		self.__search_active_label.setObjectName("Search_Field_active_label")
		self.__search_active_label.showEvent = lambda event: reduce(lambda *args: None,
		(self.__set_style_sheet(), Active_QLabel.showEvent(self.__search_active_label, event)))
		self.__search_active_label.hideEvent = lambda event: reduce(lambda *args: None,
		(self.__set_style_sheet(), Active_QLabel.hideEvent(self.__search_active_label, event)))

		self.__clear_button = QToolButton(self)
		self.__clear_button.setObjectName("Clear_Field_button")

		self.__completer = QCompleter()
		self.setCompleter(self.__completer)
		self.__completer_visible_items_count = 16

		Search_QLineEdit.__initialize_ui(self)
		self.__set_clear_button_visibility(self.text())

		# Signals / Slots.
		self.__clear_button.clicked.connect(self.clear)
		self.textChanged.connect(self.__set_clear_button_visibility)

	@property
	def ui_search_image(self):
		"""
		Property for **self.__ui_search_image** attribute.

		:return: self.__ui_search_image.
		:rtype: unicode
		"""

		return self.__ui_search_image

	@ui_search_image.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def ui_search_image(self, value):
		"""
		Setter for **self.__ui_search_image** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"ui_search_image", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("ui_search_image", value)
		self.__ui_search_image = value

	@ui_search_image.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_search_image(self):
		"""
		Deleter for **self.__ui_search_image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_search_image"))

	@property
	def ui_search_clicked_image(self):
		"""
		Property for **self.__ui_search_clicked_image** attribute.

		:return: self.__ui_search_clicked_image.
		:rtype: unicode
		"""

		return self.__ui_search_clicked_image

	@ui_search_clicked_image.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def ui_search_clicked_image(self, value):
		"""
		Setter for **self.__ui_search_clicked_image** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"ui_search_clicked_image", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format(
			"ui_search_clicked_image", value)
		self.__ui_search_clicked_image = value

	@ui_search_clicked_image.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_search_clicked_image(self):
		"""
		Deleter for **self.__ui_search_clicked_image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_search_clicked_image"))

	@property
	def ui_clear_image(self):
		"""
		Property for **self.__ui_clear_image** attribute.

		:return: self.__ui_clear_image.
		:rtype: unicode
		"""

		return self.__ui_clear_image

	@ui_clear_image.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def ui_clear_image(self, value):
		"""
		Setter for **self.__ui_clear_image** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"ui_clear_image", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format(
			"ui_clear_image", value)
		self.__ui_clear_image = value

	@ui_clear_image.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_clear_image(self):
		"""
		Deleter for **self.__ui_clear_image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_clear_image"))

	@property
	def ui_clear_clicked_image(self):
		"""
		Property for **self.__ui_clear_clicked_image** attribute.

		:return: self.__ui_clear_clicked_image.
		:rtype: unicode
		"""

		return self.__ui_clear_clicked_image

	@ui_clear_clicked_image.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def ui_clear_clicked_image(self, value):
		"""
		Setter for **self.__ui_clear_clicked_image** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"ui_clear_clicked_image", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format(
			"ui_clear_clicked_image", value)
		self.__ui_clear_clicked_image = value

	@ui_clear_clicked_image.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def ui_clear_clicked_image(self):
		"""
		Deleter for **self.__ui_clear_clicked_image** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_clear_clicked_image"))

	@property
	def search_active_label(self):
		"""
		Property for **self.__search_active_label** attribute.

		:return: self.__search_active_label.
		:rtype: QPushButton
		"""

		return self.__search_active_label

	@search_active_label.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def search_active_label(self, value):
		"""
		Setter for **self.__search_active_label** attribute.

		:param value: Attribute value.
		:type value: QPushButton
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "search_active_label"))

	@search_active_label.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def search_active_label(self):
		"""
		Deleter for **self.__search_active_label** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "search_active_label"))

	@property
	def clear_button(self):
		"""
		Property for **self.__clear_button** attribute.

		:return: self.__clear_button.
		:rtype: QPushButton
		"""

		return self.__clear_button

	@clear_button.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def clear_button(self, value):
		"""
		Setter for **self.__clear_button** attribute.

		:param value: Attribute value.
		:type value: QPushButton
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "clear_button"))

	@clear_button.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def clear_button(self):
		"""
		Deleter for **self.__clear_button** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "clear_button"))

	@property
	def completer(self):
		"""
		Property for **self.__completer** attribute.

		:return: self.__completer.
		:rtype: QCompleter
		"""

		return self.__completer

	@completer.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def completer(self, value):
		"""
		Setter for **self.__completer** attribute.

		:param value: Attribute value.
		:type value: QCompleter
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "completer"))

	@completer.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def completer(self):
		"""
		Deleter for **self.__completer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "completer"))

	@property
	def completer_visible_items_count(self):
		"""
		Property for **self.__completer_visible_items_count** attribute.

		:return: self.__completer_visible_items_count.
		:rtype: int
		"""

		return self.__completer_visible_items_count

	@completer_visible_items_count.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def completer_visible_items_count(self, value):
		"""
		Setter for **self.__completer_visible_items_count** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "completer_visible_items_count"))

	@completer_visible_items_count.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def completer_visible_items_count(self):
		"""
		Deleter for **self.__completer_visible_items_count** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "completer_visible_items_count"))

	def resizeEvent(self, event):
		"""
		Reimplements the :meth:`QLineEdit.QResizeEvent` method.

		:param event: Resize event.
		:type event: QResizeEvent
		"""

		frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
		search_active_labelSize = self.__search_active_label.sizeHint()
		self.__search_active_label.move(self.rect().left() + frame_width,
		(self.rect().bottom() - search_active_labelSize.height()) / 2 + frame_width / 2)
		clear_buttonSize = self.__clear_button.sizeHint()
		self.__clear_button.move(self.rect().right() - frame_width - clear_buttonSize.width(),
		(self.rect().bottom() - clear_buttonSize.height()) / 2 + frame_width / 2)

	def __initialize_ui(self):
		"""
		Initializes the Widget ui.
		"""

		self.__clear_button.setCursor(Qt.ArrowCursor)
		if self.__ui_clear_image and self.__ui_clear_clicked_image:
			pixmap = QPixmap(self.__ui_clear_image)
			clicked_pixmap = QPixmap(self.__ui_clear_clicked_image)
			self.__clear_button.setIcon(QIcon(pixmap))
			self.__clear_button.setMaximumSize(pixmap.size())

			# Signals / Slots.
			self.__clear_button.pressed.connect(functools.partial(self.__clear_button.setIcon, QIcon(clicked_pixmap)))
			self.__clear_button.released.connect(functools.partial(self.__clear_button.setIcon, QIcon(pixmap)))
		else:
			self.__clear_button.setText("Clear")

		self.__set_style_sheet()

		frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
		self.setMinimumSize(max(self.minimumSizeHint().width(), self.__clear_button.sizeHint().height() + frame_width * 2),
		 					max(self.minimumSizeHint().height(), self.__clear_button.sizeHint().height() + frame_width * 2))

		self.__completer.setCaseSensitivity(Qt.CaseInsensitive)
		self.__completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
		self.__completer.setMaxVisibleItems(self.__completer_visible_items_count)

	def __set_style_sheet(self):
		"""
		Sets the Widget stylesheet.
		"""

		frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
		self.setStyleSheet(QString("QLineEdit {{ padding-left: {0}px; padding-right: {1}px; }}".format(
		self.__search_active_label.sizeHint().width() if self.__search_active_label.isVisible() else 0 + frame_width,
		self.__clear_button.sizeHint().width() + frame_width)))

	def __set_clear_button_visibility(self, text):
		"""
		Sets the clear button visibility.

		:param text: Current field text.
		:type text: QString
		"""

		if text:
			self.__clear_button.show()
		else:
			self.__clear_button.hide()