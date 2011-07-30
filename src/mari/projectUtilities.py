import mari
import os
from PythonQt.QtCore import *
from PythonQt.QtGui import *

def getObjectsFromFiles(files):
	for file in files:
		os.path.exists(file) and mari.geo.load(file)

def importObjectsFromDirectory():
	directory = QFileDialog.getExistingDirectory(None, "Select a directory to import!", "/")
	if directory:
		pass

def importMultipleObjects():
	if mari.projects.current():
		files = QFileDialog.getOpenFileNames(None, "Select objects to import!", "*.obj")
		if files:
			getObjectsFromFiles(files)
	else:
		QMessageBox.critical(None, "%s | Critical exception." % __name__, "There are no active projects, please open / create one!", QMessageBox.Ok)

mari.menus.addAction(mari.actions.create("Import Objects From Directory ...", "import projectutilities;reload(projectutilities);projectutilities.importobjectsfromdirectory()"), "MainWindow/&MPC/")
mari.menus.addAction(mari.actions.create("Import Multiple Objects ...", "import projectutilities;reload(projectutilities);projectutilities.importmultipleobjects()"), "MainWindow/&MPC/")