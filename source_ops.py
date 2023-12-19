"""
Library module of all methods related to transforing a source

Notes:
    1) Please try to enforce the standard where source transform method signatures have 'im_arr'
        as their first parameter, and all other parameters are kwargs with default values
"""
from mask_ops import *


def apply_transform_cost(cost=1):
    """
    Decorator method to apply a "cost" attribute to functions
        that get wrapped by the output wrapper
    + Credit to PEP-232 [https://peps.python.org/pep-0232/]
    + Credit dimitris-fasarakis-hilliard @ https://stackoverflow.com/a/47056146

    :param int cost:
    :return:
    """
    def wrapper(fn):
        fn.transform_cost = cost
        return fn
    return wrapper


@apply_transform_cost()
def source_flip_lr(im_arr):
    """
    Flip L-R an image array

    :param np.ndarray im_arr:
    :return np.ndarray:
    """
    return np.fliplr(im_arr)


@apply_transform_cost()
def source_flip_ud(im_arr):
    """
    Flip U-D an image array

    :param np.ndarray im_arr:
    :return np.ndarray:
    """
    return np.flipud(im_arr)


@apply_transform_cost()
def source_phase_vert(im_arr, shift=None):
    """
    Phase ('roll') an image according along its vertical axis

    :param im_arr:
    :param int shift:
    :return:
    """
    if shift is None:
        # shape == (w, h)
        shape = get_np_array_shape(im_arr)
        shift = math.floor(random.random() * shape[1])

    return np.roll(im_arr, axis=0, shift=shift)


@apply_transform_cost()
def source_phase_hor(im_arr, shift=None):
    """
    Phase ('roll') an image according along its horizontal axis

    :param im_arr:
    :param int shift:
    :return:
    """
    if shift is None:
        # shape == (w, h)
        shape = get_np_array_shape(im_arr)
        shift = math.floor(random.random() * shape[0])

    return np.roll(im_arr, axis=1, shift=shift)


@apply_transform_cost()
def source_phase_complete(im_arr):
    """
    Phase ('roll') an image according to both width and height axes

    :param np.ndarray im_arr:
    :return:
    """
    im_arr = source_phase_hor(im_arr)
    im_arr = source_phase_vert(im_arr)

    return im_arr


@apply_transform_cost()
def source_rotate_180(im_arr):
    """
    Rotate 180 degrees an image array

    :param np.ndarray im_arr:
    :return np.ndarray:
    """
    return np.rot90(m=im_arr, k=2)


@apply_transform_cost()
def source_crop_random(im_arr):
    """
    Apply cropping to image array with a randomly-selected method

    :param np.ndarray im_arr:
    :return np.ndarray:
    """
    cropbox_method = random.choice(CROPBOX_OPERATIONS)
    cropped_im_arr = crop_im_arr(im_arr=im_arr, cropbox_method=cropbox_method)
    return cropped_im_arr


@apply_transform_cost()
def source_resample_random(im_arr):
    """
    Apply slice-duping to image array with a randomly-selected method

    :param np.ndarray im_arr:
    :return np.ndarray:
    """
    slice_method = random.choice(RESAMPLE_TRANSFORMS)
    method_name = slice_method.__name__
    logger.info(f"Implementing SLICE method {method_name}")

    sliced_im_arr = slice_method(im_arr)
    return sliced_im_arr


@apply_transform_cost()
def source_resample_shuffle(im_arr, num_slices=None):
    """
    Vertically slice up image and rearrange the slices randomly
        Return image as np.ndarray

    :param np.ndarray im_arr:
    :param int num_slices:      Number of slices to generate
    :return np.ndarray:
    """
    num_slices = num_slices if num_slices else 2 ** random.choice(range(1, 6))

    slices = slice_up_array_uniform(im_arr, num_slices)
    random.shuffle(slices)
    return np.hstack(slices)


@apply_transform_cost()
def source_resample_reverse(im_arr, num_slices=None):
    """
    Vertically slice up image and reverse the order

    :param np.ndarray im_arr:
    :param int num_slices:               Number of slices to generate
    :return np.ndarray:
    """
    num_slices = num_slices if num_slices else 2 ** random.choice(range(1, 6))

    slices = slice_up_array_uniform(im_arr, num_slices)
    slices = slices[::-1]
    return np.hstack(slices)


@apply_transform_cost()
def source_resample_stack_vertical(im_arr, num_dups=None, num_slices_per_dup=None):
    """
    Reorder vertical slices of an image into a stack of duplicates via uniform sampling

    :param np.ndarray im_arr:
    :param num_dups:
    :param num_slices_per_dup:
    :return np.ndarray:
    """
    num_dups = num_dups if num_dups else random.choice(range(2,8))
    num_slices_per_dup = num_slices_per_dup if num_slices_per_dup else 2 ** random.choice(range(1, 6))

    num_slices = num_dups * num_slices_per_dup
    duped_im_arr = slice_resample_array_vertical(im_arr, num_dups, num_slices)
    return duped_im_arr


@apply_transform_cost()
def source_resample_stack_horizontal(im_arr, num_dups=None, num_slices_per_dup=None):
    """
    Reorder horizontal slices of an image into a stack of duplicates of the original, via uniform sampling

    :param np.ndarray im_arr:
    :param num_dups:
    :param num_slices_per_dup:
    :return np.ndarray:
    """
    num_dups = num_dups if num_dups else random.choice(range(2,8))
    num_slices_per_dup = num_slices_per_dup if num_slices_per_dup else 2 ** random.choice(range(1, 6))

    num_slices = num_dups * num_slices_per_dup
    rotated_im_arr = np.rot90(m=im_arr, k=1)    # 90
    duped_rotated_im_arr = slice_resample_array_vertical(rotated_im_arr, num_dups, num_slices)
    final_im_arr = np.rot90(m=duped_rotated_im_arr, k=3)    # 270
    return final_im_arr


@apply_transform_cost()
def source_resample_phase_vert(im_arr, num_slices=None):
    """
    Vertically slice up image and np.roll each slice by an incremental shift

    :param np.ndarray im_arr:
    :param int num_slices:      Number of slices to generate
    :return np.ndarray:
    """
    num_slices = num_slices if num_slices else random.choice(range(8, 50))
    _, h = get_np_array_shape(im_arr)

    slices = slice_up_array_uniform(im_arr, num_slices)

    # Have the shifts go in 1 direction
    shift_rate = random.uniform(0.005, 0.025)
    direction = random.choice([1, -1])
    shifts = list(map(lambda x: math.floor(h * x * shift_rate * direction), range(num_slices)))

    slices = [np.roll(slice, axis=0, shift=shift) for slice, shift in zip(slices, shifts)]
    return np.hstack(slices)


@apply_transform_cost()
def source_resample_phase_hor(im_arr, num_slices=None):
    """
    Horizontally slice up image and np.roll each slice by an incremental shift

    :param np.ndarray im_arr:
    :param int num_slices:      Number of slices to generate
    :return np.ndarray:
    """
    im_arr = np.rot90(im_arr, k=1)
    im_arr = source_resample_phase_vert(im_arr, num_slices=num_slices)
    im_arr = np.rot90(im_arr, k=3)
    return im_arr


@apply_transform_cost()
def source_resample_flip_slices_vert(im_arr, num_slices=None, axis=None):
    """
    Take an image array, slice it up vertically, and np.flip alternating slices

    :param np.ndarray im_arr:
    :param num_slices:
    :param axis:
    :return np.ndarray :
    """
    num_slices = num_slices if num_slices else random.choice(range(2, 40))
    slices = slice_up_array_uniform(im_arr, num_slices=num_slices)
    axis = axis if isinstance(axis, int) else random.choice([0, 1])  # Flip slices UD or LR
    slices = list(map(lambda tup: tup[1] if tup[0] % 2 == 0 else np.flip(tup[1], axis=axis), enumerate(slices)))
    return np.hstack(slices)


@apply_transform_cost()
def source_resample_flip_slices_hor(im_arr, num_slices=None, axis=None):
    """
    Take an image array, slice it up horizontally, and np.flip alternating slices

    :param np.ndarray im_arr:
    :param num_slices:
    :param axis:
    :return np.ndarray:
    """
    im_arr = np.rot90(im_arr, k=1)
    im_arr = source_resample_flip_slices_vert(im_arr, num_slices, axis)
    im_arr = np.rot90(im_arr, k=3)
    return im_arr


@apply_transform_cost()
def source_resample_grid(im_arr, num_dups_vert=None, num_dups_hor=None, num_slices_per_dup=None):
    """
    Resample crisscrossed slices of an image into a grid of duplicates via uniform sampling

    :param np.ndarray im_arr:
    :param num_dups_vert:
    :param num_dups_hor:
    :param num_slices_per_dup:
    :return np.ndarray:
    """
    num_dups_vert = num_dups_vert if num_dups_vert else random.choice(range(2,8))
    num_dups_hor = num_dups_hor if num_dups_hor else random.choice(range(2, 8))
    num_slices_per_dup = num_slices_per_dup if num_slices_per_dup else 2 ** random.choice(range(1, 6))

    num_slices_vert = num_dups_vert * num_slices_per_dup
    duped_im_arr = slice_resample_array_vertical(im_arr, num_dups_vert, num_slices_vert)
    rotated_duped_im_arr = np.rot90(m=duped_im_arr, k=1)     # 90

    num_slices_hor = num_dups_hor * num_slices_per_dup
    grid_im_arr = slice_resample_array_vertical(rotated_duped_im_arr, num_dups_hor, num_slices_hor)
    final_im_arr = np.rot90(m=grid_im_arr, k=3)     # 270
    return final_im_arr


@apply_transform_cost()
def source_offcrop_recursive(im_arr, mask_text=None):
    """
    Recursively off-crop an image with itself using a bitmask

    :param np.ndarray im_arr:
    :param str mask_text:       If not None, use that as the bitmask.
                                Otherwise generate a random char for the bitmask.
    :return np.ndarray:
    """
    USE_CLEAN_COPY = random_bool()

    im_arr_a = im_arr.copy()
    im_arr_b = im_arr.copy()

    # Collage off-cropped image with another off-crop of itself
    times = random.choice(range(1, 6))
    for _ in range(times):
        im_arr_a = crop_im_arr(im_arr_a, cropbox_off_center_random)
        im_arr_b = crop_im_arr(im_arr_b, cropbox_off_center_random)

        # TODO (later) make a method to crop two images according to their shared dimensions
        crop_shape = get_common_crop_shape([im_arr_a, im_arr_b], square=False)
        im_arr_a = crop_im_arr(im_arr_a, cropbox_central_shape, crop_shape=crop_shape)
        im_arr_b = crop_im_arr(im_arr_b, cropbox_central_shape, crop_shape=crop_shape)

        if mask_text:
            bitmask = build_bitmask_to_size(text=mask_text, fontfile=BOOKMAN, shape=crop_shape)
        else:
            bitmask = build_random_text_bitmask(fontfile=BOOKMAN, shape=crop_shape, numchars=1)

        im_arr_a, im_arr_b = simple_bitmask_swap(im_arr_a, im_arr_b, bitmask)

        if USE_CLEAN_COPY:
            # Reset for next iteration
            im_arr_b = im_arr.copy()

    return im_arr_a


def crop_im_arr(im_arr, cropbox_method=None, **kwargs):
    """
    Crop image array according to method passed as parameter.
        If cropbox_method==None, default to tools.cropbox_central_square

    :param np.ndarray im_arr:
    :param function cropbox_method:
    :return np.ndarray:
    """
    if cropbox_method is None:
        cropbox_method = cropbox_central_square

    left, top, right, bottom = cropbox_method(im_arr, **kwargs)
    return im_arr[top:bottom, left:right]


def cropbox_central_square(im_arr):
    """
    Return cropbox for max-square within image array, centralized

    :param np.ndarray im_arr:
    :return tuple(int):
    """
    return cropbox_central_shape(im_arr, get_array_square_shape(im_arr))


def cropbox_off_center_random(im_arr):
    """
    Get Off-Center cropbox for image based on random "jitter"

    :param np.ndarray im_arr:
    :return (int, int, int, int):   left, top, right, bottom
    """
    jitter = float(random.choice(range(5, 10)) / 100)
    crop_cap = 1.0 - jitter

    # Determine size of image
    w, h = im_size = get_np_array_shape(im_arr)
    min_side = min(im_size)
    max_jitter = min_side * jitter / 2

    # Slightly reduce image_shape to make smaller crop_shape,
    #   so there is room for jitter of the crop box
    crop_shape = (math.floor(w * crop_cap), math.floor(h * crop_cap))

    # determine origin point for image crops
    orig_crop_box = cropbox_central_shape(im_arr, crop_shape)
    jitter_w = ffloor(max_jitter * random.uniform(-1, 1))
    jitter_h = ffloor(max_jitter * random.uniform(-1, 1))

    # apply jitter_w and jitter_h to crop_box
    left, top, right, bottom = orig_crop_box
    jitter_crop_box = (left + jitter_w, top + jitter_h, right + jitter_w, bottom + jitter_h)

    return jitter_crop_box


def cropbox_central_shape(im_arr, crop_shape=None):
    """
    Return the cropbox for an image, where you crop from the center for a given shape

    :param np.ndarray im_arr:       image array
    :param tuple(int) crop_shape:   (w, h) of the desired crop shape
    :return tuple(int):
    """
    crop_shape = get_array_square_shape(im_arr) if not crop_shape else crop_shape
    crop_w, crop_h = crop_shape
    img_w, img_h = get_np_array_shape(im_arr)
    left = (img_w - crop_w) // 2
    top = (img_h - crop_h) // 2
    right = left + crop_w
    bottom = top + crop_h
    central_crop_box = (left, top, right, bottom)
    return central_crop_box


# Operations that compute the cropbox of an array
CROPBOX_OPERATIONS = [              # relative time, out of 100
    cropbox_off_center_random,      # 20
    cropbox_central_square          # 80
]

# Operations that slice up and resample an array (e.g. vertical duping)
# TODO this can be formed with a small utility function based on function name...for now
RESAMPLE_TRANSFORMS = [                # relative time, summing to 100
    source_resample_reverse,           # 1
    source_resample_shuffle,           # 1
    source_resample_stack_vertical,    # 1
    source_resample_stack_horizontal,  # 22
    source_resample_grid,              # 23
    source_resample_phase_hor,         # 28
    source_resample_phase_vert,        # 2
    source_resample_flip_slices_vert,  # 5
    source_resample_flip_slices_hor,   # 16
]

'''
Grouping Transforms according to visual complexity
'''
D_TRANSFORMS_SIMPLE = [
    source_flip_lr,
    source_flip_ud,
    source_rotate_180,
    source_crop_random,
    source_phase_hor,
    source_phase_vert,
]

D_TRANSFORMS_COMPLEX = [
    source_offcrop_recursive,
    source_resample_random,
]