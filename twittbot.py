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

import os
import sys
import traceback
import config
import tweepy
import httplib2
import random
from time import sleep
try:
	import json
except ImportError:
	import simplejson as json

class twittbot:
	def __init__(self):
		self.active = True
		self.load_files()
		self.init_api()
		self.init_stream()
		self.init_user_stream()
	
	def load_files(self):
		try:
			with open(config.files.retweet) as f:
				self.retweet_tags = [s.rstrip('\n') for s in f.readlines()]
				print '\033[32mok\033[0m Loaded %d retweet tags.' % len(self.retweet_tags)
			with open(config.files.filter_users) as f:
				self.filter_users = [s.rstrip('\n') for s in f.readlines()]
				print '\033[32mok\033[0m Loaded %d user IDs to be filtered.' % len(self.filter_users)
			with open(config.files.tweets_store) as f:
				self.tweets_store = [s.rstrip('\n') for s in f.readlines()]
				print '\033[32mok\033[0m Loaded %d tweets.' % len(self.tweets_store)
			with open(config.files.reply_tweet) as f:
				self.reply_tweet = [s.rstrip('\n') for s in f.readlines()]
				print '\033[32mok\033[0m Loaded %d conditional reply tweets.' % len(self.reply_tweet)
			with open(config.files.reply_random) as f:
				self.reply_random = [s.rstrip('\n') for s in f.readlines()]
				print '\033[32mok\033[0m Loaded %d random reply tweets.' % len(self.reply_random)
		except:
			print '\033[31m!!\033[0m I failed loading the text files :-('
			traceback.print_exc()
			print 'System halted.'
			exit(1)
	
	def init_api(self):
		try:
			print '-- Logging in...'
			self.auth = tweepy.OAuthHandler(config.oauth.CONSUMER_KEY, config.oauth.CONSUMER_SECRET)
			self.auth.set_access_token(config.oauth.ACCESS_TOKEN, config.oauth.ACCESS_TOKEN_SECRET)
			self.api = tweepy.API(self.auth)
			self.me = self.api.me()
			print '\033[36m>>\033[0m Logged in as \033[1m' + self.me.screen_name + '\033[0m'
		except:
			print '\033[31m!!\033[0m Failed to log in.'
			traceback.print_exc()
			print 'System halted.'
			exit(1)
	
	def init_stream(self):
		print '-- Initializing tweet stream'
		class StreamListener(tweepy.StreamListener):
			def on_status(self_, status):
				self.process_status(status)
		slistener = StreamListener()
		self.stream = tweepy.Stream(auth = self.auth, listener = slistener)
		print '\033[32mok\033[0m Done.'
	
	def init_user_stream(self):
		print '-- Initializing user stream'
		class StreamListener(tweepy.StreamListener):
			def on_status(self_, status):
				self.process_status(status, timeline_reply = True)
			def on_data(self_, data):
				if 'direct_message' in data:
					dm = json.loads(data)['direct_message']
					self.process_direct_message(dm)
					return
				if '"event":"follow"' in data:
					self.auto_followback(json.loads(data)['source'])
		ulistener = StreamListener()
		self.user_stream = tweepy.Stream(auth = self.auth, listener = ulistener)
		print '\033[32mok\033[0m Done.'
	
	def run(self):
		if not self.user_stream.running:
			print '-- Connecting to user stream...'
			self.user_stream.userstream(async = True)
		if not self.stream.running:
			print '-- Connecting main tweet stream...'
			self.track = ['@' + self.me.screen_name]
			self.track.extend(self.retweet_tags)
			self.stream.filter(track = self.track, async = True)
		random_tweet = self.tweets_store[random.randint(0, len(self.tweets_store) - 1)].replace("\\n", chr(0x0A))
		if '${{{RANDOMWORD}}}' in random_tweet:
			random_tweet = random_tweet.replace('${{{RANDOMWORD}}}', self.random_word())
		try:
			self.api.update_status(status = tweepy.utils.unescape_html(random_tweet)) 
		except:
			pass
		sleep(config.twittbot.interval * 60)	
	
	def end(self):
		print '\033[31;1mWill now exit.\033[0m'
		self.active = False
		print '-- Disconnecting streams...'
		self.stream.disconnect()
		self.user_stream.disconnect()
	
	def re_load(self):
		print '-- Reloading files'
		self.load_files()
		print '-- Disconnecting main tweet stream...'
		self.stream.disconnect()
	
	def process_status(self, status, timeline_reply = False):
		if "RT @" in status.text[0:4]:
			return
		if (str(status.user.id) in self.filter_users): # We ignore that user.
			print '\033[31;1mIgnored user ' + status.user.screen_name + ':\033[0m ' + str(status.text).encode('utf-8')
			return
		if not timeline_reply:
			if not status.user.id == self.me.id:
				for tag in self.retweet_tags:          # A tweet will get retweeted.
					if tag.lower() in status.text.lower():
						self.api.retweet(status.id)
						try:
							print '\033[34;1mRetweeted ' + status.user.screen_name + ':\033[0m ' + str(status.text).encode('utf-8')
						except:
							print '\033[34;1mRetweeted a tweet.\033[0m'
				if self.me.screen_name.lower() in status.text.lower():
					try:
						print '\033[33;1mMentioned by ' + status.user.screen_name + ':\033[0m ' + str(status.text).encode('utf-8')
					except:
						print '\033[33;1mMentioned by ' + status.user.screen_name + '\033[0m'
					randrep = self.reply_random[random.randint(0, len(self.reply_random) - 1)].replace("\\n", chr(0x0A))
					if '${{{RANDOMWORD}}}' in randrep:
						randrep = randrep.replace('${{{RANDOMWORD}}}', self.random_word())
					randrep = '@' + status.user.screen_name + ' ' + randrep
					try:
						self.api.update_status(randrep[0:140], in_reply_to_status_id = status.id)
						try:
							print '\033[33mrandom replied:\033[0m ' + randrep.encode('utf-8')
						except:
							print '\033[33mrandom replied something\033[0m'
					except:
						print '\033[31m!! ' + traceback.format_exc().splitlines()[-1] + '\033[0m'
		if timeline_reply:
			pass
	
	def process_direct_message(self, data):
		if data['sender']['id_str'] in str(self.me.id):
			return
		try:
			print '\033[35;1mDirect Message from ' + data['sender']['screen_name'] + ':\033[0m ' + str(data['text']).encode('utf-8')
		except:
			print '\033[35;1mDirect Message from ' + data['sender']['screen_name'] + '.\033[0m'
		if not data['sender']['id'] in config.twittbot.admins:
			print '\033[35m' + data['sender']['screen_name'] + ' is not an admin, ignoring\033[0m'
			return
		if 'TWET ' in data['text'][0:5].upper():  # Tweets a tweet.
			try:
				print '\033[35mCommand: TWET, tweeting \033[0m' + str(data['text'][5:140]).encode('utf-8')
			except:
				print '\033[35mCommand: TWET, tweeting a tweet.\033[0m'
			tweet = data['text'][5:140]
			if '${{{RANDOMWORD}}}' in tweet:
				tweet = tweet.replace('${{{RANDOMWORD}}}', self.random_word())
			try:
				status = self.api.update_status(tweepy.utils.unescape_html(tweet))
				self.api.send_direct_message(user = data['sender']['screen_name'], text = "Success! Read the tweet at https://twitter.com/{0}/status/{1}".format(status.user.screen_name, status.id_str))
			except:
				self.api.send_direct_message(user = data['sender']['screen_name'], text = traceback.format_exc().splitlines()[-1])
				print '\033[31m!! ' + traceback.format_exc().splitlines()[-1] + '\033[0m'
		elif 'BCST ' in data['text'][0:5].upper():  # Broadcasts a direct message to all admins.
			try:
				print '\033[35mCommand: BCST, sending \033[0m' + str(data['text'][5:140]).encode('utf-8') + '\033[35m to all admins.\033[0m'
			except:
				print '\033[35mCommand: BCST, sending a direct message to all admins.\033[0m'
			message_from = "[%s] " % data['sender']['screen_name']
			for admin in config.twittbot.admins:
				try:
					self.api.send_direct_message(user = admin, text = str(message_from + tweepy.utils.unescape_html(data['text'][5:140 - len(message_from)])))
				except:
					pass
		elif 'RELO' in data['text'][0:5].upper():  # Reload all files.
			print '\033[35mCommand: RELO, reloading...\033[0m'
			self.api.send_direct_message(user = data['sender']['screen_name'], text = 'Reloading files. Please wait.')
			try:
				self.re_load()
				self.api.send_direct_message(user = data['sender']['screen_name'], text = 'Reload complete!')
				print '\033[32mok\033[0m Reload complete!'
			except:
				self.api.send_direct_message(user = data['sender']['screen_name'], text = traceback.format_exc().splitlines()[-1])
				print '\033[31m!! ' + traceback.format_exc().splitlines()[-1] + '\033[0m'
		elif '+RET ' in data['text'][0:5].upper():  # Add a retweet tag.
			try:
				print '\033[35mCommand: +RET, adding \033[0m' + str(data['text'][5:140]).encode('utf-8') + '\033[35m to the list of retweet tags\033[0m'
			except:
				print '\033[35mCommand: +RET, adding something to the list of retweet tags\033[0m'
			with open(unicode(config.files.retweet, errors = 'replace'), "a") as f:
				f.write(data['text'][5:140].encode('utf-8', errors = 'replace') + '\n')
			self.api.send_direct_message(user = data['sender']['screen_name'], text = 'Added `' + data['text'][5:140] + '`. Write `RELO` to complete.')
		elif '+RRP ' in data['text'][0:5].upper(): # Add a random reply tweet
			try:
				print '\033[35mCommand: +RRP, adding \033[0m' + str(data['text'][5:140]).encode('utf-8') + '\033[35m to the random reply list\033[0m'
			except:
				print '\033[35mCommand: +RRP, adding something to the random reply list\033[0m'
			try:
				with open(unicode(config.files.reply_random, errors = 'replace'), "a") as f:
					f.write(data['text'][5:140].replace(chr(0x0A), "\\n").encode('utf-8', errors = 'replace') + '\n')
				self.api.send_direct_message(user = data['sender']['screen_name'], text = config.twittbot.okay_texts[random.randint(0, len(config.twittbot.okay_texts) - 1)] + ' Write `RELO` to complete.')
			except:
				self.api.send_direct_message(user = data['sender']['screen_name'], text = 'Got an error: ' +  traceback.format_exc().splitlines()[-1])
		elif '+TWT ' in data['text'][0:5].upper(): # Add a tweet
			try:
				print '\033[35mCommand: +TWT, adding \033[0m' + str(data['text'][5:140]).encode('utf-8') + '\033[35m to the random tweet list.\033[0m'
			except:
				print '\033[35mCommand: +TWT, adding something to the random tweet list.\033[0m'
			try:
				with open(unicode(config.files.tweets_store, errors = 'replace'), "a") as f:
					f.write(data['text'][5:140].replace(chr(0x0A), "\\n").encode('utf-8', errors = 'replace') + '\n')
				self.api.send_direct_message(user = data['sender']['screen_name'], text = config.twittbot.okay_texts[random.randint(0, len(config.twittbot.okay_texts) - 1)] + ' Write `RELO` to complete.')
			except:
				self.api.send_direct_message(user = data['sender']['screen_name'], text = 'Got an error: ' +  traceback.format_exc().splitlines()[-1])
		elif 'FILT ' in data['text'][0:5].upper():  # Add an user to filters
			print '\033[35mCommand: FILT, adding \033[0m' + str(data['text'][5:140]).encode('utf-8') + '\033[35m to the filter of doom.\033[0m'
			try:
				user_id = self.api.get_user(data['text'][5:140]).id
				with open(unicode(config.files.filter_users, errors = 'replace'), "a") as f:
					f.write(data['text'][5:140].encode('utf-8', errors = 'replace') + '\n')
				self.api.send_direct_message(user = data['sender']['screen_name'], text = 'Added `' + data['text'][5:140] + '`. Write `RELO` to complete.')
			except:
				self.api.send_direct_message(user = data['sender']['screen_name'], text = traceback.format_exc().splitlines()[-1])
				print '\033[31m!! ' + traceback.format_exc().splitlines()[-1] + '\033[0m'
		elif 'FOLO ' in data['text'][0:5].upper():
			print '\033[35mCommand: FOLO, following user \033[0m' + str(data['text'][5:140]).encode('utf-8') + '.\033[0m'
			try:
				self.api.create_friendship(screen_name = data['text'][5:140])
				self.api.send_direct_message(user = data['sender']['screen_name'], text = 'Successfully followed user `' + data['text'][5:140] + '`.')
			except:
				self.api.send_direct_message(user = data['sender']['screen_name'], text = traceback.format_exc().splitlines()[-1])
				print '\033[31m!! ' + traceback.format_exc().splitlines()[-1] + '\033[0m'
		elif 'UFOL ' in data['text'][0:5].upper():
			print '\033[35mCommand: UFOL, unfollowing user \033[0m' + str(data['text'][5:140]).encode('utf-8') + '.\033[0m'
			try:
				self.api.destroy_friendship(screen_name = data['text'][5:140])
				self.api.send_direct_message(user = data['sender']['screen_name'], text = 'Successfully unfollowed user `' + data['text'][5:140] + '`.')
			except:
				self.api.send_direct_message(user = data['sender']['screen_name'], text = traceback.format_exc().splitlines()[-1])
				print '\033[31m!! ' + traceback.format_exc().splitlines()[-1] + '\033[0m'
		elif 'STOP BOT' in data['text'][0:8].upper():
			print '\033[35mCommand: STOP, stopping bot.\033[0m'
			self.api.send_direct_message(user = data['sender']['screen_name'], text = 'Good bye.')
			self.end()
		elif 'CMDS' in data['text'][0:4].upper():
			print '\033[35mCommand: CMDS, sending all available commands.'
			self.api.send_direct_message(user = data['sender']['screen_name'], text = '(1/2) I know the following commands:')
			self.api.send_direct_message(user = data['sender']['screen_name'], text = '(2/2) CMDS; RELO; TWET tweet; +TWT tweet; +RRP tweet; +RET tag; FILT user; FOLO user; UFOL user; STOP BOT; BCST message')
		else:
			print '\033[35mUnknown command %s. \033[0m' % data['text'][0:4]
			self.api.send_direct_message(user = data['sender']['screen_name'], text = 'Unknown command `' + data['text'][0:4] + '\'. Type CMDS for a list of a commands.')
	
	def auto_followback(self, data):
		print '\033[36;1mNew follower:\033[0m ' + data['screen_name']
		if config.twittbot.followback:
			try:
				print '\033[36mFollowing back...\033[0m'
				self.api.create_friendship(screen_name = data['screen_name'])
			except:
				print '\033[31m!! ' + traceback.format_exc().splitlines()[-1] + '\033[0m'

	def random_word(self):
		resp, word = httplib2.Http().request('http://dev.revengeday.de/pointlesswords/api/')
		return word

