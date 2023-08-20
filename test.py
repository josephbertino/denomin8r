from PIL import Image
import numpy as np

# SUCCESS :

color1 = [40, 100, 200]
color2 = [200, 100, 40]
box1 = [[color1] * 4] * 4
box2 = [[color2] * 4] * 4
mask = [[0,0,0,0], [0, 1, 1, 0], [0,1,1,0], [0,0,0,0]]
im2 = Image.fromarray(np.uint8(np.array(box2)), mode='RGB')
im1 = Image.fromarray(np.uint8(np.array(box1)), mode='RGB')

def simple_mask_swap(im1, im2, mask):
    """
    im1, im2, and mask all have to have the same dimensions
    :param Image.Image im1:
    :param Image.Image im2:
    :param mask:
    :return:
    """
    collage_1 = im1.copy()
    collage_2 = im2.copy()
    w, h = im1.size

    for x in range(w):
        for y in range(h):
            xy = (x, y)
            if mask[x][y] == 1:
                val = im1.getpixel(xy)
                collage_1.putpixel(xy, collage_2.getpixel(xy))
                collage_2.putpixel(xy, val)

    return collage_1, collage_2

# Crop an image
image1 = image1.crop(utils.get_crop_box(w,h))
n = utils.make_basic_rgb_array(w,h)
test = Image.fromarray(np.uint8(n))
test.show()
mask.show()

# Use a TrueType font
# font = ImageFont.truetype("arial.ttf", 400)
# d = font.getmask("D")
# mask_np = np.array(d)
# mask_np.resize(d.size)
# mask_np[mask_np > 255] = 1
# mask = Image.fromarray(mask_np, mode='L')
# composite = Image.alpha_composite(image1, mask)
# draw = ImageDraw.Draw(image1)
# draw.text((0, 0), "D", font=font)