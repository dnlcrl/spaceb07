#!/usr/bin/env python
# encoding: utf-8

from utils import load_json, save_json
from saver import Saver
from constants import FileNames
from datetime import datetime


class Logger:

    '''
    Class for keep a track of what's going on.
    TODO: methods docstrings
    TODO: fix logs timestamp as int not str

    '''

    def __init__(self, debug=False):
        self.debug = debug
        self.saver = Saver()
        self.last_tweets = self.maybe_load(FileNames.last_tweets)
        self.giphy_keys = self.maybe_load(FileNames.giphy_keys)

    def maybe_load(self, fname):
        try:
            return load_json(fname)
        except:
            return {}

    def save_dict(self, d, fname):
        save_json(d, fname)
        self.saver.sync()

    def save_last_tweets(self):
        self.save_dict(self.last_tweets, FileNames.last_tweets)

    def save_giphy_keys(self):
        self.save_dict(self.giphy_keys, FileNames.giphy_keys)

    def update_last_tweet(self, action, status):
        if not action in self.last_tweets.keys():
            self.last_tweets[action] = {}
        self.last_tweets[action][
            'datetime'] = datetime.now().strftime('%Y%m%d%H%M%S')
        self.last_tweets[action]['id'] = status.id
        self.save_last_tweets()

    def tweeted_gif(self, key):
        if self.giphy_keys == {}:
            self.giphy_keys['keys'] = []
            return False
        else:
            if key in self.giphy_keys['keys']:
                return True
            else:
                self.giphy_keys['keys'].append(key)
                self.save_giphy_keys()
                return False

    def last_action_id(self, action):
        try:
            return self.last_tweets[action]['id']
        except Exception:
            return None

    def last_action_past_seconds(self, action):
        t = datetime.utcfromtimestamp(0)
        try:
            t = datetime.strptime(
                self.last_tweets[action]['datetime'], '%Y%m%d%H%M%S')
        except Exception, e:
            self.log(
                'Reading self.last_tweets[action]["datetime"]' + str(e), error=True)
        return (datetime.now() - t).total_seconds()

    def log(self, message, error=False, emoji=None):
        if emoji is None:
            emoji = ('😡' if error else 'ℹ️')
        message = emoji + (' ERROR ' if error else '️ ') + \
            message + ' ' + str(datetime.now()) + '\n'

        if not self.debug:
            print message
            return

        with open(FileNames.log_file, 'a+') as outfile:
            outfile.write(message)
        self.saver.sync()
