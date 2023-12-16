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

im_arrs, filenames = load_sources(latest=False, n=5, specific_srcs=None)
for im in im_arrs:
    img = Image.fromarray(im)
    img = draw_handle_on_img(img)
    img.show()

# TODO Play around and Test EACH METHOD IN UTIL & SOURCE_OPS. In so doing, incorporate and expand upon the notes above, so that I can finally remove them from this module
# TODO tweak chaos_source_transform's parameters
# TODO finish off with a stamp
# TODO what effects would be worth considering doing multiple times? (I'm guessing with some transition transform in between)