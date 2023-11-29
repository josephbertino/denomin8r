"""
Library module of all methods related to transforing a source

Notes:
    1) Please try to enforce the standard where source transform method signatures have 'im_arr'
        as their first parameter, and all other parameters are kwargs with default values
"""
from mask_ops import *

# Source Transforms. All must accept only the image np.ndarray, and return an np.ndarray
def source_flip_lr(im_arr):
    """
    Flip L-R an image array

    :param np.ndarray im_arr:
    :return np.ndarray:
    """
    return np.fliplr(im_arr)


def source_flip_ud(im_arr):
    """
    Flip U-D an image array

    :param np.ndarray im_arr:
    :return np.ndarray:
    """
    return np.flipud(im_arr)


def source_rotate_180(im_arr):
    """
    Rotate 180 degrees an image array

    :param np.ndarray im_arr:
    :return np.ndarray:
    """
    return np.rot90(m=im_arr, k=2)


def source_crop_random(im_arr):
    """
    Apply cropping to image array with a randomly-selected method

    :param np.ndarray im_arr:
    :return np.ndarray:
    """
    cropbox_method = random.choice(CROPBOX_OPERATIONS)
    cropped_im_arr = crop_im_arr(im_arr=im_arr, cropbox_method=cropbox_method)
    return cropped_im_arr


MIN_DUPS = 2
MAX_DUPS = 7

def source_slice_random(im_arr):
    """
    Apply slice-duping to image array with a randomly-selected method

    :param np.ndarray im_arr:
    :return np.ndarray:
    """
    slice_method = random.choice(SLICE_OPERATIONS)
    method_name = slice_method.__name__
    logger.info(f"Implementing SLICE method {method_name}")

    sliced_im_arr = slice_method(im_arr)
    return sliced_im_arr


def get_common_crop_shape(crop_list, square=True):
    """
    Return max dimensions (w, h) that is not larger than any of the image arrays or cropboxes in the passed list

    :param list crop_list:  List of np.ndarray OR list of crop_boxes (left, top, right, bottom)
    :param bool square:     If True, crop dimensions should be square
    :return (int, int):     width, height
    """
    w, h = math.inf, math.inf
    for item in crop_list:
        if isinstance(item, np.ndarray):
            curr_w, curr_h = get_np_array_shape(item)
        elif isinstance(item, list | tuple) and len(item) == 4:
            l, t, r, b = item
            curr_w = r - l
            curr_h = b - t
        else:
            raise Exception(f"Unexpected type passed to get_crop_shape: {item}, {type(item)}")
        w = curr_w if curr_w < w else w
        h = curr_h if curr_h < h else h

    if square:
        return [min(w, h)] * 2
    else:
        return w, h


def slice_image_uniform(im_arr, num_slices=None):
    """
    Slice up an image into uniform vertical strips and return an np.ndarray of those slices
        Number of slices should be a power of 2

    :param np.ndarray im_arr:
    :param int num_slices:      Number of slices to generate
    :return np.ndarray:         Array of image strips, len() == num_slices
    """
    num_slices = num_slices if num_slices else 2 ** random.choice(range(1, 6))

    w, h = get_np_array_shape(im_arr)
    slice_width = math.ceil(w / num_slices)
    slices = []
    for i in range(num_slices):
        slices.append(im_arr[:, (i * slice_width):((i + 1) * slice_width)])
    return slices


def slice_image_resample_random(im_arr, num_slices=None):
    """
    Vertically slice up image and rearrange the slices randomly
        Return image as np.ndarray

    :param np.ndarray im_arr:
    :param int num_slices:      Number of slices to generate
    :return np.ndarray:
    """
    num_slices = num_slices if num_slices else 2 ** random.choice(range(1, 6))

    slices = slice_image_uniform(im_arr, num_slices)
    random.shuffle(slices)
    return np.hstack(slices)


def slice_image_resample_reverse(im_arr, num_slices=None):
    """
    Vertically slice up image and reverse the order

    :param np.ndarray im_arr:
    :param int num_slices:               Number of slices to generate
    :return np.ndarray:
    """
    num_slices = num_slices if num_slices else 2 ** random.choice(range(1, 6))

    slices = slice_image_uniform(im_arr, num_slices)
    slices = slices[::-1]
    return np.hstack(slices)


def slice_resample_image_vertical(im_arr, num_dups=None, num_slices=None):
    """
    Slice up image into vertical strips and reorder strips
        to form <num_dups> samples of original image

    :param np.ndarray im_arr:
    :param num_dups:
    :param num_slices:          Number of slices to generate
    :return np.ndarray:
    """
    num_slices = num_slices if num_slices else 2 ** random.choice(range(1, 6))
    num_dups = num_dups if num_dups else random.choice(range(2,8))

    slices = slice_image_uniform(im_arr, num_slices)
    stack = []
    for dup_i in range(num_dups):
        stack.extend(slices[dup_i::num_dups])
    return np.hstack(stack)


def img_resample_stack_vertical(im_arr, num_dups=None, num_slices_per_dup=None):
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
    duped_im_arr = slice_resample_image_vertical(im_arr, num_dups, num_slices)
    return duped_im_arr


def img_resample_stack_horizontal(im_arr, num_dups=None, num_slices_per_dup=None):
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
    duped_rotated_im_arr = slice_resample_image_vertical(rotated_im_arr, num_dups, num_slices)
    final_im_arr = np.rot90(m=duped_rotated_im_arr, k=3)    # 270
    return final_im_arr


def img_resample_grid(im_arr, num_dups_vert=None, num_dups_hor=None, num_slices_per_dup=None):
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
    duped_im_arr = slice_resample_image_vertical(im_arr, num_dups_vert, num_slices_vert)
    rotated_duped_im_arr = np.rot90(m=duped_im_arr, k=1)     # 90

    num_slices_hor = num_dups_hor * num_slices_per_dup
    grid_im_arr = slice_resample_image_vertical(rotated_duped_im_arr, num_dups_hor, num_slices_hor)
    final_im_arr = np.rot90(m=grid_im_arr, k=3)     # 270
    return final_im_arr


def crop_offcrop_recursive(im_arr, mask_text:str=None):
    """
    Recursively off-crop an image with itself using a bitmask

    :param np.ndarray im_arr:
    :param mask_text: If not None, use that as the bitmask. Otherwise generate a random char for the bitmask.
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


# Methods that return cropboxes
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
    jitter = float(random.choice(range(7, 12)) / 100)
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

CROPBOX_OPERATIONS = [
    cropbox_off_center_random,
    cropbox_central_square
]

SLICE_OPERATIONS = [
    slice_image_resample_reverse,
    slice_image_resample_random,
    img_resample_stack_vertical,
    img_resample_stack_horizontal,
    img_resample_grid
]

