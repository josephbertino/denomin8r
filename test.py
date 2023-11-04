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
"""
random_id = uuid.uuid4().__str__().split('-')[0]
img = util.load_sources(latest=True, n=1, specific_srcs=['scholler_portrait_6'])
img = img[0]
spd = 9
dupn = 3
dupn_h = 5
dupn_v = 5
dup_img_grid = util.img_resample_grid(img, dupn_v, dupn_h, spd)
# TODO img_totem = util.img_totem_stack(dupn_h, spd)
dup_img_grid = util.draw_test_params(dup_img_grid, spd=spd)
dup_img_grid = util.draw_handle(dup_img_grid)
dup_img_grid.show()

# APHEX TWIN, JEFFREY EPSTEIN

# TODO I also like what happens when is unequal between rotation slicing. Produces cool effects with the rectangles, espec. when n1 is v. different from n2
# TODO later steps: do any combination of the following with those slices: rearrange them (reverse phasing), roll them (np.roll), flip them, (ADVANCED) swap them, (ADV.) rotate canvas and repeat
# TODO should I not call Image.fromarray() until I'm done with all the slicing?