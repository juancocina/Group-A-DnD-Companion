# Map Tool Gridder
# Places a grid over an existing image

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

try:
    from PIL import Image
except ImportError:
    import Image

image = Image.open('ForestMap.png')
my_dpi = 200

fig = plt.figure(figsize=(float(image.size[0]) / my_dpi, float(image.size[1]) / my_dpi), dpi=my_dpi)
ax = fig.add_subplot(111)

fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

myInterval = 133
loc = plticker.MultipleLocator(base=myInterval)
ax.xaxis.set_major_locator(loc)
ax.yaxis.set_major_locator(loc)

ax.grid(which='major', axis='both', linestyle='-', color='w')

ax.imshow(image)

fig.savefig('ForestMapGrid.png', dpi=my_dpi)
