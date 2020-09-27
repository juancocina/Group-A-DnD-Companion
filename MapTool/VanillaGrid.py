# Map Tool Gridder
# Places a grid over an existing image

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

try:
    from PIL import Image
except ImportError:
    import Image

# Open image file
image = Image.open('ForestMap.png')
my_dpi = 200

# Set up figure
fig = plt.figure(figsize=(float(image.size[0]) / my_dpi, float(image.size[1]) / my_dpi), dpi=my_dpi)
ax = fig.add_subplot(111)

# Remove whitespace from around the image
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

# Set the gridding interval using major tick
myInterval = 133
loc = plticker.MultipleLocator(base=myInterval)
ax.xaxis.set_major_locator(loc)
ax.yaxis.set_major_locator(loc)

# Add the grid
ax.grid(which='major', axis='both', linestyle='-', color='w')

# Add the image underneath grid
ax.imshow(image)

# Save and create as new image, keeping integrity of old image
fig.savefig('ForestMapGrid.png', dpi=my_dpi)
