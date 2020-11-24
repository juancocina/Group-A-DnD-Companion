# KNOWN BUG: Matplotlib has bugs concerning colors, especially with the grayscale:
# Colors may change based on other colors generated (i.e. gray may appear white if only black is present)
# Searched fixes include converting with the PIL library


import noise
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image
from scipy.misc import imsave

shape = (800, 800)
scale = 300         # higher zoomed in factor = higher number
octaves = 5         # number of times the program layers (adds more detail for every layer but also higher run time)
persistence = 0.5   # amplitude that each octave contributes to overall shape
lacunarity = 2    # frequency of detail at each octave
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

black = [0, 0, 0]
lava = [181, 51, 7]
white = [255, 250, 250]
gray = [92, 92, 92]
water = [40, 50, 120]


def add_color(world):
    color_world = np.zeros(world.shape + (3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -0.05:
                color_world[i][j] = black
            elif world[i][j] < .37:
                color_world[i][j] = gray
            elif world[i][j] < 1:
                color_world[i][j] = lava

    return color_world


color_world = add_color(world)
imsave('cave.png', color_world)

background = Image.open('cave.png')
my_dpi = 200  # set screen dots per inch

grid = plt.figure(figsize=(float(background.size[0]) / my_dpi, float(background.size[1]) / my_dpi), dpi=my_dpi)
ax = grid.add_subplot(111)

grid.subplots_adjust(left=0, right=1, bottom=0, top=1)

myInterval = 50 # each grid plot will be 100x100
a = plticker.MultipleLocator(base=myInterval)
ax.xaxis.set_major_locator(a)
ax.yaxis.set_major_locator(a)

ax.grid(which='major', axis='both', linestyle='-', color='white', linewidth=1)

ax.imshow(background)

grid.savefig('cave_grid.png', dpi=my_dpi)

im = Image.open('cave_grid.png')
im.show()
