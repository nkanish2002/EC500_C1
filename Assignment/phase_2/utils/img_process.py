import io
import os
import wget

from PIL import Image, ImageFont, ImageDraw
from google.cloud import vision
from google.cloud.vision import types


def convert_to_png(image_name):
    """Converts any image to PNG format"""
    im = Image.open(image_name)
    new_name = "%s.png" % image_name
    im.save("%s.png" % image_name)
    os.remove(image_name)
    return new_name


def resize_image(im, size):
    """Re-sizes image"""
    width, height = im.size
    if width < size[0] and width % 2 != 0:
        width = min(width - 1, size[0])
    if height < size[1] and height % 2 != 0:
        height = min(height - 1, size[1])
    im.resize((width, height), Image.LANCZOS)
    return im


def overlay(im):
    """Overlays the image on a background image"""
    bg = Image.open("bg.png")
    bg.paste(im)
    return bg


def get_labels(client, image_name):
    """Gets most descriptive labels from Google Vision"""
    with io.open(image_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return [label.description for label in labels]


def add_text(im, text, position):
    """Adds text to the image at a given position"""
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("abel-regular.ttf", 70)
    draw.text(position, text, (255, 255, 255), font=font)
    return im


def process_image(image_name, client):
    """Converts the image to the needed format"""
    image_name = convert_to_png(image_name)
    labels = get_labels(client, image_name)
    im = Image.open(image_name)
    im = resize_image(im, (600, 600))
    im.save(image_name)
    im = Image.open(image_name)
    im = overlay(im)
    text = "Labels\n~~~~~\n" + "\n".join(labels[0:4])
    im = add_text(im, text, (1200, 50))
    im.save(image_name)


def download_files(media_files, folder_name, limit=100):
    """
    Downloads the image and processes them.
    :param media_files:
    :param folder_name:
    :param limit:
    :return:
    """
    if media_files:
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        client = vision.ImageAnnotatorClient()
        for i, media_file in enumerate(media_files):
            if i < limit:
                path = "%s/pic%04d" % (folder_name, i + 1)
                print("\tDownloading %s" % path, end="\r")
                wget.download(media_file, out=path)
                process_image(path, client)
            else:
                break
        print("\n")
