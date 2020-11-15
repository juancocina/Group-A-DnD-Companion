import noise
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image
from scipy.misc import imsave

shape = (800, 800)
scale = 300         # higher zoomed in factor = higher number
octaves = 7         # number of layers
persistence = 0.5   # amplitude that each octave contributes to overall shape
lacunarity = 2.0    # frequency of detail at each octave
seed = np.random.randint(0, 100)

world = np.zeros(shape)
for i in range(shape[0]):
    for j in range(shape[1]):
        world[i][j] = noise.pnoise2(i / scale,
                                    j / scale,
                                    octaves=octaves,
                                    persistence=persistence,
                                    lacunarity=lacunarity,
                                    repeatx=1024,
                                    repeaty=1024,
                                    base=seed)

sand = [255, 240, 194]
sandstone = [204, 192, 157]
green = [120, 143, 86]
water = [91, 176, 199]



def add_color(world):
    color_world = np.zeros(world.shape + (3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -0.25:
                color_world[i][j] = sandstone
            elif world[i][j] < -.05:
                color_world[i][j] = sand
            elif world[i][j] < .15:
                color_world[i][j] = sandstone
            elif world[i][j] < .2:
                color_world[i][j] = green
            elif world[i][j] < 1.0:
                color_world[i][j] = water

    return color_world


color_world = add_color(world)
imsave('desert.png', color_world)

background = Image.open('desert.png')
my_dpi = 200  # set screen dots per inch

grid = plt.figure(figsize=(float(background.size[0]) / my_dpi, float(background.size[1]) / my_dpi), dpi=my_dpi)
ax = grid.add_subplot(111)

grid.subplots_adjust(left=0, right=1, bottom=0, top=1)

myInterval = 50 # each grid plot will be 50x50
a = plticker.MultipleLocator(base=myInterval)
ax.xaxis.set_major_locator(a)
ax.yaxis.set_major_locator(a)

ax.grid(which='major', axis='both', linestyle='-', color='black')

ax.imshow(background)

grid.savefig('desert_grid.png', dpi=my_dpi)

im = Image.open('desert_grid.png')
im.show()
