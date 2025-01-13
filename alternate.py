from PIL import Image
from pathlib import Path

import timeit
import argparse
import os
import platform

DEFAULTSAVELOCATION = os.path.join(Path(__file__).parent, "saved")

def start(
    source = "None",
    save_location = DEFAULTSAVELOCATION,
    invert_color = False,
    flip_horizontally = False,
    flip_vertically = False,
    mirror_horizontally = False,
    mirror_vertically = False,

    fill_with_color = False,
    target_color = "None",
    color = "None",

    confidence = 1
    ):

    if source == "None":
        raise ValueError("No source specified.")

    image_lst = load_sources(source) # Getting strings of images from user specified source

    if save_location == DEFAULTSAVELOCATION: # If user did not specify save_location
        if not os.path.isdir(DEFAULTSAVELOCATION):
            os.mkdir(DEFAULTSAVELOCATION)
        save_location = do_save(save_location)

    counter = 0
    start_time = timeit.default_timer()

    for element in image_lst:
        if element != "":
            image_abs_path = f"{os.path.join(source, element)}"
            print(f"Image [{counter + 1}/{len(image_lst)}]: {image_abs_path}")

            im = Image.open(image_abs_path) # Supports many different formats.
            error_msg = ""
            try: # Mode selection
                if invert_color:
                    im = invert_colors(im)
                if flip_vertically or flip_horizontally:
                    im = flip_image(im, flip_horizontally, flip_vertically)
                if mirror_vertically:
                    im = mirror_image(im, False, mirror_vertically)
                if mirror_horizontally:
                    im = mirror_image(im, mirror_horizontally, False)
                if fill_with_color:
                    im = fill_color_with_color(im, target_color, color, confidence)
            except TypeError:
                error_msg = f"[TypeError] Image contains invalid pixel values or is transparent."
            finally:
                if error_msg != "":
                    print(f"Error while processing {image_abs_path}. {error_msg}")

            counter += 1
            if len(image_lst) == 1: # User specified only one picture
                im.save(os.path.join(save_location, f"in_{element.split(os.path.sep)[-1]}"))
            else:
                im.save(os.path.join(save_location, f"in_{element}"))

    process_time = timeit.default_timer() - start_time
    print(f"Processed {counter} images in: {round(process_time, 4)} seconds.")

def do_save(save_location):
    n = 0
    while True:
        name = f"runs{n}"
        abs_path = os.path.join(save_location, name)
        if not os.path.isdir(abs_path):
            os.mkdir(abs_path)
            return abs_path
        n += 1   


def fill_color_with_color(im, target_color, color, confidence):
    if target_color == "None" or color == "None":
        raise ValueError("User did not specify colors")

    width, height = im.size
    pixels = im.load()

    new_im = Image.new(mode = "RGB", size = (width, height), color = (0, 0, 0))
    pix = new_im.load()

    rgb_target_color = target_color
    rgb_color = color

    if "#" in target_color:
        rgb_target_color = hex_to_rgb_converter(target_color)
    if "#" in color:
        rgb_color = hex_to_rgb_converter(color)

    for y in range(height):
        for x in range(width):
            for i, e in enumerate(pixels[x, y]): # Checking for each color channel passes if each color val is within the user specified boundary.
                if rgb_target_color[i] - rgb_target_color[i] * (1 - confidence) <= e <= rgb_target_color[i] + rgb_target_color[i] * (1 - confidence): # Logic might be flawed will look later
                    pix[x, y] = rgb_color 
    return new_im


def flip_image(im, horizontal, vertical):
    width, height = im.size
    im = im.load()

    new_im = Image.new(mode = "RGB", size = (width, height), color = (0, 0, 0))
    pix = new_im.load()
    for y in range(height):
        for x in range(width):
            if horizontal:
                pix[x, y] = im[width - (x + 1), y]
            elif vertical:
                pix[x, y] = im[x, height - (y + 1)]
    return new_im

def invert_colors(im):
    pix = im.load()
    width, height = im.size
    for y in range(height):
        for x in range(width):
            lst = []
            for e in pix[x, y]:
                lst.append(int(255 - e))
            pix[x, y] = tuple(lst)
    return im

def mirror_image(im, horizontal, vertical):
    pix = im.load()
    width, height = im.size
    for y in range(height):
        for x in range(width):
            if horizontal:
                pix[x, y] = pix[width - (x + 1), y]
            elif vertical:
                pix[x, y] = pix[x, height - (y + 1)]
    return im

def load_sources(source):
    image_lst = []
    if os.path.isdir(source): # Is dir
        image_lst = os.listdir(os.path.join(source))
    else: # Is regular file
        image_lst.append(source)
    return image_lst

def hex_to_rgb_converter(hexcode):
    '''
    Assumes hex is of format "#ffde81"
    Returns a tuple of (r, g, b)
    '''

    hexidecimal_to_decimal = {
        "0": 0, "1": 1, "2": 2, "3": 3,
        "4": 4, "5": 5, "6": 6, "7": 7,
        "8": 8, "9": 9, "a": 10, "b": 11,
        "c": 12, "d": 13, "e": 14, "f": 15,
    }

    hexcode_filtered = list(str(hexcode).lower().split("#")[1])
    rgb = (
        hexidecimal_to_decimal.get(hexcode_filtered[0]) * 16 + hexidecimal_to_decimal.get(hexcode_filtered[1]),
        hexidecimal_to_decimal.get(hexcode_filtered[2]) * 16 + hexidecimal_to_decimal.get(hexcode_filtered[3]),
        hexidecimal_to_decimal.get(hexcode_filtered[4]) * 16 + hexidecimal_to_decimal.get(hexcode_filtered[5]),
    )
    
    return rgb

def parse_kwargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type = str, default = "None", help = "user can specify one image, or a directory of images. needs to specify absolute path if a directory")
    parser.add_argument('--save-location', type = str, default = DEFAULTSAVELOCATION, help = "sets the save location for processed images, please specify using the absolute path")
    parser.add_argument('--invert-color', type = bool, default = False, help = "inverts specified images color")
    parser.add_argument('--flip-vertically', type = bool, default = False, help = "flips specified images vertically")
    parser.add_argument('--flip-horizontally', type = bool, default = False, help = "flips specified images horizontally")
    parser.add_argument('--mirror-vertically', type = bool, default = False, help = "mirrors from the middle vertically")
    parser.add_argument('--mirror-horizontally', type = bool, default = False, help = "mirrors from the middle horizontally")

    parser.add_argument('--fill-with-color', type = bool, default = False, help = "fills the user specified color with another color, user can specify color with both hexcode and rgb values")
    parser.add_argument('--target-color', type = str, default = "None", help = "sets the target color used in 'fill-color'")
    parser.add_argument('--color', type = str, default = "None", help = "sets the color that will overwrite 'target-color' used in 'fill-color'")

    parser.add_argument('--confidence', type = float, default = 1, help = "an optional confidence keyword argument specifies the accuracy with which the function should locate something on screen. this is helpful in case the function is not able to locate an image due to negligible pixel differences.")

    return parser.parse_args()

if __name__ == "__main__":
    kwargs = parse_kwargs()
    start(**vars(kwargs))

# python3 alternate.py --source C:\Users\itwan\Pictures\test_programmering_kan_slette_seinare --fill-with-color True --confidence 0.99 --target-color "#FFFFFF" --color "#000000"