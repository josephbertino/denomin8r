from util import *

prep()
fontfile = BOOKMAN
kern_rate = 1.0

# -----DO NOT DELETE ABOVE THIS LINE---------------------------
# TODO Big Project 1: "Chaos Source Transforms"

def doit():
    for pa, pb in load_sources_half_latest_pairs(n=15):
        pa, pa_transform_list = chaos_source_transform(pa)
        pb, pb_transform_list = chaos_source_transform(pb)
        mask_is_pa, mask_is_pb = classic_D_swap_random(pa, pb)

        mask_is_pa = Image.fromarray(mask_is_pa)
        mask_is_pb = Image.fromarray(mask_is_pb)

        mask_is_pa = draw_test_params(mask_is_pa, ops=', '.join(pb_transform_list))
        mask_is_pb = draw_test_params(mask_is_pb, ops=', '.join(pa_transform_list))

        mask_is_pa.show()
        mask_is_pb.show()

def test2():
    im_arrs, _ = load_sources(latest=True, n=5)
    for og in im_arrs:
        for num_dups in range(2,6):
            im_arr = og.copy()
            im_arr = source_resample_stack_horizontal(im_arr, num_dups=num_dups)
            img = Image.fromarray(im_arr)
            img.show()

test2()

# TODO play with dup_n being unequal across vertical and horizontal for a grid to get rectangles as atomic elements.
# TODO finish off with a stamp
