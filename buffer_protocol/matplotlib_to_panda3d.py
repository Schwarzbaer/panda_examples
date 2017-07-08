from random import random

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import (
    CardMaker,
    PTAUchar,
    Texture,
    PNMImage,
    Point2,
    TransparencyAttrib,
)


class Plot:
    def __init__(self, x_size=640, y_size=480):
        self.data_x = list(range(101))
        self.data_y1 = [random()]
        self.data_y2 = [self.data_y1[0]]
        for _ in range(100):
            r = random()
            self.data_y1.append((self.data_y1[-1] + r) / 2.0)
            self.data_y2.append(self.data_y2[-1] + r)

        self.fig = Figure(figsize=(x_size / 100.0, y_size / 100.0), dpi=100.0)

        # The first graph
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        [self.line1_data] = self.ax1.step(
            self.data_x,
            self.data_y1,
            'g-',
            label="Nearly random data",
        )

        # X axis decoration
        self.ax1.set_xlim([0, 100])
        self.ax1.set_xlabel("A series of 100 values")

        # Y axis decoration
        self.ax1.set_ylabel("How much?")
        self.ax1.set_autoscaley_on(False)
        self.ax1.set_ylim([0.0, 1.0])
        self.ax1.set_yticks((0.0, 0.33, 0.66, 1.00))
        self.y_labels = self.ax1.set_yticklabels(
            ('None', 'Some', 'Much', 'Lots')
        )
        for label in self.y_labels:
            label.set_rotation(45)

        # A second graph with a different axis on the same plot
        self.ax2 = self.ax1.twinx()
        self.ax2.set_autoscaley_on(True)
        [self.line2_data] = self.ax2.plot(
            self.data_x,
            self.data_y2,
            'r-',
            label="Summed random data",
        )

        # Title, legend and grid
        self.ax1.set_title("A matplotlib figure")
        self.ax1.legend(loc='lower right')
        self.ax1.grid()

        # FIXME: This doesn't work yet; see comments in draw().
        # self.fig.patch.set_alpha(0.5)
        # self.ax1.patch.set_alpha(0.5)

        self.canvas = FigureCanvasAgg(self.fig)

    def draw(self):
        r = random()
        self.data_y1.append((self.data_y1[-1] + r) / 2.0)
        self.data_y1.pop(0)
        self.data_y2.append(self.data_y2[-1] + r)
        self.data_y2.pop(0)
        # If your y axis limits are going to change, you need:
        #     self.line_data.set_ydata(self.data_y)
        # or set limits explicitly, as shown in __init__().
        # set_data() doesn't realign them, but is cheaper.
        self.line1_data.set_data(self.data_x, self.data_y1)
        self.line2_data.set_ydata(self.data_y2)
        graph_bytes, _res = self.canvas.print_to_buffer()
        return graph_bytes


class MatPlotLibDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.setFrameRateMeter(True)

        m = loader.loadModel("models/smiley")
        m.reparent_to(render)
        m.set_pos(0, 5, 0)

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
        # FIXME: Apparently mpl's print_to_buffer() doesn't write
        # alpha values properly. 
        self.screen.setTransparency(TransparencyAttrib.MAlpha)

        taskMgr.add(self.update, "update plot")

    def update(self, task):
        self.input_tex.set_ram_image_as(self.plot.draw(), "RGBA")
        return task.cont


mpld = MatPlotLibDemo()
mpld.run()
