"""
Library module of math-y tools, e.g. conversions
"""
import os
import math
import string
import inspect
import random
import logging
import time

import numpy as np
from PIL import Image
import pillow_avif  # Don't delete

from enum import IntEnum, auto
from matplotlib import pyplot as plt


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ROOT = '/Users/josephbertino/Desktop/CodeProjects/denomin8r'
SOURCE_DIR = os.path.join(ROOT, 'sources')
FONT_DIR = os.path.join(ROOT, 'fonts')
BOOKMAN = 'bookman.ttf'  # 'Bookman Old Style Bold'


class BitmaskMethod(IntEnum):
    BITMASK_IMG = auto()    # User provides the mask as image file
    STATIC_TEXT = auto()    # User supplies the text to turn into mask
    RANDOM_TEXT = auto()    # util.build_random_text_bitmask


class Colors(IntEnum):
    OG_ORANGE = 0xC86428
    OG_BLUE = 0x2864C8
    WHITE = 0xFFFFFF
    BLACK = 0x000000
    YELLOW = 0xfffb1c


def get_sig_details(func):
    """
    Return list of parameter details for func
    :param func: It is recommended that every param have a type
        and a default value.
        e.g. arg_one:str="Default"
    :return: list[(arg_names, arg_types, arg_defaults)]
    """
    spec = inspect.getfullargspec(func)
    defaults = spec.defaults if spec.defaults else []
    annots = spec.annotations
    names = spec.args
    if len(annots) == len(names):
        names, types = list(zip(*annots.items()))
    else:
        types = [None] * len(names)
    if len(types) == len(defaults) and len(defaults) == len(names):
        return list(zip(names, types, defaults))
    else:
        return [names, types, defaults]


def get_array_square_shape(arr):
    """
    Return shape (w, h) where both dimensions equal the shorter of the array's 2 sides, to describe a square

    :param np.ndarray arr:
    :return tuple(int):
    """
    return [min(arr.shape[:2])] * 2


def build_random_string(k=1):
    """
    Build a random string of the given length. Only AlphaNum chars
    :param int k:
    :return str:
    """
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))
    return res


def does_image_have_alpha(image):
    """
    Test if an image has an alpha channel

    :param Image.Image image:
    :return:
    """
    try:
        image.getbands().index('A')
        return True
    except ValueError:
        return False


def ffloor(n):
    """
    Like math.floor except for negative numbers it rounds *closer* to zero

    :param float n:
    :return:
    """
    if n >= 0:
        return math.floor(n)
    else:
        return math.floor(n) + 1


def random_bool():
    """Return True/False at random"""
    return random.choice([True, False])


def get_char_widths(text, font):
    char_widths = []
    for letter in text:
        letter_left, letter_top, letter_right, letter_bottom = font.getbbox(letter)
        char_widths.append(letter_right-letter_left)
    return char_widths


def make_basic_rgb_array(shape):
    """
    Make a basic 'RGB'-mode np.ndarray, which can be passed into Image.fromarray()

    :param tuple(int, int) shape:
    :return:
    """
    w, h = shape
    pixel = [255, 40, 255]
    grid = np.array([[pixel] * w] * h)
    return np.uint8(grid)


ONE_BYTE = 8
TWO_BYTE = 16
LEFT_ONE = 1 << ONE_BYTE
LEFT_TWO = 1 << TWO_BYTE


def get_color_vals(rgb):
    """
    Return individual int values for a color in hex format (0xffffff)

    :param int rgb:
    :return tuple(int):
    """
    r_val = (rgb >> TWO_BYTE) % LEFT_ONE
    g_val = (rgb >> ONE_BYTE) % LEFT_ONE
    b_val = rgb % LEFT_ONE
    return r_val, g_val, b_val


def rgb2bgr(rgb):
    """
    Convert an RGB value (0xAABBCC) to BGR (0xCCBBAA)

    :param int rgb:     range == [0x0, 0xffffff]
    :return int:        range == [0x0, 0xffffff]
    """
    r, g, b = get_color_vals(rgb)
    bgr = (b << TWO_BYTE) + (g << ONE_BYTE) + r
    return bgr


def darken_rgb(rgb):
    """
    Darken an RGB value by reducing the intensity of all three colors

    :param int rgb:     range == [0x0, 0xffffff]
    :return int:        range == [0x0, 0xffffff]
    """
    r, g, b = get_color_vals(rgb)
    darker = ((r << TWO_BYTE) // 2) + ((g << ONE_BYTE) // 2) + (b // 2)
    return darker


def get_np_array_shape(arr):
    """
    Return dimensions of np.ndarray as (w, h)

    :param np.ndarray arr:
    :return (int, int):         width, height
    """
    return tuple(list(arr.shape[:2])[::-1])


def slice_up_array_uniform(arr, num_slices=None):
    """
    Slice up an image into uniform vertical strips and return an np.ndarray of those slices
        Number of slices should be a power of 2

    :param np.ndarray arr:      Array
    :param int num_slices:      Number of slices to generate
    :return np.ndarray:         Array of <num_slices> strips
    """
    num_slices = num_slices if num_slices else 2 ** random.choice(range(1, 6))

    w, h = get_np_array_shape(arr)
    slice_width = math.ceil(w / num_slices)
    slices = []
    for i in range(num_slices):
        slices.append(arr[:, (i * slice_width):((i + 1) * slice_width)])
    return slices


def slice_resample_array_vertical(arr, num_dups=None, num_slices=None):
    """
    Slice up array into vertical strips and reorder strips
        to form <num_dups> samples of original image

    :param np.ndarray arr:
    :param num_dups:
    :param num_slices:          Number of slices to generate
    :return np.ndarray:
    """
    num_slices = num_slices if num_slices else 2 ** random.choice(range(1, 6))
    num_dups = num_dups if num_dups else random.choice(range(2,8))

    slices = slice_up_array_uniform(arr, num_slices)
    stack = []
    for dup_i in range(num_dups):
        stack.extend(slices[dup_i::num_dups])
    return np.hstack(stack)


def profile_time_source_transform(fn, im_arr):
    """
    :param fn:
    :param im_arr:
    :return int: Nanoseconds to complete fn
    """
    start = time.perf_counter_ns()
    for _ in range(40):
        fn(im_arr)
    end = time.perf_counter_ns()
    return end - start



def profile_normalize_times(fn_times):
    """
    Given a list of times (in s or ns), return that list with values representing percentage
        of total time, out of 100
    :param fn_times:
    :return:
    """
    s = sum(fn_times)
    norm_times = list(map(lambda x: math.ceil((x / s) * 100), fn_times))
    return norm_times


def profile_bar_chart(indices, values, index_label, value_label):
    """

    :param indices:
    :param values:
    :param str index_label:
    :param str value_label:
    :return:
    """
    bars = plt.bar(indices, values, color='g', width=0.25, edgecolor='grey')
    plt.xlabel(index_label, fontweight='bold', fontsize=15)
    plt.xticks(rotation=90)
    plt.ylabel(value_label, fontweight='bold', fontsize=15)
    plt.subplots_adjust(bottom=0.4)
    plt.bar_label(bars)
    plt.show()


def profile_and_plot_fns(fn_list, im_arr):
    """
    :param list fn_list:
    :param np.ndarray im_arr:
    :return:
    """
    name_times = []
    for fn in fn_list:
        total_time = profile_time_source_transform(fn, im_arr)
        name_times.append((fn.__name__, total_time))
    # name_times = sorted(name_times, key=lambda x: x[1])
    fn_names, fn_times = list(zip(*name_times))
    norm_times = profile_normalize_times(fn_times)
    profile_bar_chart(fn_names, norm_times, "Transform", "Relative Time (%)")
    return list(fn_names), list(norm_times)


# TODO can refactor this to just get the min() of all h's and w's from a list of dimensions
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
