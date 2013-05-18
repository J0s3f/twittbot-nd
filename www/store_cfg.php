<?php
/* 
 * This file is part of twittbot-nd
 * © 2013 nilsding
 * License: AGPLv3, read the LICENSE file in the repository root.
 * Grab the current source at https://github.com/nilsding/twittbot-nd
 */
session_start();
require_once('config.php');

/* rmempty by MeikoDis - https://github.com/MeikoDis/waschi/blob/master/list.php */
function rmempty($array) {
	foreach ($array as $key => $value) {
		if ($value === '') unset ($array[$key]);
	}
	unset($key);
	return $array;
}

$admins = rmempty(explode("\n", file_get_contents(FILE_ADMINS)));
$admin = false;

if (isset($_SESSION['user_id'])) {
	foreach ($admins as $user) {
		if ((string) $_SESSION['user_id'] === rtrim($user)) {
			$admin = true;
			unset($user);
			break;
		}
	}
}

if (!$admin) {
	header('Location: /');
	die();
}
if (!isset($_POST['content'])) {
	header('Location: /admin.php');
	die();
} else {
	$content = $_POST['content'];
}

$content = str_replace ("\r", '', $content); // get rid of that nasty <CR> in the line endings, we're on Unix, not Windows!

$type = (isset($_POST['type'])) ? $_POST['type'] : null;

try {
switch ($type) {
	case 'admins':
		if (is_writable(FILE_ADMINS)) {
			if (!$fh = fopen(FILE_ADMINS, 'wb')) {
				header('Location: /admin.php?p=admins&message=1');
				die();
			}
			if (!fwrite($fh, $content)) {
				header('Location: /admin.php?p=admins&message=2');
			}
			header('Location: /admin.php?p=admins&message=0');
		} else {
			header('Location: /admin.php?p=admins&message=3');
		}
		break;
	case 'tweets':
		if (is_writable(FILE_TWEETS_STORE)) {
			if (!$fh = fopen(FILE_TWEETS_STORE, 'wb')) {
				header('Location: /admin.php?p=tweets&message=1');
				die();
			}
			if (!fwrite($fh, $content)) {
				header('Location: /admin.php?p=tweets&message=2');
			}
			header('Location: /admin.php?p=tweets&message=0');
		} else {
			header('Location: /admin.php?p=tweets&message=3');
		}
		break;
	case 'creply':
		if (is_writable(FILE_REPLY_TWEET)) {
			if (!$fh = fopen(FILE_REPLY_TWEET, 'wb')) {
				header('Location: /admin.php?p=creply&message=1');
				die();
			}
			if (!fwrite($fh, $content)) {
				header('Location: /admin.php?p=creply&message=2');
			}
			header('Location: /admin.php?p=creply&message=0');
		} else {
			header('Location: /admin.php?p=creply&message=3');
		}
		break;
	case 'rreply':
		if (is_writable(FILE_REPLY_RANDOM)) {
			if (!$fh = fopen(FILE_REPLY_RANDOM, 'wb')) {
				header('Location: /admin.php?p=rreply&message=1');
				die();
			}
			if (!fwrite($fh, $content)) {
				header('Location: /admin.php?p=rreply&message=2');
			}
			header('Location: /admin.php?p=rreply&message=0');
		} else {
			header('Location: /admin.php?p=rreply&message=3');
		}
		break;
	case 'retweet':
		if (is_writable(FILE_RETWEET)) {
			if (!$fh = fopen(FILE_RETWEET, 'wb')) {
				header('Location: /admin.php?p=retweet&message=1');
				die();
			}
			if (!fwrite($fh, $content)) {
				header('Location: /admin.php?p=retweet&message=2');
			}
			header('Location: /admin.php?p=retweet&message=0');
		} else {
			header('Location: /admin.php?p=retweet&message=3');
		}
		break;
	case 'filter':
		if (is_writable(FILE_FILTER)) {
			if (!$fh = fopen(FILE_FILTER, 'wb')) {
				header('Location: /admin.php?p=filter&message=1');
				die();
			}
			if (!fwrite($fh, $content)) {
				header('Location: /admin.php?p=filter&message=2');
			}
			header('Location: /admin.php?p=filter&message=0');
		} else {
			header('Location: /admin.php?p=filter&message=3');
		}
		break;
	default:
		header('Location: /admin.php?message=4');
}
} catch (Exception $ex) {
	echo ('Error in script: ' . $ex);
};
