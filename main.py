#!/usr/bin/env python3
import tweepy
import wget

import os
import json
import subprocess

def conf_exists():
    return os.path.isfile("conf.js")

def update_conf(conf):
    f = open("conf.js", 'w')
    f.write(json.dumps(conf, indent=4))
    f.close()

def get_conf():
    return json.loads(open("conf.js", 'r').read())

def get_api():
    if not conf_exists():
        print("Please create a config file.")
        exit(1)
    conf = get_conf()
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
                                    max_id=last_id-1)
        count += len(more_tweets)
        print("Read through " + count + " tweets")
        # There are no more tweets
        if (len(more_tweets) == 0):
            break
        else:
            last_id = more_tweets[-1].id-1
            tweets = tweets + more_tweets

    media_files = set()
    for status in tweets:
        media = status.entities.get('media', [])
        if(len(media) > 0):
            media_files.add(media[0]['media_url'])
    return media_files

def download_files(media_files, folder_name):
    if media_files:
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        for i, media_file in enumerate(media_files):
            wget.download(media_file, out="%s/%d.jpg" % (folder_name, i))

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
    print("Images to be downloaded %d" % len(media_files))
    if media_files:
        tmp_dir = "sljnfsldfjk"
        download_files(media_files, tmp_dir)
        FFMPEG_CMD = ["ffmpeg", "-r", "1", "-start_number", "1", "-i", tmp_dir + "/%d.jpg", "-vcodec", "libx264", "-crf", "25", "-pix_fmt", "yuv420p", "test.mp4"]

if __name__ == "__main__":
    main()
