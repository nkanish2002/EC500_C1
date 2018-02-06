# EC500C1 Mini-project

## Introduction

This is a simple project that downloads images tweeted by an account, recognises entities in it and creates a short movie.

## Installation

### Prerequisites

1. [Python 3](https://www.python.org/download/releases/3.0/)
2. [FFMPEG command](http://ffmpeg.org)
3. [Google Vision API](https://cloud.google.com/vision/docs/reference/libraries?authuser=1#setting_up_authentication): Download ths authentication key
4. [Twitter access key](https://apps.twitter.com)

### Process

1. Install all requirements: `pip install -r requirements.txt`
2. Set the absolute path to Google Vision JSON:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/Path/To/JSON/Project-sla123kn31231.json
```

3. Create a conf file:
```json
{
    "twitter": {
        "consumer_key": "<your consumer key>",
        "consumer_secret": "<your consumer secret>"
    }
}
```

## Run

If you have completed all the above steps, simply execute the `main.py` file: `python3 main.py` or `./main.py`
For the first run, the app will ask you to login to your twitter account, it should automatically open a browser with the link. Once you authenticate you will have to paste the pincode back into the CLI.
Then the app will ask you to enter any screen_name associated with a valid twitter account and in the end it will print the name of the movie generated. If not movie could be generated, it will print `None`.
