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
# TODO rearrange_phase (will require num_slices to be >= 2**4
random_id = uuid.uuid4().__str__().split('-')[0]
for i, img in enumerate(util.load_sources(latest=True, n=10)):
    n = 2 ** random.choice(range(1,5))
    # Generate the slices, in order
    img = util.crop_to_square(img)
    img = util.slice_image_rearrange_phase(img, n, num_phases)
    img = img.rotate(angle=90, expand=True)
    # img = util.slice_image_rearrange_random(img, n)
    # img = img.rotate(angle=270, expand=True)
    img.save(f'{random_id}_slice_{i}.jpg')


# TODO later steps: do any combination of the following with those slices: rearrange them (phasing, reverse phasing), roll them (np.roll), flip them, (ADVANCED) swap them, (ADV.) rotate canvas and repeat

# TODO should I not call Image.fromarray() until I'm done with all the slicing?