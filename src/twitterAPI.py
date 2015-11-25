#!/usr/bin/env python
# encoding: utf-8

import os
import tweepy
import giphy
import urllib
import urllib2
from datetime import datetime
from constants import Actions, TWITTER_USERS


class TwitterAPI:

    '''
    Class for accessing the Twitter API.

    Requires API credentials to be available in environment
    variables. These will be set appropriately if the bot was created
    with init.sh included with the heroku-twitterbot-starter
    '''

    def __init__(self, logger):
        consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
        consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.logger = logger
        self.logger.log('starting TwitterAPI')
        self.tries = 0
        self.max_tries = 10

    def tweet(self, message):
        '''Send a tweet'''
        self.api.update_status(status=message)

    def retweet_astronaut(self, action, word_blacklist=None, word_whitelist=None):
        '''Retweet @Astronaut image
        TODO: Refactor to make a single exception log string'''

        self.logger.log('trying to retweet @' + TWITTER_USERS[action])
        if self.logger.last_action_past_seconds(action) > 2*60*60:
            twid = ''
            try:
                timeline = self.prapare_timeline(self.api.user_timeline(TWITTER_USERS[
                                                 action]), word_whitelist=word_whitelist, word_blacklist=word_blacklist, tweet_id=self.logger.last_action_id(action))
                twid = timeline[0].id
                self.api.retweet(twid)
                self.logger.update_last_tweet(action, timeline[0])
                self.logger.log(
                    '#space image from @' + TWITTER_USERS[action] + ' retweeted', emoji='🤓')
            except IndexError as err:
                self.logger.log(
                    'Retweeting @' + TWITTER_USERS[action] + ': ' + 'NO NEW TWEETS!', error=True)
                return False
            except tweepy.TweepError as err:
                m = 'Retweeting @' + \
                    TWITTER_USERS[action] + ': ' + str(err.message)
                m = m + 'check: https://twitter.com/statuses/' + \
                    str(twid)
                self.logger.log(m, error=True)
                return False
            except Exception, e:
                self.logger.log(
                    'Retweeting @' + TWITTER_USERS[action] + ': ' + str(e), error=True)
                return False
            return True
            # break
        else:
            self.logger.log(
                'Skipping action as not enough time has passed', emoji='⏲')
            return False

    def giphy_tweet(self):
        '''Tweet a random giphy #space gif'''
        self.tries += 1
        self.logger.log('trying to tweet a #space GIF')
        if self.logger.last_action_past_seconds(Actions.TweetActions.space_gif) > 12*60*60:
            try:
                c = giphy.Giphy()
                result = c.random(tag="space")
                URL = result['data']['image_original_url']
                urllib.urlretrieve(URL, 'gif.GIF')
                # time_str = str(datetime.now()).split('.')[0]
                url = result['data']['url']
                tags_str = ''.join(['#' + x.title() + ' ' for x in urllib2.urlopen(
                    url).geturl().split('/')[-1].split('-')[:-1] if x != 'space'])[:-1]

                status = ('🚀 New #Space #GIF from @Giphy!\n'
                          '' + tags_str + '\n'
                          '🔗 {}'.format(url))
                status = self.api.update_with_media('gif.GIF', status)

                self.logger.update_last_tweet(
                    Actions.TweetActions.space_gif, status)
                self.logger.log('#space GIF tweeted', emoji='🤓')
                self.tries = 0
            except Exception, e:
                self.logger.log(str(e), error=True)
                if self.tries < self.max_tries:
                    self.giphy_tweet()
                else:
                    self.logger.log(
                        'Skipping because of too much tries', error=True)

        else:
            self.logger.log(
                'Skipping action as not enough time has passed', emoji='⏲')
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
        timeline = filter(
            lambda status: status.entities.get("media") is not None, timeline)
        timeline = filter(lambda status: not any(
            word in status.text.split() for word in _word_blacklist), timeline)
        timeline = filter(
            lambda status: status.author.screen_name not in _user_blacklist, timeline)

        timeline.reverse()
        return timeline
