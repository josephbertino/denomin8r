import math

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
    return 0, 0, w-1, h-1
