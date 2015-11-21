#!/usr/bin/env python
# encoding: utf-8
# from __future__ import unicode_literals

import os
import tweepy
import giphy
import urllib
from datetime import datetime
from logger import Logger
from constants import Actions


class TwitterAPI:

    '''
    Class for accessing the Twitter API.

    Requires API credentials to be available in environment
    variables. These will be set appropriately if the bot was created
    with init.sh included with the heroku-twitterbot-starter
    '''

    def __init__(self):
        consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
        consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.logger = Logger()
        self.logger.log('starting TwitterAPI')
        self.tries = 0
        self.max_tries = 3

    def tweet(self, message):
        '''Send a tweet'''
        self.api.update_status(status=message)

    '''TODO: Refactor to make a single function for retweets'''
    def retweet_scott_kelly(self):
        '''Retweet @StationCDRKelly #YearInSpace image'''
        if self.logger.last_action_past_seconds(Actions.TweetActions.retweet_scott_kelly) > 2*60*60:
            self.logger.log('trying to retweet Scott Kelly, @StationCDRKelly')
            timeline = self.prapare_timeline(self.api.user_timeline('StationCDRKelly'), word_whitelist=[
                                             "#YearInSpace"], tweet_id=self.logger.last_action_id(Actions.TweetActions.retweet_scott_kelly))

            self.api.retweet(timeline[0].id)
            self.logger.update_last_tweet(
                Actions.TweetActions.retweet_scott_kelly, timeline[0])
            self.logger.log('#space image from Scott retweeted 🤓')
            # break
        else:
            return False

    def retweet_astro_kjell(self):
        '''Retweet @astro_kjell image'''
        if self.logger.last_action_past_seconds(Actions.TweetActions.retweet_astro_kjell) > 2*60*60:
            self.logger.log('trying to retweet astro_kjell, @astro_kjell')
            timeline = self.prapare_timeline(self.api.user_timeline('astro_kjell'), tweet_id=self.logger.last_action_id(Actions.TweetActions.retweet_astro_kjell))

            self.api.retweet(timeline[0].id)
            self.logger.update_last_tweet(
                Actions.TweetActions.retweet_astro_kjell, timeline[0])
            self.logger.log('#space image from astro_kjell retweeted 🤓')
            # break
        else:
            return False

    def retweet_astro_kimiya(self):
        '''Retweet @astro_kimiya image'''
        if self.logger.last_action_past_seconds(Actions.TweetActions.retweet_astro_kimiya) > 2*60*60:
            self.logger.log('trying to retweet astro_kimiya, @astro_kimiya')
            timeline = self.prapare_timeline(self.api.user_timeline('astro_kimiya'), tweet_id=self.logger.last_action_id(Actions.TweetActions.retweet_astro_kimiya))

            self.api.retweet(timeline[0].id)
            self.logger.update_last_tweet(
                Actions.TweetActions.retweet_astro_kimiya, timeline[0])
            self.logger.log('#space image from astro_kimiya retweeted 🤓')
            # break
        else:
            return False

    def giphy_tweet(self):
        '''Tweet a random giphy #space gif'''
        self.tries += 1
        if self.logger.last_action_past_seconds(Actions.TweetActions.space_gif) > 24*60*60:
            self.logger.log('trying to tweet a #space GIF')
            try:
                c = giphy.Giphy()
                result = c.random(tag="space")
                URL = result['data']['image_original_url']
                urllib.urlretrieve(URL, 'gif.GIF')
                status = ('New #Space #GifOfTheDay!\n'
                          '⌚ ' + str(datetime.now()) + '\n'
                          '🔗 {}'.format(result['data']['url']))
                status = self.api.update_with_media('gif.GIF', status)

                self.logger.update_last_tweet(
                    Actions.TweetActions.space_gif, status)
                self.logger.log('#space GIF tweeted 🤓')
                self.tries = 0
            except Exception, e:
                self.logger.log(str(e), error=True)
                if self.tries < self.max_tries:
                    self.giphy_tweet()

        else:
            return False

    def prapare_timeline(self, timeline, user_blacklist=None, word_blacklist=None, word_whitelist=None, tweet_id=None):
        '''Prepare timeline for generale usasge'''
        _user_blacklist = [] if user_blacklist is None else user_blacklist
        _word_blacklist = [
            "RT", u"♺"] if word_blacklist is None else word_blacklist

        if tweet_id is not None:
            t = []
            for status in timeline:
                if status.id == tweet_id:
                    timeline = t
                    break
                t.append(status)

        if word_whitelist is not None:
            timeline = filter(lambda status: any(
                word in status.text.split() for word in word_whitelist), timeline)
        #timeline = filter(lambda status: status.text[0] != "@", timeline)
        timeline = filter(lambda status: not any(
            word in status.text.split() for word in _word_blacklist), timeline)
        timeline = filter(
            lambda status: status.author.screen_name not in _user_blacklist, timeline)

        timeline.reverse()
        return timeline
