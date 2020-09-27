# Map Tool Gridder
# Places a grid over an existing image

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

try:
    from PIL import Image
except ImportError:
    import Image

background = Image.open('ForestMap.png')
my_dpi = 200

grid = plt.figure(figsize=(float(background.size[0]) / my_dpi, float(background.size[1]) / my_dpi), dpi=my_dpi)
ax = grid.add_subplot(111)

grid.subplots_adjust(left=0, right=1, bottom=0, top=1)

myInterval = 133
a = plticker.MultipleLocator(base=myInterval)
ax.xaxis.set_major_locator(a)
ax.yaxis.set_major_locator(a)

ax.grid(which='major', axis='both', linestyle='-', color='w')

ax.imshow(background)

grid.savefig('ForestMapGrid.png', dpi=my_dpi)
