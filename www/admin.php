<?php
/* 
 * This file is part of twittbot-nd
 * © 2013 nilsding
 * License: AGPLv3, read the LICENSE file in the repository root.
 * Grab the current source at https://github.com/nilsding/twittbot-nd
 */
session_start();
require_once('config.php');

if (!isset($_GET['p'])) {
	$page = "main";
} else {
	$page = $_GET['p'];
}

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

$message = (isset($_GET['message']) ? $_GET['message'] : -1);
switch ((int) $message) {
	case 0:
		$message = "Everything's fine, send your bot a direct message with &quot;RELO&quot; to reload!";
		break;
	case 1:
		$message = "Could not open file";
		break;
	case 2:
		$message = "Could not write into file";
		break;
	case 3:
		$message = "The file is not writable :(";
		break;
	case 4:
		$message = "wait what are you doing nOOOOOOOOO";
	case -1:
	default:
		unset($message);
		break;
}
?>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>twittbot-nd admin</title>
<link rel="stylesheet" href="style.css" />
</head>
<body>
<h2>twittbot-nd admin</h2>
<div class="content">
<?php if (!isset($_SESSION['user_id'])) { ?>
<p>You do not seem to be signed in, please do this now and return to this page when done.</p>
<p><a href="signin.php">Sign in with Twitter</a></p>
<?php } else { ?>

<?php if ($admin) { /* Hello, admin! */ ?>
<ul class="adm-menu">
<li><a href="admin.php?p=main">Main page</a></li>
<li><a href="admin.php?p=admins">Admins</a></li>
<li><a href="admin.php?p=tweets">Tweets</a></li>
<!--<li><a href="admin.php?p=creply">Conditional replies</a></li>-->
<li><a href="admin.php?p=rreply">Random replies</a></li>
<li><a href="admin.php?p=retweet">Retweet tags</a></li>
<li><a href="admin.php?p=filter">Filtered users</a></li>
</ul>
<?php if (isset($message)) { ?>
<p class="message"><?php echo $message; ?></p>
<?php
}
switch ($page) {
case 'admins':
?>
<p>You are editing the file <b><?php echo FILE_ADMINS; ?></b>, which contains the Twitter user IDs of the admins.</p>
<p>Each line is the Twitter user ID of an user.</p>
<form method="post" action="store_cfg.php">
<textarea name="content" rows="20" cols="60">
<?php echo file_get_contents(FILE_ADMINS); ?>
</textarea><br />
<input name="type" type="hidden" value="admins">
<button>Save</button>
</form>
<?php
break;
case 'tweets':
?>
<p>You are editing the file <b><?php echo FILE_TWEETS_STORE; ?></b>, which contains all tweets which are tweeted every few minutes.</p>
<p>Every tweet has its own line. To create a line break, simply write <b class="dhd">\n</b>. For a random word, write <b class="dhd">${{{RANDOMWORD}}}</b>.</p>
<form method="post" action="store_cfg.php">
<textarea name="content" rows="20" cols="60">
<?php echo file_get_contents(FILE_TWEETS_STORE); ?>
</textarea><br />
<input name="type" type="hidden" value="tweets">
<button>Save</button>
</form>
<?php
break;
case 'creply':
?>
<p>You are editing the file <b><?php echo FILE_REPLY_TWEET; ?></b>, which contains all conditional replies.</p>
<p>Syntax: <b class="dhd">word,this is a tweet</b> (the <span class="dhd">,</span> is the splitter)</p>
<p>Every tweet has its own line. To create a line break, simply write <b class="dhd">\n</b>. For a random word, write <b class="dhd">${{{RANDOMWORD}}}</b>.</p>
<form method="post" action="store_cfg.php">
<textarea name="content" rows="20" cols="60">
<?php echo file_get_contents(FILE_REPLY_TWEET); ?>
</textarea><br />
<input name="type" type="hidden" value="creply">
<button>Save</button>
</form>
<?php
break;
case 'rreply':
?>
<p>You are editing the file <b><?php echo FILE_REPLY_RANDOM; ?></b>, which contains all random replies.</p>
<p>Every tweet has its own line. To create a line break, simply write <b class="dhd">\n</b>. For a random word, write <b class="dhd">${{{RANDOMWORD}}}</b>.</p>
<form method="post" action="store_cfg.php">
<textarea name="content" rows="20" cols="60">
<?php echo file_get_contents(FILE_REPLY_RANDOM); ?>
</textarea><br />
<input name="type" type="hidden" value="rreply">
<button>Save</button>
</form>
<?php
break;
case 'retweet':
?>
<p>You are editing the file <b><?php echo FILE_RETWEET; ?></b>, which contains all retweet tags.</p>
<p>Every tag has its own line.</p>
<form method="post" action="store_cfg.php">
<textarea name="content" rows="20" cols="60">
<?php echo file_get_contents(FILE_RETWEET); ?>
</textarea><br />
<input name="type" type="hidden" value="retweet">
<button>Save</button>
</form>
<?php
break;
case 'filter':
?>
<p>You are editing the file <b><?php echo FILE_FILTER; ?></b>, which contains the Twitter user IDs of the admins.</p>
<p>Each line is the Twitter user ID of an user.</p><form method="post" action="store_cfg.php">
<textarea name="content" rows="20" cols="60">
<?php echo file_get_contents(FILE_FILTER); ?>
</textarea><br />
<input name="type" type="hidden" value="filter">
<button>Save</button>
</form>
<?php
break;
case 'main':
default:
?>
<p>Welcome to the administration page of my bot <?php echo BOT_NAME; ?>!<p>
<?php 
}
} else {
/* not an admin */
?>

<p>You are not an admin of my bot <?php echo BOT_NAME; ?>.</p>

<?php
}
}
?>

</div>
<div class="footer">
This site is part of <a href="https://github.com/nilsding/twittbot-nd">twittbot-nd</a>, which is free software, <br />
licensed under the <a href="http://www.gnu.org/licenses/agpl-3.0.html">GNU Affero General Public License version 3</a>.
</div>
</body>
</html>
