from PIL import Image
import util
import uuid
from util import BitmaskMethod, SourceGetter

# Options
BITMASK_METHOD = BitmaskMethod.STATIC_TEXT
SOURCE_GETTER = SourceGetter.GRAB_TWO
USE_LATEST = False
JITTER = 0.07
SPEC_SRCS = []
MASK = 'D_mask.jpg'  # If I am using a pre-built mask image
TEXT = 'D'
KERN_RATE = 1.0


def main():
    random_id = uuid.uuid4().__str__().split('-')[0]
    mask_img = Image.open(MASK)
    image1 = image2 = bitmask = None
    crop_shape = (100, 100,)

    for x in range(20):

        # Get Source Images
        match SOURCE_GETTER:
            case SourceGetter.OFF_CROPPED:
                image1, image2 = util.get_off_cropped_images(latest=USE_LATEST, jitter=JITTER)
                crop_shape = util.get_crop_shape([image1, image2], square=True)
            case SourceGetter.GRAB_TWO:
                image1, image2 = util.load_sources(latest=USE_LATEST, specific_srcs=SPEC_SRCS)
                crop_shape = util.get_crop_shape([image1, image2], square=True)
                image1 = util.random_transform(image1, crop_shape)
                image2 = util.random_transform(image2, crop_shape)

        # Generate Bitmask
        match BITMASK_METHOD:
            case BitmaskMethod.BITMASK_IMG:
                mask_img = mask_img.resize(crop_shape)
                bitmask = util.make_bitmask_from_bw_image(mask_img)
            case BitmaskMethod.STATIC_TEXT:
                bitmask = util.build_bitmask_to_size(text=TEXT, fontfile=util.BOOKMAN, shape=crop_shape, kern_rate=KERN_RATE)
            case BitmaskMethod.RANDOM_TEXT:
                bitmask = util.build_random_text_bitmask(fontfile=util.BOOKMAN, shape=crop_shape)

        # Apply Bitmask to Source Images
        collage_A, collage_B = util.simple_bitmask_swap(image1, image2, bitmask)

        Image.fromarray(collage_A).save(f'{random_id}_{x}_A.jpg')
        Image.fromarray(collage_B).save(f'{random_id}_{x}_B.jpg')

# TODO add ability to "watermark" collages with "@denomin8r" at the bottom... Play around with colors for the @ watermark
# TODO MAKE STICKERS For Myself!!!!!!!!
# TODO add capability for lists as args in fn_runner
# TODO implement util.fn_runner on main()... this requires adding arguments to main for all the settings I set at the top
# TODO Big Project 1: "Chaos Source Transforms"
# TODO can I self-tesselate an image?
# TODO text things to randomize: text margin, text size, text style, text kerning
# TODO RANDOM WORDS generated, Pulled from where???
# TODO turning any image into a bitmask by running it through a filter
# TODO should util.get_func_args return a list of tuples, or 3 lists?
# TODO random transform of the bitmask! (rotation, tesselation, resizing (stretching) the text_image then converting to bitmask, rather than expanding the bitmask with whitespace. This will fuck with the proportions of the mask, which is cool)
# TODO integrate with shutterstock API
# TODO allow for line breaks in the mask text
# TODO generate bitmasks from other images, LOVE, I <3 NY... ask Nadia for others
# TODO experiment with ImageFont.getmask() for making a bitmask
# TODO have MAX_PADDING in util be a function (fraction) of fontsize... or maybe just have left and right padding be a parameter
# TODO make logo for PUSH
# TODO Make website to sell stickers, tshirts, and totes... images are randomly generated, or "classic collection". In fact, have different types of "collections"... users can generate a custom one of a kind image to put on a tote bag or tshirt, and they have the option of "obliterating" their design so that no one else can use it.
# TODO if SOURCE_FILES gets large enough or the rendering process starts to slow down, will have to consider refactoring for speed
# TODO QR code to access website, premiered on Insta
# TODO Incoprorate Alpha channel to make the 'boundaries' between source elements blurred
# TODO autogenerate posts daily so I no longer have to lol
# TODO make a bunch of sources based on a bunch of images, and save the individual pieces derived from masking into separate lists (one for the Inner shape, one for the outer), and recombine randomly
# TODO if ever I am at a loss for enhancements or experiments, read the docstrings of Image methods I use to get inspiration
# TODO for NFTs... start coming up with the concept of "Rare" sources
# TODO tesselating multiple images to become a "source"
# TODO website to generate one-of-a-kind totes and t-shirts
# TODO warping and shifting, corrupting the bitmask
# TODO non-D or non-8's are extremely rare and aberrant
# TODO experiments with putting all image transformation methods and bitmask application methods into a list that randomly selects what to do so every time I run it's unexpected what will happen
# TODO randomize the order of operations in random_transform. Allow for multiple occurences of an operation, not necessarily in sequence
# TODO create my own font
# TODO overlaying multiple letters in the bitmask, centered at different coords so they spill off the canvas
# TODO swap 2 stamps across 2 pictures. Swap X stamps across X pictures

if __name__ == '__main__':
    util.prep()
    main()

'''
Big Goals
+ Experiment with many themes (or combinations thereof)
    + 1-source collages where you simply shift/crop one of the copies (UpDown, LeftRight, Half one way and Half the Other)
    + Specific Patterns: Camo, Sand, Rainbows
    + Other stamps: Robert Indiana's "LOVE", "I <3 NY"
+ Once I develop enough distinct methods of transforming or combining source, meta-abstract all those methods so they can be combined randomly 
+ Once the mask and 2 source images are established, randomize the process of transforming and aligning the source images
+ Be able to pull N source images and generate M combinations of them, using some automated process or API
+ Swapping X stamps across Y sources
'''

'''
Big Project 1: "Chaos Source Transforms"
    + Modularize all the ways to transform a source. Then repeatedly select those tranformations to apply to a source, kind of like a daisy chain of effects. You can even have the same effect multiple times in a chain. Eventually the chain terminates and the source gets transformed.
    + Flip, Rotate, Crop, Resize, **Tessellate**, **Warp**

Big Project 2: Gradual Transformation a la Philip Glass
+ First draw a canvas then Start of with painting a portion of a source image on the left hand side (or wherever you decide is the start). Then duplicate, reiterate, replicate the source image across the space but shifting and glitching it, transforming, modulating it, until gradually you transition it into a completely different image, or a combination of multiple images
'''