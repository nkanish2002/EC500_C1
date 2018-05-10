import tweepy
import requests
import os


def download_tw_img(Username, numofimgs=999):
    # Downloads Images for user
    timeline = api.user_timeline(
        screen_name=Username, count=numofimgs, include_rts=True)
    urls = []
    for tweet in timeline:
        for media in tweet.entities.get("media", [{}]):
            if media.get("type", None) == "photo":
                urls.append(media["media_url"])
    index = 1
    for url in urls:
        request = requests.get(url, stream=True)
        if request.status_code == 200:
            index = index + 1
            with open(url.split('/')[-1], 'wb') as image:
                for chunk in request:
                    image.write(chunk)


def twitter_api(consumer_token, consumer_secret, key, secret):
    # Initiates a twitter session
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(key, secret)
    global api
    api = tweepy.API(auth)
    return api
