"""
Library module of all methods related to transforing a source
"""
from PIL import Image

from tools import *


def get_crop_shape(crop_list, square=True):
    """
    Returns max dimensions (w, h) that is not larger than any of the images or cropboxes in the passed list
    :param list crop_list: List of Image.Image OR list of crop_boxes (left, top, right, bottom)
    :param bool square: If True, crop dimensions should be square
    :return:
    """
    w, h = math.inf, math.inf
    for item in crop_list:
        if isinstance(item, Image.Image):
            curr_w, curr_h = item.size
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


def crop_central(image, shape):
    """
    Crop the image to the given shape, from the center of the image
    :param Image.Image image:
    :param tuple[int] shape:
    :return Image.Image:
    """
    box = get_cropbox_central(image.size, shape)
    return image.crop(box)


def crop_to_square(image):
    """
    Crop an image to a square based on its smaller side
    :param Image.Image image:
    :return:
    """
    w, h = image.size
    s = w if w < h else h
    return crop_central(image, (s, s))


def get_random_off_center_cropbox(img:Image=None):
    """
    Get Off-Center cropbox for image based on random "jitter"
    :param Image.Image img:
    :return:
    """
    jitter = float(random.choice(range(7,12)) / 100)
    crop_cap = 1.0 - jitter

    # Determine size of image
    w, h = img.size
    min_side = min(w, h)
    max_jitter = min_side * jitter / 2

    # Slightly reduce image_shape to make smaller crop_shape,
    #   so there is room for jitter of the crop box
    crop_shape = (math.floor(w * crop_cap), math.floor(h * crop_cap))

    # determine origin point for image crops
    orig_crop_box = get_cropbox_central(img.size, crop_shape)
    jitter_w = ffloor(max_jitter * random.uniform(-1, 1))
    jitter_h = ffloor(max_jitter * random.uniform(-1, 1))

    # apply jitter_w and jitter_h to crop_box
    left, top, right, bottom = orig_crop_box
    jitter_crop_box = (left + jitter_w, top + jitter_h, right + jitter_w, bottom + jitter_h)

    return jitter_crop_box


def crop_off_center_random(img:Image=None):
    return img.crop(get_random_off_center_cropbox(img))


def random_transform(image, shape):
    """
    Apply a series of transforms to an image, determined by chance
        + Flip over vertical axis
        + Crop vs. Resize
    :param Image.Image image:
    :param tuple(int) shape:
    :return Image.Image:
    """
    random.seed()
    # Flip Left-Right
    if random.random() > .5:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)

    # Crop vs. Resize
    if random.random() > .5:
        # Crop
        image = crop_central(image, shape)
    else:
        # Resize
        image = image.resize(shape)

    # Rotate
    if random.random() > 0.75:
        image = image.rotate(angle=180)

    return image



def slice_image_uniform(img, num_slices=None):
    """
    Slice up an image into uniform vertical strips and return an np.array of those slices
    Number of slices should be a power of 2
    :param Image.Image img:
    :param int num_slices: Number of slices to generate
    :return np.array: Array of image strips, len()==num_slices
    """
    arr = np.array(img)
    num_slices = num_slices if num_slices else 2 ** random.choice(range(1, 6))
    w = img.size[0]  # width
    slice_width = math.ceil(w / num_slices)
    slices = []
    for i in range(num_slices):
        slices.append(arr[:,(i * slice_width):((i + 1) * slice_width)])
    return slices


def slice_image_resample_random(img, num_slices=None):
    """
    Vertically slice up image and rearrange the slices randomly
        Return image as np.array
    :param Image.Image img:
    :param int num_slices: Number of slices to generate
    :return np.array:
    """
    slices = slice_image_uniform(img, num_slices)
    random.shuffle(slices)
    return np.hstack(slices)


def slice_image_resample_reverse(img, n=None):
    """
    Vertically slice up image and reverse the order
    :param Image.Image img:
    :param int n: Number of slices to generate
    :return np.array:
    """
    slices = slice_image_uniform(img, n)
    slices = slices[::-1]
    return np.hstack(slices)


def slice_resample_image_vertical(img, num_dups, num_slices):
    """
    Slice up image into vertical strips and reorder strips
        to form <num_dups> samples of original image
    :param img:
    :param num_dups:
    :param num_slices: Number of slices to generate
    :return np.array:
    """
    slices = slice_image_uniform(img, num_slices)
    stack = []
    for dup_i in range(num_dups):
        stack.extend(slices[dup_i::num_dups])
    return np.hstack(stack)


def img_resample_stack_vertical(img, num_dups, slices_per_dup):
    """
    Reorder vertical slices of an image into a stack of duplicates via uniform sampling
    :param img:
    :param num_dups:
    :param slices_per_dup:
    :return Image.Image:
    """
    slicen = num_dups * slices_per_dup
    stack = slice_resample_image_vertical(img, num_dups, slicen)
    return Image.fromarray(stack)


def img_resample_stack_horizontal(img, num_dups, slices_per_dup):
    """
    Reorder horizontal slices of an image into a stack of duplicates via uniform sampling
    :param Image.Image img:
    :param num_dups:
    :param slices_per_dup:
    :return Image.Image:
    """
    slicen = num_dups * slices_per_dup
    img = img.rotate(angle=90, expand=True)
    stack = slice_resample_image_vertical(img, num_dups, slicen)
    dupimg = Image.fromarray(stack)
    return dupimg.rotate(angle=270, expand=True)


def img_resample_grid(img, dups_v, dups_h, slices_per_dup):
    """
    Resample crisscrossed slices of an image into a grip of duplicates via uniform sampling
    :param Image.Image img:
    :param dups_v:
    :param dups_h:
    :param slices_per_dup:
    :return Image.Image:
    """
    slicen_v = dups_v * slices_per_dup
    vstack = slice_resample_image_vertical(img, dups_v, slicen_v)
    img = Image.fromarray(vstack)
    img = img.rotate(angle=90, expand=True)
    slicen_h = dups_h * slices_per_dup
    stack = slice_resample_image_vertical(img, dups_h, slicen_h)
    dupimg = Image.fromarray(stack)
    return dupimg.rotate(angle=270, expand=True)


def crop_img_with_shape(img, crop_shape, lefttop):
    """
    Crop an Image from the lefttop coordinate, to the specified crop_shape
    :param Image.Image img:
    :param tuple(int) crop_shape:
    :param tuple(int) lefttop:
    :return:
    """
    left, top = lefttop
    w, h = crop_shape
    right = left + w
    bottom = top + h
    cropbox = (left, top, right, bottom)
    return img.crop(cropbox)