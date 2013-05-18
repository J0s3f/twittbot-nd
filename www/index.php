<?php
/* 
 * This file is part of twittbot-nd
 * © 2013 nilsding
 * License: AGPLv3, read the LICENSE file in the repository root.
 * Grab the current source at https://github.com/nilsding/twittbot-nd
 */
session_start();
require_once('oauth/twitteroauth.php');
require_once('config.php');

function gen_key($acctoken, $acctokensecret) {
	$key = CONSUMER_KEY . '|' . CONSUMER_SECRET . '|' . $acctoken . '|' . $acctokensecret;
	$key = str_rot13($key);
	$key = strrev($key);
	$key = base64_encode($key);
	$key = strrev($key);
	$key = str_rot13($key);
	return $key;
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
?>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>twittbot-nd keygen</title>
<link rel="stylesheet" href="style.css" />
</head>
<body>
<h2>The Keygen™</h2>
<div class="content">
<p>This is a keygen for <a href="https://github.com/nilsding/twittbot-nd">twittbot-nd</a>, which generates you a key which you can use to let your bot tweet over my API keys, if you don't want to make a new app at dev.twitter.com.<br />I would not describe it as very secure, though.</p>
<p><?php if (!isset($_SESSION['access_token'])) { ?><a href="signin.php">Sign in with Twitter</a><?php } else { ?>
Your generated key is:<br />
<code><?php echo gen_key($_SESSION['access_token']['oauth_token'], $_SESSION['access_token']['oauth_token_secret']); ?></code><br />
Copy and paste it into your <strong>config.py</strong> file at line 27. Also be sure to set KEY_ENABLED to <strong>True</strong> 
<?php if ($admin) { ?></p>
<p>It seems you also are an admin for my bot, do you want to <a href="admin.php">administrate</a> it?
<?php } } ?></p>
</div>
<div class="footer">
This site is part of <a href="https://github.com/nilsding/twittbot-nd">twittbot-nd</a>, which is free software, <br />
licensed under the <a href="http://www.gnu.org/licenses/agpl-3.0.html">GNU Affero General Public License version 3</a>.
</div>
</body>
</html>
