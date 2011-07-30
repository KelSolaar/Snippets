import maya.cmds as cmds
import maya.mel as mel
import os

USER_HOOK = "@user"
EXPORT_DIRECTORY = "textures/images/%s/objs" % USER_HOOK
FILE_DEFAULT_PREFIX = "Export"
FILE_TYPES = {"Obj" : {"extension" : "obj", "type" : "OBJexport", "options" : "groups=1;ptgroups=1;materials=0;smoothing=1;normals=1"}}

def stacksHandler(object):
	"""
	This decorator is used to handle various Maya stacks.

	@param object: Python object. ( Object )
	@return: Python function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This decorator is used to handle various Maya stacks.

		@return: Python object. ( Python )
		"""

		cmds.undoInfo(openChunk=True)
		value = object(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya produces a weird command error if not wrapped here.
		try:
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")"% (__name__, __name__, object.__name__), addCommandLabel=object.__name__)
		except:
			pass
		return value

	return stacksHandlerCall

def getTransform(node, fullPath=True):
	"""
	This definition returns transform of the provided node.

	@param node: Current object. ( String )
	@param fullPath: Current full path state. ( Boolean )
	@return: Object transform. ( String )
	"""

	transform = node
	if cmds.nodeType(node) != "transform":
		parents = cmds.listRelatives(node, fullPath=fullPath, parent=True)
		transform = parents[0]
	return transform

def setPadding(data, padding, affix="0"):
	"""
	This definition pads the provided data.

	@param data: Data to pad. ( String )
	@param padding: Padding. ( Integer )
	@param affix: Padding affix. ( String )
	"""

	while len(data) < padding:
		data = affix + data
	return data

def getUserExportDirectory():
	"""
	This definition gets the user export directory.

	@return: Export directory. ( String )
	"""

	workspace = cmds.workspace(q=True, rd=True)
	user = os.environ["USER"]
	return os.path.join(workspace, EXPORT_DIRECTORY.replace(USER_HOOK, user))

def exportObjectsToFiles(objects, exportType, useObjectsNames=True, useLongNames=False):
	"""
	This definition export provided objects to files.

	@param objects: Objects to export. ( List )
	@param exportType: Export type. ( String )
	@param useObjectsNames: Use objects names. ( Boolean )
	@param useLongNames: Use long Maya names. ( Boolean )
	@return: Exported files. ( List )
	"""

	exportDirectory = getUserExportDirectory()
	not os.path.exists(exportDirectory) and os.makedirs(exportDirectory)

	exportedFiles = []
	for i, object in enumerate(objects):
		if useObjectsNames:
			basename = useLongNames and object.replace("|","_") or object.split("|")[-1]
		else:
			basename = "%s_%s" % (FILE_DEFAULT_PREFIX, setPadding(str(i), 3))
		name = os.path.join(exportDirectory, "%s.%s" % (basename, FILE_TYPES[exportType]["extension"]))
		print("%s | Export '%s' to '%s'!" % (__name__, object, name))
		cmds.select(object)
		cmds.file(name, force=True, options=FILE_TYPES[exportType]["options"], typ=FILE_TYPES[exportType]["type"], es=True)
		exportedFiles.append(name)
	return exportedFiles

def exportSelectedObjectsToShortObjFiles():
	"""
	This definition exports selected objects to short named obj files.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	selection and exportObjectsToFiles(selection, "Obj", True, False)

@stacksHandler
def IExportSelectedObjectsToShortObjFiles():
	"""
	This definition is the exportSelectedObjectsToShortObjFiles definition Interface.
	"""

	exportSelectedObjectsToShortObjFiles()

def exportSelectedObjectsToLongObjFiles():
	"""
	This definition exports selected objects to long named obj files.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	selection and exportObjectsToFiles(selection, "Obj", True, True)

@stacksHandler
def IExportSelectedObjectsToLongObjFiles():
	"""
	This definition is the exportSelectedObjectsToLongObjFiles definition Interface.
	"""

	exportSelectedObjectsToLongObjFiles()

def exportDefaultObject(object):
	"""
	This definition exports the default object.
	"""

	exportObjectsToFiles((object, ), "Obj", False)[0]

@stacksHandler
def IExportDefaultObject():
	"""
	This definition is the exportDefaultObject definition Interface.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	selection and exportDefaultObject(selection[0])

def exportSelectedObjectToUvLayout(object):
	"""
	This definition exports the selected object to uvlayout.
	"""

	file = exportObjectsToFiles((object, ), "Obj", False)[0]
	os.system("uvlayout %s&" % file)

@stacksHandler
def IExportSelectedObjectToUvLayout():
	"""
	This definition is the exportSelectedObjectToUvLayout definition Interface.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	selection and exportSelectedObjectToUvLayout(selection[0])

def importDefaultObject():
	"""
	This definition imports the default object: 'Export_000.obj'.
	"""

	name = os.path.join(getUserExportDirectory(), "%s.%s" % ("%s_%s" % (FILE_DEFAULT_PREFIX, setPadding(str(0), 3)), FILE_TYPES["Obj"]["extension"]))
	if os.path.exists(name):
		nodesBefore = cmds.ls()
		cmds.file(name, r=True, dns=True)
		cmds.select([node for node in list(set(cmds.ls()).difference(set(nodesBefore))) if cmds.nodeType(node) == "transform"])
	else:
		mel.eval("warning(\"%s | '%s' file does't exists!\")" % (__name__, name))
@stacksHandler
def IImportDefaultObject():
	"""
	This definition is the importDefaultObject definition Interface.
	"""

	importDefaultObject()
