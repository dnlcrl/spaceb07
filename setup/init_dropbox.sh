#!/bin/bash
#This script sets up DropBox on Heroku + your local environment

echo
echo "We're going to need some DropBox API credentials."
echo "Check out https://www.dropbox.com/developers/apps"
echo "for instructions on creating your Access Token."
echo

confirmed_creds="n"
while [ $confirmed_creds != "y" ]; do

    echo -n "Access token: "
    read accesstoken

    echo "We read these credentials:"
    cat <<EOF
DROPBOX_ACCESS_TOKEN=$accesstoken
EOF
    echo "Is this correct? [y/n]"
    read confirmed_creds
done

#add the dropbox credentials to the Heroku app environment
echo
echo "Sending your DropBox API credentials up to Heroku..."
heroku config:add DROPBOX_ACCESS_TOKEN=$accesstoken

#create a script for setting up your local environment
cat <<EOF > setup_env_dropbox.sh
export DROPBOX_ACCESS_TOKEN=$accesstoken
EOF

echo
echo "Pushing to Heroku so that we can set up worker process"
git push heroku master

echo "Now you can \"source setup_env_dropbox.sh\" and get to work on that dropbox API!"
