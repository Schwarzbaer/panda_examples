import numpy as np
from panda3d.core import PTAUchar, Texture, LVecBase4f

                    # numpy  Panda3D (without transpose)
a = [0, 1, 2]       #  0,0     0,0
b = [3, 4, 5]       #  0,1     1,0
c = [6, 7, 8]       #  0,2     0,1
d = [9, 10, 11]     #  1,0     1,1
e = [12, 13, 14]    #  1,1     0,2
f = [15, 16, 17]    #  1,2     1,2

a_np = np.array([[a, b, c],
                 [d, e, f]],
                dtype=np.uint8)

# When accessed through the buffer protocol, ndarrays are (apparently)
# linearized in reverse order of axes. So as we have an [x, y, c] array here,
# the data will be linearized in the order seen above, monotonically ascending.
# This can be seen if you PTAUchar(a_np).get_subdata(0, 18). First all c-columns
# in x=0 get written in order of y, then all in x=1.
# However, Texture.set_ram_image will delinearize the data slightly different.
# c-column order can be manipulated with an additional argument to
# set_ram_image_as, but x/y-wise, it will first write along the x-axis in y=0,
# then y=1 and so on.
# So to preserve x/y coordinate equality between numpy and Panda3D, the array
# first has to be transposed, swapping its x and y axes. That in turn seems to
# somehow "dirty" the returned array, making it necessary to copy it first.
# So basically you have the choice between one additional copy of the whole
# array that you're transferring, or you think of numpy arrays as [y, x, c]
# images.

a_np_t = a_np.transpose(1, 0, 2).copy()
a_p3d = PTAUchar(a_np_t)

tex = Texture()
# Note that if the Texture's dimentions and component type don't match that of
# your numpy array, you're gonna have a bad time.
tex.setup_2d_texture (2, 3, Texture.T_unsigned_byte, Texture.F_rgb)
tex.set_ram_image_as(a_p3d, 'RGB')

# Now let's see the data that we've just moved around.
p = LVecBase4f()
for x in range(2):
    for y in range(3):
        tex.peek().fetch_pixel(p, x, y); print(x,y,p*256, a_np[x,y])

