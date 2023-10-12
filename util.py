import os
import math
import random
import string
import numpy as np
from enum import IntEnum, auto
from PIL import Image, ImageFont, ImageDraw
import pillow_avif
from sortedcontainers import SortedSet
import logging
import inspect
import PySimpleGUI as sg


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ROOT = '/Users/josephbertino/PycharmProjects/denomin8r'
SOURCE_DIR = os.path.join(ROOT, 'sources')
FONT_DIR = os.path.join(ROOT, 'fonts')

SOURCE_FILES = None
BOOKMAN = 'bookman.ttf'  # 'Bookman Old Style Bold'

COLOR_WHITE = "#FFFFFF"
COLOR_BLACK = "#000000"


class BitmaskMethod(IntEnum):
    BITMASK_IMG = auto()   #
    STATIC_TEXT = auto()    # User supplies the text
    RANDOM_TEXT = auto()    # util.build_random_text_bitmask

class SourceGetter(IntEnum):
    OFF_CROPPED = auto()
    GRAB_TWO = auto()

class COLORS(IntEnum):
    OG_ORANGE = 0xC86428
    OG_BLUE = 0x2864C8


def prep():
    """
    1) All .webp files converted to .jpg
    2) All files with extension '.jpeg' renamed to '.jpg'
    """
    global SOURCE_FILES

    for root, dirs, files in os.walk("./sources/"):
        for file in files:
            if file == '.DS_Store':
                continue
            fname = file.rsplit('.', maxsplit=1)[0]
            new_file_path = os.path.join(root, fname + '.jpg')
            if not file.endswith('.jpg'):
                filepath = os.path.join(root, file)
                image = Image.open(filepath).convert(mode='RGB')
                image.save(new_file_path, format="JPEG")
                os.remove(filepath)

    os.chdir(SOURCE_DIR)
    SOURCE_FILES = SortedSet([f for f in os.listdir() if f != '.DS_Store'], key=os.path.getmtime)
    os.chdir(ROOT)


def get_specific_sources(srcs):
    """

    :param list(str) srcs:
    :return list(str):
    """
    filenames = []
    for s in srcs:
        fname = s + '.jpg'
        if fname in SOURCE_FILES:
            filenames.append(fname)
        else:
            logger.warning(f"Source file with name {s} not found!")

    return filenames


def load_sources(latest=True, n=2, specific_srcs=None):
    """
    Return 2 images from the sources directory

    :param bool latest: If True, get latest images according to name (numeric id)
    :param int n:       Number of source images to grab
    :param list(str) specific_srcs: If not empty, a list of source files to grab before grabbing the rest
    :return:
    """
    random.seed()

    filenames = []
    if specific_srcs:
        filenames = get_specific_sources(specific_srcs)
        n -= len(filenames)

    if latest:
        filenames.extend(SOURCE_FILES[(-1 * n):])
    else:
        filenames.extend(random.sample(SOURCE_FILES, n))

    sources = [Image.open(os.path.join(SOURCE_DIR, f)) for f in filenames]
    return sources


def does_image_have_alpha(image):
    """Test if an image has an alpha channel"""
    try:
        image.getbands().index('A')
        return True
    except ValueError:
        return False


def get_crop_shape(imglist, square=True):
    """
    Returns max size (w, h) that is not larger than any of the images in the passed list
    :param list imglist: List of Image.Image
    :param bool square: If True, crop dimensions should be square
    :return:
    """
    w, h = math.inf, math.inf
    for img in imglist:
        tw, th = img.size
        w = tw if tw < w else w
        h = th if th < h else h

    if square:
        return [min(w, h)] * 2
    else:
        return w, h


def get_crop_box_central(img_size, crop_shape):
    """
    Return the crop_box for an image, where you crop from the center for a given shape
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


def crop_central(image, shape):
    """
    Crop the image to the given shape, from the center of the image
    :param Image.Image image:
    :param tuple[int] shape:
    :return Image.Image:
    """
    box = get_crop_box_central(image.size, shape)
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


def simple_bitmask_swap(image1, image2, mask):
    """
    im1, im2, and mask all have to have the same dimensions
    :param Image.Image image1:
    :param Image.Image image2:
    :param mask:
    :return:
    """

    collage_1 = np.where(mask, image1, image2)
    collage_2 = np.where(mask, image2, image1)

    return collage_1, collage_2


def make_bitmask_from_bw_image(mask_src):
    """
    Convert a 3-dimensional Image (mode-'RGB') into a 2-dimensional bitmask
        Criteria: Foreground/Background (Black/White)
    :param Image.Image mask_src:
    :return np.array:
    """
    LOHI_THRESHOLD = 128
    arr = np.array(mask_src)
    bitmask = (arr[:,:,0] < LOHI_THRESHOLD) & (arr[:,:,1] < LOHI_THRESHOLD) & (arr[:,:,2] < LOHI_THRESHOLD)
    bitmask = bitmask[:,:,np.newaxis]
    return bitmask


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


def image_from_text(text, fontfile, fontsize, kern_rate):
    """
    Build an Image.Image from input text
    :param string text:
    :param str fontfile:
    :param int fontsize:
    :param float kern_rate: > 1.0 means stretch the text, < 1.0 means squeeze the text
    :return Image.Image:

    ** Credit to Harsha @ https://gist.github.com/bornfree for providing code to generate
        a "draw pad" on which to convert text to an image
    ** Credit to Steven Woerpel  @ https://stackoverflow.com/a/63182161/1975297
        for providing a method to kern text one character at a time

    """
    MAX_PADDING = 18

    # Create a Font object from the .ttf
    fontfile = os.path.join(FONT_DIR, fontfile)
    font_obj = ImageFont.truetype(fontfile, fontsize)

    # Determine the text's dimensions when printing to image
    left, top, right, bottom = font_obj.getbbox(text)
    text_height = bottom - top
    char_widths = get_char_widths(text, font_obj)
    kerned_width = int(kern_rate * sum(char_widths[:-1])) + char_widths[-1]

    # Create a new Image, which will serve as the canvas for drawing the image
    text_image = Image.new(mode='RGB', size=(kerned_width + (MAX_PADDING * 2), text_height + (MAX_PADDING * 2)), color=COLOR_WHITE)
    # Create a 'Drawing Pad' which will draw text to your image canvas
    draw = ImageDraw.Draw(text_image)

    # Draw text to your image canvas, one character at a time
    xpos = MAX_PADDING
    for letter, width in zip(text, char_widths):
        draw.text((xpos, MAX_PADDING - top), letter, font=font_obj, fill=COLOR_BLACK)
        xpos += int(kern_rate * width)

    return text_image


def get_char_widths(text, font):
    char_widths = []
    for letter in text:
        letter_left, letter_top, letter_right, letter_bottom = font.getbbox(letter)
        char_widths.append(letter_right-letter_left)
    return char_widths


def build_bitmask_to_size(text, fontfile, shape, kern_rate=1.0):
    """
    Generate Image.Image from text and font, to fit the given shape (w, h)
    :param str text:
    :param str fontfile: Name of the font file stored in FONT_DIR
    :param tuple(int) shape:
    :param float kern_rate:
    :return Image.Image :
    """
    best_size = fit_text_to_shape(text, fontfile, shape, kern_rate)
    text_image = image_from_text(text, fontfile, best_size, kern_rate)
    bitmask = make_bitmask_from_bw_image(text_image)
    bitmask = expand_bitmask_to_shape(bitmask, shape)
    return bitmask


def expand_bitmask_to_shape(bitmask, shape):
    """
    If bitmask is lacking in some dimension, add rows/columns of False to fit shape
    :param np.array bitmask:
    :param tuple(int) shape:
    :return np.array:
    """
    w, h = shape
    # np.array.shape returns (height, width)
    w_diff = w - bitmask.shape[1]
    h_diff = h - bitmask.shape[0]

    # use numpy to stack extra columns / rows around the bitmask
    if w_diff:
        curr_h = bitmask.shape[0]
        left_add, right_add = math.floor(w_diff / 2), math.ceil(w_diff / 2)
        left_stack = np.full((curr_h, left_add, 1), False)
        right_stack = np.full((curr_h, right_add, 1), False)
        bitmask = np.hstack((left_stack, bitmask, right_stack))

    if h_diff:
        curr_w = bitmask.shape[1]
        top_add, bottom_add = math.ceil(h_diff / 2), math.floor(h_diff / 2)
        top_stack = np.full((top_add, curr_w, 1), False)
        bottom_stack = np.full((bottom_add, curr_w, 1), False)
        bitmask = np.vstack((top_stack, bitmask, bottom_stack))

    return bitmask

def fit_text_to_shape(text, fontfile, shape, kern_rate):
    """

    :param str text:
    :param str fontfile:
    :param tuple(int) shape:
    :param float kern_rate:
    :return int:                The font_size to get the text_mask closest to shape without exceeding
    """
    shape_w, shape_h = shape
    # TODO due to the trial-and-error nature of this method, there's no 'best' font_size to start with. I guess smaller is better. As long as the starting text is not too large, 80 should be a good initial size
    best_size = 20
    text_image = image_from_text(text, fontfile, best_size, kern_rate)
    text_w, text_h = text_image.size

    # Get text_image as large as possible using fontfile
    while (text_w < shape_w) and (text_h < shape_h):
        WL = (shape_w - text_w) / (shape_h - text_h)
        WGR = (text_w / text_h)
        if WGR >= WL:
            # text_image will bump into source sides as it continues to grow
            size_rate = shape_w / text_w
        else:
            # text_image will bump into top/bottom as it continues to grow
            size_rate = shape_h / text_h

        # math.ceil() might push the font size slighty above optimal
        best_size = math.ceil(size_rate * best_size)
        text_image = image_from_text(text, fontfile, best_size, kern_rate)
        text_w, text_h = text_image.size

    # Reduce fontsize gradually until we are in bounds of the source images
    while (text_w > shape_w) or (text_h > shape_h):
        best_size -= 1
        text_image = image_from_text(text, fontfile, best_size, kern_rate)
        text_w, text_h = text_image.size

    return best_size


def build_random_string(k=1):
    """
    Build a random string of the given length. Only AlphaNum chars
    :param int k:
    :return:
    """
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))
    return res


def build_random_text_bitmask(fontfile, shape):
    k = math.floor(random.random() * 4) + 1
    text = build_random_string(k=k)
    kern_rate = random.choice([0.75, 0.8, 0.9, 1.0])
    bitmask = build_bitmask_to_size(text, fontfile=fontfile, shape=shape, kern_rate=kern_rate)
    return bitmask


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


def get_off_cropped_images(latest=False, jitter=0.07):
    """
    Return two images which are from the same source but slightly off-crapped from center
    :param bool latest: Use the latest image from sources?
    :param float jitter: The %age by which the cropped image can be off from center,
        relative to smaller dimension of the source image
    :return:
    """
    crop_cap = 1.0 - jitter

    # load both images
    image1, = load_sources(latest=latest, n=1)
    image2 = image1.copy()

    # Determine size of image
    w, h = image1.size
    image_square_side = min(w, h)
    max_jitter = image_square_side * jitter / 2

    # slightly reduce image_shape to make crop_shape,
    #   so there is room for jitter of the crop box
    cropped_square_side = math.floor(image_square_side * crop_cap)
    crop_shape = (cropped_square_side, cropped_square_side)

    # determine origin point for image crops
    orig_crop_box = get_crop_box_central(image1.size, crop_shape)
    jitter_crop_boxes = []
    for _ in range(2):
        jitter_w = ffloor(max_jitter * random.uniform(-1, 1))
        jitter_h = ffloor(max_jitter * random.uniform(-1, 1))

        # apply jitter_w and jitter_h to crop_box
        left, top, right, bottom = orig_crop_box
        jitter_crop_box = (left + jitter_w, top + jitter_h, right + jitter_w, bottom + jitter_h)

        jitter_crop_boxes.append(jitter_crop_box)

    image1 = image1.crop(jitter_crop_boxes[0])
    image2 = image2.crop(jitter_crop_boxes[1])

    return image1, image2


def get_sig_details(func):
    """
    Return list of parameter details for func
    :param func: Every param must have a type and a default value
        e.g. arg_one:str="Default"
    :return: list[(arg_name, arg_type, arg_default)]
    """
    spec = inspect.getfullargspec(func)
    defaults = spec.defaults
    annots = spec.annotations
    names, types = list(zip(*annots.items()))
    return list(zip(names, types, defaults))


def fn_runner(func):
    sg.set_options(font=("Helvetica", 16))
    sg.theme('dark grey 9')  # Add a touch of color
    func_args = get_sig_details(func)
    layout = []
    for name, datatype, default_val in func_args:
        typename = datatype.__name__
        if typename in ('str', 'list', 'int', 'float'):
            layout.append([sg.Text(name), sg.Input(default_text=default_val, key=name)])
        elif typename == 'bool':
            layout.append([sg.Checkbox(text=name, default=default_val, key=name)])
        elif typename == 'Enum':
            enum_name = default_val.__class__.__name__
            row = [sg.Text(enum_name)]
            for opt in default_val._member_names_:
                d = (opt == default_val.name)
                row.append(sg.Radio(text=opt, group_id=enum_name, default=d, key=f"{enum_name}_{opt}"))
            layout.append(row)
        else:
            raise Exception(f"Unexpected datatype, {name=}, {datatype=}, {default_val=}")

    layout.append([sg.Button('Run'), sg.Button('Cancel')])

    # Create the Window
    window = sg.Window('Runner', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel', 'Run'):
            window.close()
            break

    if event == 'Run':
        # For each argument in the function signature, get its value from the popup and set it, then call the runner
        arg_dict = {}
        for name, datatype, default_val in func_args:
            arg_val = None
            if datatype.__name__ == 'Enum':
                # Get the Enum class hosting the options
                enum_class = default_val.__class__
                for opt in default_val._member_names_:
                    opt_key = f"{enum_class.__name__}_{opt}"
                    if values[opt_key]:
                        arg_val = enum_class[opt]
            else:
                arg_val = values[name]
            arg_dict[name] = arg_val
        func(**arg_dict)


def RGB2BGR(rgb):
    """
    Convert an RGB value (0xAABBCC) to BGR (0xCCBBAA)
    :param int rgb:
    :return int:
    """
    one = 16 ** 2
    two = 16 ** 4
    r = rgb % one
    m = (rgb % two) - r
    l = rgb - m - r
    bgr = (r * two) + m + (l // two)
    return bgr


def draw_handle(img):
    """
    Draw the "@denomin8r" handle on bottom right of the image then return the image
    :param img:
    :return:
    """
    TEXT = "@denomin8r"
    w, h = img.size
    draw = ImageDraw.Draw(img)

    position = (math.floor(.75 * w), math.floor(.94 * h))
    ultimate_left, ultimate_top = position
    fontsize = math.floor(h * .03)
    fontfile = os.path.join(FONT_DIR, BOOKMAN)
    font_obj = ImageFont.truetype(fontfile, fontsize)

    # Determine key coordinates for placing handle
    at_left, _, at_right, _ = draw.textbbox(position, "@", font=font_obj)
    text_left, text_top, text_right, text_bottom = draw.textbbox(position, TEXT, font=font_obj)
    text_width = text_right - text_left
    text_height = text_bottom - text_top
    extra = math.ceil(text_height * 0.1)  # padding
    lilextra = math.ceil(text_height * 0.05)
    diameter = text_height + (2 * extra)
    at_radius = diameter // 2
    ultimate_bottom = ultimate_top + diameter
    rectangle_left = ultimate_left + at_radius

    # Draw handle region backgrounds
    draw.ellipse(
        ((ultimate_left, ultimate_top), (ultimate_left + diameter, ultimate_bottom)),  # (lefttop, rightbottom)
        fill=RGB2BGR(COLORS.OG_ORANGE)
    )
    draw.rectangle(
        ((rectangle_left, ultimate_top), (rectangle_left + text_width + (2 * extra), ultimate_bottom)),  # (lefttop, rightbottom)
        fill=RGB2BGR(COLORS.OG_ORANGE)
    )

    # Draw handle region text
    draw.text((ultimate_left + extra + lilextra, ultimate_top - extra - lilextra), "@", font=font_obj, fill="black")
    draw.text((rectangle_left + at_radius + extra, ultimate_top), "denomin8r", font=font_obj, fill="white")

    return img