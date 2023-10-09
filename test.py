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

sg.set_options(font=("Helvetica", 16))
sg.theme('dark grey 9')   # Add a touch of color

def simple(arg1:enum.Enum = util.BitmaskMethod.BITMASK_IMG, arg2:str = "one"):
    print(f"{arg1=}, {arg2=}")

func_args = util.get_sig_details(simple)
layout = []
for name, datatype, default_val in func_args:
    typename = datatype.__name__
    if typename in ('str', 'list', 'int', 'float'):
        layout.append([sg.Text(name), sg.Input(default_text=default_val, key=name)])
    elif typename == 'bool':
        layout.append([sg.Checkbox(text=name, default=default_val, key=name)])
    elif typename == 'Enum':
        enum_name = default_val.__class__.__name__
        row = [sg.Text(enum_name)]
        for opt in default_val._member_names_:
            d = (opt == default_val.name)
            row.append(sg.Radio(text=opt, group_id=enum_name, default=d, key=f"{enum_name}_{opt}"))
        layout.append(row)
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
    # For each argument in the function signature, get its value from the popup and set it, then call the runner
    arg_dict = {}
    for name, datatype, default_val in func_args:
        if datatype.__name__ == 'Enum':
            optclass = default_val.__class__
            for opt in default_val._member_names_:
                opt_key = f"{optclass.__name__}_{opt}"
                if values[opt_key]:
                    arg_val = optclass[opt]
        else:
            arg_val = values[name]
        arg_dict[name] = arg_val
    simple(**arg_dict)