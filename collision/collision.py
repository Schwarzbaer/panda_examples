#!/usr/bin/env python

from math import sin, cos, pi

from panda3d.core import Vec3, BitMask32
from panda3d.core import CollisionNode, CollisionSphere, CollisionRay
from panda3d.core import CollisionHandlerQueue, CollisionTraverser

from boilerplate.base import Base


BM_LEFT = BitMask32(0x1)
BM_RIGHT = BitMask32(0x10)


class SphereThatGetsCollidedWith:
    def __init__(self):
        # Target; a sphere. You should attach it to your actual model,
        # not .show() it directly. Also, the sphere you see is a low-
        # poly model, but the collisions will be calculated against a
        # mathematically perfect sphere.
        self.targets = [self.create_sphere(model_name, bitmask)
                        for model_name, bitmask in [("smiley", BM_LEFT), ("frowney", BM_RIGHT), ("jack", BM_LEFT | BM_RIGHT)]]
        base.taskMgr.add(self.move_collidee, "Moving Target Task")
    
    def create_sphere(self, model_name, bitmask):
        model = loader.loadModel("models/" + model_name)
        model.reparent_to(base.render)
        target = CollisionSphere(0, 0, 0, 1)
        target_node = CollisionNode('collision_target')
        target_node.setIntoCollideMask(bitmask)
        target_nodepath = model.attach_new_node(target_node)
        target_nodepath.node().addSolid(target)
        target_nodepath.show()
        return model

    def move_collidee(self, task):
        def circle_pos(t):
            return Vec3(cos(t) * 3, 0, sin(t) * 3)
        t_task = task.time
        [target.set_pos(circle_pos(t_task + idx * pi*2./3.))
         for idx, target in enumerate(self.targets)]
        return task.cont


class RayThatCollidesWithScene:
    def __init__(self):
        self.collision_rays = [self.setup_collision_ray(offset, bitmask)
                               for offset, bitmask in [(-3, BM_LEFT), (3, BM_RIGHT)]]
        self.queue = CollisionHandlerQueue()
        self.traverser = CollisionTraverser('Collision Traverser')
        self.traverser.showCollisions(base.render)
        for ray in self.collision_rays:
            self.traverser.add_collider(ray, self.queue)
        base.taskMgr.add(self.collide, "Collision Task")

    def setup_collision_ray(self, offset, bitmask):
        # Hitter. Do note that not every combination of object works,
        # there is a table for that in the manual.
        hitter = CollisionRay(0, 0, 0, 0, 1, 0)
        hitter_node = CollisionNode('collision_hitter')
        hitter_node.setFromCollideMask(bitmask)
        hitter_nodepath = base.render.attach_new_node(hitter_node)
        hitter_nodepath.node().addSolid(hitter)
        hitter_nodepath.set_pos(offset, -2, 0)
        hitter_nodepath.show()
        return hitter_nodepath

    def collide(self, task):
        self.traverser.traverse(render)
        for entry in self.queue.get_entries():
            print(entry)
        return task.cont


if __name__ == '__main__':
    app = Base(create_model=False)
    from_object = RayThatCollidesWithScene()
    into_object = SphereThatGetsCollidedWith()
    app.run()

