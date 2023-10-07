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
# TODO make a "runner" like bobFns that I can tune the parameters before running??


sg.set_options(font=("Helvetica", 16))
sg.theme('dark grey 9')   # Add a touch of color


def simple(arg1:str = 'One', arg2:bool = True):
    print(f"{arg1=}, {arg2=}")

func_args = util.get_sig_details(simple)

layout = []
for name, datatype, default_val in func_args:
    typename = datatype.__name__
    if typename in ('str', 'list', 'int', 'float'):
        # TODO Label and Text Input
        pass
    elif typename == 'bool':
        # TODO Checkbox
        pass
    elif typename == 'Enum':
        # TODO Label and radio buttons for all options
        pass
    else:
        raise Exception(f"Unexpected datatype, {name=}, {datatype=}, {default_val=}")

layout.append([sg.Button('Run'), sg.Button('Cancel')])

# Create the Window
window = sg.Window('Runner', layout)
# Event Loop to process "events" and get the "values" of the inputs

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel', 'Run'):
        window.close()
        break

if event == 'Run':
    # TODO run method with parameters set
    pass