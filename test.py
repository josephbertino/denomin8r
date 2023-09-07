import math
import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import util
import uuid

util.prep()
fontfile = util.BOOKMAN
kern_rate = 1.0

text = 'D'
source_w, source_h = 700, 500
source_shape = (source_w, source_h)
font_size = source_h
print(f"{text=}")
print(f"{font_size=}")
print()
trial = util.image_from_text(text, fontfile, font_size, kern_rate)
w, h = trial.size

# get text image as large as possible using fontfile
while (w < source_w) and (h < source_h):
    WL = (source_w - w) / (source_h - h)
    WGR = (w / h)
    print(f"{w=}, {h=}")
    print(f"{WL=}")
    print(f"{WGR=}")
    if WGR >= WL:
        size_rate = source_w / w
    else:
        size_rate = source_h / h
    print(f"{size_rate=}")

    # math.ceil() might push the font size slighty above optimal
    font_size = math.ceil(size_rate * font_size)
    print(f"{font_size=}")
    trial = util.image_from_text(text, fontfile, font_size, kern_rate)
    w, h = trial.size
    print(f"{trial.size=}, {source_shape=}")
    print()

# Reduce fontsize gradually until we are in bounds of the source images
while (w > source_w) or (h > source_h):
    font_size -= 1
    print(f"{font_size=}")
    trial = util.image_from_text(text, fontfile, font_size, kern_rate)
    w, h = trial.size
    print(f"{trial.size=}, {source_shape=}")
    print()

# final refinement of text image, fitting to source
print(trial.size, source_shape)

# This method was for some crude testing
def put_aside():
    for N in range(200, 1000, 50):
        for M in range(200, 1000, 50):
            for text in ['i', 'I', 'D', 'PUSH', 'OOOOOO']:
                print('----------------------')
                trial = util.image_from_text(text, fontfile, font_size, kern_rate)
                left, top, right, bottom = trial.getbbox()
                trial_shape = (right - left, bottom - top)
                source_shape = (N, M)
                print(f"{text=}")
                print(f"{trial_shape=}, {source_shape=}")
                w, h = trial_shape
                WL = (N - w) / (M - h)
                HL = 1 / WL
                WGR = (w / h)
                HGR = 1 / WGR
                print()
                print(f"{(N-w)=}, {(M-h)=}")
                print(f"{WL=}, {HL=}")
                print(f"{WGR=}, {HGR=}")
                print(f"{(WGR >= WL)=}, {(HGR >= HL)=}")

                assert (WGR >= WL) or (HGR >= HL)

    print('done')
