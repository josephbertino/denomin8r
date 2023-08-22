from PIL import Image
import numpy as np
import utils

# SUCCESS :
PHOTO1 = 'photo3.jpg'
PHOTO2 = 'photo4.jpg'
image1 = Image.open(PHOTO1)
image2 = Image.open(PHOTO2)
color1 = [40, 100, 200]
color2 = [200, 100, 40]
box1 = [[color1] * 4] * 4
box2 = [[color2] * 4] * 4
mask = [[0,0,0,0], [0, 1, 1, 0], [0,1,1,0], [0,0,0,0]]
im2 = Image.fromarray(np.uint8(np.array(box2)), mode='RGB')
im1 = Image.fromarray(np.uint8(np.array(box1)), mode='RGB')

# Generate a bitmask from a mode-'RGB' JPEG
D_MASK = 'D_mask.jpg'
d_mask = Image.open(D_MASK)
w, h = utils.get_max_size([image1, image2, d_mask])
image1 = image1.crop(utils.get_crop_box(w, h))
image2 = image2.crop(utils.get_crop_box(w, h))
d_mask = d_mask.crop(utils.get_crop_box(w, h))

blacks = utils.make_bitmask_from_black_white(d_mask)

print(image1.size, image2.size, blacks.shape)

collage_1, collage_2 = utils.simple_mask_swap(image1, image2, blacks)
collage_1.show()
collage_2.show()

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