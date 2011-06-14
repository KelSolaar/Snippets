import mari
import os
from PythonQt.QtCore import * 
from PythonQt.QtGui import * 

def getObjectsFromFiles(files):
	for file in files:
		os.path.exists(file) and mari.geo.load(file) 

def importObjectsFromDirectory():
	directory = QFileDialog.getExistingDirectory(None, "Select A Directory To Import!", "/")
	if directory:
		pass

def importMultipleObjects():
	if mari.projects.current():
		files = QFileDialog.getOpenFileNames(None, "Select Objects To Import!", "*.obj")
		if files:
			getObjectsFromFiles(files)
	else:
		QMessageBox.critical(None, "%s | Critical Exception." % __name__, "There Are No Active Projects, Please Open / Create One!", QMessageBox.Ok)

mari.menus.addAction(mari.actions.create("Import Objects From Directory ...", "import projectUtilities;reload(projectUtilities);projectUtilities.importObjectsFromDirectory()"), "MainWindow/&MPC/") 
mari.menus.addAction(mari.actions.create("Import Multiple Objects ...", "import projectUtilities;reload(projectUtilities);projectUtilities.importMultipleObjects()"), "MainWindow/&MPC/")

#def createProject():
#	files = ['/jobs/uap/build/vhclVickersModule/maya/textures/images/thomas-ma/objs/pCylinder1.obj','/jobs/uap/build/vhclVickersModule/maya/textures/images/thomas-ma/objs/pTorus1.obj','/jobs/uap/build/vhclVickersModule/maya/textures/images/thomas-ma/objs/pCone1.obj','/jobs/uap/build/vhclVickersModule/maya/textures/images/thomas-ma/objs/pSphere1.obj','/jobs/uap/build/vhclVickersModule/maya/textures/images/thomas-ma/objs/pCube1.obj','/jobs/uap/build/vhclVickersModule/maya/textures/images/thomas-ma/objs/pPlane1.obj']
#	mari.projects.create("default_example", files, [mari.ChannelInfo('color'), mari.ChannelInfo('blue', 512, 512, 16, False, True, mari.Color(0, 0, 0.5))])

#def getDirectoryObjects():
#	mari.geo.load('/jobs/uap/build/vhclVickersModule/maya/textures/images/thomas-ma/objs/pTorus1.obj') 
