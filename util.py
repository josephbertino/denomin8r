import os
import math
import random
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import pillow_avif

ROOT = '/Users/josephbertino/PycharmProjects/denomin8r'
SOURCE_DIR = os.path.join(ROOT, 'sources')
FONT_DIR = os.path.join(ROOT, 'fonts')

SOURCE_IMAGES = []
FONTFACE = 'Bookman Old Style Bold'

COLOR_WHITE = "#FFFFFF"
COLOR_BLACK = "#000000"


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


def get_crop_size(imglist):
    """
    Returns max size (w, h) that is not larger than any of the images in the passed list
    """
    w, h = math.inf, math.inf
    for img in imglist:
        tw, th = img.size
        w = tw if tw < w else w
        h = th if th < h else h
    return w, h


def get_crop_box(w, h):
    """
    Returns params to pass to Image.crop()
    Note that coord (0,0) of an Image is the top-left corner
    """
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


def make_basic_rgb_array(w, h):
    """
    Make a basic 'RGB'-mode numpy array,
        which can be passed into Image.fromarray()
    :param int w: Width
    :param int h: Height
    :return:
    """
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


def make_bitmask_from_black_white(mask_src):
    """
    Convert a 3-dimensional Image (mode-'RGB') into a 2-dimensional bitmask
        Criteria: Foreground/Background (Black/White)
    :param Image.Image mask_src:
    :return:
    """
    LOHI_THRESHOLD = 128
    arr = np.array(mask_src)
    bitmask = (arr[:,:,0] < LOHI_THRESHOLD) & (arr[:,:,1] < LOHI_THRESHOLD) & (arr[:,:,2] < LOHI_THRESHOLD)
    bitmask = bitmask[:,:,np.newaxis]
    return bitmask


def random_transform(image, crop_size):
    """
    Apply a series of transforms to an image, determined by change
        + Flip over vertical axis
        + Crop vs. Resize
            + If Crop, Crop from Top/Left vs. Bottom/Right vs. Center
    :param Image.Image image:
    :param tuple[int, int] crop_size:
    :return Image.Image:
    """
    random.seed()
    # Flip Left-Right
    if random.random() > .5:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)

    # Crop vs. Resize
    if random.random() > .5:
        # Crop
        image = crop_central(image, crop_size)
    else:
        # Resize
        image = image.resize(crop_size)

    # Rotate
    rotate = random.sample([0,1,2,3], 1)
    image = image.rotate(angle=rotate * 90)

    return image


def image_from_text(text, size, kern_rate):
    """
    Build an Image.Image from input text
    :param string text:
    :param int size:
    :param float kern_rate: > 1.0 means stretch the text, < 1.0 means squeeze the text
    :return Image.Image:

    ** Credit to "Harsha" @ https://gist.github.com/bornfree for providing code to generate
        a "draw pad" on which to convert text to an image
    ** Credit to Steven Woerpel  @ https://stackoverflow.com/a/63182161/1975297
        for providing a method to kern text one character at a time

    """
    MAX_PADDING = 18

    # Create a Font object from the .ttf
    fontfile = os.path.join(FONT_DIR, 'bookman.ttf')
    font = ImageFont.truetype(fontfile, size)

    # Determine the text's dimensions when printing to image
    left, top, right, bottom = font.getbbox(text)
    text_width = right - left
    text_height = bottom - top
    char_widths = get_char_widths(text, font)
    kerned_width = int(kern_rate * sum(char_widths[:-1])) + char_widths[-1]
    print(f"{text_width=}")
    print(text_width * kern_rate)

    # Create a new Image, which will serve as the canvas for drawing the image
    text_image = Image.new(mode='RGB', size=(kerned_width + (MAX_PADDING * 2), text_height + (MAX_PADDING * 2)), color=COLOR_WHITE)
    # Create a 'Drawing Pad' which will draw text to your image canvas
    draw = ImageDraw.Draw(text_image)

    # Draw text to your image canvas, one character at a time
    xpos = MAX_PADDING
    for letter, width in zip(text, char_widths):
        draw.text((xpos, MAX_PADDING - top), letter, font=font, fill=COLOR_BLACK)
        xpos += int(kern_rate * width)

    return text_image


def get_char_widths(text, font):
    char_widths = []
    for letter in text:
        letter_left, letter_top, letter_right, letter_bottom = font.getbbox(letter)
        char_widths.append(letter_right-letter_left)
    return char_widths