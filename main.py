from PIL import Image, ImageFont, ImageDraw
import utils
import numpy as np

def main():
    # Import photo1 and photo2
    PHOTO1 = 'photo1.jpg'
    PHOTO2 = 'photo2.jpg'
    image1 = Image.open(PHOTO1)
    image2 = Image.open(PHOTO2)
    MASK = 'D_mask.jpg'
    mask = Image.open(MASK)

    # Get max dimensions for image1, image2, and mask
    w, h = utils.get_max_size([image1, image2, mask])

    # Crop an image
    im1 = image1.crop(utils.get_crop_box(w, h))
    im2 = image2.crop(utils.get_crop_box(w, h))

    mask = 0
    collage1, collage2 = utils.simple_mask_swap(im1, im2, mask)

    # TODO make a smarter filter to grab imperfect blacks... maybe a lambda
    # TODO generate a bitmask from a font file
    # TODO rename project to denomin8r
    # TODO get the vector of Arial's "D" and rasterize
    # TODO determine regions in photo1 and photo2 where we'll swap information
    # TODO stretch out mask to fit swap-regions of photo1 and photo2
    # TODO swap information between photo1 and photo2 using mask
    # TODO save new photo1 and photo2
    # TODO integrate with shutterstock API to get unlimited images

if __name__ == '__main__':
    main()

# TODO learn about the structure of a font file, and how a font is transformed into pixels