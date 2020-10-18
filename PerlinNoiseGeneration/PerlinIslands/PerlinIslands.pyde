noise_scale = .012

def setup():
  size(1000, 1000)
  # brown background rgb
  background(100, 66, 13)
  
  # Set up x and y grid (2D perlin noise)
  for x in range(1000):
      for y in range(1000):
        n = noise(x * noise_scale, y * noise_scale)
        if (n > .4): # light green rgb
            stroke(86, 146, 84)
        if (n > .48): # dark green
            stroke(28, 95, 12)
        if (n > .7): # grey
            stroke(161, 161, 161)
        if (n > .3):
            point(x,y)
