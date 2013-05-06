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
<?php } ?></p>
</div>
<div class="footer">
This keygen part of <a href="https://github.com/nilsding/twittbot-nd">twittbot-nd</a>, which is free software, licensed under the <a href="http://www.gnu.org/licenses/agpl-3.0.html">GNU Affero General Public License version 3</a>.
</div>
</body>
</html>
