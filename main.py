from PIL import Image
import math
import utils

def main():
    # Import photo1 and photo2
    PHOTO1 = 'photo1.jpg'
    PHOTO2 = 'photo2.jpg'
    image1 = Image.open(PHOTO1)
    image2 = Image.open(PHOTO2)
    MASK = 'D_mask.jpg'
    mask = Image.open(MASK)

    # Resize image1, image2, and mask to same size
    w, h = utils.get_max_size([image1, image2, mask])

    crop_box = utils.get_crop_box(image1, w, h)

    image1.show()
    image1 = image1.crop(crop_box)
    image1.show()

    # TODO get all pixel locations where the D_mask is black

    # TODO import a bitmap or some sort of 2D vector, to use as mask
    # TODO get the vector of Arial's "D" and rasterize
    # TODO determine regions in photo1 and photo2 where we'll swap information
    # TODO stretch out mask to fit swap-regions of photo1 and photo2
    # TODO swap information between photo1 and photo2 using mask
    # TODO save new photo1 and photo2

if __name__ == '__main__':
    main()

# TODO learn about the structure of a font file, and how a font is transformed into pixels