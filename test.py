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
GOAL:
Use numpy to create slices of an image, vertically or horizontally
"""
# TODO experiment with dupn and n
random_id = uuid.uuid4().__str__().split('-')[0]
for i, img in enumerate(util.load_sources(latest=False, n=10)):
    slice_n = 2 ** random.choice(range(4, 7))
    dup_n = random.choice([2, 3, 4])
    slices = util.slice_up_image_uniform(img, slice_n)
    stack = []
    print(f"{slice_n=}, {dup_n=}")
    for i in range(dup_n):
        stack.extend(slices[i::dup_n])
    slice_stack = np.hstack(stack)
    newimg = Image.fromarray(slice_stack)
    newimg.show()

# TODO I also like what happens when is unequal between rotation slicing. Produces cool effects with the rectangles, espec. when n1 is v. different from n2
# TODO later steps: do any combination of the following with those slices: rearrange them (reverse phasing), roll them (np.roll), flip them, (ADVANCED) swap them, (ADV.) rotate canvas and repeat

# TODO should I not call Image.fromarray() until I'm done with all the slicing?