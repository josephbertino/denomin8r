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
"""
tkinter
pysimplegui
    + https://www.pysimplegui.org/en/latest/
    + Seems like I should be able to fashion what I need with this
pyqt5

functools.partial: pretty cool, it's basically a wrapper for a function where you can pass in *some* of the args and kargs so that they are included by default, and then in the wrapped function you just pass whatever else you need to.
"""

sg.set_options(font=("Helvetica", 16))
sg.theme('dark grey 9')   # Add a touch of color


def simple(arg1:str='One', arg2:bool=True):
    print(f"{arg1=}, {arg2=}")

func_args = util.get_sig_details(simple)

layout = []
for name, type, default in func_args:
    ''' 
    layout = [
        [sg.Text('checkbox'), sg.Checkbox('Hell')],
        [sg.Text('checkbox'), sg.Checkbox('Heaven')]
    ]
    '''
    layout.append([])
layout.append([sg.Button('Run'), sg.Button('Cancel')])

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Ok':  # if user closes window or clicks cancel
        break
print(f"{values=}")
window.close()