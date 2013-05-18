<?php
/* 
 * This file is part of twittbot-nd
 * © 2013 nilsding
 * License: AGPLv3, read the LICENSE file in the repository root.
 * Grab the current source at https://github.com/nilsding/twittbot-nd
 */

define('CONSUMER_KEY', 'your_consumer_key');
define('CONSUMER_SECRET', 'your_consumer_secret');
define('OAUTH_CALLBACK', 'http://example.com/path/to/callback.php');

$path_to_twittbot = '/home/nilsding/dev/twittbot-nd/'; # the / at the end is important

define('BOT_NAME', 'MySuperAwesomeTwitterBot666');
define('FILE_ADMINS', $path_to_twittbot . 'admins.txt'); # python: config.files.admins
define('FILE_TWEETS_STORE', $path_to_twittbot . 'tweets/tweet_file.txt'); # python: config.files.tweets_store
define('FILE_REPLY_TWEET', $path_to_twittbot . 'tweets/reply_tweet.txt'); # python: config.files.reply_tweet
define('FILE_REPLY_RANDOM', $path_to_twittbot . 'tweets/reply_random.txt'); # python: config.files.reply_random
define('FILE_RETWEET', $path_to_twittbot . 'tweets/retweet.txt'); # python: config.files.retweet
define('FILE_FILTER', $path_to_twittbot . 'filter.txt'); # python: config.files.filter_users

