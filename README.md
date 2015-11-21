# spaceb07
:rocket: Space addicted twitter bot: http://twitter.com/spaceb07, running on Heroku.

- Tweets a random GIF tagged "space" from Giphy.com (one every 24 hours).
- Retweets image pictures from astronauts curently in space (one every 30 minutes, 2 hours between retweets from the same user. Check http://www.howmanypeopleareinspacerightnow.com/ for a list of curently in space astronauts). Currently retweeting from:
  - Kjell Lindgren: https://twitter.com/astro_kjell
  - Scott Kelly: https://twitter.com/StationCDRKelly
  - Kimiya Yui: https://twitter.com/astro_kimiya
  - Sergey Volkov: https://twitter.com/volkov_iss

# Create Your Own Twitter Bot:

1. Create your twitter account and setup an app for that account on the twitter's developers page, so you can have all the needed security tokens.
2. Run `setup/init.sh` and follow the instructions to create an Heroku app for your bot.
4. Run `setup/init_dropbox.sh` and follow the instructions to link the Heroku app to your dropbox.
5. Edit the `bot.py` file to customize your bot and cast some spells.
6. Push the edits on heroku with `git push heroku master`.
7. Enjoy.
