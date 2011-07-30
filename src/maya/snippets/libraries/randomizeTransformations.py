import random
import maya.cmds as cmds

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

def randomizeTranslations(objects, randomRange = 15):
	for object in objects:
		cmds.setAttr(object + ".tx", cmds.getAttr(object + ".tx") + random.randrange(-1, 1) * (random.random() * randomRange))
		cmds.setAttr(object + ".ty", cmds.getAttr(object + ".ty") + random.randrange(-1, 1) * (random.random() * randomRange))
		cmds.setAttr(object + ".tz", cmds.getAttr(object + ".tz") + random.randrange(-1, 1) * (random.random() * randomRange))

def randomizeRotations(objects, randomRange = 5):
	for object in objects:
		cmds.setAttr(object + ".rx", cmds.getAttr(object + ".rx") + random.randrange(-1, 1) * (random.random() * randomRange))
		cmds.setAttr(object + ".ry", cmds.getAttr(object + ".ry") + random.randrange(-1, 1) * (random.random() * randomRange))
		cmds.setAttr(object + ".rz", cmds.getAttr(object + ".rz") + random.randrange(-1, 1) * (random.random() * randomRange))

def randomizeScales(objects, randomRange = 2):
	for object in objects:
		randomValue = random.randrange(-1, 1) * (random.random() * randomRange)
		cmds.setAttr(object + ".sx", cmds.getAttr(object + ".sx") + randomValue)
		cmds.setAttr(object + ".sy", cmds.getAttr(object + ".sy") + randomValue)
		cmds.setAttr(object + ".sz", cmds.getAttr(object + ".sz") + randomValue)
