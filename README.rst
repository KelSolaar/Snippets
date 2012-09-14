Snippets
========

Introduction
------------

Snippets is a GitHub Repository I decided to create as a host to the various code snippets I use on a daily basis and that are not properly interfaced. The idea came from this Thread at CGFeedback where I provided a few Snippets: http://www.cgfeedback.com/cgfeedback/showthread.php?t=900

Installation / Usage
--------------------

The Snippets are usually executed by a simple copy / paste into your target 3d Package Scripting Interpreter.
Adobe Photoshop scripts must be installed into the Adobe Photoshop scripting folder:

-  Mac Os X: /Applications/Adobe Photoshop CS*/Presets/Scripts/
-  Windows: C:\Program Files\Adobe\Adobe Photoshop CS*\Presets\Scripts\

Alternatively, on Maya, a Snippets Loader is provided, it requries PyQt and Foundations package available from Github: https://github.com/KelSolaar/Foundations.
Launching it is done issuing the following Python code::

   import sys
   
   FOUNDATIONS_PATH = "Path/To/Foundations/Folder/Foundations/src/"
   
   if FOUNDATIONS_PATH not in sys.path:
   	sys.path.append(FOUNDATIONS_PATH)
   
   LOADER_PATH = "Path/To/Snippets/Folder/Snippets/src/maya"
   
   if LOADER_PATH not in sys.path:
   	sys.path.append(LOADER_PATH)
   
   import snippets.engine
   snippets.engine.run()
   
   import snippets.loader
   import snippets.ui.common
   
   LOADER = snippets.loader.Loader(snippets.ui.common.getMayaWindow())
   LOADER.show()

About
-----

| Snippets by Thomas Mansencal - 2010 - 2012
| Copyright© 2010 - 2012 – Thomas Mansencal – `thomas.mansencal@gmail.com <mailto:thomas.mansencal@gmail.com>`_
| This software is released under terms of GNU GPL V3 license: http://www.gnu.org/licenses/
| `http://www.thomasmansencal.com/ <http://www.thomasmansencal.com/>`_
