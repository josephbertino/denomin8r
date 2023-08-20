# PIL Image object methods

## On Image modes
+ https://pillow.readthedocs.io/en/latest/handbook/concepts.html#modes
+ The mode of an image describes the type and depth of each pixel in an image.
+ '1' == (1-bit pixels, black and white, stored with one pixel per byte)
+ 'RGB' == (3x8-bit pixels, true color)
  + An 'RBG' image's pixel is simple a 3-tuple (representing R, G, B)

## Gotchas
+ Keep in mind: Image.crop() takes a 4-tuple (x1, y1, x2, y2), but 