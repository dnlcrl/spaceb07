#!/usr/bin/env python
# encoding: utf-8
import time
from twitterAPI import TwitterAPI
from constants import Actions
from logger import Logger


def main():
    logger = Logger()
    twitter = TwitterAPI(logger)
    actions = [Actions.TweetActions.space_gif,
               Actions.TweetActions.retweet_scott_kelly,
               Actions.TweetActions.retweet_astro_kjell,
               Actions.TweetActions.retweet_astro_kimiya,
               Actions.TweetActions.retweet_volkov_iss]

    while True:

        for action in actions:
            if action == Actions.TweetActions.space_gif:
                if twitter.giphy_tweet():
                    break
            else:
                word_whitelist = None
                word_blacklist = None
                if action == Actions.TweetActions.retweet_scott_kelly:
                    word_whitelist = ["#YearInSpace"]
                if twitter.retweet_astronaut(action, word_blacklist, word_whitelist):
                    break

        logger.log('Going to sleep for 30mins')
        time.sleep(1800)  # repeat every 30 mins


if __name__ == "__main__":
    main()
