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
def me(arg1:list=['a','b'], arg2:list=[], arg3:list=['d'], arg4:list=['d', 'e']):
    print(f"{arg1=} {arg2=} {arg3=} {arg4=}")

util.fn_runner(me)