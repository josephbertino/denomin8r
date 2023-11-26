from util import *
import uuid

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
SOURCE_TRANSFORM_BUDGET = 9
SOURCE_TRANSFORMS = [
    (source_flip_lr, 1),
    (source_flip_ud, 1),
    (source_rotate_180, 2),
    (source_crop_random, 3),  # Randomly select a cropping method
    (source_slice_random, 6),  # Randomly select a slicing method
    (crop_offcrop_recursive, 9)  # Special method
]

def chaos_source_transform(im_arr):
    """
    Take an image and run it through a series of transformations, then return the modified image.
        The number and order of transformations will be determined by chance, but there is a
        "cost" to each transformation, and once the "transform budget" is spent, abort and return.

    :param np.ndarray im_arr:
    :return np.ndarray, operation_list:
    """
    budget = SOURCE_TRANSFORM_BUDGET
    operations = 0
    op_list = []
    random.shuffle(SOURCE_TRANSFORMS)
    for transform, cost in SOURCE_TRANSFORMS:
        if cost > budget:
            # This operation is too complex
            continue
        im_arr = transform(im_arr)
        op_list.append(transform.__name__)
        budget -= cost
        operations += 1
        if operations == 3 or budget < 1 or random.random() > 0.66:
            break
    return im_arr, op_list, 9 - budget

n = 10
im_arrs, filenames = load_sources(latest=False, n=n, specific_srcs=[])
for im_arr, filename in zip(im_arrs, filenames):
    print(f'{filename}')
    new_im_arr, op_list, spent = chaos_source_transform(im_arr)
    img = Image.fromarray(new_im_arr)
    img = draw_test_params(img, spent=spent, op_list=op_list)
    img.show()

# TODO profile each source transform method against a control image to get a better idea of what cost to assign them. This includes each method in source_slice random and source_crop_random
# TODO play around with util.slice_image_resample_random
# TODO TEST EACH METHOD IN UTIL & SOURCE_OPS
