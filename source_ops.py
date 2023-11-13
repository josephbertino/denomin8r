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


# TODO can refactor this method so that you pass in the function you want to use to get the cropbox! (e.g. square central, random jitter)
def crop_central(im_arr, shape):
    """
    Crop the image array to the given shape, from the center of the image

    :param np.ndarray im_arr:
    :param (int, int) shape:    width, height
    :return np.ndarray:
    """
    size = get_np_array_shape(im_arr)
    cropbox = get_cropbox_central(size, shape)
    left, top, right, bottom = cropbox
    return im_arr[top:bottom, left:right]


def crop_to_square(im_arr):
    """
    Crop an image to a square based on its smaller side

    :param np.ndarray im_arr:
    :return np.ndarray:
    """
    s = min(im_arr.shape[:2])
    return crop_central(im_arr, (s, s))


def get_random_off_center_cropbox(im_arr):
    """
    Get Off-Center cropbox for image based on random "jitter"

    :param np.ndarray im_arr:
    :return (int, int, int, int):   left, top, right, bottom
    """
    jitter = float(random.choice(range(7,12)) / 100)
    crop_cap = 1.0 - jitter

    # Determine size of image
    w, h = im_size = get_np_array_shape(im_arr)
    min_side = min(im_size)
    max_jitter = min_side * jitter / 2

    # Slightly reduce image_shape to make smaller crop_shape,
    #   so there is room for jitter of the crop box
    crop_shape = (math.floor(w * crop_cap), math.floor(h * crop_cap))

    # determine origin point for image crops
    orig_crop_box = get_cropbox_central(im_size, crop_shape)
    jitter_w = ffloor(max_jitter * random.uniform(-1, 1))
    jitter_h = ffloor(max_jitter * random.uniform(-1, 1))

    # apply jitter_w and jitter_h to crop_box
    left, top, right, bottom = orig_crop_box
    jitter_crop_box = (left + jitter_w, top + jitter_h, right + jitter_w, bottom + jitter_h)

    return jitter_crop_box


def crop_off_center_random(im_arr):
    """
    Crop an np.ndarray by a random margin from the central point

    :param np.ndarray im_arr:
    :return np.ndarray:
    """
    left, top, right, bottom = get_random_off_center_cropbox(im_arr)
    return im_arr[top:bottom, left:right]


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
    else:
        # Resize
        # TODO need to fix this
        im_arr = im_arr.resize(shape)

    # Rotate
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
    slicen = num_dups * slices_per_dup
    stack = slice_resample_image_vertical(im_arr, num_dups, slicen)
    return Image.fromarray(stack)


def img_resample_stack_horizontal(im_arr, num_dups, slices_per_dup):
    """
    Reorder horizontal slices of an image into a stack of duplicates via uniform sampling

    :param np.ndarray im_arr:
    :param num_dups:
    :param slices_per_dup:
    :return np.ndarray:
    """
    slicen = num_dups * slices_per_dup
    im_arr = np.rot90(m=im_arr, k=1)
    # TODO fix this stack thing
    stack = slice_resample_image_vertical(im_arr, num_dups, slicen)
    im_arr = np.rot90(m=im_arr, k=3)
    return im_arr


def img_resample_grid(im_arr, dups_v, dups_h, slices_per_dup):
    """
    Resample crisscrossed slices of an image into a grip of duplicates via uniform sampling

    :param np.ndarray im_arr:
    :param dups_v:
    :param dups_h:
    :param slices_per_dup:
    :return np.ndarray:
    """
    slicen_v = dups_v * slices_per_dup
    # TODO fix this vstack/stack thing. Just fix the method
    vstack = slice_resample_image_vertical(im_arr, dups_v, slicen_v)
    im_arr = np.rot90(m=im_arr, k=1)
    slicen_h = dups_h * slices_per_dup
    stack = slice_resample_image_vertical(im_arr, dups_h, slicen_h)
    stack = np.rot90(m=stack, k=3)
    return stack


# TODO generalize method to crop images. Pass in the cropping function as an argument
def crop_img_with_shape(im_arr, crop_shape, lefttop):
    """
    Crop an Image from the lefttop coordinate, to the specified crop_shape
    :param np.ndarray im_arr:
    :param tuple(int) crop_shape:
    :param tuple(int) lefttop:
    :return np.ndarray:
    """
    left, top = lefttop
    w, h = crop_shape
    right = left + w
    bottom = top + h
    return im_arr[top:bottom, left:right, :]