import enum

from PIL import Image
import util
import uuid
from enum import Enum
from util import BitmaskMethod

# Options
MASK = 'D_mask.jpg'  # If I am using a pre-built mask image
TEXT = 'D'
BITMASK_METHOD = BitmaskMethod.STATIC_TEXT
USE_LATEST = True
ADD_HANDLE = False
OFF_CROPPED = False
KERN_RATE = 1.0
ITERS = 5
SPEC_SRCS = []


def main(mask:str=MASK,
         text:str=TEXT,
         bitmask_method:Enum=BITMASK_METHOD,
         use_latest:bool=USE_LATEST,
         add_handle:bool=ADD_HANDLE,
         off_cropped:bool=OFF_CROPPED,
         kern_rate:float=KERN_RATE,
         iters:int=ITERS,
         spec_srcs:list=SPEC_SRCS,
         ):
    random_id = uuid.uuid4().__str__().split('-')[0]
    mask_img = Image.open(mask)
    image1 = image2 = bitmask = None
    crop_shape = (100, 100,)

    for x in range(iters):

        # Get Source Images
        image1, image2 = util.load_sources(latest=use_latest, specific_srcs=spec_srcs)

        if off_cropped:
            # Off-crop each image with a simple random bitmask and jitter
            # TODO move this transformation to the "Chaos Source Transforms", and it does not necessarily have to apply to BOTH sources
            image1 = util.recursive_off_crop(image1)
            image2 = util.recursive_off_crop(image2)
            crop_shape = util.get_crop_shape([image1, image2], square=True)
            image1 = util.crop_central(image1, crop_shape)
            image2 = util.crop_central(image2, crop_shape)
        else:
            crop_shape = util.get_crop_shape([image1, image2], square=True)
            image1 = util.random_transform(image1, crop_shape)
            image2 = util.random_transform(image2, crop_shape)

        # Generate Bitmask
        match bitmask_method:
            case BitmaskMethod.BITMASK_IMG:
                mask_img = mask_img.resize(crop_shape)
                bitmask = util.make_bitmask_from_bw_image(mask_img)
            case BitmaskMethod.STATIC_TEXT:
                bitmask = util.build_bitmask_to_size(text=text, fontfile=util.BOOKMAN, shape=crop_shape, kern_rate=kern_rate)
            case BitmaskMethod.RANDOM_TEXT:
                bitmask = util.build_random_text_bitmask(fontfile=util.BOOKMAN, shape=crop_shape)

        # Apply Bitmask to Source Images
        collage_A, collage_B = util.simple_bitmask_swap(image1, image2, bitmask)
        collage_A = Image.fromarray(collage_A)
        collage_B = Image.fromarray(collage_B)

        if add_handle:
            collage_A = util.draw_handle(collage_A)
            collage_B = util.draw_handle(collage_B)

        collage_A.save(f'{random_id}_{x}_A.jpg')
        collage_B.save(f'{random_id}_{x}_B.jpg')


# TODO Big Project 1: "Chaos Source Transforms"... requires self-tessellation if possible... and note that OFF-CROPPED is no longer a SOURCE_GETTER option, it's just a transformation option for a single image...also phase an image so it spills over to the other side
# TODO make logo for PUSH
# TODO experiment with ImageFont.getmask() for making a bitmask
# TODO generate bitmasks from other images, LOVE, I <3 NY... ask Nadia for others
# TODO can I self-tesselate the Bitmask? What other transformation can I make on the bitmask?
# TODO text things to randomize: text margin, text size, text style, text kerning
# TODO RANDOM WORDS generated, Pulled from where???
# TODO turning any image into a bitmask by running it through a filter
# TODO should util.get_func_args return a list of tuples, or 3 lists?
# TODO make a method that can crop from center smaller and smaller, using the same char "D" or "O" to produce a tunnel effect
# TODO random transform of the bitmask! (rotation, tesselation, resizing (stretching) the text_image then converting to bitmask, rather than expanding the bitmask with whitespace. This will fuck with the proportions of the mask, which is cool)
# TODO integrate with shutterstock API
# TODO allow for line breaks in the mask text
# TODO have MAX_PADDING in util be a function (fraction) of fontsize... or maybe just have left and right padding be a parameter
# TODO as a joke be able to add watermarks to my collages...the watermarks are bitmasked
# TODO Make website to sell stickers, tshirts, and totes... images are randomly generated, or "classic collection". In fact, have different types of "collections"... users can generate a custom one of a kind image to put on a tote bag or tshirt, and they have the option of "obliterating" their design so that no one else can use it.
# TODO for util.fn_runner: group all bool types so the checkboxes can be put on same line... or just organize the runner GUI better
# TODO if SOURCE_FILES gets large enough or the rendering process starts to slow down, will have to consider refactoring for speed
# TODO QR code to access website, premiered on Insta
# TODO Incoprorate Alpha channel to make the 'boundaries' between source elements blurred
# TODO autogenerate posts daily so I no longer have to lol
# TODO make a bunch of sources based on a bunch of images, and save the individual pieces derived from masking into separate lists (one for the Inner shape, one for the outer), and recombine randomly
# TODO if ever I am at a loss for enhancements or experiments, read the docstrings of Image methods I use to get inspiration
# TODO for NFTs... start coming up with the concept of "Rare" sources. e.g. non-D or non-8's are extremely rare and aberrant
# TODO tesselating multiple images to become a "source"
# TODO website to generate one-of-a-kind totes and t-shirts
# TODO warping and shifting, corrupting the bitmask
# TODO create my own font
# TODO overlaying multiple letters in the bitmask, centered at different coords so they spill off the canvas
# TODO swap 2 stamps across 2 pictures. Swap X stamps across X pictures

if __name__ == '__main__':
    util.prep()
    util.fn_runner(main)


'''
Big Goals
+ Experiment with many themes (or combinations thereof)
    + 1-source collages where you simply shift/crop one of the copies (UpDown, LeftRight, Half one way and Half the Other)
    + Specific Patterns: Camo, Sand, Rainbows, Water, Clouds
+ Other stamps: Robert Indiana's "LOVE", "I <3 NY"
+ Once I develop enough distinct methods of transforming or combining source, meta-abstract all those methods so they can be combined randomly 
+ Once the mask and 2 source images are established, randomize the process of transforming and aligning the source images
+ Be able to pull N source images and generate M combinations of them, using some automated process or API
+ Swapping X stamps across Y sources
'''

'''
Big Project 1: "Chaos Source Transforms"
    + Modularize all the ways to transform a source. Then repeatedly select those tranformations to apply to a source, kind of like a daisy chain of effects. You can even have the same effect multiple times in a chain. Eventually the chain terminates and the source gets transformed.
    + Maybe there is a "cost" per transform and you only get a certain "budget" for each source image. Once you spend the budget or you have enough of a particular item, you get kicked out
    + Flip, Rotate, Crop, Jitter applied to an image, Resize, **Tessellate**, **Warp**

Big Project 2: Gradual Transformation a la Philip Glass
+ First draw a canvas then Start of with painting a portion of a source image on the left hand side (or wherever you decide is the start). Then duplicate, reiterate, replicate the source image across the space but shifting and glitching it, transforming, modulating it, until gradually you transition it into a completely different image, or a combination of multiple images
'''