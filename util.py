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

    if n:
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


def get_crop_shape(crop_list, square=True):
    """
    Returns max size (w, h) that is not larger than any of the images in the passed list
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

    img1_over_img2 = np.where(mask, image1, image2)
    img2_over_img1 = np.where(mask, image2, image1)

    return img1_over_img2, img2_over_img1


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
    # TODO OPTIMIZATION compute the initial font size as some rough estimate function based on the image shape and font properties
    best_size = 50
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


def build_random_text_bitmask(fontfile, shape, numchars:int=None):
    """

    :param fontfile:
    :param shape:
    :param numchars:
    :return:
    """
    if not numchars:
        numchars = 4
    k = math.floor(random.random() * numchars) + 1
    text = build_random_string(k=k)
    kern_rate = random.uniform(0.75, 1.0)
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


def get_random_off_center_cropbox(img:Image=None):
    """
    Get Off-Center cropbox for image based on random "jitter"
    :param Image img:
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


def crop_off_center(img:Image=None):
    return img.crop(get_random_off_center_cropbox(img))


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
        if typename == 'list':
            layout.append([sg.Text(name), sg.Input(default_text=','.join(default_val), key=name)])
        elif typename in ('str', 'int', 'float'):
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
            typename = datatype.__name__
            if typename == 'Enum':
                # Get the Enum class hosting the options
                enum_class = default_val.__class__
                for opt in default_val._member_names_:
                    opt_key = f"{enum_class.__name__}_{opt}"
                    if values[opt_key]:
                        arg_val = enum_class[opt]
            elif typename == 'int':
                arg_val = int(values[name])
            elif typename == 'float':
                arg_val = float(values[name])
            elif typename == 'list':
                # Convert comma-delimited string into a list
                l_str = values[name]
                arg_val = l_str.split(',') if l_str else []
            else:  # types [string, bool]
                arg_val = values[name]
            arg_dict[name] = arg_val
        func(**arg_dict)


def rgb2bgr(rgb):
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

    # TODO might need smarter logic to determine position
    position = (math.floor(.71 * w), math.floor(.94 * h))
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
        fill=rgb2bgr(COLORS.OG_ORANGE)
    )
    draw.rectangle(
        ((rectangle_left, ultimate_top), (rectangle_left + text_width + (2 * extra), ultimate_bottom)),  # (lefttop, rightbottom)
        fill=rgb2bgr(COLORS.OG_ORANGE)
    )

    # Draw handle region text
    draw.text((ultimate_left + extra + lilextra, ultimate_top - extra - lilextra), "@", font=font_obj, fill="black")
    draw.text((rectangle_left + at_radius + extra, ultimate_top), "denomin8r", font=font_obj, fill="white")

    return img


def recursive_off_crop(img, mask_char:str=None):
    """
    Recursively off-crop an image with itself using a 1-character bitmask
    :param Image.Image img:
    :param mask_char: If not None, use that as the bitmask. Otherwise generate a random char for the bitmask.
    :return:
    """
    img_a = img.copy()
    img_b = img.copy()
    CLEAN_COPY = random_bool()

    # Collage off-cropped image with another off-crop of itself
    times = random.choice(range(1, 6))
    for _ in range(times):
        cropbox_a = get_random_off_center_cropbox(img_a)
        cropbox_b = get_random_off_center_cropbox(img_b)
        # Extract topleft coords from cropboxes
        topleft_a = (cropbox_a[0], cropbox_a[1])
        topleft_b = (cropbox_b[0], cropbox_b[1])

        crop_shape = get_crop_shape([cropbox_a, cropbox_b], square=False)

        img_a = crop_shape_from_coord(img_a, crop_shape, topleft_a)
        img_b = crop_shape_from_coord(img_b, crop_shape, topleft_b)

        if mask_char:
            bitmask = build_bitmask_to_size(text=mask_char, fontfile=BOOKMAN, shape=crop_shape)
        else:
            bitmask = build_random_text_bitmask(fontfile=BOOKMAN, shape=crop_shape, numchars=1)
        img_a, img_b = simple_bitmask_swap(img_a, img_b, bitmask)
        img_a = Image.fromarray(img_a)
        if CLEAN_COPY:
            img_b = img.copy()
        else:
            img_b = Image.fromarray(img_b)

    return img_a


def crop_shape_from_coord(img, crop_shape, lefttop):
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


def random_bool():
    return random.choice([True, False])


def draw_test_params(img, **kwargs):
    """
    Draw the passed kwargs key:value pairs onto the image and return the image
    Primarily used for debugging purposes
    :param img:
    :return:
    """
    w, h = img.size
    draw = ImageDraw.Draw(img)

    position = (math.floor(.05 * w), math.floor(.95 * h))
    pos_left, pos_top = position
    fontsize = math.floor(h * .03)
    fontfile = os.path.join(FONT_DIR, BOOKMAN)
    font_obj = ImageFont.truetype(fontfile, fontsize)

    # Set parameter text
    text = ""
    for k, v in kwargs.items():
        text += f"{k}={v}, "
    text_left, text_top, text_right, text_bottom = draw.textbbox(position, text, font=font_obj)
    text_width = text_right - text_left
    text_height = text_bottom - text_top
    extra = math.ceil(text_height * 0.1)  # padding

    # Draw background
    draw.rectangle(((pos_left, pos_top), (pos_left + text_width + extra, pos_top + text_height + extra)), fill="black")
    draw.text((pos_left, pos_top), text, font=font_obj, fill="red")

    return img


def classic_D_swap_random(img1=None, img2=None, force_crop_shape=None):
    """
    Make a classic collage with 2 random images and the letter 'D'
    :param img1:
    :param img2:
    :param int force_crop_shape:
    :return:
    """
    if img1 is None:
        img1 = load_sources(latest=False, n=1)[0]
    if img2 is None:
        img2 = load_sources(latest=False, n=1)[0]

    if force_crop_shape:
        if force_crop_shape == 1:
            crop_shape = img1.size
        elif force_crop_shape == 2:
            crop_shape = img2.size
    else:
        crop_shape = get_crop_shape([img1, img2], square=False)

    img1 = crop_central(img1, crop_shape)
    img2 = crop_central(img2, crop_shape)
    bitmask = build_bitmask_to_size(text='D', fontfile=BOOKMAN, shape=crop_shape)
    return simple_bitmask_swap(img1, img2, bitmask)


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
