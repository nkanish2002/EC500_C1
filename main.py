#!/usr/bin/env python3
import tweepy

import os
import json


def update_conf(conf):
    f = open("conf.js", 'w')
    f.write(json.dumps(conf, indent=4))
    f.close()


def main():
    print("Starting process")
    if not os.path.isfile("conf.js"):
        print("Please create a config file.")
        exit(1)
    conf, auth = None, None
    try:
        conf = json.loads(open("conf.js", 'r').read())
        print("Config loaded")
        auth = tweepy.OAuthHandler(conf["twitter"]["consumer_key"],
                                     conf["twitter"]["consumer_secret"])
    except Exception as e:
        print(str(e))
        exit(1)
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
    screen_name = input("Enter the User ID: ")
    tweets = api.user_timeline(screen_name=screen_name, include_entities=True)
    return tweets, api


if __name__ == "__main__":
    main()
