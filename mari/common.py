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
	Loader Module.

**Others:**

"""

from __future__ import unicode_literals

import inspect
import itertools
import mari
import os
import re
from PythonQt.QtCore import *
from PythonQt.QtGui import *

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["unpack_default",
	"fill_paint_buffer",
	"project_color",
	"project_black",
	"project_white",
	"get_selected_patches",
	"display_selected_patches",
	"get_patches_from_sequence",
	"select_patches",
	"select_input_patches",
	"playblast_time_range",
	"write_uvs_masks",
	"export_uvs_masks"]

def unpack_default(data, length=3, default=None):
	"""
	Unpack given iterable data with default if needed.

	:param data: Iterable.
	:type data: str or tuple or list
	:param length: Default length.
	:type length: int
	:param default: Default value.
	:type default: object
	:return: Definition success.
	:rtype: bool
	"""

	return itertools.islice(itertools.chain(iter(data), itertools.repeat(default)), length)

def fill_paint_buffer(color):
	"""
	Fills the paint buffer with given color.

	:param color: Color.
	:type color: QColor
	:return: Definition success.
	:rtype: bool
	"""

	paint_buffer = mari.canvases.paintBuffer()
	image = paint_buffer.getPaint()
	image.fill(color.rgba())
	paint_buffer.setPaint(image)
	return True

def project_color(color):
	"""
	Projects the given color.

	:param color: Color.
	:type color: QColor
	:return: Definition success.
	:rtype: bool
	"""

	if fill_paint_buffer(color):
		mari.canvases.paintBuffer().bakeAndClear()
		return True

def project_black():
	"""
	Projects black color.

	:return: Definition success.
	:rtype: bool
	"""

	return project_color(QColor(0, 0, 0,255))

def project_white():
	"""
	Projects white color.

	:return: Definition success.
	:rtype: bool
	"""

	return project_color(QColor(255, 255, 255,255))

def get_selected_patches():
	"""
	Returns current selected patches.

	:return: Selected patches.
	:rtype: list
	"""

	patches = []
	for patch in mari.geo.current().patches():
    		if patch.isSelected():
			patches.append(patch.name())
	return sorted(patches)

def display_selected_patches():
	"""
	Displays current selected patches.

	:return: Definition success.
	:rtype: bool
	"""

	patches = get_selected_patches()
	print "%s | Current object: '%s'" % (inspect.getmodulename(__file__), mari.geo.current().name())
	print "%s | Selected patches: '%s'" % (inspect.getmodulename(__file__), patches)
	mari.utils.misc.message("Current object: '%s'\nSelected patches: '%s'" % (mari.geo.current().name(), ", ".join(patches)), title="Current Object Selected Patches")
	return True

def get_patches_from_sequence(sequence):
	"""
	Returns patches from the given sequence.

	:param sequence: sequence.
	:type sequence: str
	:return: Patches.
	:rtype: list
	"""

	patches = []
	for pattern in sequence.split(","):
		start, end, step = (item.strip() for item in unpack_default(re.split(r"-|%", pattern), default=""))
		if start and not end:
			patches.append(int(start))
		elif start and end and not step:
			patches.extend(range(int(start), int(end) + 1))
		elif start and end and step:
			patches.extend(range(int(start), int(end) + 1, int(step)))
	return patches

def select_patches(patches):
	"""
	Selects given patches.

	:param patches: patches.
	:type patches: list
	:return: Definition success.
	:rtype: bool
	"""

	patches	= [str(patch) for patch in patches]
	for patch in mari.geo.current().patches():
		patch.setSelected(patch.name() in patches)

	return True

def select_input_patches():
	"""
	Selects input patches.

	:return: Definition success.
	:rtype: bool
	"""

	sequence = QInputDialog.getText(None, "Select Patches", "Patches Sequences:")
	if sequence:
        	return select_patches(get_patches_from_sequence(sequence))

def playblast_time_range():
	"""
	Playblasts current time range.

	:return: Definition success.
	:rtype: bool
	"""

	mari.actions.find('/Mari/Canvas/Screenshot settings').trigger()

	current_frame = mari.clock.frame()
	start_frame = mari.clock.startFrame()
	end_frame = mari.clock.stopFrame()

	mari.clock.setFrame(start_frame)
	#mari.app.startProcessing("Playblasting ...", end_frame - start_frame)
	mari.app.processEvents()
	for i in range(start_frame, end_frame):
		mari.actions.find('/Mari/Canvas/Take Screenshot').trigger()
		mari.clock.stepForward()
		mari.app.processEvents()
		#mari.app.stepProgress()
	#mari.app.stopProcessing()
	mari.clock.setFrame(current_frame)

	return True

def write_uvs_masks(directory):
	"""
	Writes UVs masks to given output directory.

	:return: Definition success.
	:rtype: bool
	"""

	if not directory:
		return

	images = mari.images.list()
	patches = mari.geo.current().patches()

	# mari.app.startProcessing("Exporting UVs Masks", len(patches))
	for patch in patches:
		patch.setSelected(True)
		mari.actions.find('/Mari/Geometry/Patches/UV Mask to Image Manager').trigger()
		patch.setSelected(False)
		currentImage = tuple(set(mari.images.list()).difference(images))[0]
		currentImage.saveAs(os.path.join(directory, "%s_%s.tif" % (mari.projects.current().name(), patch.name())))
		currentImage.close()
		# mari.app.stepProgress()
	# mari.app.stopProcessing()
	return True

def export_uvs_masks():
	"""
	Exports UVs masks.

	:return: Definition success.
	:rtype: bool
	"""

	return write_uvs_masks(QFileDialog.getExistingDirectory(None, "Select Output Directory",))


mari.menus.addAction(mari.actions.create("Show Selected Patches ...", "import common;reload(common);common.display_selected_patches()"), "MainWindow/&MPC/")
mari.menus.addAction(mari.actions.create("Select Input Patches ...", "import common;reload(common);common.select_input_patches()"), "MainWindow/&MPC/")
mari.menus.addSeparator("MainWindow/&MPC/")
mari.menus.addAction(mari.actions.create("Export UVs Masks ...", "import common;reload(common);common.export_uvs_masks()"), "MainWindow/&MPC/")
mari.menus.addSeparator("MainWindow/&MPC/")
mari.menus.addAction(mari.actions.create("Playblast Time Range ...", "import common;reload(common);common.playblast_time_range()"), "MainWindow/&MPC/")
mari.menus.addSeparator("MainWindow/&MPC/")
mari.menus.addAction(mari.actions.create("Project Black", "import common;reload(common);common.project_black()"), "MainWindow/&MPC/")
mari.menus.addAction(mari.actions.create("Project White", "import common;reload(common);common.project_white()"), "MainWindow/&MPC/")
mari.menus.addSeparator("MainWindow/&MPC/")
mari.menus.addAction(mari.actions.create("Clear History Queue ...", "mari.history.clear()"), "MainWindow/&MPC/")
