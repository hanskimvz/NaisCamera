<?php
header("Content-Type: text/json");
include $_SERVER['DOCUMENT_ROOT']."/phpseclib/Net/SSH2.php";

$ssh = new Net_SSH2('127.0.0.1');
print ("hello");
$ret = $ssh->login('root', 'pass');
print_r($ret);
print ("hello");
// print_r($ssh);
echo $ssh->exec('pwd');
// echo $ssh->exec('ls -la');
?>