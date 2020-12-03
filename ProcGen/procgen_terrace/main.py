import noise
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image
from scipy.misc import imsave

shape = (800, 800)
scale = 500         # higher zoomed in factor = higher number
octaves = 4         # number of layers
persistence = .5    # amplitude that each octave contributes to overall shape
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

light_green = [0, 255, 27]
green = [0, 227, 24]
dark_green = [0, 194, 20]
darker_green = [2, 156, 17]
darkerer_green = [1, 143, 15]
darkest_green = [0, 122, 12]
spring = [3, 252, 240]
dirt = [133, 104, 66]
tan = [176, 149, 113]
river = [138, 255, 237]


def add_color(world):
    color_world = np.zeros(world.shape + (3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -.30:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = spring
                else:
                    color_world[i][j] = dark_green
            elif world[i][j] < -.28:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dirt
                else:
                    color_world[i][j] = tan
            elif world[i][j] < -.22:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = spring
                else:
                    color_world[i][j] = green
            elif world[i][j] < -.2:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dirt
                else:
                    color_world[i][j] = tan
            elif world[i][j] < -.14:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = spring
                else:
                    color_world[i][j] = light_green
            elif world[i][j] < -.12:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dirt
                else:
                    color_world[i][j] = tan
            elif world[i][j] < -.07:
                color_world[i][j] = river
            elif world[i][j] < -.05:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dirt
                else:
                    color_world[i][j] = tan
            elif world[i][j] < .01:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = spring
                else:
                    color_world[i][j] = light_green
            elif world[i][j] < .03:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dirt
                else:
                    color_world[i][j] = tan
            elif world[i][j] < .09:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = spring
                else:
                    color_world[i][j] = green
            elif world[i][j] < .11:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dirt
                else:
                    color_world[i][j] = tan
            elif world[i][j] < .17:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = spring
                else:
                    color_world[i][j] = dark_green
            elif world[i][j] < .19:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dirt
                else:
                    color_world[i][j] = tan
            elif world[i][j] < .25:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = spring
                else:
                    color_world[i][j] = darker_green
            elif world[i][j] < .27:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dirt
                else:
                    color_world[i][j] = tan
            elif world[i][j] < .33:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = spring
                else:
                    color_world[i][j] = darkerer_green
            elif world[i][j] < .35:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dirt
                else:
                    color_world[i][j] = tan
            elif world[i][j] <= 1:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = spring
                else:
                    color_world[i][j] = darkest_green
    return color_world


color_world = add_color(world)
imsave('terrace.png', color_world)

background = Image.open('terrace.png')
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

grid.savefig('terrace_grid.png', dpi=my_dpi)

im = Image.open('terrace_grid.png')
im.show()
