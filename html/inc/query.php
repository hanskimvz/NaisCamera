<?php
# do not use, json is used.
$fname ="/mnt/db/param.db";
$db = new SQLite3($fname);


if ($_GET['page']=='users') {
    $sq = "select * from user_tbl";
    $level = array("Administrator", "Operator","Viewer");

    // $tag_userlist = '';
    // while ($row = $rs->fetchArray()) {
    //     // print_r($row);
    //     $user_info =  $row['id'].FillText($level[$row['level']], 30, "right");
    //     $tag_userlist .= '<option value="'.$row['prino'].'">'.$user_info.'</option>';
    // }
}

else if ($_GET['page'] == 'netloss'){
    $sq = "select * from param_tbl where group1='netloss'";
}
else if ($_GET['page'] == 'heartbeat'){
    $sq = "select * from param_tbl where group1='heartbeat'";
}
else if ($_GET['page'] == 'event_profile') {
    $sq = "select * from param_tbl where group1='eventprofile'";
}


else if ($_GET['page'] == 'tcpip') {
    $sq = "select * from param_tbl where group1='network' and (group2='eth0' or group2='dns')";
}
else if ($_GET['page'] == 'http') {
    $sq = "select * from param_tbl where group1='network' and (group2='http' or group2='https')";
}
else if ($_GET['page'] == 'upnp') {
    $sq = "select * from param_tbl where group1='network' and group2='upnp'";
}

else if ($_GET['page'] == 'rtprtsp') {
    $sq = "select * from param_tbl where group1='network' and (group2='rtp' or group2='rtsp' or group2='srtp')";
}

else if ($_GET['page'] == 'rtmp') {
    $sq = "select * from param_tbl where group1='network' and (group2='rtmp' or group2='eth0')";
}
else if ($_GET['page'] == 'mdns') {
    $sq = "select * from param_tbl where group1='network' and group2='mdns'";
}
else if ($_GET['page'] == 'wsdiscovery') {
    $sq = "select * from param_tbl where group1='network' and group2='wsdiscovery'";
}
else if ($_GET['page'] == 'ddns') {
    $sq = "select * from param_tbl where group1='ddns'";
}

else if ($_GET['page'] == 'ntp') {
    $sq = "select * from param_tbl where group1='system' and group2='datetime' and group3='ntp'";
}

$rs = $db->query($sq);

$arr_rs= array();
while ($row = $rs->fetchArray()) {
	// print_r($row);
	$arr_rs[$row['groupPath'].'.'.$row['entryName']] = $row['entryValue'];
}
$db->close();
$arr_rs['sq'] = $sq;

require_once $_SERVER['DOCUMENT_ROOT']."/inc/json.php";
$json = new Services_JSON();
$json_str = $json->encode($arr_rs);
print($json_str);

?>

