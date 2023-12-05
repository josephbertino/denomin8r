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

# TODO do I want to crop here?
# TODO it should be sufficient to phase max 1 time in each direction
im_arrs, filenames = load_sources(latest=True, n=10)
done = []
for im_arr in im_arrs:
    for _ in range(1,random.choice(range(2,7))):
        im_arr = source_phase(im_arr)
    done.append(im_arr)
save_images_from_arrays(done, draw_handle=True)

# TODO Phase a whole image so it spills over to the other side (horizontally or vertically)
# TODO Slice Transform: Reverse phasing (possibly just a small modification of regular phasing
# TODO Slice Transform: np.roll the slices by incremental (or random) shifts
# TODO Slice Transform: flip alternating slices
# TODO Slice Transform: swap slices between 2 or more sources

# TODO tweak chaos_source_transform's parameters
# TODO Play around and Test EACH METHOD IN UTIL & SOURCE_OPS