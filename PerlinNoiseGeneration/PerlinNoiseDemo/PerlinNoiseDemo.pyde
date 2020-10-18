noise_scale = .008

def setup():
  size(1000, 1000)
  # blue background rgb
  background(43, 89, 249)
  
  # Set up x and y grid (2D perlin noise)
  for x in range(1000):
      for y in range(1000):
        n = noise(x * noise_scale, y * noise_scale)
        if (n > .55): # tan
            stroke(229, 223, 171)
        if (n > .58): # dark green
            stroke(28, 95, 12)
        if (n > .8): # grey
            stroke(161, 161, 161)
        if (n > .55):
            point(x,y)
