from PIL import Image
import utils

def main():
    # Import photo1 and photo2
    PHOTO1 = 'sources/11.jpg'
    PHOTO2 = 'sources/12.jpg'
    image1 = Image.open(PHOTO1)
    image2 = Image.open(PHOTO2)
    MASK = 'D_mask.jpg'
    mask = Image.open(MASK)

    # Get max dimensions for image1, image2, and mask
    crop_size = utils.get_crop_size([image1, image2, mask])

    for x in range(3):

        # Randomly transform an image
        im1 = utils.random_transform(image1, crop_size)
        im2 = utils.random_transform(image2, crop_size)

        mask = mask.resize(crop_size)

        bitmask = utils.make_bitmask_from_black_white(mask)
        collage_A, collage_B = utils.simple_mask_swap(im1, im2, bitmask)

        utils.crop_square(Image.fromarray(collage_A)).save(f'collage{x}_A.jpg')
        utils.crop_square(Image.fromarray(collage_B)).save(f'collage{x}_B.jpg')

    # TODO learn about the structure of a font file, and how a font is transformed into pixels
    # TODO Learn about how a font can be transformed into pixels. Learn how to transform a font 'D' into an Image.image or a bitmask
    # TODO generate a bitmask from a font file
    # TODO get the vector of Arial's "D" and rasterize
    # TODO stretch out vectorizded font mask to fit source images

    # TODO chaos_crop_resize where it crops and resizes over and over again
    # TODO allow the crop method to accept cropping from any specified origin point
    # TODO experiments with putting all image transformation methods and bitmask application methods into a list that randomly selects what to do so every time I run it's unexpected what will happen

    # TODO make small util to crop source iamges to squares (for instagram)
    # TODO automatically make collages with an entire fontface.
    # TODO integrate with shutterstock API to get unlimited images
    # TODO experiments with flipping same image
    # TODO experiments with rotating same image
    # TODO Make a mask out of 2 letters side by side
    # TODO swap 2 stamps across 2 pictures. Swap X stamps across X pictures

if __name__ == '__main__':
    utils.prep()
    main()

'''
Big Goals

1) Be able to Collage entire words using the 2-source format 
2) Once the mask and 2 source images are established, randomize the process of transforming and aligning the source images
3) Be able to pull N source images and generate M combinations of them, using some automated process or API
4) Swapping X stamps across Y sources
'''