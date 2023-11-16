"""
Library module of all methods related to transforing a source
"""
from tools import *


def get_crop_shape(crop_list, square=True):
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


# TODO this method will be scrapped for the chaos_source_transform
def random_transform(im_arr, shape):
    """
    Apply a series of transforms to an image, determined by chance
        + Flip over vertical axis
        + Crop vs. Resize

    :param np.ndarray im_arr:
    :param (int, int) shape:    width, height
    :return np.ndarray:
    """
    random.seed()
    # Flip Left-Right
    if random.random() > .5:
        im_arr = np.fliplr(im_arr)

    # Flip Up-Down
    if random.random() > .5:
        im_arr = np.flipud(im_arr)

    # Crop vs. Resize
    if random.random() > .5:
        # Crop
        im_arr = crop_central(im_arr, shape)

    # Rotate 180
    if random.random() > 0.70:
        im_arr = np.rot90(m=im_arr, k=2)

    return im_arr


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
    slices = slice_image_uniform(im_arr, num_slices)
    random.shuffle(slices)
    return np.hstack(slices)


def slice_image_resample_reverse(im_arr, n=None):
    """
    Vertically slice up image and reverse the order

    :param np.ndarray im_arr:
    :param int n:               Number of slices to generate
    :return np.ndarray:
    """
    slices = slice_image_uniform(im_arr, n)
    slices = slices[::-1]
    return np.hstack(slices)


def slice_resample_image_vertical(im_arr, num_dups, num_slices):
    """
    Slice up image into vertical strips and reorder strips
        to form <num_dups> samples of original image

    :param np.ndarray im_arr:
    :param num_dups:
    :param num_slices:          Number of slices to generate
    :return np.ndarray:
    """
    slices = slice_image_uniform(im_arr, num_slices)
    stack = []
    for dup_i in range(num_dups):
        stack.extend(slices[dup_i::num_dups])
    return np.hstack(stack)


def img_resample_stack_vertical(im_arr, num_dups, slices_per_dup):
    """
    Reorder vertical slices of an image into a stack of duplicates via uniform sampling

    :param np.ndarray im_arr:
    :param num_dups:
    :param slices_per_dup:
    :return np.ndarray:
    """
    num_slices = num_dups * slices_per_dup
    duped_im_arr = slice_resample_image_vertical(im_arr, num_dups, num_slices)
    return duped_im_arr


def img_resample_stack_horizontal(im_arr, num_dups, slices_per_dup):
    """
    Reorder horizontal slices of an image into a stack of duplicates of the original, via uniform sampling

    :param np.ndarray im_arr:
    :param num_dups:
    :param slices_per_dup:
    :return np.ndarray:
    """
    num_slices = num_dups * slices_per_dup
    rotated_im_arr = np.rot90(m=im_arr, k=1)    # 90
    duped_rotated_im_arr = slice_resample_image_vertical(rotated_im_arr, num_dups, num_slices)
    final_im_arr = np.rot90(m=duped_rotated_im_arr, k=3)    # 270
    return final_im_arr


def img_resample_grid(im_arr, num_dups_vert, num_dups_hor, slices_per_dup):
    """
    Resample crisscrossed slices of an image into a grid of duplicates via uniform sampling

    :param np.ndarray im_arr:
    :param num_dups_vert:
    :param num_dups_hor:
    :param slices_per_dup:
    :return np.ndarray:
    """
    num_slices_vert = num_dups_vert * slices_per_dup
    duped_im_arr = slice_resample_image_vertical(im_arr, num_dups_vert, num_slices_vert)
    rotated_duped_im_arr = np.rot90(m=duped_im_arr, k=1)     # 90

    num_slices_hor = num_dups_hor * slices_per_dup
    grid_im_arr = slice_resample_image_vertical(rotated_duped_im_arr, num_dups_hor, num_slices_hor)
    final_im_arr = np.rot90(m=grid_im_arr, k=3)     # 270
    return final_im_arr


def crop_im_arr(im_arr, cropbox_method=None, **kwargs):
    """
    Crop image np.ndarray according to method passed as parameter.
        If cropbox_method==None, default to tools.cropbox_central_square

    :param np.ndarray im_arr:
    :param function cropbox_method:
    :return:
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
    s = min(im_arr.shape[:2])
    return cropbox_central_shape(im_arr, (s, s))


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


def cropbox_central_shape(im_arr, crop_shape):
    """
    Return the cropbox for an image, where you crop from the center for a given shape

    :param np.ndarray im_arr:       image array
    :param tuple(int) crop_shape:   (w, h) of the desired crop shape
    :return tuple(int):
    """
    crop_w, crop_h = crop_shape
    img_w, img_h = get_np_array_shape(im_arr)
    left = (img_w - crop_w) // 2
    top = (img_h - crop_h) // 2
    right = left + crop_w
    bottom = top + crop_h
    central_crop_box = (left, top, right, bottom)
    return central_crop_box
