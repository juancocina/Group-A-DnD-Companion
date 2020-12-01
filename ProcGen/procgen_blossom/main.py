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

green = [0, 255, 27]
pink = [255, 166, 233]
light_pink = [252, 215, 247]
light_yellow = [252, 247, 215]
river = [138, 255, 237]


def add_color(world):
    color_world = np.zeros(world.shape + (3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -0.2:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = pink
                elif random_int == 1:
                    color_world[i][j] = light_pink
            elif world[i][j] < -.1:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = light_pink
                elif random_int == 1:
                    color_world[i][j] = light_yellow
            elif world[i][j] < -.05:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = light_yellow
                elif random_int == 1:
                    color_world[i][j] = green
            elif world[i][j] < 0:
                color_world[i][j] = river
            elif world[i][j] < .05:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = light_yellow
                elif random_int == 1:
                    color_world[i][j] = green
            elif world[i][j] < .15:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = light_pink
                elif random_int == 1:
                    color_world[i][j] = light_yellow
            elif world[i][j] < 1:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = pink
                elif random_int == 1:
                    color_world[i][j] = light_pink

    return color_world


color_world = add_color(world)
imsave('blossom.png', color_world)

background = Image.open('blossom.png')
my_dpi = 100  # set screen dots per inch

grid = plt.figure(figsize=(float(background.size[0]) / my_dpi, float(background.size[1]) / my_dpi), dpi=my_dpi)
ax = grid.add_subplot(111)

grid.subplots_adjust(left=0, right=1, bottom=0, top=1)

myInterval = 50 # each grid plot will be myInterval by myInterval

a = plticker.MultipleLocator(base=myInterval)
ax.xaxis.set_major_locator(a)
ax.yaxis.set_major_locator(a)

ax.grid(which='major', axis='both', linestyle='-', color='black', linewidth=1)

ax.imshow(background)

grid.savefig('blossom_grid.png', dpi=my_dpi)

im = Image.open('blossom_grid.png')
im.show()
