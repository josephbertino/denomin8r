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
TEXT = "@ denomin8r"
img = Image.open(f'./stickers/set 1 - 20231010/D{2}.jpg')
img = util.draw_handle(img)
img.show()