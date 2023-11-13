"""
Library module of math-y tools, e.g. conversions
"""
import os
import math
import random
import numpy as np
from PIL import Image
from enum import IntEnum, auto


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
    Like math.floor except for negative numbers it rounds CLOSER to zero
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


def get_cropbox_central(img_size, crop_shape):
    """
    Return the cropbox for an image, where you crop from the center for a given shape
    :param tuple(int) img_size:     (w, h) of the Image
    :param tuple(int) crop_shape:   (w, h) of the desired crop shape
    :return tuple(int):
    """
    crop_w, crop_h = crop_shape
    img_w, img_h = img_size
    left = (img_w - crop_w) // 2
    top = (img_h - crop_h) // 2
    right = left + crop_w
    bottom = top + crop_h
    central_crop_box = (left, top, right, bottom)
    return central_crop_box


def get_char_widths(text, font):
    char_widths = []
    for letter in text:
        letter_left, letter_top, letter_right, letter_bottom = font.getbbox(letter)
        char_widths.append(letter_right-letter_left)
    return char_widths


def make_basic_rgb_array(shape):
    """
    Make a basic 'RGB'-mode numpy array,
        which can be passed into Image.fromarray()
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