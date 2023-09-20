import math
import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import util
import uuid
import string
import random

util.prep()
fontfile = util.BOOKMAN
kern_rate = 1.0

# -----DO NOT DELETE ABOVE THIS LINE---------------------------
'''
determine a random "jitter" for cropping an image according to shape. don't just crop it directly on the center... jitter the box around a bit
have a method where image1 and image2 are the same source, just cropped slightly differently
'''
JITTER_PERCENT = 0.05
CROP_CAP = 1 - JITTER_PERCENT
# load both images
image1, = util.load_images(latest=False, n=1)
image2 = image1.copy()
# Determine size of image
im1w, im1h = image1.size
# slightly reduce desired image size so there is room for jitter (from 0--5%)
redw = math.floor(im1w * CROP_CAP)
redh = math.floor(im1h * CROP_CAP)

# get crop width and height
cropw = croph = min(redw, redh)
crop_shape = (cropw, croph)
# determine origin point for image crops
crop_box_1 = util.get_crop_box_central(image1.size, crop_shape)
crop_box_2 = util.get_crop_box_central(image1.size, crop_shape)

print(image1.size)
print(crop_shape)
jitter_w = math.floor(random.uniform(-1,1) * JITTER_PERCENT/2 * crop_shape[0])
jitter_h = math.floor(random.uniform(-1,1) * JITTER_PERCENT/2 * crop_shape[0])
print(jitter_w, jitter_h)

# apply jitter_w and jitter_h to each of image1 and image2 crop boxes. then crop
