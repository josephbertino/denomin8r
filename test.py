import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import util

text = "PUSH"
fg = "#000000"  # black foreground
bg = "#FFFFFF"  # white background
MAX_PADDING = 18
SIZE = 200
fontfile = os.path.join(util.FONT_DIR, 'bookman.ttf')
font = ImageFont.truetype(fontfile, SIZE)

for x in range(92,105,2):
    rate = x / 100
    image = util.image_from_text(text, SIZE, rate)
    image.show()
