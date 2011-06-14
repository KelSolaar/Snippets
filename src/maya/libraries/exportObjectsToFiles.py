import maya.cmds as cmds
import maya.mel as mel
import os

USER_HOOK = "@user"
EXPORT_DIRECTORY = "textures/images/%s/objs" % USER_HOOK
FILE_DEFAULT_PREFIX = "Export"
FILE_TYPES = {"Obj" : {"extension" : "obj", "type" : "OBJexport", "options" : "groups=1;ptgroups=1;materials=0;smoothing=1;normals=1"}}

def stacksHandler(object_):
	"""
	This Decorator Is Used To Handle Various Maya Stacks.

	@param object_: Python Object ( Object )
	@return: Python Function. ( Function )
	"""

	def stacksHandlerCall(*args, **kwargs):
		"""
		This Decorator Is Used To Handle Various Maya Stacks.

		@return: Python Object. ( Python )
		"""
		
		cmds.undoInfo(openChunk=True)
		value = object_(*args, **kwargs)
		cmds.undoInfo(closeChunk=True)
		# Maya Produces A Weird Command Error If Not Wrapped Here.
		try:
			cmds.repeatLast(addCommand="python(\"import %s; %s.%s()\")"% (__name__, __name__, object_.__name__), addCommandLabel=object_.__name__)
		except:
			pass
		return value

	return stacksHandlerCall

def setPadding(data, padding, affix="0"):
	"""
	This Definition Pads The Provided Data.
	
	@param data: Data To Pad. ( String )
	@param padding: Padding. ( Integer )
	@param affix: Padding Affix. ( String )
	"""

	while len(data) < padding:
		data = affix + data
	return data

def getUserExportDirectory():
	"""
	This Definition Gets The User Export Directory.
	
	@return: Export directory. ( String )
	"""

	workspace = cmds.workspace(q=True, rd=True)
	user = os.environ["USER"]
	return os.path.join(workspace, EXPORT_DIRECTORY.replace(USER_HOOK, user))
	 
def exportObjectsToFiles(objects, exportType, useObjectsNames=True, useLongNames=False):
	"""
	This Definition Export Provided Objects To Files.
	
	@param objects: Objects To Export. ( List )
	@param exportType: Export Type. ( String )
	@param useObjectsNames: Use Objects Names. ( Boolean )
	@param useLongNames: Use Long Maya Names. ( Boolean )
	@return: Exported Files. ( List )
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
		print("%s | Export '%s' To '%s'!" % (__name__, object, name))
		cmds.select(object)
		cmds.file(name, force=True, options=FILE_TYPES[exportType]["options"], typ=FILE_TYPES[exportType]["type"], es=True)
		exportedFiles.append(name)
	return exportedFiles

def exportSelectedObjectsToShortObjFiles():
	"""
	This Definition Export Selected Objects To Short Named Obj Files.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	selection and exportObjectsToFiles(selection, "Obj", True, False)

@stacksHandler
def IExportSelectedObjectsToShortObjFiles():
	"""
	This Definition Is The exportSelectedObjectsToShortObjFiles Method Interface.
	"""

	exportSelectedObjectsToShortObjFiles()

def exportSelectedObjectsToLongObjFiles():
	"""
	This Definition Export Selected Objects To Long Named Obj Files.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	selection and exportObjectsToFiles(selection, "Obj", True, True)

@stacksHandler
def IExportSelectedObjectsToLongObjFiles():
	"""
	This Definition Is The exportSelectedObjectsToLongObjFiles Method Interface.
	"""

	exportSelectedObjectsToLongObjFiles()

def exportSelectedObjectToUvLayout(object):
	"""
	This Definition Export The Selected Object To UVLayout.
	"""

	file = exportObjectsToFiles((object, ), "Obj", False)[0]
	os.system("uvlayout %s" % file)

@stacksHandler
def IExportSelectedObjectToUvLayout():
	"""
	This Definition Is The exportSelectedObjectToUvLayout Method Interface.
	"""

	selection = list(set(cmds.ls(sl=True, l=True, o=True)))
	selection and exportSelectedObjectToUvLayout(selection[0])

def importDefaultObject():
	"""
	This Definition Import The Default Object: 'Export_000.obj'.
	"""

	name = os.path.join(getUserExportDirectory(), "%s.%s" % ("%s_%s" % (FILE_DEFAULT_PREFIX, setPadding(str(0), 3)), FILE_TYPES["Obj"]["extension"]))
	if os.path.exists(name):
		cmds.file(name, r=True, dns=True)
	else:
		mel.eval("warning(\"%s | '%s' File Does't Exists!\")" % (__name__, name))
@stacksHandler
def IImportDefaultObject():
	"""
	This Definition Is The importDefaultObject Method Interface.
	"""

	importDefaultObject()
