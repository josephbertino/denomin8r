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

def img_filter_black_white(imgarr):
    """
    Filters a 3D array of RGB pixels so that all pixels "close to" black become
        black and all pixels "close to" white become white
    :param Image.Image imgarr:
    :return: Image.Image
    """
    LOHI_THRESHOLD = 128
    filtered = np.copy(imgarr)
    blacks = (filtered[:,:,0] < LOHI_THRESHOLD) & (filtered[:,:,1] < LOHI_THRESHOLD) & (filtered[:,:,2] < LOHI_THRESHOLD)
    filtered[blacks] = [0, 0, 0]
    filtered[~blacks] = [255, 255, 255]
    return filtered

def make_bitmask_from_black_white(mask_src):
    """
    Convert a 3-dimensional Image (mode-'RGB') into a 2-dimensional bitmask
        Criteria: Foreground/Background (Black/White)
    :param Image.Image mask_src:
    :return:
    """
    mask_arr = np.array(mask_src)
    filtered_mask_arr = img_filter_black_white(mask_arr)
    bitmask = np.where(np.all(filtered_mask_arr == [0, 0, 0], axis=-1), 1, 0).transpose()
    return bitmask
