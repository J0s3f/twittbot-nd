# -*- coding: utf-8 -*-
# This file is part of twittbot-nd
# Copyright (C) 2013 nilsding
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the 
# License, or (at your option) any later version. 
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details. 
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class oauth:
# Enter here the access tokens you got from dev.twitter.com
	CONSUMER_KEY        = ""
	CONSUMER_SECRET     = ""
	ACCESS_TOKEN        = ""
	ACCESS_TOKEN_SECRET = ""
	
	# If you're using my API keys using The Keygen™, be sure to check this.
	KEY_ENABLED = False
	KEY = ""

class twittbot:
	admins = [29952844] # Twitter user IDs of the admins.
	interval = 10        # The interval in minutes the tweets are posted.
	followback = False   # Follow back new followers
	okay_texts = ["Looks great.", "Okay.", "Success!", "Whee!", "\o/", "You now should", "Awesome!"]

class files:
	tweets_store = "tweets/tweet_file.txt" # Contains all tweets.
	reply_tweet = "tweets/reply_tweet.txt" # Contains all conditional replies. 
	reply_random = "tweets/reply_random.txt" # Contains all random replies.
	retweet = "tweets/retweet.txt" # Contains the terms to auto-retweet things.
	filter_users = "filter.txt" # Contains the user IDs of the user not to react to.
