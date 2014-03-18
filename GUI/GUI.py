#!/usr/bin/env python

import sys
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DirectRadioButton

s = ShowBase()

class ConfigMenu:
    def __init__(self):
        main_window  = DirectFrame(frameColor = (0.8, 0.8, 0.8, 1.0),
                                   frameSize  = (-1.0, 1.0, -0.9, 0.9),
                                   pos        = (0.0, 0.0, 0.0))
        main_tabs    = DirectRadioButton()

b = DirectButton(text       = ("OK", "click!", "rolling over", "disabled"),
                 text_scale = 0.1,
                 #test_pos   = (0.0, 0.15),
                 frameColor = (0.6, 0.6, 0.6, 1.0),
                 frameSize  = (-0.3, 0.3, -0.3, 0.3),
                 pos        = (0.0, 0.0, -0.7))
b.reparent_to(GUI_main)

s.accept("escape", sys.exit)

s.run()
