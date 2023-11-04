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
"""
take image
turn it into np array
slice it up vertically
rotate it
slice it up vertically
rotate it back
turn it into image array
"""
# TODO methods for slicing vertical and horizontal
# TODO keep track of angling so that it ends up right side up
# TODO stacking heads like totems
random_id = uuid.uuid4().__str__().split('-')[0]
img = util.load_sources(latest=True, n=1, specific_srcs=['scholler_portrait_2'])
img = img[0]
spd = 22
for dupn in range(2,5):
    slicen = spd * dupn
    dupimg = img.rotate(90, expand=True)
    dupimg = util.slice_image_duplicate_sampling(dupimg, dupn, slicen)
    dupimg = dupimg.rotate(270, expand=True)
    dupimg = util.draw_test_params(dupimg, spd=spd, dupn=dupn, slicen=slicen)
    dupimg = util.draw_handle(dupimg)
    dupimg.show()

# TODO I also like what happens when is unequal between rotation slicing. Produces cool effects with the rectangles, espec. when n1 is v. different from n2
# TODO later steps: do any combination of the following with those slices: rearrange them (reverse phasing), roll them (np.roll), flip them, (ADVANCED) swap them, (ADV.) rotate canvas and repeat

# TODO should I not call Image.fromarray() until I'm done with all the slicing?