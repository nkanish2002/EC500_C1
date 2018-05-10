#!/usr/bin/env python3

from time import time
import shutil

from utils.twitter import get_api, get_media_files
from utils.img_process import download_files
from utils.ffmpeg import create_movie
from utils.db import Mongo


def main(screen_name, limit):
    """
    Processes the screen name, fetches user tweets, creates video out of the
    images posted by the user and adds description.
    :param screen_name:
    :param limit:
    :return: file name
    """
    print("Starting process")
    api = None
    try:
        api = get_api()
        mongo_cli = Mongo()
        db = mongo_cli.get_database(collection="twitter_data")
    except Exception as e:
        print(str(e))
        raise e
    media_files = get_media_files(api, screen_name)
    print("Images to be downloaded %d" % min(len(media_files), limit))
    db.insert_one({
        "screen_name": screen_name,
        "media_links": list(media_files)
    })
    if media_files:
        tmp_dir = "tmp_%d" % (int(time()))
        download_files(media_files, tmp_dir, limit=limit)
        create_movie(tmp_dir + ".mp4", tmp_dir)
        shutil.rmtree(tmp_dir)
        return tmp_dir + ".mp4"
    mongo_cli.mongo_cli.close()
    return None


if __name__ == "__main__":
    name = input("Enter the User ID: ")
    print(main(name, limit=20))
