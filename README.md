panda\_examples
===============

These are examples for functionality of Panda3D. They are meant to be as minimal as possible, each showing exactly one thing, and each be executable right out of the box. The intention is rather to get you started than being complete examples of anything, though in the future further examples will delve into more advanced features.

basics
------

Let the camera rotate around the camera with your left and right cursor key.

Features demonstrated:
* Loading a model and attaching it to the scene graph
* Events
* Tasks
* Moving a node

bullet\_physics
---------------

Features demonstrated:
* Setting up and stepping a physics simulation
* Adding a Rigid Body
* Apply an impulse

cubemap
-------

This one sets up a scene and saves a cube map snapshot of it a six images in industry standard format. This should later come in handy to precreate skyboxes.

Features demonstrated:
* Save a cube map

FSM
---

This sets up a simple state machine that lets a sphere rotate clockwise, counterclockwise or not at all. Using the left and right cursor keys, you can switch between states.

Features demonstrated:
* Finite State Machine

geometry
--------

Here I show how to create geometry in Python code. The peed bottleneck here is how fast the CPU can crunch through the code to generate the data. 900 vertices / 1682 triangles each frame drop the framerate to just above 20 for me. In normal applications, recreating the whole mesh either isn't done each frame, or is done in geometry shaders.

I create two heightmaps consisting of white noise only, and interpolate them based on time, one second for a full blendover. After a full blend, I set a new heightmap to blend to.

Features demonstrated:
* Creating Geoms / GeomNodes from scratch
* Writing (and, in comments, reading) vertex data

GUI
---

Okay, it *does* get a bit ridiculous here. All I did here was plaster a button on the screen. I guess the point here is mostly that DirectGUI widgets reparent themselves to aspect2d automagically, so... Keep in mind to manage your scene graph?

Features demonstrated:
* DirectGUI elements

libRocket
---------

A minimal libRocket GUI

Features demonstrated:
* Loading a font
* Setting up the Python-side of the GUI
* RML / RCSS

lod
---

Level of detail. I created a model of a tree on tree different detail levels and you're allowed to laugh, but even for programmers art I did them quarter-assed. Anyways, your up and down cursor keys will move you towards and away from the tree, showing how the mesh gets exchanged automagically.

Features demonstrated:
* Level of Detail nodes

render\_to\_texture
-------------------

You have a camera sonewhere in your game world and a screen that shows wat's on the camera? You want 2D displays showing something that's easier to model in 3D? Or you have any other purpose for having a Panda3D camera render into a texture? This is the example for you.

Features demonstrated:
* Set up a secondary scene graph, which will get rendered into textures.
* Create a butter, set its sort order.
* Create a camera and let it render into that buffer.
* Get a texture from the buffer and set it as a "monitors" texture.

selfshadow
----------

Features demonstrated:
* Set up a shadow-casting light.
* Make all objects in the scene graph receive shadows.

skybox
------

I admit that this is a bit of a weird one. I've assembled an .egg file mostly by hand to tile a texture onto a cube, where the texture coords of each vertex is smack in the middle of the corner pixel of that sides tile, so that mipmapping should be avoided. The point is that with this, you can create high-quality skybox textures.

A bunch of spheres in the scene show that the skybox gets rendered "behind" objects in the scene, even though the box should be too small to contain the outer spheres.

Features demonstrated:
* Rendering objects as background
