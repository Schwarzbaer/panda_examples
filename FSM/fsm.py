#!/usr/bin/env python

from direct.showbase.ShowBase import ShowBase
from direct.fsm.FSM import FSM
from direct.task import Task
import sys

# A Finite State Machines state names are defined by the presence of
# enterX() or exitX() methods, where X is the state name. These
# methods will be called when a state is entered or exited. A state
# change can be induced by calling fsm.request("X").
# If the current state also has a filterX() method, that will be
# called instead by request("arg"), so that arg can be used in
# determining the actual state that the machine should move into.
# filter() should return that states name, or None if no change
# should occur.
#
# FIXME: Explain "arguments to request"=="arguments to enterX"
# FIXME: Explain FSM.defaultTransitions
# FIXME: Catch FSM.RequestDenied
# FIXME: Mention fsm.state and FSM.AlreadyInTransition
# FIXME: Explain defaultFilter
# FIXME: demand(), forceTransition()

class MyApp(ShowBase):
    def __init__(self):
        # Basics
        ShowBase.__init__(self)
        base.disableMouse()
        self.camera.set_pos(0, -10, 0)
        self.camera.look_at(0, 0, 0)
        self.accept("escape", sys.exit)
        # State machine
        self.fsm = RotationState(self)
        self.rotation = 0
        # Model, control and rotation task
        self.model = self.loader.loadModel("models/smiley")
        self.model.reparent_to(self.render)
        self.accept("arrow_left", self.fsm.request, ['left'])
        self.accept("arrow_right", self.fsm.request, ['right'])
        self.taskMgr.add(self.rotate, "rotation")
    def set_rotation(self, rotation):
        self.rotation = rotation
    def rotate(self, task):
        self.model.set_h(self.model.get_h() + self.rotation * task.getDt() * 360.0)
        return Task.cont

class RotationState(FSM):
    def __init__(self, statekeeper):
        FSM.__init__(self, "RotationStateFSM")
        self.statekeeper = statekeeper
        self.request('RotationStop')
    # State for rotating left
    def enterRotationLeft(self):
        self.statekeeper.set_rotation(-360.0)
    def exitRotationLeft(self):
        pass
    def filterRotationLeft(self, request, args):
        if request == "right":
            return "RotationStop"
        else:
            return None
    # State for rotating right
    def enterRotationRight(self):
        self.statekeeper.set_rotation(360.0)
    def exitRotationRight(self):
        pass
    def filterRotationRight(self, request, args):
        if request == "left":
            return "RotationStop"
        else:
            return None
    # State for rotating left
    def enterRotationStop(self):
        self.statekeeper.set_rotation(0.0)
    def exitRotationStop(self):
        pass
    def filterRotationStop(self, request, args):
        if request == "left":
            return "RotationLeft"
        elif request == "right":
            return "RotationRight"
        else:
            return None

app = MyApp()
app.run()

