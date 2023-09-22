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
# load both images
image1, = util.load_images(latest=False, n=1)
image2 = image1.copy()

# Determine size of image
w, h = image1.size
image_square_side = min(w, h)

JITTER = 0.05
CROP_CAP = 1 - JITTER

# slightly reduce image_shape to make crop_shape, so there is room for jitter
#  of the crop box
cropped_square_side = math.floor(image_square_side * CROP_CAP)
crop_shape = (cropped_square_side, cropped_square_side)

# determine origin point for image crops
crop_box_1 = util.get_crop_box_central(image1.size, crop_shape)
crop_box_2 = util.get_crop_box_central(image1.size, crop_shape)

print(JITTER)
print(image1.size, image_square_side)
print(crop_shape, cropped_square_side)
MAX_JITTER = image_square_side * JITTER / 2
jitter_w = util.ffloor(MAX_JITTER * random.uniform(-1, 1))
jitter_h = util.ffloor(MAX_JITTER * random.uniform(-1, 1))
print('-----')
print(MAX_JITTER)
print(jitter_w, jitter_h)

# apply jitter_w and jitter_h to each of image1 and image2 crop boxes. then crop
left1, top1, right1, bottom1 = crop_box_1
left1 += jitter_w
top1 += jitter_h
right1 += jitter_w
bottom1 += jitter_h
cb1 = (left1, top1, right1, bottom1)

jitter_w_2 = util.ffloor(MAX_JITTER * random.uniform(-1, 1))
jitter_h_2 = util.ffloor(MAX_JITTER * random.uniform(-1, 1))
left2, top2, right2, bottom2 = crop_box_2
left2 += jitter_w_2
top2 += jitter_h_2
right2 += jitter_w_2
bottom2 += jitter_h_2
cb2 = (left2, top2, right2, bottom2)

image1 = image1.crop(cb1)
image2 = image2.crop(cb2)


# What do I want to return exactly? The two slightly off-cropped images