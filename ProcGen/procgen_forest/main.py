import noise
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image
from scipy.misc import imsave

shape = (800, 800)
scale = 300         # higher zoomed in factor = higher number
octaves = 6         # number of layers
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

dirt = [66, 36, 0]
dark_brown = [56, 33, 0]
green = [14, 117, 0]
dark_green = [7, 56, 0]
super_green = [0, 48, 11]
gray = [46, 46, 46]
black = [0, 0, 0]


def add_color(world):
    color_world = np.zeros(world.shape + (3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -0.2:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = super_green
                elif random_int == 1:
                    color_world[i][j] = dark_green
            elif world[i][j] < -.1:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dark_green
                elif random_int == 1:
                    color_world[i][j] = green
            elif world[i][j] < -.05:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dirt
                elif random_int == 1:
                    color_world[i][j] = dark_brown
            elif world[i][j] < 0:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = gray
                elif random_int == 1:
                    color_world[i][j] = black
            elif world[i][j] < .05:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dirt
                elif random_int == 1:
                    color_world[i][j] = dark_brown
            elif world[i][j] < .15:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dark_green
                elif random_int == 1:
                    color_world[i][j] = green
            elif world[i][j] < 1:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = super_green
                elif random_int == 1:
                    color_world[i][j] = dark_green

    return color_world


color_world = add_color(world)
imsave('forest.png', color_world)

background = Image.open('forest.png')
my_dpi = 200  # set screen dots per inch

grid = plt.figure(figsize=(float(background.size[0]) / my_dpi, float(background.size[1]) / my_dpi), dpi=my_dpi)
ax = grid.add_subplot(111)

grid.subplots_adjust(left=0, right=1, bottom=0, top=1)

myInterval = 50 # each grid plot will be 100x100
a = plticker.MultipleLocator(base=myInterval)
ax.xaxis.set_major_locator(a)
ax.yaxis.set_major_locator(a)

ax.grid(which='major', axis='both', linestyle='-', color='black', linewidth=1)

ax.imshow(background)

grid.savefig('forest_grid.png', dpi=my_dpi)

im = Image.open('forest_grid.png')
im.show()
