from util import *
from enum import Enum
from util import BitmaskMethod

# Options
MASK = 'D_mask.jpg'  # If I am using a pre-built mask image
TEXT = 'D'
BITMASK_METHOD = BitmaskMethod.STATIC_TEXT
USE_LATEST = True
DRAW_HANDLE = False
KERN_RATE = 1.0
ITERS = 5
SPEC_SRCS = []


def main(mask:str=MASK,
         text:str=TEXT,
         bitmask_method:Enum=BITMASK_METHOD,
         use_latest:bool=USE_LATEST,
         draw_handle:bool=DRAW_HANDLE,
         kern_rate:float=KERN_RATE,
         iters:int=ITERS,
         spec_srcs:list=SPEC_SRCS,
         ):

    mask_img = Image.open(mask)
    bitmask = None

    for x in range(iters):

        # Get Source Images
        imgs, filenames = load_sources(latest=use_latest, specific_srcs=spec_srcs)
        imarr_1, imarr_2 = imgs

        imarr_1, op_list = chaos_source_transform(imarr_1)
        imarr_2, op_list = chaos_source_transform(imarr_2)

        crop_shape = get_common_crop_shape([imarr_1, imarr_2], square=True)
        imarr_1 = crop_im_arr(imarr_1, cropbox_central_shape, crop_shape=crop_shape)
        imarr_2 = crop_im_arr(imarr_2, cropbox_central_shape, crop_shape=crop_shape)

        # Generate Bitmask
        match bitmask_method:
            case BitmaskMethod.BITMASK_IMG:
                mask_img = mask_img.resize(crop_shape)
                bitmask = make_bitmask_from_bw_image(mask_img)
            case BitmaskMethod.STATIC_TEXT:
                bitmask = build_bitmask_to_size(text=text, fontfile=BOOKMAN, shape=crop_shape, kern_rate=kern_rate)
            case BitmaskMethod.RANDOM_TEXT:
                bitmask = build_random_text_bitmask(fontfile=BOOKMAN, shape=crop_shape)

        # Apply Bitmask to Source Images
        collage_A, collage_B = simple_bitmask_swap(imarr_1, imarr_2, bitmask)
        save_images_from_arrays([collage_A, collage_B], draw_handle=draw_handle)

'''Flags'''
# TODO Slice Transform: swap slices between 2 or more sources

'''Masks'''
# TODO experiment with ImageFont.getmask() for making a bitmask
# TODO generate bitmasks from other images, LOVE, I <3 NY... ask Nadia for others
# TODO can I self-tesselate the Bitmask? What other transformation can I make on the bitmask?
# TODO turning any image into a bitmask by running it through a filter
# TODO swap 2 masks across 2 pictures. Swap X stamps across X pictures
# TODO as a joke be able to add watermarks to my collages...the watermarks are bitmasked
# TODO make a method that can crop from center smaller and smaller, using the same char "D" or "O" to produce a tunnel effect

'''Text'''
# TODO allow for line breaks in the mask text
# TODO have MAX_PADDING in util be a function (fraction) of fontsize... or maybe just have left and right padding be a parameter
# TODO text things to randomize: text margin, text size, text style, text kerning
# TODO RANDOM WORDS generated, Pulled from where???
# TODO create my own font
# TODO warping and shifting, corrupting the bitmask
# TODO overlaying multiple letters in the bitmask, centered at different coords so they spill off the canvas

'''Tech'''
# TODO should util.get_func_args return a list of tuples, or 3 lists?
# TODO integrate with shutterstock API or other photo source
# TODO for util.fn_runner: group all bool types so the checkboxes can be put on same line... or just organize the runner GUI better
# TODO Make website to sell stickers, tshirts, and totes... images are randomly generated, or "classic collection". In fact, have different types of "collections"... users can generate a custom one of a kind image to put on a tote bag or tshirt, and they have the option of "obliterating" their design so that no one else can use it.
# TODO QR code to access website, premiered on Insta
# TODO website to generate one-of-a-kind totes and t-shirts
# TODO for NFTs... start coming up with the concept of "Rare" sources. e.g. non-D or non-8's are extremely rare and aberrant
# TODO autogenerate posts daily so I no longer have to lol

'''Uncategorized'''
# TODO play with dup_n being unequal across vertical and horizontal for a grid to get rectangles as atomic elements.
# TODO util to make gifs of sequence images?
# TODO make logo for PUSH
# TODO Make Totem pole with different heads. Will require to put all portrait sources into separate folder, thus organize sources better. util.img_totem_stack(dupn_h, spd). Heads include APHEX TWIN, JEFFREY EPSTEIN, Artist's faces, recognizeable faces mixed with obscure faces, totems of people we SHOULD admire and adore but unfortunately dont know all that well
# TODO can also vertically dup portraits and alternate different faces
# TODO random transform of the bitmask! (rotation, tesselation, resizing (stretching) the text_image then converting to bitmask, rather than expanding the bitmask with whitespace. This will fuck with the proportions of the mask, which is cool)
# TODO if SOURCE_FILES gets large enough or the rendering process starts to slow down, will have to consider refactoring for speed
# TODO Incoprorate Alpha channel to make the 'boundaries' between source elements blurred
# TODO make a bunch of sources based on a bunch of images, and save the individual pieces derived from masking into separate lists (one for the Inner shape, one for the outer), and recombine randomly
# TODO if ever I am at a loss for enhancements or experiments, read the docstrings of Image methods I use to get inspiration
# TODO tesselating multiple images to become a "source"
# TODO weave two sources by using a checkerboard pattern for the mask


if __name__ == '__main__':
    prep()
    fn_runner(main)

'''
Big Goals
+ Experiment with many themes (or combinations thereof)
    + 1-source collages where you simply shift/crop one of the copies (UpDown, LeftRight, Half one way and Half the Other)
    + Specific Patterns: Camo, Sand, Rainbows, Water, Clouds
+ Grid resamplings of classic geometric and pattern-based art, like Sol Lewitt, Frank Stella, Robert Indiana
+ Other stamps: Robert Indiana's "LOVE", "I <3 NY"
+ Once I develop enough distinct methods of transforming or combining source, meta-abstract all those methods so they can be combined randomly 
+ Once the mask and 2 source images are established, randomize the process of transforming and aligning the source images
+ Be able to pull N source images and generate M combinations of them, using some automated process or API
+ Swapping X stamps across Y sources
'''

'''
Big Project: Flags, Colonialism, Imperialism
# TODO Slice Transform: swap slices between 2 or more sources
+ Blend flags of colonizing nations (e.g. UK) with flags of the nations they colonized, or fucked over in some way.
+ Will have to keep in mind that flags have different dimensions/aspect ratios, and we don't want to crop a flag
+ Unless! Cropping is an artistic statement to express colonialism / imperialism and stripping / depleting a nation

Big Project: Gradual Transformation a la Philip Glass
+ First draw a canvas then Start of with painting a portion of a source image on the left hand side (or wherever you decide is the start). Then duplicate, reiterate, replicate the source image across the space but shifting and glitching it, transforming, modulating it, until gradually you transition it into a completely different image, or a combination of multiple images
+ Celebrity surgery transitions
'''

'''
EXHIBIT IDEAS

0) Chaos Source Transform
Just a fun exhibit of everything up to Chaos Source Transform. Playing on a smaller scale with a bunch of different source image motifs and themes.

1) Dolonialism
+ Flag project showing effects of colonization and imperialism on the identities of the victims / subjected
+ Thesis: Typically national flags are the product of emergence from the hold / ownership of a former colonizer. A nation only earns a flag when it becomes a nation---sovereign, free, and with its own identity. Well what happens when I interweave nations' flags with the flags of their former colonizers or identity? What emerges from this act of visual and political regression? What happens when the symbol of one's pride, culture, heritage, and identity becomes visually massacred, evocative of the bloody wars that were fought to secure new freedom and that very identity which is now once again vulnerable and split open? Moreover, can we ignore the lasting influence that former colonizers might still exert upon "sovereign" nations? Is not part of the nation's identity interwoven already with that of its former possessor
+ Idea: Take images of flags and interweave them with the flags of their former colonizers or oppressors.
+ Idea: Take images of flags and interweave them with random flags to see what happens
+ Idea: Interweave symbols of money / currency / commodities / natural resources relevant to the flag's country

2) Big D Energy
+ Debut of Denominator plastering itself across all walks of life, art, fake life, fake art, capitalism
+ Large prints, one-offs, as well as unique projected works that auto-generated and destroyed
+  (something else cool)
+  (something else cool)

3) "(Your Text Here)"
+ Users scan QR codes, and plug in what they want to be generated. They give prompts for (a) source images and (b) the stamp
+ Users can also submit selfies to get their faces Denominated
+ (what else can users submit?)
+ (what else can users submit?)
+ Sell merch
'''

'''
# Series Ideas

+ How D8 started to where it got today (more and more fucked and abstracted over time)
+ Start doing series on just one idea
'''

'''
# Source Ideas
NYPD Logos and Imagery
Birds
Sol Lewitt: everything (incl. 10 Geometric Figures)
Grids of Flags
Video Game Fight Scenes, esp. Street Fighter
Max Bill: 1970's shapes
'''

'''
# Phrase Ideas
NYPD
OCD
'''
