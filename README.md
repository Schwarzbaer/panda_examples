panda\_examples
===============

These are examples for functionality of Panda3D. They are meant to be as minimal as possible, each showing exactly one thing, and each be executable right out of the box. The intention is rather to get you started than being complete examples of anything, though in the future further examples will delve into more advanced features.


Procedural modeling and animation
---------------------------------

In this course we will deal with using code to create geometric models, and animate them. We will not deal with advanced procedural generation algorithms to create complex objects, only with the underlying API that would also be used to turn such complex models into actual data that Panda3D can work on.


### geometry

Here we generate a static model purely in code, so as to see what is
going on under the hood. In
[`basic_model.py`][./geometry/basic_model.py] we learn
* how to define a table for vertices,
* how to fill it with data,
* how to add primitives, in particular triangles.

[`main.py`][./geometry/main.py] is mostly a convenience so that we can
actually look at something.


### pbr

Building on `geometry`, we discuss the properties of PBR-capable models
and their textures. [`pbr_model.py`][./pbr/pbr_model.py] shows
* what vertex columns a PBR model typically uses,
* what materials are and do,
* what information is encoded in textures, and how,
* how to procedurally generate images to load into textures.

There are three executable progrems this time, where
* [`main_no_pbr.py`][./pbr/main_no_pbr.py] shows how the model looks in
  the default renderer,
* [`main_simplepbr.py`][./pbr/main_simplepbr.py.py] uses Moguri's
  [`panda3d-simplepbr` package][https://github.com/Moguri/panda3d-simplepbr],
* and [`main_complexpbr.py`][./pbr/main_complexpbr.py] does the same for
  Simulan's
  [`panda3d-complexpbr` package][https://github.com/rayanalysis/panda3d-complexpbr].


### bones

Also building on `geometry`, we create the model of a tentacle, and
give it a chain of bones to animate it around. As you will doubtlessly
expect by now, [`bones_model.py`][./bones/bones_model.py] does the same
old "Create a table, fill it with vertices, add triangles" song and
dance, while adding information to the vertices about which bones they
should consider for changing their apparent data while the model is
being animated.

There are four paradigms of animation that I am aware of, with advanced
procedural animation techniques building on those. There are
* Forward Kinematics, basically just setting bones to translations
  generated ad hoc in code, shown in
  [`main_control_joints.py`][./bones/main_control_joints.py],
* Skeletal animation, which is basically the same, using pre-recorded
  and usually artist-generated animations; Here we use
  [`main_mocap.py`][./bones/main_mocap.py] to record an animation using
  [rdb's][https://github.com/rdb/] [`mocap.py`][./bones/mocap.py], and
  play it back with [`main_animation.py`][./bones/main_animation.py],
* Inverse Kinematics, which is the reverse of Forward Kinematics, in
  that the code provides a target that a chain of bones should reach
  for, and leaves it to mathematical tools to move the bones within
  provided constraints so as to reach the target, demonstrated in
  [`main_inverse_kinematics.py`][./bones/main_inverse_kinematics.py]
  using [CCD-IK-Panda3D][https://github.com/Germanunkol/CCD-IK-Panda3D]
  by [germanunkol][https://github.com/Germanunkol/],
* and Physical Simulation, where we add information about a physical
  approximation of our model to simulate how it moves under the
  influence of gravity and collisions by using Panda3D's Bullet
  integration as in [`main_physics.py`][./bones/main_physics.py].


Miscellaneous snippets
----------------------

### basics

Let the camera rotate around the camera with your left and right cursor key.

Features demonstrated:
* Loading a model and attaching it to the scene graph
* Events
* Tasks
* Moving a node


### 3d-sound

Have an object in the scene emit a sound which is then rendered appropriately.

This example uses a sound file downloaded at http://www.freesound.org/people/lth_stp/sounds/120490/ created by the sound department of the states theater of Lower Austria (Landestheater Niederösterreich). I have dropped an audio channel (the original is stereo, this version is mono) and converted it to Ogg Vorbis. The file is licensed under the Creative Commons 3.0 license, Attribution-NonCommercial: http://creativecommons.org/licenses/by-nc/3.0/

Features demonstrated:
* 3D sound

Features not yet demonstrated:
* Doppler shift


### bullet\_physics

Features demonstrated:
* Setting up and stepping a physics simulation
* Adding a Rigid Body
* Apply an impulse


### cubemap

This one sets up a scene and saves a cube map snapshot of it a six images in industry standard format. This should later come in handy to precreate skyboxes.

Features demonstrated:
* Save a cube map


### FSM

This sets up a simple state machine that lets a sphere rotate clockwise, counterclockwise or not at all. Using the left and right cursor keys, you can switch between states.

Features demonstrated:
* Finite State Machine


### GUI

Okay, it *does* get a bit ridiculous here. All I did here was plaster a button on the screen. I guess the point here is mostly that DirectGUI widgets reparent themselves to aspect2d automagically, so... Keep in mind to manage your scene graph?

Features demonstrated:
* DirectGUI elements


### libRocket

A minimal libRocket GUI

Features demonstrated:
* Loading a font
* Setting up the Python-side of the GUI
* RML / RCSS


### lod

Level of detail. I created a model of a tree on tree different detail levels and you're allowed to laugh, but even for programmers art I did them quarter-assed. Anyways, your up and down cursor keys will move you towards and away from the tree, showing how the mesh gets exchanged automagically.

Features demonstrated:
* Level of Detail nodes


### offscreen\_filming

If you want to use Panda3D to render frames to image files on the disk
instead of a window on the screen, that is remarkably easy; Just combine
`window-type offscreen` with a window's `screenshot()` method. To turn
the outputted images into a video, you can use
`ffmpeg -framerate 30 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p out.mp4`.

Features demonstrated:
* Offscreen rendering
* Screenshots


### render\_to\_texture

You have a camera somewhere in your game world and a screen that shows what's on the camera? You want 2D displays showing something that's easier to model in 3D? Or you have any other purpose for having a Panda3D camera render into a texture? This is the example for you.

Features demonstrated:
* Set up a secondary scene graph, which will get rendered into textures.
* Create a butter, set its sort order.
* Create a camera and let it render into that buffer.
* Get a texture from the buffer and set it as a "monitors" texture.


### reprojection

Scene graph position to camera frustum position and back.

Features demonstrated:
* `Lens.project`
* `Lens.extrude_depth()`


### selfshadow

Features demonstrated:
* Set up a shadow-casting light.
* Make all objects in the scene graph receive shadows.


### shaders

Features demonstrated:
* Minimal shader pipeline
* Full shader pipeline


### skybox

I admit that this is a bit of a weird one. I've assembled an .egg file mostly by hand to tile a texture onto a cube, where the texture coords of each vertex is smack in the middle of the corner pixel of that sides tile, so that mipmapping should be avoided. The point is that with this, you can create high-quality skybox textures.

A bunch of spheres in the scene show that the skybox gets rendered "behind" objects in the scene, even though the box should be too small to contain the outer spheres.

Features demonstrated:
* Rendering objects as background


### filter

Features demonstrated:
* Post-processing effects with fragment shaders

This is mostly a copy-and-paste job of the Hello World application in Panda3D's manual, with a filter slapped on at the end. The FilterManager causes a scene to not be rendered directly to the scene, but instead to textures on a quad, which then does get fed back into fragment shading.


### buffer\_protocol

The buffer protocol is a Python feature that lets C extensions efficiently share memory. In the context on Panda3D, this is a viable way to share texture and vertex data with non-Panda3D modules.

Features demonstrated:
* (gizeh_to_panda3d.py) Creating images on a canvas backed by a numpy array (which is the standard way of storing images in Python), and copying it into a Panda3D texture. Requires Gizeh (a Python module for rendering vector graphics, akin to Cairo).


### boilerplate

This is code I find helpful when developing experiments with.
