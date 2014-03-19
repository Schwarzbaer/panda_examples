#!/usr/bin/env python

import sys
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton

s = ShowBase()

b = DirectButton(text       = ("OK", "click!", "rolling over", "disabled"),
                 text_scale = 0.1,
                 frameColor = (0.6, 0.6, 0.6, 1.0),
                 frameSize  = (-0.3, 0.3, -0.3, 0.3),
                 pos        = (0.0, 0.0, -0.7))

s.accept("escape", sys.exit)

s.run()
