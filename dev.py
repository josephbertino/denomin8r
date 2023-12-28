from util import *

prep()
fontfile = BOOKMAN
kern_rate = 1.0

# -----DO NOT DELETE ABOVE THIS LINE---------------------------
# TODO Big Project 1: "Chaos Source Transforms"

# dev code
for pa, pb in load_sources_half_latest_pairs(n=15):
    pa, pa_transform_list = chaos_source_transform(pa)
    pb, pb_transform_list = chaos_source_transform(pb)
    mask_is_pa, mask_is_pb = classic_D_swap_random(pa, pb)

    mask_is_pa = Image.fromarray(mask_is_pa)
    mask_is_pb = Image.fromarray(mask_is_pb)

    mask_is_pa = draw_test_params(mask_is_pa, ops=', '.join(pb_transform_list))
    mask_is_pb = draw_test_params(mask_is_pb, ops=', '.join(pa_transform_list))

    mask_is_pa.show()
    mask_is_pb.show()

# TODO consider "Observation" notes below for method tweaking
# TODO finish off with a stamp

'''
I definitely vibe more with images that are less processed. Have to especially be gentle with source_resample transforms, like grid and vertical/horizontal restacks
'''
"""
# Observations

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
