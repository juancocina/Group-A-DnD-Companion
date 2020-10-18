noise_scale = .012

def setup():
  size(1000, 1000)
  # brown background rgb
  background(0, 0, 0)
  
  # Set up x and y grid (2D perlin noise)
  for x in range(1000):
      for y in range(1000):
        n = noise(x * noise_scale, y * noise_scale)
        if (n > .45): # light green rgb
            stroke(135, 135, 135)
        if (n > .45):
            point(x,y)
