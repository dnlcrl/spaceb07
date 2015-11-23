#!/usr/bin/env python
# encoding: utf-8


class Actions:

    '''
    Actions constants
    '''
    class TweetActions:

        '''
        Tweets constants
        TODO: split tweets and retweets action
        '''
        space_gif = 'space_gif'
        retweet_scott_kelly = 'retweet_scott_kelly'
        retweet_astro_kjell = 'retweet_astro_kjell'
        retweet_astro_kimiya = 'retweet_astro_kimiya'
        retweet_volkov_iss = 'retweet_volkov_iss'


class FileNames:

    '''
    Filenames constants
    '''
    last_tweets = 'data/last_tweets.json'
    log_file = 'data/log.txt'


TWITTER_USERS = {
    Actions.TweetActions.retweet_scott_kelly: 'StationCDRKelly',
    Actions.TweetActions.retweet_astro_kjell: 'astro_kjell',
    Actions.TweetActions.retweet_astro_kimiya: 'astro_kimiya',
    Actions.TweetActions.retweet_volkov_iss: 'volkov_iss'
}
