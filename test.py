import enum
import math
import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import util
import uuid
import string
import random
import string
import PySimpleGUI as sg
import inspect

util.prep()
fontfile = util.BOOKMAN
kern_rate = 1.0

# -----DO NOT DELETE ABOVE THIS LINE---------------------------
# Off-crop an image... have a method simply off-crop an image from center
images = util.load_sources(latest=False, n=1)
img_orig = images[0]
ret_img = util.recursive_off_crop(img_orig)
ret_img.show()
