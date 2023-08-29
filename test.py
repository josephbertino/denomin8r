import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import util

fontfile = os.path.join(util.FONT_DIR, 'bookman.ttf')

word = "PUSH"
fg = "#000000"  # black foreground
bg = "#FFFFFF"  # white background
MAX_PADDING = 4
SIZE = 200

# Create a Font object from the .ttf
font = ImageFont.truetype(fontfile, SIZE)
# Determine the width and length of the word at the given size
_, _, text_width, text_height = font.getbbox(word)
# Create a new Image, which will serve as the canvas for drawing the image
image = Image.new(mode='RGB', size=(text_width + MAX_PADDING*2, text_height + MAX_PADDING*2), color=bg)
# Create a 'Drawing Pad' which will draw text to your image canvas
draw_pad = ImageDraw.Draw(image)
# Draw text to your image canvas
draw_pad.text((MAX_PADDING-4, MAX_PADDING-10), word, font=font, fill=fg, features={"kern": 0.6})

''' Give credit to https://gist.github.com/bornfree and his image_using_font.py '''
image.show()

# file_name = "output.png"
#
# mask = font.getmask("D")
# mask_arr = np.asarray(mask)
# image = Image.fromarray(mask_arr)
# image.show()

# Use a TrueType font
# mask_np = np.array(d)
# mask_np.resize(d.size)
# mask_np[mask_np > 255] = 1
# mask = Image.fromarray(mask_np, mode='L')
# composite = Image.alpha_composite(image1, mask)
# draw = ImageDraw.Draw(image1)
# draw.text((0, 0), "D", font=font)