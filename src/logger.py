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

    '''
    def __init__(self):
        self.saver = Saver()
        try:
            self.last_tweets = load_json(FileNames.last_tweets)
        except Exception:
            self.last_tweets = {}

    def save_last_tweets(self):
        save_json(self.last_tweets, FileNames.last_tweets)
        self.saver.sync()

    def update_last_tweet(self, action, status):
        if not action in self.last_tweets.keys():
           # self.last_tweets[action]
     #   if self.last_tweets[action] is None
            self.last_tweets[action] = {}
        self.last_tweets[action]['datetime'] = datetime.now().strftime('%Y%m%d%H%M%S')
        self.last_tweets[action]['id'] = status.id
        self.save_last_tweets()

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
            self.log(str(e), error=True)
        return (datetime.now() - t).total_seconds()

    def log(self, message, error=False):
        with open(FileNames.log_file, 'a+') as outfile:
            outfile.write(('ERROR 😡' if error else '') + message + ' ' + str(datetime.now()) + '\n')
        self.saver.sync()
