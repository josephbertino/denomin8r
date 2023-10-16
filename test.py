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
# Off-crop an image... have a method simply off-crop an image from center
images = util.load_sources(latest=False, n=1)
img_orig = images[0]
img1 = img_orig.copy()
img2 = img_orig.copy()
CLEAN_COPY = util.get_bool()

# Collage off-cropped image with another off-crop of itself
times = random.choice(range(1,5))
for _ in range(times):
    # TODO util.crop_off_center doesn't crop, it just returns the cropbox
    img1 = util.crop_off_center(img1)
    img2 = util.crop_off_center(img2)
    # TODO util.get_crop_shape can take a list of images OR crop_boxes
    crop_shape = util.get_crop_shape([img1, img2], square=True)
    img1 = util.crop_central(img1, crop_shape)
    img2 = util.crop_central(img2, crop_shape)
    # TODO bitmask char can be random or specified
    bitmask = util.build_random_text_bitmask(fontfile=util.BOOKMAN, shape=crop_shape, numchars=1)
    img1, img2 = util.simple_bitmask_swap(img1, img2, bitmask)
    img1 = Image.fromarray(img1)
    if CLEAN_COPY:
        img2 = img_orig.copy()
    else:
        img2 = Image.fromarray(img2)

img1.show()
