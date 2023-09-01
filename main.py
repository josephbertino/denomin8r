from PIL import Image
import util

def main():
    MASK = 'D_mask.jpg'
    mask = Image.open(MASK)

    for x in range(3):
        image1, image2 = util.load_images(latest=True)
        # Get max dimensions for image1, image2, and mask
        crop_size = util.get_crop_size([image1, image2, mask])

        # Randomly transform an image
        im1 = util.random_transform(image1, crop_size)
        im2 = util.random_transform(image2, crop_size)

        mask = mask.resize(crop_size)

        bitmask = util.make_bitmask_from_black_white(mask)
        collage_A, collage_B = util.simple_mask_swap(im1, im2, bitmask)

        util.crop_square(Image.fromarray(collage_A)).save(f'collage{x}_A.jpg')
        util.crop_square(Image.fromarray(collage_B)).save(f'collage{x}_B.jpg')

    # TODO MAX_PADDING / Left Right Margins should probably be determined by some formula involving kern rate and text_width/height, because as the letters get squished together, the text runs off the right
    # TODO util.get_random_mask() where 'D' or '8' is returned
    # TODO expand the auto-generated bitmask by fitting it to the cropped size of the source images
    # TODO if ever I am at a loss for enhancements or experiments, read the docstrings of Image methods I use to get inspiration
    # TODO get the vector of Arial's "D" and rasterize
    # TODO stretch out vectorizded font mask to fit source images
    # TODO things to randomize: text margin, text size, text style, text kerning
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
    util.prep()
    main()

'''
Big Goals

1) Be able to Collage entire words using the 2-source format 
2) Once the mask and 2 source images are established, randomize the process of transforming and aligning the source images
3) Be able to pull N source images and generate M combinations of them, using some automated process or API
4) Swapping X stamps across Y sources
'''