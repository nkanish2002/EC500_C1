import os
import tweepy
from .conf import conf_exists, get_conf, update_conf


def get_api():
    """
    Reads the config file and creates the twitter client object
    :return: tweepy api object
    """
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


def get_media_files(api, screen_name, limit=100):
    """
    Downloads all images uploaded by the user
    :param api:
    :param screen_name:
    :param limit:
    :return: list of image url's
    """
    tweets = api.user_timeline(screen_name=screen_name,
                               count=20, include_rts=False,
                               exclude_replies=True)
    last_id = tweets[-1].id
    count = 0
    media_files = set()
    while count < 3000:
        more_tweets = api.user_timeline(screen_name=screen_name,
                                        count=20,
                                        include_rts=False,
                                        exclude_replies=True,
                                        max_id=last_id - 1)
        count += len(more_tweets)
        print("Read through %d tweets" % count, end="\r")
        if len(more_tweets) == 0 or len(media_files) > limit:
            break
        else:
            last_id = more_tweets[-1].id - 1
            for tw in more_tweets:
                if len(media_files) > limit: break
                media = tw.entities.get('media', [])
                if len(media) > 0:
                    media_files.add(media[0]['media_url'])
    return media_files
