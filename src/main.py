#!/usr/bin/env python
# encoding: utf-8
import time
from twitterAPI import TwitterAPI
from constants import Actions


def main():
    twitter = TwitterAPI()
    actions = [Actions.TweetActions.space_gif,
               Actions.TweetActions.retweet_scott_kelly,
               Actions.TweetActions.retweet_astro_kjell,
               Actions.TweetActions.retweet_astro_kimiya]
    while True:
        # Send a tweet here!
        tweeted = False

        if not tweeted and Actions.TweetActions.space_gif in actions:
            if twitter.giphy_tweet():
                tweeted = True

        if not tweeted and Actions.TweetActions.retweet_scott_kelly in actions:
            if twitter.retweet_scott_kelly():
                tweeted = True

        if not tweeted and Actions.TweetActions.retweet_astro_kjell in actions:
            if twitter.retweet_astro_kjell():
                tweeted = True

        if not tweeted and Actions.TweetActions.retweet_astro_kimiya in actions:
            if twitter.retweet_astro_kimiya():
                tweeted = True
        print 'sleeping for 30 mins'
        time.sleep(1800)  # repeat every 30 mins


if __name__ == "__main__":
    main()
