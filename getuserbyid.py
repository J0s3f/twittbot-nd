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

# This program gets the user ID of a given Twitter user (using sys.argv[1])

import sys
import tweepy
from config import oauth

try:
	auth = tweepy.OAuthHandler(oauth.CONSUMER_KEY, oauth.CONSUMER_SECRET)
	auth.set_access_token(oauth.ACCESS_TOKEN, oauth.ACCESS_TOKEN_SECRET)
	print tweepy.API(auth).get_user(sys.argv[1]).screen_name
except tweepy.error.TweepError, err:
	print(err.reason)

