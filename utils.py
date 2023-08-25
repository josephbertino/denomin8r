import os
import math
import numpy as np
from PIL import Image

# Load the webp image
image = Image.open("image.webp")

# Convert the image to jpg
image.save("image.jpg", format="JPEG")


def prep():
    """
    1) All .webp files converted to .jpg
    2) All files with extension '.jpeg' renamed to '.jpg'
    """
    for root, dirs, files in os.walk("./"):
        for file in files:
            fname = file.rsplit('.', maxsplit=1)[0]
            new_name = fname + '.jpg'
            if file.endswith('.jpeg'):
                os.rename(file, new_name)
            elif file.endswith('.webp'):
                image = Image.open(file)
                image.save(new_name, format="JPEG")


def get_max_size(imglist):
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


def crop_central(image, crop_w, crop_h):
    """
    Crop the image to the given w, h but from the center of the image
    :param Image.Image image:
    :param int crop_w:
    :param int crop_h:
    :return Image.Image:
    """
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
    return crop_central(image, s, s)


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