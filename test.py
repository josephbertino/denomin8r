import enum
import math
import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import util
import uuid
import string
import random
import string
import PySimpleGUI as sg
import inspect

util.prep()
fontfile = util.BOOKMAN
kern_rate = 1.0
foreground_color = 'darkgoldenrod'  # 0xb8860b
background_color = 'royalblue'  # 0x4169e1
background_comp = 0xb83d0b  # BGR!   RGB would be 0x0b3db8
og_foreground = 0xC86428
og_background = 0x2864C8

# -----DO NOT DELETE ABOVE THIS LINE---------------------------
TEXT = "@ denomin8r"
for num in range(1,4):
    img = Image.open(f'D{num}.jpg')
    w, h = img.size
    position = (math.floor(.72 * w),math.floor(.93 * h))
    fontsize = math.floor(h * .04)
    font_obj = ImageFont.truetype(fontfile, fontsize)

    draw = ImageDraw.Draw(img)

    left, top, right, bottom = draw.textbbox(position, TEXT, font=font_obj)
    extra = math.ceil((bottom - top) * 0.1)
    diameter = bottom + extra - top + extra
    draw.rectangle(((left - extra, top - extra), (right - (diameter//2) + (extra*2), bottom+extra)), fill=og_foreground)
    draw.ellipse(((left - extra - (diameter // 2), top - extra),(left - extra + (diameter // 2), bottom + extra)), fill=background_comp)
    draw.text((position[0] - (diameter // 2), position[1]), TEXT, font=font_obj, fill=foreground_color)

    # draw.text(position, "@denomin8r", fill='darkgoldenrod', background='black', font=font_obj)

    img.show()