import random

from util import *

prep()
fontfile = BOOKMAN
kern_rate = 1.0

# -----DO NOT DELETE ABOVE THIS LINE---------------------------

"""
Observations:
Vertical Slicing
    dup_n:
        from 2 up to ~7 gives good results, with it getting creepier the higher you go.
        I wouldn't go more than 7 for my intended aesthetic.
    slice_per_dup:
        slice_per_dup >= 8 starts to resemble a face
        Once dupn goes above 3, I think >20 slices per dupe looks good
    I really love how creepy it is to make many thin tall slices of faces, or squished faces
Horizontal Slicing
    dupn:
        3 or 4 seems great. Like totems
    slice_per_dup:
        Needs to be larger, like >12
Grid:
    I like what happens when dup_n is unequal between rotation slicing.
    Produces cool effects with the rectangles.
"""

# TODO Big Project 1: "Chaos Source Transforms"

# TODO Slice Transform: flip alternating slices
def source_resample_flip_slices_vert(im_arr, num_slices=None):
    """

    :param im_arr:
    :param num_slices:
    :return:
    """
    num_slices = num_slices if num_slices else random.choice(range(8, 50))
    slices = slice_up_array_uniform(im_arr, num_slices=num_slices)
    slices = map(lambda i, s: s if i % 2 == 0 else np.flip(s, axis=1), enumerate(slices))
    return np.hstack(slices)



# im_arrs, filenames = load_sources(latest=False, n=10)
# ims = []
# for im in im_arrs:
#     im1 = source_resample_phase_hor(im)
#     im2 = source_resample_phase_vert(im)
#     ims.extend([im1, im2])
# save_images_from_arrays(ims, draw_handle=True)


# TODO Slice Transform: swap slices between 2 or more sources

# TODO tweak chaos_source_transform's parameters
# TODO Play around and Test EACH METHOD IN UTIL & SOURCE_OPS