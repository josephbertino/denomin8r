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
image1, image2 = util.load_images(latest=False)
# Get max dimensions for image1, image2, and mask
crop_size = util.get_crop_size([image1, image2], square=True)

# Randomly transform images
im1 = util.random_transform(image1, crop_size)
im2 = util.random_transform(image2, crop_size)

for kr in [.6, .7, .8, .9, 1.0]:
    text = 'PUSH'
    bitmask = util.build_mask_to_size(text=text, fontfile=util.BOOKMAN, shape=crop_size, kern_rate=kr)

    collage_A, collage_B = util.simple_mask_swap(im1, im2, bitmask)

    Image.fromarray(collage_A).show()