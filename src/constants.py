#!/usr/bin/env python
# encoding: utf-8


class Actions:

    '''
    Actions constants
    '''
    class TweetActions:

        '''
        Tweets constants
        TODO: write once those freaking actons
        '''
        space_gif = 'space_gif'
        retweet_scott_kelly = 'retweet_scott_kelly'
        retweet_astro_kjell = 'retweet_astro_kjell'
        retweet_astro_kimiya = 'retweet_astro_kimiya'
        retweet_volkov_iss = 'retweet_volkov_iss'
        retweet_astro_jeff = 'retweet_astro_jeff'
        retweet_astro_tim = 'retweet_astro_tim'
        retweet_astro_timpeake = 'retweet_astro_timpeake'
        retweet_thom_astro = 'retweet_thom_astro'
        retweet_astropeggy = 'retweet_astropeggy'
        retweet_astro_kimbrough = 'retweet_astro_kimbrough'


class FileNames:

    '''
    Filenames constants
    '''
    _dir = 'data/'

    last_tweets = _dir + 'last_tweets.json'
    log_file = _dir + 'log.txt'
    giphy_keys = _dir + 'giphy_keys.txt'

    all_names = [last_tweets, log_file, giphy_keys]


TWITTER_USERS = {
    Actions.TweetActions.retweet_scott_kelly: 'StationCDRKelly',
    Actions.TweetActions.retweet_astro_kjell: 'astro_kjell',
    Actions.TweetActions.retweet_astro_kimiya: 'astro_kimiya',
    Actions.TweetActions.retweet_volkov_iss: 'volkov_iss',
    Actions.TweetActions.retweet_astro_jeff: 'Astro_Jeff',
    Actions.TweetActions.retweet_astro_tim: 'astro_tim',
    Actions.TweetActions.retweet_astro_timpeake: 'astro_timpeake',
    Actions.TweetActions.retweet_thom_astro: 'Thom_astro',
    Actions.TweetActions.retweet_astropeggy: 'AstroPeggy',
    Actions.TweetActions.retweet_astro_kimbrough: 'astro_kimbrough'
}
