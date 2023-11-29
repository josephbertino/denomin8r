from util import *
import uuid

prep()
fontfile = BOOKMAN
kern_rate = 1.0

# -----DO NOT DELETE ABOVE THIS LINE---------------------------

"""
Observations:
Vertical Slicing
    dup_n:
        from 2 up to ~7 gives good results, with it getting creepier the higher you go.
        I wouldn't go more than 7 for my intended aesthetic.
    slice_per_dup:
        slice_per_dup >= 8 starts to resemble a face
        Once dupn goes above 3, I think >20 slices per dupe looks good
    I really love how creepy it is to make many thin tall slices of faces, or squished faces
Horizontal Slicing
    dupn:
        3 or 4 seems great. Like totems
    slice_per_dup:
        Needs to be larger, like >12
Grid:
    I like what happens when dup_n is unequal between rotation slicing.
    Produces cool effects with the rectangles.
"""

# TODO Big Project 1: "Chaos Source Transforms"


# TODO profile each source transform method against a control image to get a better idea of what cost to assign them. This includes each method in source_slice random and source_crop_random
import matplotlib.pyplot as plt
import inspect
import time


def fn_timer(fn, im_arr):
    start = time.perf_counter_ns()
    for _ in range(10):
        fn(im_arr)
    end = time.perf_counter_ns()
    return end - start


def run_for_all_fns():
    import source_ops

    im_arrs, filenames = load_sources(latest=False, n=1, specific_srcs=['koons2'])
    im_arr = im_arrs[0]

    all_source_fns = []
    for name, fn in inspect.getmembers(source_ops, inspect.isfunction):
        args = inspect.getfullargspec(fn).args
        if args and args[0] == 'im_arr':
            all_source_fns.append((name, fn))

    name_times = []
    for name, fn in all_source_fns:
        total_time = fn_timer(fn, im_arr)
        name_times.append((name, total_time))
    name_times = sorted(name_times, key=lambda x: x[1])

    fn_names, fn_times = list(zip(*name_times))
    plt.bar(fn_names, fn_times, color='g', width=0.25, edgecolor='grey')
    plt.xlabel('Transforms', fontweight='bold', fontsize=15)
    plt.xticks(rotation=45)
    plt.ylabel('Seconds', fontweight='bold', fontsize=15)
    plt.subplots_adjust(bottom=1)
    plt.show()


def run_for_all_fns_2():

    im_arrs, filenames = load_sources(latest=False, n=1, specific_srcs=['koons2'])
    im_arr = im_arrs[0]

    name_times = []
    for fn, cost in CHEAP_TRANSFORMS:
        total_time = fn_timer(fn, im_arr)
        name_times.append((fn.__name__, total_time))
    name_times = sorted(name_times, key=lambda x: x[1])

    fn_names, fn_times = list(zip(*name_times))
    plt.bar(fn_names, fn_times, color='g', width=0.25, edgecolor='grey')
    plt.xlabel('Transforms', fontweight='bold', fontsize=15)
    plt.xticks(rotation=45)
    plt.ylabel('Seconds', fontweight='bold', fontsize=15)
    plt.subplots_adjust(bottom=0.15)
    plt.show()

run_for_all_fns_2()

# TODO Perform Timer analysis on all individual slicing and cropping methods
# TODO put profiler methods in utils
# TODO Play around and Test EACH METHOD IN UTIL & SOURCE_OPS
