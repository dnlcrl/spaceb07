#!/usr/bin/env python
# encoding: utf-8
import os
import time
import giphy
import tweepy
import urllib
from datetime import datetime


class TwitterAPI:
    """
    Class for accessing the Twitter API.

    Requires API credentials to be available in environment
    variables. These will be set appropriately if the bot was created
    with init.sh included with the heroku-twitterbot-starter
    """

    def __init__(self):
        consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
        consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        """Send a tweet"""
        self.api.update_status(status=message)


def main():
    twitter = TwitterAPI()
    while True:
        # Send a tweet here!
        c = giphy.Giphy()
        result = c.random(tag="space")
        URL = result['data']['image_original_url']
        urllib.urlretrieve(URL, 'gif.GIF')
        status = ('New #Space #GifOfTheDay!\n'
                  '⌚ ' + str(datetime.now()) + '\n'
                  '🔗 {}'.format(result['data']['url']))
        twitter.api.update_with_media('gif.GIF', status)
        t = time.localtime()
        t = time.mktime(t[:3] + (0, 0, 0) + t[6:])
        time.sleep(t + 24*3600 - time.time())


if __name__ == "__main__":
    main()
