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

# -----DO NOT DELETE ABOVE THIS LINE---------------------------
TEXT = "@ denomin8r"
for x in range(1,4):
    img = Image.open(f'./stickers/set 1 - 20231010/D{x}.jpg')
    w, h = img.size

    draw = ImageDraw.Draw(img)

    position = (math.floor(.78 * w),math.floor(.94 * h))
    fontsize = math.floor(h * .03)
    font_obj = ImageFont.truetype(fontfile, fontsize)

    at_left, _, at_right, _ = draw.textbbox(position, "@", font=font_obj)
    left, top, right, bottom = draw.textbbox(position, TEXT, font=font_obj)
    extra = math.ceil((bottom - top) * 0.1)
    diameter = bottom + extra - top + extra

    draw.ellipse(
        ((left - extra - (diameter // 2), top - extra),(left - extra + (diameter // 2), bottom + extra)),
        fill=util.RGB2BGR(util.COLORS.OG_ORANGE)
    )
    draw.rectangle(
        ((left - extra, top - extra), (right - (diameter//2) + extra, bottom+extra)),
        fill=util.RGB2BGR(util.COLORS.OG_ORANGE)
    )
    draw.text((position[0] - (diameter // 2), position[1]), "@", font=font_obj, fill="black")
    draw.text((position[0] + extra + (at_right - at_left) - (diameter // 2), position[1] + extra), "denomin8r", font=font_obj, fill="white")

    img.show()