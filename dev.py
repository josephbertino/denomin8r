import util
import uuid

util.prep()
fontfile = util.BOOKMAN
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
random_id = uuid.uuid4().__str__().split('-')[0]
img = util.load_sources(latest=False, n=1, specific_srcs=['lewitt1'])
img = img[0]

# TODO Big Project 1: "Chaos Source Transforms". Includes Off-cropping, rotating, cropping, slice transformations, flipping, & resizing. Of course, finish off with a stamp.

def chaos_source_transform(img):
    """
    Take an image and run it through a series of transformations, then return the modified image.
        The number and order of transformations will be determined by chance, but there is a
        "cost" to each transformation, and once the "transform budget" is spent, abort and return.
    :param img:
    :return:
    """

    # TODO refactor all source transform methods to accept a numpy array and return a numpy array
    # TODO after refactor all source transforms, need to refactor the calls to those transforms (mainly in main.py)
    # TODO maintain a data structure (list?) of all the transform methods, and during chaos_source_transform, pick from the list.
    # TODO dont transform to Image.Image until after the bitmask is applied and you are ready to save


# I'm thinking that I should first transform the image to an np.array,
# and all the transforms would be really fast bc they are numpy operations,
# and finally at the end transform it back to an Image.Image
# Start standardizing the verbiage "source" for an image that goes into the collage
# and "mask" for the template for swapping slices between sources.
# I want each method to be associated with a "cost" or "price"
# Perhaps I can create a list of tuples such that (method, cost) is the tuple,
# That way I don't have to turn the methods into classes
# I mean I CAN see a way to make a class that does this. class chaos_source_transform will be initialized with the source and have a default budget, and there will be a method that runs through all the ... nah my way is easier. I just want to get the shit off the ground