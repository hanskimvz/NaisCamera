<?php

$fname ="/usr/hbin/param.db";
$db = new SQLite3($fname);

if ($_GET['page'] == 'event_profile') {
    $sq = "select * from param_tbl where group1='eventprofile'";
}

$rs = $db->query($sq);
$arr_rs= array();

while ($row = $rs->fetchArray()) {
	// print_r($row);
	$arr_rs[$row['groupPath'].'.'.$row['entryName']] = $row['entryValue'];
}
$db->close();

require_once $_SERVER['DOCUMENT_ROOT']."/inc/json.php";
$json = new Services_JSON();
$json_str = $json->encode($arr_rs);
print($json_str);

?>


