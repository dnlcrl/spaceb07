# spaceb07
Code for my first Twitter bot: http://twitter.com/spaceb07, running on Heroku.

spaceb07 tweets a random GIF tagged "space" from Giphy.com, every 24 hours,
retweets image pictures from astronauts curently in space (check http://www.howmanypeopleareinspacerightnow.com/ for a list of curently in space astronauts).


# Create Your Own Twitter Bot:

1. Create your twitter account and setup an app for that account on the twitter's developers page, so you can have all the needed security tokens.
2. Run `setup/init.sh` and follow the instructions to create an Heroku app for your bot.
4. Run `setup/init_dropbox.sh` and follow the instructions to link the Heroku app to your dropbox.
5. Edit the `bot.py` file to customize your bot and cast some spells.
6. Push the edits on heroku with `git push heroku master`.
7. Enjoy.
