from random import random

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import CardMaker, PTAUchar, Texture, PNMImage, Point2


class Plot:
    def __init__(self, x_size=640, y_size=480):
        self.data_x = list(range(100))
        self.data_y = [random()]
        for _ in range(99):
            self.data_y.append((self.data_y[-1] + random()) / 2.0)

        self.fig = Figure(figsize=(x_size / 100.0, y_size / 100.0), dpi=100.0)
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        [self.line_data] = self.ax1.step(
            self.data_x,
            self.data_y,
            'g-',
            label="Nearly random data",
        )
        self.ax1.set_title("A matplotlib figure")
        self.ax1.set_autoscaley_on(False)
        self.ax1.set_ylim([0.0, 1.0])
        self.ax1.legend(loc=4)
        self.ax1.grid()

    def draw(self):
        self.data_y.append((self.data_y[-1] + random()) / 2.0)
        self.data_y.pop(0)
        # If your y axis limits are going to change, you need:
        #     self.line_data.set_ydata(self.data_y)
        # or set limits explicitly, as shown in __init__().
        # set_data() doesn't realign them, but is cheaper.
        self.line_data.set_data(self.data_x, self.data_y)
        graph_bytes, _res = FigureCanvasAgg(self.fig).print_to_buffer()
        return graph_bytes


class MatPlotLibDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.setFrameRateMeter(True)

        x_size, y_size = 640, 480
        xy_ratio = float(y_size) / float(x_size)
        self.plot = Plot(x_size, y_size)

        self.input_img = PNMImage(x_size, y_size)
        self.input_tex = Texture()
        self.input_tex.load(self.input_img)

        self.card = CardMaker('pygame_card')
        self.card.setUvRange(Point2(0, 1),  # ll
                             Point2(1, 1),  # lr
                             Point2(1, 0),  # ur
                             Point2(0, 0))  # ul
        self.screen = render.attach_new_node(self.card.generate())
        self.screen.set_scale(1, 1, xy_ratio)
        self.screen.set_pos(-0.5, 2, -0.5 * xy_ratio)
        self.screen.setTexture(self.input_tex)

        taskMgr.add(self.update, "update pygame_card")

    def update(self, task):
        self.input_tex.set_ram_image_as(self.plot.draw(), "RGBA")
        return task.cont


mpld = MatPlotLibDemo()
mpld.run()
