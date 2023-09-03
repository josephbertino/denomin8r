from PIL import Image
import util
import uuid


def main():
    random_id = uuid.uuid4().__str__().split('-')[0]
    MASK = 'D_mask.jpg'
    mask = Image.open(MASK)

    for x in range(4):
        image1, image2 = util.load_images(latest=True)
        # Get max dimensions for image1, image2, and mask
        crop_size = util.get_crop_size([image1, image2, mask])

        # Randomly transform an image
        im1 = util.random_transform(image1, crop_size)
        im2 = util.random_transform(image2, crop_size)

        mask = mask.resize(crop_size)

        bitmask = util.make_bitmask_from_black_white(mask)
        collage_A, collage_B = util.simple_mask_swap(im1, im2, bitmask)

        util.crop_square(Image.fromarray(collage_A)).save(f'{random_id}_{x}_A.jpg')
        util.crop_square(Image.fromarray(collage_B)).save(f'{random_id}_{x}_B.jpg')

# TODO expand the auto-generated bitmask by fitting it to the cropped size of the source images. Probably the most important thing is determining the SIZE of the font before you type it out, and consider the length of the text
# TODO util.get_random_mask() where 'D' or '8' is returned
# TODO MAKE STICKERS NOW!!!!!!!!
# TODO make logo for PUSH
# TODO expand the random transforms... random cropping and resize (within parameters)
# TODO allow for breaking up the text into multiple lines
# TODO if ever I am at a loss for enhancements or experiments, read the docstrings of Image methods I use to get inspiration
# TODO get the vector of Arial's "D" and rasterize
# TODO things to randomize: text margin, text size, text style, text kerning
# TODO chaos_crop_resize where it crops and resizes over and over again
# TODO Incoprorate Alpha channel to make the 'boundaries' between source elements blurred
# TODO tesselating multiple images to become a "source"
# TODO website to generate one-of-a-kind totes and t-shirts
# TODO warping and shifting, corrupting the bitmask
# TODO non-D or non-8's are extremely rare and aberrant
# TODO allow the crop method to accept cropping from any specified origin point
# TODO experiments with putting all image transformation methods and bitmask application methods into a list that randomly selects what to do so every time I run it's unexpected what will happen
# TODO randomize the order of operations in random_transform. Allow for multiple occurences of an operation, not necessarily in sequence
# TODO automatically make collages with an entire fontface.
# TODO integrate with shutterstock API to get unlimited images
# TODO experiments with flipping same image
# TODO experiments with rotating same image
# TODO create my own font
# TODO swap 2 stamps across 2 pictures. Swap X stamps across X pictures
# TODO website where users can generate a custom one of a kind image to put on a tote bag or tshirt

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