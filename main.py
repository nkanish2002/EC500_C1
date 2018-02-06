#!/usr/bin/env python3

from time import time
import shutil

from utils.twitter import get_api, get_media_files
from utils.img_process import download_files
from utils.ffmpeg import create_movie


def main(screen_name, limit):
    print("Starting process")
    api = None
    try:
        api = get_api()
    except Exception as e:
        print(str(e))
        raise e
    media_files = get_media_files(api, screen_name)
    print("Images to be downloaded %d" % min(len(media_files), limit))
    if media_files:
        tmp_dir = "tmp_%d" % (int(time()))
        download_files(media_files, tmp_dir, limit=limit)
        create_movie(tmp_dir + ".mp4", tmp_dir)
        shutil.rmtree(tmp_dir)
        return tmp_dir + ".mp4"
    return None


if __name__ == "__main__":
    name = input("Enter the User ID: ")
    print(main(name, limit=20))
