
<?PHP
// error_reporting( E_ALL );
// ini_set( 'display_errors', '1' );

header("Content-Type: text/json");
// require_once $_SERVER['DOCUMENT_ROOT']."/inc/json.php";

foreach($_GET as $key =>$val){
    $_GET[strtolower($key)] = strtolower($val);
}
// print_r($_GET);

function startsWith($haystack, $needle) {
    // search backwards starting from haystack length characters from the end
    return $needle === "" || strrpos($haystack, $needle, -strlen($haystack)) !== false;
}

function endsWith($haystack, $needle) {
    // search forward starting from end minus needle length characters
    return $needle === "" || (($temp = strlen($haystack) - strlen($needle)) >= 0 && strpos($haystack, $needle, $temp) !== false);
}

function dot2array(&$arr, $path, $value, $separator='.') {
    $keys = explode($separator, $path);

    foreach ($keys as $key) {
        $arr = &$arr[$key];
    }
    $arr = $value;
}

function array2dot($arr, $narr = array(), $nkey = '') {
    foreach ($arr as $key => $value) {
        if (is_array($value)) {
            $narr = array_merge($narr, array2dot($value, $narr, $nkey . $key . '.'));
        } else {
            $narr[$nkey . $key] = $value;
        }
    }
    return $narr;
}


$_COOKIE['role'] ='admin';
// print "cookie: "; print_r($_COOKIE); 

if ($_COOKIE['role'] !='admin') {
    print "not permitted \n";
    exit();
}

if($_GET['action'] == 'sys'){
    if ($_GET['gorup'] == 'datetime'){

    }
}

function getArrayFromFile($grp_str, $dot=False){
    $arr = array();
    $arr_grp = array();
    $ex_grp = explode(",", $grp_str);
    for ($i=0; $i<sizeof($ex_grp); $i++) {
        if ($ex_grp[$i]) {
            array_push($arr_grp, explode(".", $ex_grp[$i]));
        }
    }

    for ($i=0; $i<sizeof($arr_grp);$i++) {
        $fname ="/root/data/setting/".$arr_grp[$i][0].".tbl";
        
        if(file_exists(($fname))) {
            $body = file_get_contents($fname);
            $arr[$arr_grp[$i][0]] = json_decode($body, 1);
        }
        else {
            $fname ="/root/data/setting/param.tbl";
            $body = file_get_contents($fname);
            $arr_t = json_decode($body, 1);
            foreach($arr_t as $g =>$a){
                $arr[$g] = $a;
            }
        }
        $arr[$arr_grp[$i][0]]['fname'] = $fname;
        // array_push($arr, array("fname"=>$fname, "key"=>$arr_grp[$i][0], "values"=> json_decode($body, 1)));
    }
    if ($dot) {
        return array2dot($arr);
    }
    return $arr;
}

function writeFile($fname, $arr){
    $json_str =  json_encode($arr, JSON_PRETTY_PRINT);
    $rs = file_put_contents($fname, $json_str);
    return $rs;
}
function getUser($arr_user, $username){
    for($i=0; $i<count($arr_user); $i++){
        if ($username == trim($arr_user[$i]['username'])) {
            return $arr_user[$i];
        }
    }
    return False;
}
$arr_rs = array();

if ($_GET['group']=='user'){
    $arr = getArrayFromFile($_GET['group'],0);
    // print_r($arr);
    $fname = $arr['user']['fname'];
    unset($arr['user']['fname']);

    if($_GET['action'] == 'list') {
        if (isset($_GET['username'])){
            $arr['user'] = getUser($arr['user'], trim($_GET['username']));
        }
        
        if ($_GET['format'] == 'json'){
            print json_encode($arr['user'], JSON_PRETTY_PRINT);
        }
        else {
            foreach(array2dot($arr) as $key =>$val){
                print $key.'='.$val."\r\n";
            }
        }
    }
    else if  ($_GET['action'] == 'update'){
        for($i=0; $i<count($arr['user']); $i++){
            if ($_GET['username'] == trim($arr['user'][$i]['username'])) {
                if (isset($_GET['password']) && trim($_GET['password'])) {
                    $arr['user'][$i]['password'] = md5(trim($_GET['password']));
                }
                if (isset($_GET['level'])) {
                    $arr['user'][$i]['level'] = trim($_GET['level']);
                }
                break;
            }
        }
        if (writeFile($fname, $arr['user'])){
            print "user '".$_GET['username']."' update OK";
        }
    }
    else if ($_GET['action'] == 'add') {
        if (getUser($arr['user'], trim($_GET['username']))) {
            print "user '".$_GET['username']."' already exists";
            exit();
        }
        if (!trim($_GET['username'])) {
            print "username is essential";
            exit();
        }
        array_push($arr['user'], array("username"=>trim($_GET['username']), "password"=>md5(trim($_GET['password'])), "level"=>$_GET['level']));
        if (writeFile($fname, $arr['user'])){
            print "user ".$_GET['username']." add OK";
        }

    }
    else if ($_GET['action'] == 'delete'){
        if (!getUser($arr['user'], trim($_GET['username']))) {
            print "user '".$_GET['username']."' not exists";
            exit();
        }
        for($i=0; $i<count($arr['user']); $i++){
            if ($_GET['username'] == trim($arr['user'][$i]['username'])) {
                unset($arr['user'][$i]);
            }
        }
        if (writeFile($fname, $arr['user'])){
            print "user ".$_GET['username']." delete OK";
        }
        
    }
    else if ($_GET['action'] == 'query'){
        
    }
}
else {
    $arr = getArrayFromFile($_GET['group'], 1);
    // print_r($arr);
    if($_GET['action'] == 'list'){
        $grps = explode(",",$_GET['group']);
        foreach ($grps as $grp){
            foreach($arr as $key =>$val){
                if (startsWith($key, $grp)){
                    $arr_rs[$key] =  $val;
                    // array_push($arr_rs, $key."=".$val);
                }
            }
        }
        // print_r($arr_rs);
        if($_GET['format'] == 'json') {
            $arr = array();
            foreach($arr_rs as $key =>$val){
                dot2array($arr, $key, $val);
             }
            print json_encode($arr, JSON_PRETTY_PRINT);
        }
        else {
            foreach($arr_rs as $key =>$val){
                print $key."=".$val."\r\n";
             }
        }
    }
    else if($_GET['action'] == 'update'){
        foreach($_GET as $get=>$t){
            if (!in_array($get, ['action', 'group', 'format'])){
                $arr[$_GET['group'].".".$get] = $t;
            }
        }
        // print_r($arr);
        $arr_rs = array();
        foreach($arr as $key =>$val){
            dot2array($arr_rs, $key, $val);
         }
        $x = writeFile($fname, $arr_rs['network']);
         if($x) {
            print "update OK";
         }
    }
    
    
//     if($_GET['format'] == 'json') {
//         print json_encode($arr_rs, JSON_PRETTY_PRINT);
//     }
//     else {
//         print (implode("\r\n", $arr_rs));
//     }
}


exit();

$SSTR = '
VERSION.bootloader=1.1.116
VERSION.kernel=1.1.2
VERSION.firmware=1.12.0.27
VERSION.description=Official Release
VERSION.revision=3532e87ac7ebeed8cc9fdb90afffe9762bd9a0a6
VERSION.hwrevision=000C
VERSION.userfs=1.12.0.25A
VERSION.serialno=G90A0031F
VERSION.db=0.3.310
BRAND.brand=SEJIN TECH LTD.
BRAND.authenkey=8BA4D163B633007248531BA8CB6D2F07
BRAND.Product.fullname=SC6102HD-6311
BRAND.Product.shortname=SC6102HD
BRAND.Product.description=NETWORK CAMERA
BRAND.Model.productid=B104
ADREC.backupinterval=60
ADREC.duration=0
ADREC.enable=no
ADREC.maxduration=0
ADREC.recycle=yes
ADREC.resource=video
ADREC.segmentsize=700
ADREC.source=first
ADREC.storage=sd
ADREC.version=1
ADREC.Ftp.account=
ADREC.Ftp.address=
ADREC.Ftp.name=
ADREC.Ftp.port=21
ADREC.Ftp.prefixname=usn
ADREC.Ftp.prefixusername=
ADREC.Ftp.targetpath=
ADREC.Ftp.Infofile.enable=no
AVIREC.enable=no
AVIREC.enableautosense=no
AVIREC.prefixname=REC
AVIREC.recycle=yes
AVIREC.resource=video
AVIREC.segsize=100
AVIREC.segtime=10
AVIREC.segtype=size
AVIREC.source=first
AVIREC.storage=sd
AVIREC.verifyintegrity=no
BITXT.nbrofchannel=1
BITXT.Ch0.nbrofstream=1
BITXT.Ch0.St0.enable=yes
BITXT.Ch0.St0.Date.enable=yes
BITXT.Ch0.St0.Date.position=6%:12%
BITXT.Ch0.St0.Name.enable=no
BITXT.Ch0.St0.Name.position=6%:20%
BITXT.Ch0.St0.Name.text=SC6102HD
BITXT.Ch0.St0.Time.enable=yes
BITXT.Ch0.St0.Time.millisec=no
BITXT.Ch0.St0.Time.position=6%:16%
DDNS.domainname=
DDNS.enable=no
DDNS.servertype=DynDNS
DDNS.updatetime=600
DDNS.user=
DIDO.Di.enable=yes
DIDO.Di.nbrofchannel=0
DIDO.Di.type=relay
DIDO.Di.Ch0.enable=yes
DIDO.Di.Ch0.name=DI1_NAME
DIDO.Di.Ch0.trig=ready
DIDO.Di.Ch0.type=relay
DIDO.Do.nbrofchannel=0
DIDO.Do.Ch0.enable=yes
DIDO.Do.Ch0.name=DO1_NAME
DIDO.Do.Ch0.opermanu=yes
DIDO.Do.Ch0.trig=ready
DIDO.Map.Di.nbrofchannel=0
DIDO.Map.Di.Ch0.detectiontype=edge
DIDO.Map.Di.Ch0.duration=5
DIDO.Map.Di.Ch0.elapse=5
DIDO.Map.Di.Ch0.type=no
DIDO.Map.Do.Ch0.detectiontype=edge
DIDO.Map.Do.Ch0.duration=5
DIDO.Map.Do.Ch0.elapse=5
FD.enable=yes
FD.nbrofchannel=1
FD.Ch0.cliprateh=150
FD.Ch0.clipratew=130
FD.Ch0.confidence=128
FD.Ch0.enable=no
FD.Ch0.ignorecnt=3
FD.Ch0.list=0,1,2,3
FD.Ch0.maxcnt=4
FD.Ch0.maxsizerate=100
FD.Ch0.minsizerate=0
FD.Ch0.nbrofzone=4
FD.Ch0.sizeorder=descending
FD.Ch0.trkfactorh=100
FD.Ch0.trkfactorw=100
FD.Ch0.trkholdon=3000
FD.Ch0.Da0.description=
FD.Ch0.Da0.enable=no
FD.Ch0.Da0.name=da
FD.Ch0.Da0.position=0,0,9999,0
FD.Ch0.Da0.trkduration=120
FD.Ch0.Ez0.enable=no
FD.Ch0.Ez0.name=ez0
FD.Ch0.Ez0.position=0,0,0,0
FD.Ch0.Ez1.enable=no
FD.Ch0.Ez1.name=ez1
FD.Ch0.Ez1.position=0,0,0,0
FD.Ch0.Ez2.enable=no
FD.Ch0.Ez2.name=ez2
FD.Ch0.Ez2.position=0,0,0,0
FD.Ch0.Ez3.enable=no
FD.Ch0.Ez3.name=ez3
FD.Ch0.Ez3.position=0,0,0,0
FD.Ch0.Osd.enable=no
FD.Ch0.Osd.snapshot=no
FD.Ch0.Osd.st0=no
FD.Ch0.Osd.st1=no
FD.Ch0.Osd.zone=no
FD.Ch0.Z0.description=
FD.Ch0.Z0.enable=no
FD.Ch0.Z0.name=zone
FD.Ch0.Z0.number=0
FD.Ch0.Z0.position=0,0,9999,9999
FD.Ch0.Z1.description=
FD.Ch0.Z1.enable=no
FD.Ch0.Z1.name=zone
FD.Ch0.Z1.number=1
FD.Ch0.Z1.position=2500,0,4999,9999
FD.Ch0.Z2.description=
FD.Ch0.Z2.enable=no
FD.Ch0.Z2.name=zone
FD.Ch0.Z2.number=2
FD.Ch0.Z2.position=5000,0,7499,9999
FD.Ch0.Z3.description=
FD.Ch0.Z3.enable=no
FD.Ch0.Z3.name=zone
FD.Ch0.Z3.number=3
FD.Ch0.Z3.position=7500,0,10000,9999
FWUPGRADE.Server.enable=no
FWUPGRADE.Server.url=
GENETEC.enable=yes
GENETEC.version=1.0.0
HEARTBEAT.enable=yes
HEARTBEAT.interval=60
HEARTBEAT.Multicast.enable=yes
HEARTBEAT.Tcp.enable=yes
HEARTBEAT.Tcppush.enable=no
HOST.address=
HOST.enable=no
HOST.port=5000
HOST.updateinterval=60
IOT.address=iot.ucount.it
IOT.enable=no
IOT.port=1883
IOT.status=init
IPFILTER.adminip=
IPFILTER.alwaysallowicmp=yes
IPFILTER.enable=no
IPFILTER.type=deny
IPFILTER.Allowlist.filter=
IPFILTER.Denylist.filter=
MD.enable=yes
MD.nbrofchannel=1
MD.zonemode=position
MD.Ch0.enable=yes
MD.Ch0.list=0,1,2,3,4,5,6,7
MD.Ch0.nbrofzone=8
MD.Ch0.Z0.bitmask=
MD.Ch0.Z0.description=
MD.Ch0.Z0.duration=0
MD.Ch0.Z0.enable=no
MD.Ch0.Z0.name=zone
MD.Ch0.Z0.number=0
MD.Ch0.Z0.objectsize=128
MD.Ch0.Z0.position=0,0,2499,4999
MD.Ch0.Z0.sensitivity=128
MD.Ch0.Z1.bitmask=
MD.Ch0.Z1.description=
MD.Ch0.Z1.duration=0
MD.Ch0.Z1.enable=no
MD.Ch0.Z1.name=zone
MD.Ch0.Z1.number=1
MD.Ch0.Z1.objectsize=128
MD.Ch0.Z1.position=2500,0,4999,4999
MD.Ch0.Z1.sensitivity=128
MD.Ch0.Z2.bitmask=
MD.Ch0.Z2.description=
MD.Ch0.Z2.duration=0
MD.Ch0.Z2.enable=no
MD.Ch0.Z2.name=zone
MD.Ch0.Z2.number=2
MD.Ch0.Z2.objectsize=128
MD.Ch0.Z2.position=5000,0,7499,4999
MD.Ch0.Z2.sensitivity=128
MD.Ch0.Z3.bitmask=
MD.Ch0.Z3.description=
MD.Ch0.Z3.duration=0
MD.Ch0.Z3.enable=no
MD.Ch0.Z3.name=zone
MD.Ch0.Z3.number=3
MD.Ch0.Z3.objectsize=128
MD.Ch0.Z3.position=7500,0,10000,4999
MD.Ch0.Z3.sensitivity=128
MD.Ch0.Z4.bitmask=
MD.Ch0.Z4.description=
MD.Ch0.Z4.duration=0
MD.Ch0.Z4.enable=no
MD.Ch0.Z4.name=zone
MD.Ch0.Z4.number=4
MD.Ch0.Z4.objectsize=128
MD.Ch0.Z4.position=0,5000,2499,10000
MD.Ch0.Z4.sensitivity=128
MD.Ch0.Z5.bitmask=
MD.Ch0.Z5.description=
MD.Ch0.Z5.duration=0
MD.Ch0.Z5.enable=no
MD.Ch0.Z5.name=zone
MD.Ch0.Z5.number=5
MD.Ch0.Z5.objectsize=128
MD.Ch0.Z5.position=2500,5000,4999,10000
MD.Ch0.Z5.sensitivity=128
MD.Ch0.Z6.bitmask=
MD.Ch0.Z6.description=
MD.Ch0.Z6.duration=0
MD.Ch0.Z6.enable=no
MD.Ch0.Z6.name=zone
MD.Ch0.Z6.number=6
MD.Ch0.Z6.objectsize=128
MD.Ch0.Z6.position=5000,5000,7499,10000
MD.Ch0.Z6.sensitivity=128
MD.Ch0.Z7.bitmask=
MD.Ch0.Z7.description=
MD.Ch0.Z7.duration=0
MD.Ch0.Z7.enable=no
MD.Ch0.Z7.name=zone
MD.Ch0.Z7.number=7
MD.Ch0.Z7.objectsize=128
MD.Ch0.Z7.position=7500,5000,10000,10000
MD.Ch0.Z7.sensitivity=128
MD.Default.Zone.bitmask=
MD.Default.Zone.description=
MD.Default.Zone.duration=0
MD.Default.Zone.enable=yes
MD.Default.Zone.name=zone
MD.Default.Zone.number=0
MD.Default.Zone.objectsize=128
MD.Default.Zone.position=500,900,3000,4000
MD.Default.Zone.sensitivity=128
MD.Metadata.enable=yes
MD.Metadata.blob.enable=yes
NETLOSS.Detect.Ethlink.enable=yes
NETLOSS.Detect.Ping.address=
NETLOSS.Detect.Ping.enable=no
NETLOSS.Detect.Ping.interval=10
PIR.interval=5
PRIVACYZONE.enable=yes
PRIVACYZONE.nbrofchannel=1
PRIVACYZONE.Ch0.enable=yes
PRIVACYZONE.Ch0.list=0,1,2,3,4,5,6,7
PRIVACYZONE.Ch0.nbrofzone=8
PRIVACYZONE.Ch0.type=static
PRIVACYZONE.Ch0.Z0.dynamic=
PRIVACYZONE.Ch0.Z0.enable=no
PRIVACYZONE.Ch0.Z0.name=zone
PRIVACYZONE.Ch0.Z0.position=0,102,591,1899
PRIVACYZONE.Ch0.Z1.dynamic=
PRIVACYZONE.Ch0.Z1.enable=no
PRIVACYZONE.Ch0.Z1.name=zone
PRIVACYZONE.Ch0.Z1.position=5000,2500,7498,4999
PRIVACYZONE.Ch0.Z2.dynamic=
PRIVACYZONE.Ch0.Z2.enable=no
PRIVACYZONE.Ch0.Z2.name=zone
PRIVACYZONE.Ch0.Z2.position=2500,5000,4999,7499
PRIVACYZONE.Ch0.Z3.dynamic=
PRIVACYZONE.Ch0.Z3.enable=no
PRIVACYZONE.Ch0.Z3.name=zone
PRIVACYZONE.Ch0.Z3.position=5000,5000,7498,7499
PRIVACYZONE.Ch0.Z4.dynamic=
PRIVACYZONE.Ch0.Z4.enable=no
PRIVACYZONE.Ch0.Z4.name=zone
PRIVACYZONE.Ch0.Z4.position=0,0,0,0
PRIVACYZONE.Ch0.Z5.dynamic=
PRIVACYZONE.Ch0.Z5.enable=no
PRIVACYZONE.Ch0.Z5.name=zone
PRIVACYZONE.Ch0.Z5.position=0,0,0,0
PRIVACYZONE.Ch0.Z6.dynamic=
PRIVACYZONE.Ch0.Z6.enable=no
PRIVACYZONE.Ch0.Z6.name=zone
PRIVACYZONE.Ch0.Z6.position=0,0,0,0
PRIVACYZONE.Ch0.Z7.dynamic=
PRIVACYZONE.Ch0.Z7.enable=no
PRIVACYZONE.Ch0.Z7.name=zone
PRIVACYZONE.Ch0.Z7.position=0,0,0,0
';



// print $SSTR;
$arr = array();
$lines = explode("\n",$SSTR);
for($i=0; $i<sizeof($lines); $i++){
    if (!trim($lines[$i])) {
        continue;
    }
    $exr = explode("=", trim($lines[$i]));
    // $keys = explode(".", $exr[0]);
    dot2array($arr, strtolower($exr[0]), $exr[1], $separator='.');
    // $arr = $exr[1];
}

// print_r($arr);

print (json_encode($arr, JSON_PRETTY_PRINT));
exit();





if ($_GET['action'] == 'list' && $_GET['table']=='param_tbl'){
    if (!isset($_GET['format'])){
        $_GET['format'] = 'plain';
    }
    if (isset($_GET['group'])){
// select groupPath, entryName, entryValue from param_tbl where group1='network' and group2='dns' and (group3='preferred' or entryName='preferred') order by groupPath asc
        $eGroups = array();
        $arr_sq = array();
        $arr_rs = array();

        foreach(explode(",", $_GET['group']) as $grps){
            $grps = trim($grps);
            $arr = array();
            foreach(explode(".", $grps) as $exgrp){
                array_push($arr, strtolower(trim($exgrp)));
            }
            array_push($eGroups, $arr);
        }    

        foreach($eGroups as $grps) {
            $arr = array();
            for($i=0; $i<sizeof($grps); $i++){
                if (sizeof($grps) > 1 && $i==(sizeof($grps)-1)){
                    array_push($arr, "(group".($i+1)."='".$grps[$i]."' or entryName='".$grps[$i]."')");
                }
                else{
                    array_push($arr, "group".($i+1)."='".$grps[$i]."'");
                }
            }
            if ($arr){
                $sq = "where ".join(" and ", $arr);
                array_push($arr_sq, $sq);
            }
        }
    }
    else {
        $arr_sq = array('');
    }
    // print_r($arr_sq);
    $db = new SQLite3($fname); 
    foreach($arr_sq as $wsq) {
        $sq = "select groupPath, entryName, entryValue from ".$_GET['table']." ".$wsq." order by groupPath asc";
        // print $sq."\n";
        $rs = $db->query($sq);
        while ($row = $rs->fetchArray()) {
            $arr_rs[$row['groupPath'].".".$row['entryName']] = $row['entryValue'];
        }
    }
    $db->close();
    // print_r($arr_rs);
    if($_GET['format']=='json'){
        header("Content-Type: text/json");
        require_once $_SERVER['DOCUMENT_ROOT']."/inc/json.php";
        $json = new Services_JSON();
        $json_str = $json->encode($arr_rs);
        print($json_str);
    }
    else if($_GET['format']=="plain"){
        header("Content-Type: text/plain");
        foreach($arr_rs as $A => $B) {
            print $A."=".$B."\n";
        }
    }
   
}
else if ($_GET['action'] == 'list' && $_GET['table']=='user_tbl'){
    $arr_rs = array();
    $sq = "select id, passwd, level, explain, login_count, lastlogin, regdate from ".$_GET['table']." ";
    $db = new SQLite3($fname); 
    $rs = $db->query($sq);
    while ($row = $rs->fetchArray()) {
        array_push($arr_rs, array("id"=>$row['id'], "level"=>$row['level'], 'explain'=>$row['explain'], 'login_count'=>$row['login_count'], "last_login"=>$row['lastlogin']));
    }
    $db->close();
    header("Content-Type: text/json");
    require_once $_SERVER['DOCUMENT_ROOT']."/inc/json.php";
    $json = new Services_JSON();
    $json_str = $json->encode($arr_rs);
    print($json_str);    
}

else if($_GET['action']=='update'){
    $arr_grp = array();
    $arr_sq = array();
    header("Content-Type: text/plain");
    if(isset($_GET['group'])) {
        $_GET['group'] .= ".";
    }
    else {
        $_GET['group'] .= "";
    }

    foreach(explode("&",$_SERVER['QUERY_STRING']) as $qstr){
        list($key, $val) = explode("=", $qstr);
        if ($key == 'action' || $key == 'format' || $key=='group' || $key=='table'){
            continue;
        }
        array_push($arr_grp, $_GET['group'].$key."=".$val);
    }

    $db = new SQLite3($fname); 
    foreach($arr_grp as $gstr){
        // print $gstr."\n";
        list($grp, $entryValue) = explode("=",$gstr);
        $grps = explode(".", $grp);
        $entryName = array_pop($grps);
        $groupPath = join(".",$grps);

        $sq = "select datatype, option, readonly from ".$_GET['table']." where groupPath='".$groupPath."' and entryName='".$entryName."'";
        $rs = $db->query($sq);
        $row = $rs->fetchArray();
        if (!$row) {
            print "Key error, ".$groupPath.".".$entryName."\n";
            continue;
        }
        if ($row['readonly'] == 1) {
            print "this parameter is read only\n";
            continue;
        }
        if($row['datatype']=='int' || $row['datatype']=='port') {
            if (!is_numeric($entryValue)) {
                print "Values Error, Integer only \n";
                continue;
            }
        }
        if ($row['datatype']=='yesno' || $row['datatype']=='select') {
            if (!strpos(" ".$row['option'], $entryValue)){
                print "Values Error: value should be in '".$row['option']."' \n";
                continue;
            }
        
        }
        array_push($arr_sq, array("entryValue"=>$entryValue, "groupPath"=>$groupPath, "entryName"=>$entryName));
        // array_push($arr_sq, "update ".$_GET['table']." set entryValue='".$entryValue."' where groupPath='".strtolower($groupPath)."' and entryName='".$entryName."'");
        
    }
    // select * from param_tbl where groupPath='network.eth0' and entryName='subnet'
    // select * from param_tbl where groupPath='NETWORK.Eth0' and entryName='subnet'
    // select * from param_tbl where groupPath='network.eth0' and entryName='ipaddr'
       
    foreach($arr_sq as $arr) {
        $sq = "update ".$_GET['table']." set entryValue='".$arr['entryValue']."' where groupPath='".strtolower($arr['groupPath'])."' and entryName='".$arr['entryName']."'";
        // print $sq."\n";
        $rs = $db->query($sq);
        if($rs){
            print "update OK, ".$arr['groupPath'].".".$arr['entryName']."=".$arr['entryValue']."\n";
        }
        else {
            print "update FAIL\n";
        }
    }
    $db->close();
   
}

else if($_GET['action'] == 'add'){
    header("Content-Type: text/plain");
    $groupAvailable= ['EVENT', 'EVENTPROFILE','MD','PTZ',"SCHEDULE"];
    if (!isset($_GET['group'])) {
        print "Error, add action needs group";
        exit();
    }
    $ex_grp = explode(".",$_GET['group']);
    $grp_header = strtoupper($ex_grp[0]);
    if (!in_array($grp_header, $groupAvailable)) {
        print "Error, group should be one of [".join(", ", $groupAvailable )."]";
        exit();
    }
    $arr =array();
    for ($i=0; $i<sizeof($ex_grp); $i++){
        array_push($arr, "group".($i+1)."='".$ex_grp[$i]."'");
    }
    $sq = join(" and ",$arr);
    $sq = "select * from ".$_GET['table']." where ".$sq;

    print $sq;
    
}
else if($_GET['action'] == 'delete'){
    header("Content-Type: text/plain");

}

else if($_GET['action'] == 'modify'){
    header("Content-Type: text/plain");
}


else if($_GET['action'] == 'query'){
    header("Content-Type: text/plain");
    if (isset($_GET['group'])){
        $eGroups = array();
        $arr_sq = array();
        $arr_rs = array();

        foreach(explode(",", $_GET['group']) as $grps){
            $grps = trim($grps);
            $arr = array();
            foreach(explode(".", $grps) as $exgrp){
                array_push($arr, strtolower(trim($exgrp)));
            }
            array_push($eGroups, $arr);
        }    

        foreach($eGroups as $grps) {
            $arr = array();
            for($i=0; $i<sizeof($grps); $i++){
                if (sizeof($grps) > 1 && $i==(sizeof($grps)-1)){
                    array_push($arr, "(group".($i+1)."='".$grps[$i]."' or entryName='".$grps[$i]."')");
                }
                else{
                    array_push($arr, "group".($i+1)."='".$grps[$i]."'");
                }
            }
            if ($arr){
                $sq = "where ".join(" and ", $arr);
                array_push($arr_sq, $sq);
            }
        }
    }
    else {
        $arr_sq = array('');
    }
    // print_r($arr_sq);
    $db = new SQLite3($fname); 
    foreach($arr_sq as $wsq) {
        $sq = "select groupPath, entryName, datatype, option, readonly from ".$_GET['table']." ".$wsq." order by groupPath asc";
        // print $sq."\n";
        $rs = $db->query($sq);
        while ($row = $rs->fetchArray()) {
            if (!$row['option']) {
                $row['option'] = 0;
            }
            $arr_rs[$row['groupPath'].".".$row['entryName']] = $row['datatype']."|".$row['option'];
            if($row['readonly']==1) {
                $arr_rs[$row['groupPath'].".".$row['entryName']] .= "|readonly";
            }
        }
    }
    $db->close();
    // print_r($arr_rs);

    header("Content-Type: text/plain");
    foreach($arr_rs as $A => $B) {
        print $A."=".$B."\n";
    }
}
exit();

if ($action == 'add'){
    for ($i=0; $i<sizeof($eGroups); $i++) {
        if($eGroups[$i][0] == 'grouppath'){
            $exp_grp = explode(".",$eValues[$i]);
            $entryName = array_pop($exp_grp);
            $groupPath ="";
            for($j=0; $j<sizeof($exp_grp); $j++){
                if ($groupPath) {
                    $groupPath .= ".";
                }
                $groupPath .= $exp_grp[$j];
                $grp[$j] = $exp_grp[$j];
            }
        }
        else {
            ${$eGroups[$i][0]} = $eValues[$i];
        }
    }
    if($datatype=='int' || $datatype=='port') {
        if (!is_numeric($value)) {
            print "Values Error, Integer only \n";
            exit();
        }
    }
    else if ($datatype=='yesno' || $datatype=='select') {
        if (!strpos(" ".$option, $value)){
            print "Values Error: value should be in '".$option."' \n";
            exit();
        }
    }

    $sq = "insert into ".$_GET['table']."
        (groupPath, entryName, entryValue, group1, group2, group3, group4, group5, group6, made, regdate, description, datatype, option, create_permission, delete_permission, update_permission, read_permission,  readonly, writeonly) 
        values('".$groupPath."','".$entryName."', '".$value."', '".$grp[0]."', '".$grp[1]."', '".$grp[2]."', '".$grp[3]."', '".$grp[4]."', '".$grp[5]."', '".$made."', '".time()."', '".$description."', '".$datatype."', '".$option."', '".$create_permission."', '".$delete_permission."', '".$update_permission."', '".$read_permission."', '".$readonly."', '".$writeonly."') ";

    // print $sq;
    $rs = $db->query($sq);
    if($rs){
        print "add OK\n";
    }
    else {
        print "add FAIL\n";
    }    
}


else if ($action == 'modify'){
}
else if ($action == 'delete'){
}
else if ($action == 'query'){
    for ($i=0; $i<sizeof($eGroups); $i++){
        $upd_sq = "";
        $sel_sq = "";
        $sq = "";
        for($j=0; $j<6; $j++){
            if (!isset($eGroups[$i][$j]) || !$eGroups[$i][$j]) {
                continue;
            }
            if ($sq) {
                $sq .= " and ";
            }
            $sq .= "group".($j+1)."='".$eGroups[$i][$j]."'";
        }
        if ($sq) {
            $sq = "where ".$sq;
        }
        $sel_sq = "select groupPath, entryName, entryValue from ".$_GET['table']." ".$sq." order by groupPath asc";
        $sel_sq = "select  * from ".$_GET['table']." ".$sq." order by groupPath asc";
        array_push($arr_sq, $sel_sq);
    }
    $arr_rs = array();
    for ($i=0; $i<sizeof($arr_sq); $i++){
        $rs = $db->query($arr_sq[$i]);
        while ($row = $rs->fetchArray()) {
            // array_push($arr_rs, ($row['groupPath'].".".$row['entryName']."=".$row['entryValue']));
            array_push($arr_rs, ($row['groupPath'].".".$row['entryName']."=".join("|",$row)));
        }
    }
    $db->close();
    header("Content-Type: text/plain");
    foreach($arr_rs as $A => $B) {
        print $B;
        print "\n";
    }   
}


$db->close();

exit();



?>
