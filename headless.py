#!/usr/bin/env python

from panda3d.core import loadPrcFileData
from direct.showbase.ShowBase import ShowBase


loadPrcFileData("", "window-type none")
s = ShowBase()
base.task_mgr.do_method_later(3, print, "Panda3D is still running", ["foo"])


s.run()

