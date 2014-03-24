#!/usr/bin/env python2

from direct.showbase.ShowBase import ShowBase
from panda3d.rocket import RocketRegion, RocketInputHandler, LoadFontFace
import sys

class GUI(ShowBase):
    def __init__(self):
        # Basics
        ShowBase.__init__(self)
        base.disableMouse()
        self.accept("escape", sys.exit)

        LoadFontFace("./gnu-freefont_freesans/FreeSans.ttf")

        self.region = RocketRegion.make('pandaRocket', base.win)
        self.region.setActive(1)
        self.region.initDebugger()
        self.region.setDebuggerVisible(False)
        self.context = self.region.getContext()

        self.documents = {}
        self.documents['main'] = self.context.LoadDocument('./demo.rml')
        # .Show() to display document, .Hide() to hide.
        self.documents['main'].Show()

        self.elementEffects = []

        # setup the mouse
        self.inputHandler = RocketInputHandler()
        base.mouseWatcher.attachNewNode(self.inputHandler)
        self.region.setInputHandler(self.inputHandler)

        # taskMgr.doMethodLater(5, self.loadingFinished, 'HUD Loading Finished')

        # Setup the messages we accept.
        #self.accept('update', self.updateMessage)

	def update(self, dt):
		BaseDirectObject.update(self, dt)
		self.updateElementEffects(dt)
		
	def destroy(self):
		BaseDirectObject.destroy(self)
		 
		for key in self.documents:
			self.documents[key].Close()
			self.context.UnloadDocument(self.documents[key])
		del self.documents
		
		del self.context
		base.win.removeDisplayRegion(self.region)
		del self.region
		
	#def updateElementEffects(self, dt):
	#	for elementEffect in self.elementEffects:
	#		elementEffect.update(dt)
	#		element = self.documents['main'].GetElementById(elementEffect.element)
	#		if elementEffect.property == 'opacity':
	#			element.style.opacity = elementEffect.currentValue()
	#		elif elementEffect.property == 'top':
	#			element.style.top = elementEffect.currentValue()
	#		elif elementEffect.property == 'bottom':
	#			element.style.bottom = elementEffect.currentValue()
	#		elif elementEffect.property == 'left':
	#			element.style.left = elementEffect.currentValue()
	#		elif elementEffect.property == 'right':
	#			element.style.right = elementEffect.currentValue()
	#		if elementEffect.finished():
	#			self.elementEffects.remove(elementEffect)

	#def updateMessage(self, updateType, *args):
	#	if updateType == "debug":
	#		debugInfo1 = self.documents['main'].GetElementById('debugInfo1')
	#		debugInfo2 = self.documents['main'].GetElementById('debugInfo2')
	#		text = ""
	#		for arg in args:
	#			if text == "":
	#				text = arg
	#			else:
	#				text = strcat(text, "<br />\n", arg)
	#		debugInfo1.inner_rml = text
	#	if updateType == "debug2":
	#		debugInfo1 = self.documents['main'].GetElementById('debugInfo1')
	#		debugInfo2 = self.documents['main'].GetElementById('debugInfo2')
	#		text = ""
	#		for arg in args:
	#			if text == "":
	#				text = arg
	#			else:
	#				text = strcat(text, "<br />\n", arg)
	#		debugInfo2.inner_rml = text
	#	elif updateType == "messageBox":
	#		messageBox = self.documents['main'].GetElementById('messageBox')
	#		text = ""
	#		for arg in args:
	#			if text == "":
	#				text = arg
	#			else:
	#				text = strcat(text, "<br />\n", arg)
	#		messageBox.inner_rml = text
		
	#def toggleGuiMode(self):
	#	# no switching while things are moving
	#	if self.elementEffects:
	#		return self.guiMode
		
	#	self.guiMode = not self.guiMode
	#	self.setMessageBoxVisible(self.guiMode)
	#	self.setHudVisible(not self.guiMode)
		
	#	return self.guiMode
	
	#def setMessageBoxVisible(self, visible):
	#	if visible:
	#		self.documents['main'].GetElementById('messageBox').style.visibility = "visible"
	#	else:
	#		self.documents['main'].GetElementById('messageBox').style.visibility = "hidden"
	
	#def setHudVisible(self, visible, duration=0.1):
	#	topContainer = self.documents['main'].GetElementById('topContainer')
	#	bottomContainer = self.documents['main'].GetElementById('bottomContainer')
	#	if not visible:
	#		self.elementEffects.append(ElementMoveEffect('topContainer', 0, 0 - topContainer.offset_height, duration, 'top'))
	#		self.elementEffects.append(ElementMoveEffect('bottomContainer', 0, 0 - bottomContainer.offset_height, duration, 'bottom'))
	#	else:
	#		self.elementEffects.append(ElementMoveEffect('topContainer', 0 - topContainer.offset_height, 0, duration, 'top'))
	#		self.elementEffects.append(ElementMoveEffect('bottomContainer', 0 - bottomContainer.offset_height, 0, duration, 'bottom'))
	#	self.updateElementEffects(0)

	#def toggleDebugger(self):
	#	self.region.setDebuggerVisible(not self.region.isDebuggerVisible())

	#def debuggerPrint(self, message, type="always"):
	#	options = {
	#		"always": logtype.always,
	#		"error": logtype.error,
	#		"warning": logtype.warning,
	#		"info": logtype.info,
	#		"debug": logtype.debug,
	#		}
	#	Log(options[type], message)
		
	#def loadingFinished(self, task=None):
	#	self.setMessageBoxVisible(self.guiMode)
	#	self.setHudVisible(not self.guiMode, 0)
	#	self.docLoading.Hide()
	#	self.documents['main'].Show()
		
	#	if task:
	#		return task.done

	#def removeCoordType(self, coord):
	#	return float(str(coord).rstrip("%px"))

gui = GUI()
gui.run()

