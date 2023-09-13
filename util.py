import os
import math
import random
import string
import numpy as np
from enum import IntEnum, auto
from PIL import Image, ImageFont, ImageDraw
import pillow_avif

ROOT = '/Users/josephbertino/PycharmProjects/denomin8r'
SOURCE_DIR = os.path.join(ROOT, 'sources')
FONT_DIR = os.path.join(ROOT, 'fonts')

SOURCE_IMAGES = []
BOOKMAN = 'bookman.ttf'  # 'Bookman Old Style Bold'

COLOR_WHITE = "#FFFFFF"
COLOR_BLACK = "#000000"


class BitmaskMethod(IntEnum):
    MASK_IMG = auto()   #
    STATIC_TEXT = auto()    # User supplies the text
    RANDOM_TEXT = auto()    # util.build_random_text_bitmask


def prep():
    """
    1) All .webp files converted to .jpg
    2) All files with extension '.jpeg' renamed to '.jpg'
    """
    global SOURCE_IMAGES

    for root, dirs, files in os.walk("./sources/"):
        for file in files:
            if file == '.DS_Store':
                continue
            fname = file.rsplit('.', maxsplit=1)[0]
            new_file_path = os.path.join(root, fname + '.jpg')
            if not file.endswith('.jpg'):
                filepath = os.path.join(root, file)
                image = Image.open(filepath)
                if does_image_have_alpha(image):
                    image = image.convert(mode='RGB')
                image.save(new_file_path, format="JPEG")
                os.remove(filepath)

    os.chdir(SOURCE_DIR)
    files = os.listdir()
    files = [f for f in files if f != '.DS_Store']
    SOURCE_IMAGES = sorted(files, key=os.path.getmtime)
    os.chdir(ROOT)


def load_images(latest=True):
    """
    Return 2 images from the sources directory

    :param bool latest: If True, get latest images according to name (numeric id)
    :return:
    """
    random.seed()
    if latest:
        imfiles = SOURCE_IMAGES[-2:]
    else:
        imfiles = random.sample(SOURCE_IMAGES,2)

    images = []
    for f in imfiles:
        images.append(Image.open(os.path.join(SOURCE_DIR, f)))
    return images


def does_image_have_alpha(image):
    """Test if an image has an alpha channel"""
    try:
        image.getbands().index('A')
        return True
    except ValueError:
        return False


def get_crop_size(imglist, square=True):
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
        return [min([w, h])] * 2
    else:
        return w, h


def get_crop_box(shape):
    """
    Returns params to pass to Image.crop()
    Note that coord (0,0) of an Image is the top-left corner
    """
    w, h = shape
    return 0, 0, 0+w, 0+h


def crop_central(image, shape):
    """
    Crop the image to the given w, h but from the center of the image
    :param Image.Image image:
    :param tuple[int] shape:
    :return Image.Image:
    """
    crop_w, crop_h = shape
    img_w, img_h = image.size
    box = ((img_w - crop_w) // 2, (img_h - crop_h) // 2, (img_w + crop_w) // 2, (img_h + crop_h) // 2)
    cropped = image.crop(box)
    return cropped


def crop_square(image):
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


def simple_mask_swap(image1, image2, mask):
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
    Apply a series of transforms to an image, determined by change
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


def build_mask_to_size(text, fontfile, shape, kern_rate):
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
    :return int:            The font_size to get the text_mask closest to shape without exceeding
    """
    shape_w, shape_h = shape
    # TODO due to the trial-and-error nature of this method, there's no 'best' font_size to start with. I guess smaller is better. As long as the starting text is not too large, 80 should be a good initial size
    best_size = 80
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
    bitmask = build_mask_to_size(text, fontfile=fontfile, shape=shape, kern_rate=kern_rate)
    return bitmask
