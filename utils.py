import math
import numpy as np

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

def simple_mask_swap(im1, im2, mask):
    """
    im1, im2, and mask all have to have the same dimensions
    :param Image.Image im1:
    :param Image.Image im2:
    :param mask:
    :return:
    """
    collage_1 = im1.copy()
    collage_2 = im2.copy()
    w, h = im1.size

    for x in range(w):
        for y in range(h):
            xy = (x, y)
            if mask[x][y] == 1:
                val = im1.getpixel(xy)
                collage_1.putpixel(xy, collage_2.getpixel(xy))
                collage_2.putpixel(xy, val)

    return collage_1, collage_2

def simple_bitmask_from_rgb(mask_src):
    """
    :param Image.Image mask_src:
    :return:
    """
    arr = np.array(mask_src)
    bitmask = np.where(np.all(arr == [0, 0, 0], axis=-1), 1, 0).transpose()
    return bitmask
