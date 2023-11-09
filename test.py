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

"""
Observations:
Vertical Slicing
    dup_n:
        from 2 up to ~7 gives good results, with it getting creepier the higher you go. 
        I wouldn't go more than 7 for my intended aesthetic.
    slice_per_dup:
        Above 8 starts to resemble a face
        Once dupn goes above 3, I think >20 slices per dupe look good
    I really love how creepy it is to make many thin tall slices of faces
Horizontal Slicing
    dupn:
        3 or 4 seems great. Like totems
    slice_per_dup:
        Needs to be larger, like >12
Grid:
    I like what happens when dup_n is unequal between rotation slicing. 
    Produces cool effects with the rectangles.
"""
random_id = uuid.uuid4().__str__().split('-')[0]
img = util.load_sources(latest=False, n=1, specific_srcs=['lewitt1'])
img = img[0]

for dupv in range(2, 6):
    for duph in range(2, 6):
        dup = util.img_resample_grid(img, dupv, duph, 18)
        dup = util.draw_handle(dup)
        dup.show()
