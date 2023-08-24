from PIL import Image
import utils

def main():
    # Import photo1 and photo2
    PHOTO1 = 'photo5.webp'
    PHOTO2 = 'photo6.jpg'
    image1 = Image.open(PHOTO1)
    image2 = Image.open(PHOTO2)
    MASK = 'D_mask.jpg'
    mask = Image.open(MASK)

    # Get max dimensions for image1, image2, and mask
    w, h = utils.get_max_size([image1, image2, mask])

    # Crop an image
    box = utils.get_crop_box(w, h)
    im1 = utils.crop_central(image1, w, h)
    im2 = utils.crop_central(image2, w, h)
    mask = mask.resize(size=(w,h))

    bitmask = utils.make_bitmask_from_black_white(mask)
    collage1, collage2 = utils.simple_mask_swap(im1, im2, bitmask)

    Image.fromarray(collage1).save('collage1.jpg')
    Image.fromarray(collage2).save('collage2.jpg')

    # TODO make a resize method for the bitmask that keeps original proportion and adds False in the buffer margins
    # TODO learn about the structure of a font file, and how a font is transformed into pixels
    # TODO generate a bitmask from a font file
    # TODO get the vector of Arial's "D" and rasterize
    # TODO stretch out mask to fit swap-regions of photo1 and photo2
    # TODO automatically make collages with an entire fontface.
    # TODO integrate with shutterstock API to get unlimited images
    # TODO experiments with flipping same image
    # TODO experiments with rotating same image
    # TODO experiments with putting all image transformation methods and bitmask application methods into a list that randomly selects what to do so every time I run it's unexpected what will happen
    # TODO Make a mask out of 2 letters side by side

if __name__ == '__main__':
    main()
