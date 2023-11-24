"""
Library module for mask-related operations
"""
from PIL import Image, ImageDraw, ImageFont
from tools import *

def build_random_text_bitmask(fontfile, shape, numchars:int=None):
    """

    :param fontfile:
    :param shape:
    :param numchars:
    :return np.ndarray:
    """
    if not numchars:
        numchars = 4
    k = math.floor(random.random() * numchars) + 1
    text = build_random_string(k=k)
    kern_rate = random.uniform(0.75, 1.0)
    bitmask = build_bitmask_to_size(text, fontfile=fontfile, shape=shape, kern_rate=kern_rate)
    return bitmask


def build_mask_from_text(text, fontfile, fontsize, kern_rate):
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
    text_image = Image.new(
        mode='RGB', size=(kerned_width + (MAX_PADDING * 2), text_height + (MAX_PADDING * 2)), color=Colors.WHITE)
    # Create a 'Drawing Pad' which will draw text to your image canvas
    draw = ImageDraw.Draw(text_image)

    # Draw text to your image canvas, one character at a time
    xpos = MAX_PADDING
    for letter, width in zip(text, char_widths):
        draw.text((xpos, MAX_PADDING - top), letter, font=font_obj, fill=Colors.BLACK)
        xpos += int(kern_rate * width)

    return text_image



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
    text_image = build_mask_from_text(text, fontfile, best_size, kern_rate)
    bitmask = make_bitmask_from_bw_image(text_image)
    bitmask = expand_bitmask_to_shape(bitmask, shape)
    return bitmask


def simple_bitmask_swap(image1, image2, mask):
    """
    im1, im2, and mask all have to have the same dimensions
    :param np.ndarray image1:
    :param np.ndarray image2:
    :param np.ndarray mask:
    :return tuple(np.ndarray) :
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
    Determine maximum fonsize for text in a bitmask of specified shape
    :param str text:
    :param str fontfile:
    :param tuple(int) shape:
    :param float kern_rate:
    :return int:                The font_size to get the text_mask closest to shape without exceeding
    """
    shape_w, shape_h = shape
    # TODO (later) OPTIMIZATION compute the initial font size as some rough estimate function based on the image shape and font properties
    best_size = 50
    text_image = build_mask_from_text(text, fontfile, best_size, kern_rate)
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
        text_image = build_mask_from_text(text, fontfile, best_size, kern_rate)
        text_w, text_h = text_image.size

    # Reduce fontsize gradually until we are in bounds of the source images
    while (text_w > shape_w) or (text_h > shape_h):
        best_size -= 1
        text_image = build_mask_from_text(text, fontfile, best_size, kern_rate)
        text_w, text_h = text_image.size

    return best_size
