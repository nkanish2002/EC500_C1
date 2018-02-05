#!/usr/bin/env python3
import tweepy
import wget

import os
import io
import shutil
import json
import subprocess
from time import time
from PIL import Image, ImageFont, ImageDraw
from google.cloud import vision
from google.cloud.vision import types


def conf_exists():
    return os.path.isfile("conf.json")


def update_conf(conf):
    f = open("conf.json", 'w')
    f.write(json.dumps(conf, indent=4))
    f.close()


def get_conf():
    return json.loads(open("conf.json", 'r').read())


def get_api():
    if not conf_exists():
        print("Please create a config file.")
        exit(1)
    conf = get_conf()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = conf["google-vision-key"]
    auth = tweepy.OAuthHandler(conf["twitter"]["consumer_key"],
                               conf["twitter"]["consumer_secret"])
    if "access_token" in conf and "access_token_secret" in conf:
        print("Using cached user info")
        auth.set_access_token(conf["access_token"], conf["access_token_secret"])
    else:
        print("Please head to the following URL and login with twitter")
        url = auth.get_authorization_url()
        print(url)
        os.system("open " + url)
        verifier = input("Enter PIN: ")
        auth.get_access_token(verifier)
        auth.set_access_token(auth.access_token, auth.access_token_secret)
        conf["access_token"] = auth.access_token
        conf["access_token_secret"] = auth.access_token_secret
        update_conf(conf)
    api = tweepy.API(auth)
    return api


def get_media_files(api, screen_name):
    # screen_name = input("Enter the User ID: ")
    tweets = api.user_timeline(screen_name=screen_name,
                               count=20, include_rts=False,
                               exclude_replies=True)
    last_id = tweets[-1].id
    count = 0
    while (count < 3000):
        more_tweets = api.user_timeline(screen_name=screen_name,
                                        count=20,
                                        include_rts=False,
                                        exclude_replies=True,
                                        max_id=last_id - 1)
        count += len(more_tweets)
        print("Read through %d tweets" % count)
        # There are no more tweets
        if (len(more_tweets) == 0):
            break
        else:
            last_id = more_tweets[-1].id - 1
            tweets = tweets + more_tweets

    media_files = set()
    for status in tweets:
        media = status.entities.get('media', [])
        if (len(media) > 0):
            media_files.add(media[0]['media_url'])
    return media_files


def resize_image(im, size):
    width, height = im.size
    if width < size[0] and width % 2 != 0:
        width = width - 1
    if height < size[1] and height % 2 != 0:
        height = height - 1
    im.thumbnail((width, height), Image.ANTIALIAS)
    return im


def overlay(im):
    bg = Image.open("bg.jpg")
    bg.paste(im)
    return bg


def get_labels(client, image_name):
    file_name = os.path.join(os.path.dirname(__file__), image_name)
    with io.open(file_name, 'rb') as image_file: 
        content = image_file.read()
    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return [label.description for label in labels]
    

def add_text(im, text, position):
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("abel-regular.ttf", 70)
    draw.text(position,text,(255,255,255),font=font)
    return im

def process_image(image_name, client):
    labels = get_labels(client, image_name)
    im = Image.open(image_name)
    im = resize_image(im, (600, 600))
    im.save(image_name)
    im = Image.open(image_name)
    im = overlay(im)
    text = "Labels: " + ",".join(labels[0:4])
    im = add_text(im, text, (50, 700))
    im.save(image_name)


def download_files(media_files, folder_name, limit=100):
    if media_files:
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        client = vision.ImageAnnotatorClient()
        for i, media_file in enumerate(media_files):
            if i < limit:
                path = "%s/pic%04d.jpg" % (folder_name, i + 1)
                wget.download(media_file, out=path)
                process_image(path, client)
            else:
                break


def create_movie(name, folder):
    cmd = ["ffmpeg", "-framerate", "1", "-i", folder + "/pic%04d.jpg", "-c:v",
           "libx264", "-r", "30", "-pix_fmt", "yuv420p", name]
    return subprocess.call(cmd)


def main():
    print("Starting process")
    api = None
    try:
        api = get_api()
    except Exception as e:
        print(str(e))
        exit(1)
    screen_name = input("Enter the User ID: ")
    media_files = get_media_files(api, screen_name)
    print("Images to be downloaded %d" % min(len(media_files), 100))
    if media_files:
        tmp_dir = "tmp_%d" % (int(time()))
        download_files(media_files, tmp_dir)
        create_movie(tmp_dir + ".mp4", tmp_dir)
        shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    main()
