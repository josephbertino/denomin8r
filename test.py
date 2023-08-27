from PIL import Image
import numpy as np
import utils

color1 = [40, 100, 200]
color2 = [200, 100, 40]

PHOTO1 = 'photo5.jpg'
PHOTO2 = 'photo6.jpg'
MASK = 'D_mask.jpg'

image1 = Image.open(PHOTO1)
image2 = Image.open(PHOTO2)
mask_im = Image.open(MASK)

image1.transpose()

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