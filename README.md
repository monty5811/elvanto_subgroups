# Elvanto Subgroups

Small webapp to provide one way sync for Elvanto groups. 

**NOTE** this may destroy all your data - this has not been fully tested yet!!

This app was developed for use at [St Columba's Free Church](http://www.stcsfc.org/). 

![Screenshot](/screenshot.png?raw=true)

## Example use case

You have a "sound" group and a "screens" group in Elvanto and want to create a "technial team" group made up of the "sound" and "screens" group. 

1. Setup this apps
2. Link the groups
3. Populate the subgroups
4. Wait for the sync to run
5. Enjoy your synchronised groups

## Installation

This app should run comfortably on Heroku's free tier providing you do not sync too frequently.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

 - Create credentials on google TODO: link
 - Click the push to deploy button
 - Add secrets as config variables on heroku
 - Setup a recurring task to run the command `./manage.py pull_from_elvanto && ./manage.py sync_groups` using the scheduler addon

## Contributing

All contributionsa are welcome. However, to make things as easy as possible, please fork this repo and then create a new feature branch and work in that - it makes things far [easier](http://codeinthehole.com/writing/pull-requests-and-other-good-practices-for-teams-using-github/).

## Todo

 - Migrate authenitcation to Elvanto oauth instead of Google
 - Propagate group properties on sync (e.g. group pictures)
 - Warn user of circular dependencies
 - Store relations in a custom field in Elvanto - allows for a stateless app
