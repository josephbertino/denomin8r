from util import *

prep()
fontfile = BOOKMAN
kern_rate = 1.0

# -----DO NOT DELETE ABOVE THIS LINE---------------------------
# TODO Big Project 1: "Chaos Source Transforms"

# TODO re-run profiler methods to determine new costs, and apply costs to all transform methods. Make sure to update / rearrange all lists of transform methods
# TODO refactor chaos_source_transform to consider function cost once again
# TODO what effects would be worth considering doing multiple times? (I'm guessing with some transition transform in between)
# TODO consider "Observation" notes below for method tweaking
# TODO move cropbox methods to tools.py?
# TODO finish off with a stamp

'''
Tweaks
. source_offcrop_recursive should be less frequent. Maybe have RARE as well as COMPLEX and SIMPLE transforms
. I might want NOTHING to happen to the image. It doesn't always have to be transformed... that should sort of be a special occurrence
. Yeah, chance should first dictate whether SOMETHING happens at all, and then chance should dictate which things happen
'''

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
