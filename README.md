twittbot-nd
===========

`twittbot-nd` is a [twittbot.net](http://twittbot.net)-like application, written in Python. Thanks to tweepy it even supports Twitter's Streaming API, which makes it possible to answer to tweets instantly.

There still are some bugs, though. But who knows if they are actually bugs?

Features
--------

As of now (May 2013), `twittbot-nd` covers some important functions twittbot.net has to offer:

* Randomly tweet something every x minutes
* Reply people mentioning your bot
* Automatically follow back new followers (haven't tested it on my bot yet, but I think it should work)

`twittbot-nd` also features

* Instant replies through the Streaming API
* Control your bot using direct messages
* Automatically retweet tweets based on a list of words
* Ignore some users.
* RandomWords™ by Revengeday (can be used by placing `${{{RANDOMWORD}}}` in a tweet)
* Lots of spaghetti code! (don't even TRY to understand it)

Installation
------------

You need a **Python 2.7** installation and have tweepy installed. Install it by executing `easy_install tweepy`.

You run `twittbot-nd` by executing `python2.7 twbot.py` as the current user. If you want to run the bot in background, try using a terminal multiplexer, e.g. [tmux](http://tmux.sourceforge.net) or [GNU screen](http://www.gnu.org/software/screen/).

The files where the tweets are stored are located in `./tweets`.

**Important note if you're importing your tweets from twittbot.net:** Rename the file `retweet.txt` to `reply_tweet.txt`. It does not only make more sense, it also does not conflict with twittbot-nd's retweet.txt. 

Of course, if you want to, you can also change the file names in the `config.py` file. Which brings us to the...

Configuration
-------------

You configure twittbot-nd by editing the `config.py` file. It contains your Twitter API keys which you get by making a new application on [dev.twitter.com](https://dev.twitter.com) and setting the access rights to **Read, Write and Direct Messages**.

You define the admins of the bot (who can control it over direct messages) in the list `admins`. This contains the user IDs, which you can get by executing `python getuserid.py nilsding`. 

The rest of the config file should be self-explaining.

If you want to add someone to the great ignore list of hell, try `python getuserid.py userName >> filters.txt`.

Commands
--------

If you are an admin and send your bot a direct message, he will automatically reply to it and execute it. If you're not a known admin, he just ignores the direct message.
You can use the following commands to control the bot:

* `**CMDS**` - Lists all available commands.
* `**RELO**` - Reloads the bot.
* `**BCST** text` - Sends a text to all known admins
* `**TWET** tweet` - Tweets a tweet.
* `**+TWT** tweet` - Adds a tweet to the tweet store.
* `**+RRP** tweet` - Adds a tweet to the random reply tweet store.
* `**+RET** tag` - Adds a tag to the auto retweet list.
* `**FILT** username` - Adds this user to the filter list.
* `**FOLO** username` - Follows an user.
* `**UFOL** username` - Unfollows an user.
* `**STOP BOT**` - Stops the bot. 

The commands are case-insensitive.
