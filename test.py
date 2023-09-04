import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import util
import uuid

""" 
TODO expand the auto-generated bitmask by fitting it to the cropped size of the source images. 
Probably the most important thing is determining the SIZE of the font before you type it out, 
and consider the length of the text. Resize/Expand a font image to fit the source images, 
before turning it into a bitmask

Resize the sources to be the same size
Square them up
^ all done already

Determine the height of the text based on the dimensions of the squared source image
Generate the text image
resize the text image
turn text image to bitmask
apply bitmask
save sources

"""
util.prep()
random_id = uuid.uuid4().__str__().split('-')[0]
MASK = 'D_mask.jpg'
mask = Image.open(MASK)

for x in range(1):
    image1, image2 = util.load_images(latest=False)
    # Get max dimensions for image1, image2, and mask
    crop_size = util.get_crop_size([image1, image2], square=False)

    # Randomly transform an image
    im1 = util.random_transform(image1, crop_size)
    im2 = util.random_transform(image2, crop_size)

    # This code assumes that the 'mask' is a pre-fab image, so we adjust the mask to the sources, which may or may
    # not be square. Alternatively, we build the mask from scratch to have the proportions we want
    mask = mask.resize(crop_size)

    bitmask = util.make_bitmask_from_black_white(mask)
    collage_A, collage_B = util.simple_mask_swap(im1, im2, bitmask)

    Image.fromarray(collage_A).save(f'{random_id}_{x}_A.jpg')
    Image.fromarray(collage_B).save(f'{random_id}_{x}_B.jpg')
