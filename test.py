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
random_id = uuid.uuid4().__str__().split('-')[0]
for i, img in enumerate(util.load_sources(latest=False, n=10)):
    # Generate the slices, in order
    new_img = util.slice_image_reverse(img)
    new_img.save(f'{random_id}_slice_{i}.jpg')


# TODO later steps: do any combination of the following with those slices: rearrange them (phasing, reverse phasing), roll them (np.roll), flip them, (ADVANCED) swap them, (ADV.) rotate canvas and repeat

# looks like Image.transform() is a good place to start
# What I really want is an AFFINE transformation (shearing) where the spillover from one side is
# superimposed onto the other side, and to be able to do this in all 4 directions (LRUD)

# Use this link to help build a method: https://stackoverflow.com/a/4998741/1975297