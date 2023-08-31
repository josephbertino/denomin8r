import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import util

word = "PUSH"
fg = "#000000"  # black foreground
bg = "#FFFFFF"  # white background
MAX_PADDING = 18
SIZE = 200
fontfile = os.path.join(util.FONT_DIR, 'bookman.ttf')

''' Give credit to https://gist.github.com/bornfree and his image_using_font.py
 for the skeleton of drawing text to an image'''
# Create a Font object from the .ttf
font = ImageFont.truetype(fontfile, SIZE)
# Determine the width and length of the word at the given size
left_offset, top_offset, right, bottom = font.getbbox(word)
print(left_offset, top_offset, right, bottom)
text_width = right - left_offset
text_height = bottom - top_offset
# Create a new Image, which will serve as the canvas for drawing the image
image = Image.new(mode='RGB', size=(544 + MAX_PADDING*2, text_height + MAX_PADDING*2), color=bg)
# Create a 'Drawing Pad' which will draw text to your image canvas
draw = ImageDraw.Draw(image)

# Draw text to your image canvas
if False:
    draw.text((MAX_PADDING - 2, MAX_PADDING - top_offset), word, font=font, fill=fg)

'''https://stackoverflow.com/a/63182161/1975297  Steven Woerpel
    Credit for writing my own method to kern text'''
desired_width_of_text = int(0.85 * text_width)
width_difference = text_width - desired_width_of_text
gap_width = int(width_difference / (len(word) - 1))  # width between each character
xpos = MAX_PADDING - 2
calc_word_width = 0
for letter in word:
    draw.text((xpos,MAX_PADDING - top_offset),letter, (0,0,0), font=font)
    left, top, letter_width, letter_height = draw.textbbox((0,0), letter, font=font)
    xpos += letter_width - 8
    calc_word_width += letter_width - 8
print(calc_word_width)

image.show()
