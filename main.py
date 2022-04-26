import os
import random
from tkinter import filedialog, Tk

from PIL import Image
from PIL.Image import Resampling
from tqdm import tqdm

# noinspection SpellCheckingInspection
image = None
path = None
latest_path = None

Tk().withdraw()


def path_to_image(path):
    return Image.open(path)


def img_to_grayscale(_image):
    global latest_path
    size = _image.height * _image.width  # define the size of the image
    with tqdm(total=size, desc="Converting to Grayscale", unit="Pixels", ncols=100) as pbar:
        for i in range(_image.height):  # iterate through the height of the image
            for j in range(_image.width):  # iterate through the width of the image
                pbar.update(1)
                r, g, b = _image.getpixel((j, i))  # get the pixel at the current position
                gray = int((r + g + b) / 3)  # calculate the average of the RGB values
                _image.putpixel((j, i), (gray, gray, gray))  # set the pixel to the average
    r = "output/grey.jpg"
    _image.save(r)  # save the image
    latest_path = r
    tqdm.write("Conversion to Grayscale Complete, Saving Image to " + r)


def switch_color_channels(_image):
    global latest_path
    size = _image.height * _image.width  # define the size of the image
    with tqdm(total=size, desc="Switching Color Channels", unit="Pixels", ncols=100) as pbar:
        for i in range(_image.height):  # iterate through the height of the image
            for j in range(_image.width):  # iterate through the width of the image
                r, g, b = _image.getpixel((j, i))  # get the pixel at the current position
                _image.putpixel((j, i), (b, g, r))  # switch the color channels
                pbar.update(1)
    r = "output/switched.jpg"
    _image.save(r)  # save the image
    latest_path = r
    tqdm.write("Switching Color Channels Complete, Saving Image to " + r)


def invert_img(_image):
    global latest_path
    size = _image.height * _image.width  # define the size of the image
    with tqdm(total=size, desc="Inverting Image", unit="Pixels", ncols=100) as pbar:
        for i in range(_image.height):  # iterate through the height of the image
            for j in range(_image.width):  # iterate through the width of the image
                r, g, b = _image.getpixel((j, i))  # get the pixel at the current position
                _image.putpixel((j, i),
                                (255 - r, 255 - g, 255 - b))  # invert the pixel
                pbar.update(1)
    r = "output/inverted.jpg"
    _image.save(r)  # save the image
    latest_path = r
    tqdm.write("Inversion Complete, Saving Image to " + r)


def img_brightness(_image, factor, pbar):
    for i in range(_image.height):  # iterate through the height of the image
        for j in range(_image.width):  # iterate through the width of the image
            r, g, b = _image.getpixel((j, i))  # get the pixel at the current position
            _image.putpixel((j, i),
                            (int(r * factor), int(g * factor),
                             int(b * factor)))  # adjust the brightness of the pixel by the factor
            pbar.update(1)


def brighten_img(_image, amount):
    global latest_path
    # noinspection PyUnboundLocalVariable
    factor = 255 / 10 * amount
    size = _image.height * _image.width  # define the size of the image
    with tqdm(total=size, desc="Brightening Image", unit="Pixels", ncols=100) as pbar:
        img_brightness(_image, factor, pbar)
    r = "output/brightened.jpg"
    _image.save(r)  # save the image
    latest_path = r
    tqdm.write("Brightening Complete, Saving Image to " + r)


def darken_img(_image, amount):
    global latest_path
    # noinspection PyUnboundLocalVariable
    factor = 10 / 255 * amount
    size = _image.height * _image.width  # define the size of the image
    with tqdm(total=size, desc="Darkening Image", unit="Pixels", ncols=100) as pbar:
        img_brightness(_image, factor, pbar)
    r = "output/darkened.jpg"
    _image.save(r)  # save the image
    latest_path = r
    tqdm.write("Darkening Complete, Saving Image to " + r)


def img_noise(_image, amount):
    global latest_path
    # noinspection PyUnboundLocalVariable
    factor = 255 / 10 * amount
    factor = int(factor)
    size = _image.height * _image.width  # define the size of the image
    with tqdm(total=size, desc="Adding Noise", unit="Pixels", ncols=100) as pbar:
        for i in range(_image.height):  # iterate through the height of the image
            for j in range(_image.width):  # iterate through the width of the image
                r, g, b = _image.getpixel((j, i))  # get the pixel at the current position
                _image.putpixel((j, i),
                                (int(r + random.randint(-factor, factor)),
                                 int(g + random.randint(-factor, factor)),
                                 int(b + random.randint(-factor,
                                                        factor))))  # add noise to the pixel
                pbar.update(1)
    r = "output/noised.jpg"
    _image.save(r)  # save the image
    latest_path = r
    tqdm.write("Noise Complete, Saving Image to " + r)


def img_pixelate(_image, amount):
    global latest_path
    amount_dict = {
        0: 2048,
        1: 1024,
        2: 512,
        3: 256,
        4: 128,
        5: 64,
        6: 32,
        7: 16,
        8: 8,
        9: 4,
        10: 2
    }
    # noinspection PyUnboundLocalVariable
    if amount > 10 or amount < 0:
        amount = 10
    small_img = _image.resize((amount_dict[amount], amount_dict[amount]),
                              resample=Resampling.BILINEAR)  # resize the image to 16x16
    result = small_img.resize(_image.size, Resampling.NEAREST)
    r = "output/pixelated.jpg"
    result.save(r)  # save the image
    latest_path = r
    tqdm.write("Pixelating Complete, Saving Image to " + r)


def gaussian_blur_img(_image, amount):
    global latest_path
    amount_dict = {
        0: 3,
        1: 5,
        2: 7,
        3: 9,
        4: 11,
        5: 13,
        6: 15,
        7: 17,
        8: 19,
        9: 21,
        10: 23
    }
    # noinspection PyUnboundLocalVariable
    if amount > 10 or amount < 0:
        amount = 10
    size = _image.height * _image.width  # define the size of the image
    with tqdm(total=size, desc="Gaussian Blurring", unit="Pixels", ncols=100) as pbar:
        for i in range(_image.height):  # iterate through the height of the image
            for j in range(_image.width):  # iterate through the width of the image
                surrounding_pixels = []  # create a list to store the surrounding pixels
                for x in range(amount_dict[amount]):  # iterate through the surrounding pixels
                    for y in range(amount_dict[amount]):
                        try:
                            r2, g2, b2 = _image.getpixel((j + x, i + y))  # get the pixel at the current position
                            surrounding_pixels.append((r2, g2, b2))  # add the pixel to the list
                        except IndexError:
                            pass
                r = sum(pixel[0] for pixel in surrounding_pixels) / len(surrounding_pixels)  # get the average red
                g = sum(pixel[1] for pixel in surrounding_pixels) / len(surrounding_pixels)  # get the average green
                b = sum(pixel[2] for pixel in surrounding_pixels) / len(surrounding_pixels)  # get the average blue
                _image.putpixel((j, i),
                                (int(r), int(g), int(b)))  # set the pixel to the average of the surrounding pixels
                pbar.update(1)
    r = "output/blurred.jpg"
    _image.save(r)  # save the image
    latest_path = r
    tqdm.write("Gaussian Blurring Complete, Saving Image to " + r)


# def filter_menu():
#     choices = {
#         "Image to Grayscale": img_to_grayscale,
#         "Switch Color Channels": switch_color_channels,
#         "Invert Image": invert_img,
#         "Brighten Image": brighten_img,
#         "Darken Image": darken_img,
#         "Add Noise": img_noise,
#         "Pixelate Image": img_pixelate,
#         "Blur Image": gaussian_blur_img,
#     }
#     print("\nImage Processing Menu")
#     for i in range(1, len(choices) + 1):
#         print(str(i) + ": " + list(choices.keys())[i - 1])
#     choice = input("Please select an option > ")
#     if choice.isdigit():
#         choice = int(choice)
#         if 0 < choice <= len(choices):
#             choices[list(choices.keys())[choice - 1]](image)
#         else:
#             print("Invalid Choice")
#             filter_menu()
#     else:
#         print("Invalid Choice")
#         filter_menu()


def select_file():
    global image
    global path
    _path = filedialog.askopenfilename()
    if _path:
        image = Image.open(_path)
        # if the image is larger than 400 pixels in width resize it but keep the aspect ratio
        if image.width > 600:
            image = image.resize((600, int(image.height * 600 / image.width)), Image.ANTIALIAS)
            current = "output/resized.jpg"
            for i in range(1, 10):
                if os.path.isfile(current):
                    current = "output/resized" + str(i) + ".jpg"
                else:
                    break
            else:
                raise RuntimeError("Too many resized images")
            image.save(current)
            path = current
            image.save("output/resized.jpg")
            path = "output/resized.jpg"
        else:
            path = _path
    else:
        print("No File Selected")

# def menu():
#     print("\nImage Processing Menu\n")
#     print("Selected File: " + str(path) + "\n")
#     print("1: Select File")
#     print("2: Image Processing Menu")
#     print("3: Show Latest Processed Image")
#     choice = input("Please select an option > ")
#     if choice == "1":
#         select_file()
#     elif choice == "2":
#         if image is None:
#             print("No Image Selected")
#             menu()
#         else:
#             filter_menu()
#     elif choice == "3":
#         if latest_path is None:
#             print("No recent image")
#             menu()
#         else:
#             # noinspection PyTypeChecker
#             Image.open(latest_path).show()
#             menu()
#     else:
#         print("Invalid Choice")
#         menu()
