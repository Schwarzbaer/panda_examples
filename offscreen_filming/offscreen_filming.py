import sys

from panda3d.core import loadPrcFileData
from direct.showbase.ShowBase import ShowBase


loadPrcFileData('', 'window-type offscreen')
ShowBase()
model = base.loader.load_model('models/panda-model')
model.reparent_to(base.render)
camera_gimbal = base.render.attach_new_node('gimbal')
base.cam.reparent_to(camera_gimbal)
base.cam.set_pos(0, -5000, 1000)
base.cam.look_at(0, 0, 0)
image_count = 0
def rotate_gimbal(task):
    global image_count
    camera_gimbal.set_h(image_count * 12.0)
    return task.cont
def screenshot_and_possibly_abort(task):
    global image_count
    base.screenshot(f"screenshot-{image_count:03d}.png", False)
    image_count += 1
    if image_count == 30:
        sys.exit()
    return task.cont
base.task_mgr.add(rotate_gimbal, sort=49)
base.task_mgr.add(screenshot_and_possibly_abort, sort=51)
base.run()
