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
    for _ in range(40):
        fn(im_arr)
    end = time.perf_counter_ns()
    return end - start


def plot_bars(indices, values):
    bars = plt.bar(indices, values, color='g', width=0.25, edgecolor='grey')
    plt.xlabel('Transforms', fontweight='bold', fontsize=15)
    plt.xticks(rotation=90)
    plt.ylabel('Relative Time (%)', fontweight='bold', fontsize=15)
    plt.subplots_adjust(bottom=0.4)
    plt.bar_label(bars)
    plt.show()


def normalize_times(fn_times):
    s = sum(fn_times)
    norm_times = list(map(lambda x: (x / s) * 100, fn_times))
    return norm_times


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
    plot_bars(fn_names, fn_times)


def run_for_all_fns_2():

    im_arrs, filenames = load_sources(latest=False, n=1, specific_srcs=['koons2'])
    im_arr = im_arrs[0]

    name_times = []
    for fn in CROPBOX_OPERATIONS:
        total_time = fn_timer(fn, im_arr)
        name_times.append((fn.__name__, total_time))
    name_times = sorted(name_times, key=lambda x: x[1])
    fn_names, fn_times = list(zip(*name_times))
    norm_times = normalize_times(fn_times)
    plot_bars(fn_names, norm_times)


run_for_all_fns_2()

# TODO Perform Timer analysis on all individual slicing and cropping methods
# TODO put profiler methods in utils
# TODO Play around and Test EACH METHOD IN UTIL & SOURCE_OPS

'''
What am I trying to accomplish?
Assigning relative costs to each method
And coming up with a method whereby, once I add new methods, the relative costs re-calculate
So I'll need the following
[] a comprehensive list of ALL methods that are considered SOURCE_TRANSFORMS...no middlemen or utility methods, the actual final product
[] Not only a method, but a way to identify methods as SOURCE transforms, so that if I added a new method I can re-process all relative costs
    + Could be simply any source_op method that has as its first argument "im_arr"'
    + I think that works for now, for me. I can always enhance the complexity of this later, by adding some super smart way of categorizing methods
[] The the chaos_source_transforms method will automatically be able to pick up the new costs for all new methods when running
'''