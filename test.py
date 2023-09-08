import math
import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import util
import uuid

util.prep()
fontfile = util.BOOKMAN
kern_rate = 1.0

image1, image2 = util.load_images(latest=False)
# Get max dimensions for image1, image2, and mask
crop_size = util.get_crop_size([image1, image2], square=True)

# Randomly transform an image
im1 = util.random_transform(image1, crop_size)
im2 = util.random_transform(image2, crop_size)

bitmask = util.build_mask_to_size(text='NADIA', fontfile=fontfile, shape=crop_size, kern_rate=1.0)
collage_A, collage_B = util.simple_mask_swap(im1, im2, bitmask)
random_id = uuid.uuid4().__str__().split('-')[0]

Image.fromarray(collage_A).show()
Image.fromarray(collage_B).show()
