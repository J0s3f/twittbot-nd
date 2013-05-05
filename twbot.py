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

import traceback
import config
import os.path
import twittbot

def main():
	check_config()
	bot = twittbot.twittbot()
	while bot.active:
		try:
			bot.run()
		except KeyboardInterrupt:
			bot.end()
		except:
			traceback.print_exc()

def check_config():
	print '-- Checking if config is valid...'
	err = False
	if config.twittbot.interval < 1:
		print '\033[33m>!\033[0m `interval\' is set to a value which is less than 1.'
		print '   This is NOT recommended unless you know what you\'re doing.'
		err = True
	
	if not config.twittbot.admins:
		print '\033[36m>>\033[0m There are no values in the `admins\' list.'
		print '   Do not expect to control the bot using direct messages.'
	
	if err:
		print '\033[31m!!\033[0m You should review the config file.'
	else:
		print '\033[32mok\033[0m Config file seems to be fine.'
	
	print '-- Checking if files exist...'
	err = False
	
	try:
		with open(config.files.tweets_store): pass
	except IOError:
		print '\033[31m!!\033[0m The file \033[1m' + config.files.tweets_store + '\033[0m does not exist. Please create it.'
		err = True
	try:
		with open(config.files.reply_tweet): pass
	except IOError:
		print '\033[31m!!\033[0m The file \033[1m' + config.files.reply_tweet + '\033[0m does not exist. Please create it.'
		err = True
	try:
		with open(config.files.reply_random): pass
	except IOError:
		print '\033[31m!!\033[0m The file \033[1m' + config.files.reply_random + '\033[0m does not exist. Please create it.'
		err = True
	try:
		with open(config.files.retweet): pass
	except IOError:
		print '\033[31m!!\033[0m The file \033[1m' + config.files.retweet + '\033[0m does not exist. Please create it.'
		err = True
	try:
		with open(config.files.filter_users): pass
	except IOError:
		print '\033[31m!!\033[0m The file \033[1m' + config.files.filter_users + '\033[0m does not exist. Please create it.'
		err = True
	
	if err:
		print '\033[31m!!\033[0m Some files do not exist, please create them! System halted.'
		exit(2)
	else:
		print '\033[32mok\033[0m Yes they do exist.'

try:
	main()
except KeyboardInterrupt: pass