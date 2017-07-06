from direct.showbase.ShowBase import *
from direct.task import Task
from panda3d.core import CardMaker, PTAUchar, Texture, PNMImage, Point2

import pygame
import random


class Game:
    def __init__(self):
        pygame.init()
        self.res = (320, 320)
        self.surface = pygame.Surface(self.res)

    def update(self):
        r = []
        for i in range(7):
            r.append(random.randint(0,255))
        self.surface.fill((r[0],r[1],r[2]),(r[3], r[4], r[5], r[6]))


class PygameCard(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.game = Game()
        self.camLens.setFov(120)
        self.input_img = PNMImage(self.game.res[0], self.game.res[1])
        self.input_tex = Texture()
        self.input_tex.load(self.input_img)

        self.card = CardMaker('pygame_card')
        self.screen = render.attach_new_node(self.card.generate())
        self.screen.setPos(-0.5,2,-0.5)
        self.screen.setTexture(self.input_tex)

        taskMgr.add(self.update, "update pygame_card")

    def update(self, task):
        self.game.update()
        ram = self.game.surface.get_view("0")
        self.input_tex.set_ram_image_as(ram, "RGBA")
        return task.cont


p = PygameCard()
p.run()
