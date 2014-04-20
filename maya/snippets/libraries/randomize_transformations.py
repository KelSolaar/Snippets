import random
import maya.cmds as cmds

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2010 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["randomize_translations", "randomize_rotations", "randomize_scales"]

def randomize_translations(objects, randomRange=15):
	for object in objects:
		cmds.setAttr("{0}.tx".format(object), cmds.getAttr("{0}.tx".format(object)) + random.randrange(-1, 1) * (random.random() * randomRange))
		cmds.setAttr("{0}.ty".format(object), cmds.getAttr("{0}.ty".format(object)) + random.randrange(-1, 1) * (random.random() * randomRange))
		cmds.setAttr("{0}.tz".format(object), cmds.getAttr("{0}.tz".format(object)) + random.randrange(-1, 1) * (random.random() * randomRange))

def randomize_rotations(objects, randomRange=5):
	for object in objects:
		cmds.setAttr("{0}.rx".format(object), cmds.getAttr("{0}.rx".format(object)) + random.randrange(-1, 1) * (random.random() * randomRange))
		cmds.setAttr("{0}.ry".format(object), cmds.getAttr("{0}.ry".format(object)) + random.randrange(-1, 1) * (random.random() * randomRange))
		cmds.setAttr("{0}.rz".format(object), cmds.getAttr("{0}.rz".format(object)) + random.randrange(-1, 1) * (random.random() * randomRange))

def randomize_scales(objects, randomRange=2):
	for object in objects:
		randomValue = random.randrange(-1, 1) * (random.random() * randomRange)
		cmds.setAttr("{0}.sx".format(object), cmds.getAttr("{0}.sx".format(object)) + randomValue)
		cmds.setAttr("{0}.sy".format(object), cmds.getAttr("{0}.sy".format(object)) + randomValue)
		cmds.setAttr("{0}.sz".format(object), cmds.getAttr("{0}.sz".format(object)) + randomValue)
