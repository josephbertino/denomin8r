import math
import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import util
import uuid
import string
import random
import string

util.prep()
fontfile = util.BOOKMAN
kern_rate = 1.0

# -----DO NOT DELETE ABOVE THIS LINE---------------------------
# TODO make a "runner" like bobFns that I can tune the parameters before running??
"""
tkinter
pysimplegui
    + https://www.pysimplegui.org/en/latest/
    + Seems like I should be able to fashion what I need with this
pyqt5

functools.partial: pretty cool, it's basically a wrapper for a function where you can pass in *some* of the args and kargs so that they are included by default, and then in the wrapped function you just pass whatever else you need to.
"""
import PySimpleGUI as sg
import inspect

sg.set_options(font=("Helvetica", 16))
sg.theme('dark grey 9')   # Add a touch of color
# All the stuff inside your window.

def get_default_args(func):
    signature = inspect.signature(func)
    return [
        (k, v.default) for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    ]
    # TODO use this instead. Generate a tuple of (arg_name, arg_type, arg_default)
    spec = inspect.getfullargspec(my_func).annotations

def simple(arg1, arg2):
    print(f"{arg1=}, {arg2=}")

default_args = get_default_args(simple)

layout = []
for arg, val in default_args:
    # Get the arg type and default value and construct the prompt
    # can use type()... and limit the types to bool (checkbox)
    # string (textbox) and float (textbox) and also probably Enums (radio buttons)
    # What to do for lists?
    dataype =
    default_val =
    ''' 
    layout = [
        [sg.Text('checkbox'), sg.Checkbox('Hell')],
        [sg.Text('checkbox'), sg.Checkbox('Heaven')]
    ]
    '''
    layout.append([])
layout.append([sg.Button('Run'), sg.Button('Cancel')])

# TODO this is how to get datatypes
# inspect.getfullargspec(simple).annotations.values()

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Ok':  # if user closes window or clicks cancel
        break
print(f"{values=}")
window.close()