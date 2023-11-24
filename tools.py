"""
Library module of math-y tools, e.g. conversions
"""
import os
import math
import string
import inspect
import random
import logging
import numpy as np
from PIL import Image
from enum import IntEnum, auto


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ROOT = '/Users/josephbertino/PycharmProjects/denomin8r'
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


def get_array_square_shape(im_arr):
    """
    Return shape (w, h) where both dimensions equal the shorter of the array's 2 sides, to describe a square

    :param np.ndarray im_arr:
    :return tuple(int):
    """
    return min(im_arr.shape[:2])


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


def get_np_array_shape(im_arr):
    """
    Return dimensions of np.ndarray as (w, h)

    :param np.ndarray im_arr:
    :return (int, int):         width, height
    """
    return tuple(list(im_arr.shape[:2])[::-1])
