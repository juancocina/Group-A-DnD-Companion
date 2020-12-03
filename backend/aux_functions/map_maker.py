import sqlite3
import noise
import imageio
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from ast import literal_eval as make_tuple
from PIL import Image

CAMPAIGN_DATABASE = '../database/db/DnDEZ_Campaigns.db'

seed = np.random.randint(0,100)


class map_config:
    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])


def make_world(shape, scale, octaves, persistence, lacunarity): 
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
    
    return world

def color_forest(world, dict, shape, path):
    color_world = np.zeros(world.shape + (3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -0.2:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['super_green']
                elif random_int == 1:
                    color_world[i][j] = dict['dark_green']
            elif world[i][j] < -.1:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['dark_green']
                elif random_int == 1:
                    color_world[i][j] = dict['green']
            elif world[i][j] < -.05:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['dirt']
                elif random_int == 1:
                    color_world[i][j] = dict['dark_brown']
            elif world[i][j] < 0:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['gray']
                elif random_int == 1:
                    color_world[i][j] = dict['black']
            elif world[i][j] < .05:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['dirt']
                elif random_int == 1:
                    color_world[i][j] = dict['dark_brown']
            elif world[i][j] < .15:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['dark_green']
                elif random_int == 1:
                    color_world[i][j] = dict['green']
            elif world[i][j] < 1:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['super_green']
                elif random_int == 1:
                    color_world[i][j] = dict['dark_green']
    imageio.imwrite(path, color_world)

def color_islands(world, dict, shape, path):
    color_world = np.zeros(world.shape + (3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -0.05:
                color_world[i][j] = dict['blue']
            elif world[i][j] < 0:
                color_world[i][j] = dict['beach']
            elif world[i][j] < .20:
                color_world[i][j] = dict['green']
            elif world[i][j] < 0.35:
                color_world[i][j] = dict['mountain']
            elif world[i][j] < 1.0:
                color_world[i][j] = dict['snow']

    imageio.imwrite(path, color_world)

def color_desert(world, dict ,shape, path):
    color_world = np.zeros(world.shape + (3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -0.25:
                color_world[i][j] = dict['sandstone']
            elif world[i][j] < -.05:
                color_world[i][j] = dict['sand']
            elif world[i][j] < .15:
                color_world[i][j] = dict['sandstone']
            elif world[i][j] < .2:
                color_world[i][j] = dict['green']
            elif world[i][j] < 1.0:
                color_world[i][j] = dict['water']

    imageio.imwrite(path, color_world)

def color_caves(world, dict, shape, path):
    color_world = np.zeros(world.shape + (3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -0.05:
                color_world[i][j] = dict['black']
            elif world[i][j] < .37:
                color_world[i][j] = dict['gray']
            elif world[i][j] < 1:
                color_world[i][j] = dict['lava']

    imageio.imwrite(path, color_world)

def color_blossom(world, dict, shape, path):
    color_world = np.zeros(world.shape + (3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -0.2:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['pink']
                elif random_int == 1:
                    color_world[i][j] = dict['light_pink']
            elif world[i][j] < -.1:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['light_pink']
                elif random_int == 1:
                    color_world[i][j] = dict['light_yellow']
            elif world[i][j] < -.05:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['light_yellow']
                elif random_int == 1:
                    color_world[i][j] = dict['green']
            elif world[i][j] < 0:
                color_world[i][j] = dict['river']
            elif world[i][j] < .05:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['light_yellow']
                elif random_int == 1:
                    color_world[i][j] = dict['green']
            elif world[i][j] < .15:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['light_pink']
                elif random_int == 1:
                    color_world[i][j] = dict['light_yellow']
            elif world[i][j] < 1:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['pink']
                elif random_int == 1:
                    color_world[i][j] = dict['light_pink']

    imageio.imwrite(path, color_world)


def color_terrace(world, dict, shape, path):
    color_world = np.zeros(world.shape + (3,))
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -.30:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = dict['spring']
                else:
                    color_world[i][j] = dict['dark_green']
            elif world[i][j] < -.28:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['dirt']
                else:
                    color_world[i][j] = dict['tan']
            elif world[i][j] < -.22:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = dict['spring']
                else:
                    color_world[i][j] = dict['green']
            elif world[i][j] < -.2:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['dirt']
                else:
                    color_world[i][j] = dict['tan']
            elif world[i][j] < -.14:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = dict['spring']
                else:
                    color_world[i][j] = dict['light_green']
            elif world[i][j] < -.12:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['dirt']
                else:
                    color_world[i][j] = dict['tan']
            elif world[i][j] < -.07:
                color_world[i][j] = dict['river']
            elif world[i][j] < -.05:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['dirt']
                else:
                    color_world[i][j] = dict['tan']
            elif world[i][j] < .01:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = dict['spring']
                else:
                    color_world[i][j] = dict['light_green']
            elif world[i][j] < .03:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['dirt']
                else:
                    color_world[i][j] = dict['tan']
            elif world[i][j] < .09:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = dict['spring']
                else:
                    color_world[i][j] = dict['green']
            elif world[i][j] < .11:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['dirt']
                else:
                    color_world[i][j] = dict['tan']
            elif world[i][j] < .17:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = dict['spring']
                else:
                    color_world[i][j] = dict['dark_green']
            elif world[i][j] < .19:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['dirt']
                else:
                    color_world[i][j] = dict['tan']
            elif world[i][j] < .25:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = dict['spring']
                else:
                    color_world[i][j] = dict['darker_green']
            elif world[i][j] < .27:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['dirt']
                else:
                    color_world[i][j] = dict['tan']
            elif world[i][j] < .33:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = dict['spring']
                else:
                    color_world[i][j] = dict['darkerer_green']
            elif world[i][j] < .35:
                random_int = random.randint(0, 1)
                if random_int == 0:
                    color_world[i][j] = dict['dirt']
                else:
                    color_world[i][j] = dict['tan']
            elif world[i][j] <= 1:
                random_int = random.randint(0, 2)
                if random_int == 0:
                    color_world[i][j] = dict['spring']
                else:
                    color_world[i][j] = dict['darkest_green']
    imageio.imwrite(path, color_world)


def add_grid(filepath, environment):
    background = imageio.imread(filepath)
    my_dpi = 200  # set screen dots per inch

    grid = plt.figure(figsize=(float(background.shape[0]) / my_dpi, float(background.shape[1]) / my_dpi), dpi=my_dpi)
    ax = grid.add_subplot(111)

    grid.subplots_adjust(left=0, right=1, bottom=0, top=1)

    myInterval = 50 # each grid plot will be 100x100
    a = plticker.MultipleLocator(base=myInterval)
    ax.xaxis.set_major_locator(a)
    ax.yaxis.set_major_locator(a)

    if environment == 'caves':
        ax.grid(which='major', axis='both', linestyle='-', color='white', linewidth=1)
    else:
        ax.grid(which='major', axis='both', linestyle='-', color='black', linewidth=1)


    ax.imshow(background)

    grid.savefig(filepath, dpi= my_dpi)

def save_grid(name, description, id, filename):

    conn = sqlite3.connect(CAMPAIGN_DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO maps (map_name, map_description, map_path, campaign_id) VALUES (?,?,?,?)", (name, description, filename, id))
    conn.commit()
    c.close()
    conn.close()
