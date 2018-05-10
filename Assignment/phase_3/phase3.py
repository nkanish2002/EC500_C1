#!/usr/bin/env python3
import sys
import twmanager
import img2video
import vision
import json
import mogoLog as lg
import glob
import compare

screenname = "CaseyNeistat"
with open('twittersecrete.json') as secret:
    Tsecret = json.load(secret)

# Initiating a Twitter Session
twmanager.twitter_api(Tsecret['Consumer_Key'], Tsecret['Consumer_Secret'],
                      Tsecret['Access_Token'], Tsecret['Access_Token_Secret'])

# Downloading Images for screen name
twmanager.download_tw_img(screenname)

# Connecting to Mongo
cli = lg.loguser("mongodb://localhost:27017", screenname)

for infile in glob.glob("*.jpg"):
    lab = vision.labels(infile, '')
    if (lab != False):
        text = img2video.labelonImage(lab, infile)
        for t in text:
            lg.loginterests(t)

lg.savetop(40)
top5 = lg.uploadlog()
img2video.jpg2mp4()
img2video.rmPWDImg()

compare.showcompare(screenname, top5)
