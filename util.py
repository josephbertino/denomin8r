import string
from PIL import Image
import pillow_avif
from sortedcontainers import SortedSet
import logging
import inspect
import PySimpleGUI as sg

from mask_ops import *
from source_ops import *


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SOURCE_FILES = None


def prep():
    """
    1) All .webp files converted to .jpg
    2) All files with extension '.jpeg' renamed to '.jpg'
    """
    global SOURCE_FILES

    for root, dirs, files in os.walk("./sources/"):
        for file in files:
            if file == '.DS_Store':
                continue
            fname = file.rsplit('.', maxsplit=1)[0]
            new_file_path = os.path.join(root, fname + '.jpg')
            if not file.endswith('.jpg'):
                filepath = os.path.join(root, file)
                image = Image.open(filepath).convert(mode='RGB')
                image.save(new_file_path, format="JPEG")
                os.remove(filepath)

    os.chdir(SOURCE_DIR)
    SOURCE_FILES = SortedSet([f for f in os.listdir() if f != '.DS_Store'], key=os.path.getmtime)
    os.chdir(ROOT)


def get_specific_sources(srcs):
    """

    :param list(str) srcs:
    :return list(str):
    """
    filenames = []
    for s in srcs:
        fname = s + '.jpg'
        if fname in SOURCE_FILES:
            filenames.append(fname)
        else:
            logger.warning(f"Source file with name {s} not found!")

    return filenames


def load_sources(latest=True, n=2, specific_srcs=None):
    """
    Return 2 images from the sources directory

    :param bool latest: If True, get latest images according to name (numeric id)
    :param int n:       Number of source images to grab
    :param list(str) specific_srcs: If not empty, a list of source files to grab before grabbing the rest
    :return:
    """
    random.seed()

    filenames = []
    if specific_srcs:
        filenames = get_specific_sources(specific_srcs)
        n -= len(filenames)

    if n:
        if latest:
            filenames.extend(SOURCE_FILES[(-1 * n):])
        else:
            filenames.extend(random.sample(SOURCE_FILES, n))

    sources = [Image.open(os.path.join(SOURCE_DIR, f)) for f in filenames]
    return sources


def recursive_off_crop(img, mask_char:str=None):
    """
    Recursively off-crop an image with itself using a 1-character bitmask
    :param Image.Image img:
    :param mask_char: If not None, use that as the bitmask. Otherwise generate a random char for the bitmask.
    :return:
    """
    img_a = img.copy()
    img_b = img.copy()
    CLEAN_COPY = random_bool()

    # Collage off-cropped image with another off-crop of itself
    times = random.choice(range(1, 6))
    for _ in range(times):
        cropbox_a = get_random_off_center_cropbox(img_a)
        cropbox_b = get_random_off_center_cropbox(img_b)
        # Extract topleft coords from cropboxes
        topleft_a = (cropbox_a[0], cropbox_a[1])
        topleft_b = (cropbox_b[0], cropbox_b[1])

        crop_shape = get_crop_shape([cropbox_a, cropbox_b], square=False)

        img_a = crop_img_with_shape(img_a, crop_shape, topleft_a)
        img_b = crop_img_with_shape(img_b, crop_shape, topleft_b)

        if mask_char:
            bitmask = build_bitmask_to_size(text=mask_char, fontfile=BOOKMAN, shape=crop_shape)
        else:
            bitmask = build_random_text_bitmask(fontfile=BOOKMAN, shape=crop_shape, numchars=1)
        img_a, img_b = simple_bitmask_swap(img_a, img_b, bitmask)
        img_a = Image.fromarray(img_a)
        if CLEAN_COPY:
            img_b = img.copy()
        else:
            img_b = Image.fromarray(img_b)

    return img_a


def build_random_string(k=1):
    """
    Build a random string of the given length. Only AlphaNum chars
    :param int k:
    :return:
    """
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))
    return res


def build_random_text_bitmask(fontfile, shape, numchars:int=None):
    """

    :param fontfile:
    :param shape:
    :param numchars:
    :return:
    """
    if not numchars:
        numchars = 4
    k = math.floor(random.random() * numchars) + 1
    text = build_random_string(k=k)
    kern_rate = random.uniform(0.75, 1.0)
    bitmask = build_bitmask_to_size(text, fontfile=fontfile, shape=shape, kern_rate=kern_rate)
    return bitmask


def get_sig_details(func):
    """
    Return list of parameter details for func
    :param func: Every param must have a type and a default value
        e.g. arg_one:str="Default"
    :return: list[(arg_name, arg_type, arg_default)]
    """
    spec = inspect.getfullargspec(func)
    defaults = spec.defaults
    annots = spec.annotations
    names, types = list(zip(*annots.items()))
    return list(zip(names, types, defaults))


def fn_runner(func):
    sg.set_options(font=("Helvetica", 16))
    sg.theme('dark grey 9')  # Add a touch of color
    func_args = get_sig_details(func)
    layout = []
    for name, datatype, default_val in func_args:
        typename = datatype.__name__
        if typename == 'list':
            layout.append([sg.Text(name), sg.Input(default_text=','.join(default_val), key=name)])
        elif typename in ('str', 'int', 'float'):
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
            arg_val = None
            typename = datatype.__name__
            if typename == 'Enum':
                # Get the Enum class hosting the options
                enum_class = default_val.__class__
                for opt in default_val._member_names_:
                    opt_key = f"{enum_class.__name__}_{opt}"
                    if values[opt_key]:
                        arg_val = enum_class[opt]
            elif typename == 'int':
                arg_val = int(values[name])
            elif typename == 'float':
                arg_val = float(values[name])
            elif typename == 'list':
                # Convert comma-delimited string into a list
                l_str = values[name]
                arg_val = l_str.split(',') if l_str else []
            else:  # types [string, bool]
                arg_val = values[name]
            arg_dict[name] = arg_val
        func(**arg_dict)


def draw_handle(img):
    """
    Draw the "@denomin8r" handle on bottom right of the image then return the image
    :param img:
    :return:
    """
    TEXT = "@denomin8r"
    w, h = img.size
    draw = ImageDraw.Draw(img)

    # TODO might need smarter logic to determine position
    position = (math.floor(.71 * w), math.floor(.94 * h))
    ultimate_left, ultimate_top = position
    fontsize = math.floor(h * .03)
    fontfile = os.path.join(FONT_DIR, BOOKMAN)
    font_obj = ImageFont.truetype(fontfile, fontsize)

    # Determine key coordinates for placing handle
    at_left, _, at_right, _ = draw.textbbox(position, "@", font=font_obj)
    text_left, text_top, text_right, text_bottom = draw.textbbox(position, TEXT, font=font_obj)
    text_width = text_right - text_left
    text_height = text_bottom - text_top
    extra = math.ceil(text_height * 0.1)  # padding
    lilextra = math.ceil(text_height * 0.05)
    diameter = text_height + (2 * extra)
    at_radius = diameter // 2
    ultimate_bottom = ultimate_top + diameter
    rectangle_left = ultimate_left + at_radius

    # Draw handle region backgrounds
    bg_color = int(random.random() * 0xffffff)
    draw.rectangle(
        ((rectangle_left, ultimate_top), (rectangle_left + text_width + (2 * extra), ultimate_bottom)),
        # (lefttop, rightbottom)
        fill=rgb2bgr(darken_rgb(bg_color))
    )
    draw.ellipse(
        ((ultimate_left, ultimate_top), (ultimate_left + diameter, ultimate_bottom)),  # (lefttop, rightbottom)
        fill=rgb2bgr(bg_color)
    )

    # Draw handle region text
    draw.text((ultimate_left + extra + lilextra, ultimate_top - extra - lilextra), "@", font=font_obj, fill="black")
    draw.text((rectangle_left + at_radius + extra, ultimate_top), "denomin8r", font=font_obj, fill="white")

    return img


def draw_test_params(img, **kwargs):
    """
    Draw the passed kwargs key:value pairs onto the image and return the image
    Primarily used for debugging purposes
    :param img:
    :return:
    """
    w, h = img.size
    draw = ImageDraw.Draw(img)

    position = (math.floor(.05 * w), math.floor(.95 * h))
    pos_left, pos_top = position
    fontsize = math.floor(h * .03)
    fontfile = os.path.join(FONT_DIR, BOOKMAN)
    font_obj = ImageFont.truetype(fontfile, fontsize)

    # Set parameter text
    text = ""
    for k, v in kwargs.items():
        text += f"{k}={v}, "
    text_left, text_top, text_right, text_bottom = draw.textbbox(position, text, font=font_obj)
    text_width = text_right - text_left
    text_height = text_bottom - text_top
    extra = math.ceil(text_height * 0.1)  # padding

    # Draw background
    draw.rectangle(((pos_left, pos_top), (pos_left + text_width + extra, pos_top + text_height + extra)), fill="black")
    draw.text((pos_left, pos_top), text, font=font_obj, fill="red")

    return img


def classic_D_swap_random(img1=None, img2=None, force_crop_shape=None):
    """
    Make a classic collage with 2 random images and the letter 'D'
    :param img1:
    :param img2:
    :param int force_crop_shape:
    :return:
    """
    if img1 is None:
        img1 = load_sources(latest=False, n=1)[0]
    if img2 is None:
        img2 = load_sources(latest=False, n=1)[0]

    if force_crop_shape:
        if force_crop_shape == 1:
            crop_shape = img1.size
        elif force_crop_shape == 2:
            crop_shape = img2.size
    else:
        crop_shape = get_crop_shape([img1, img2], square=False)

    img1 = crop_central(img1, crop_shape)
    img2 = crop_central(img2, crop_shape)
    bitmask = build_bitmask_to_size(text='D', fontfile=BOOKMAN, shape=crop_shape)
    return simple_bitmask_swap(img1, img2, bitmask)

