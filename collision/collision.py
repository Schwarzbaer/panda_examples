#!/usr/bin/env python

from math import sin

from panda3d.core import Vec3
from panda3d.core import CollisionNode, CollisionSphere, CollisionRay
from panda3d.core import CollisionHandlerQueue, CollisionTraverser

from boilerplate.base import Base


class SphereThatGetsCollidedWith:
    def __init__(self):
        # Target; a sphere. You should attach it to your actual model,
        # not .show() it directly. Also, the sphere you see is a low-
        # poly model, but the collisions will be calculated against a
        # mathematically perfect sphere.
        self.target = CollisionSphere(0, 0, 0, 1)
        self.target_nodepath = base.render.attach_new_node(CollisionNode('collision_target'))
        self.target_nodepath.node().addSolid(self.target)
        self.target_nodepath.show()
        base.taskMgr.add(self.move_collidee, "Moving Target Task")

    def move_collidee(self, task):
        self.target_nodepath.set_pos(sin(task.time) * 3, 0, 0)
        return task.cont


class RayThatCollidesWithScene:
    def __init__(self):
        self.setup_collision_ray() #  Now we have self.hitter_nodepath
        self.queue = CollisionHandlerQueue()
        self.traverser = CollisionTraverser('Collision Traverser')
        self.traverser.showCollisions(base.render)
        self.traverser.add_collider(self.hitter_nodepath, self.queue)
        base.taskMgr.add(self.collide, "Collision Task")

    def setup_collision_ray(self):
        # Hitter. Do note that not every combination of object works,
        # there is a table for that in the manual.
        hitter = CollisionRay(0, 0, 0, 0, 1, 0)
        self.hitter_nodepath = base.render.attach_new_node(CollisionNode('collision_hitter'))
        self.hitter_nodepath.node().addSolid(hitter)
        self.hitter_nodepath.set_pos(0, -10, 0)
        self.hitter_nodepath.show()

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

