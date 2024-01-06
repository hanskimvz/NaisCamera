<?PHP
header("Content-Type: text/json");
include $_SERVER['DOCUMENT_ROOT']."/inc/functions.php";

foreach($_GET as $key =>$val){
    $key = strtolower($key);
    if (in_array($key, ['action', 'group', 'format'])){
        $val= strtolower($val);
    }

    $_GET[$key] = $val;
}

$_COOKIE['role'] ='admin';
// print "cookie: "; print_r($_COOKIE); 

if ($_COOKIE['role'] !='admin') {
    print "not permitted \n";
    exit();
}

// if($_GET['action'] == 'sys'){
//     if ($_GET['gorup'] == 'datetime'){

//     }
// }

if($_GET['action'] == 'list'){
    $arr = getArrayFromFile($_GET['group'], true);
    // print_r($arr);
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
    // print_r($_GET);
    foreach($_GET as $get=>$t){
        $get = str_replace("_", ".", $get);
        if (!in_array($get, ['action', 'group', 'format'])){
            if($_GET['group']) {
                $arr[$_GET['group'].".".$get] = $t;
            }
            else {
                $arr[$get] = $t;
            }
        }
    }
    // print_r($arr);
    $arr_do = array();
    foreach($arr as $key =>$val){
        $grp = explode(".",$key)[0];
        $arr_rs = getArrayFromFile($grp, true);
        if ($arr_rs[$key] == $val){
            continue;
        }
        // print $key;
        $arr_rs[$key] = $val;
        $arr_t = array();
        foreach($arr_rs as $k =>$v) {
            dot2array($arr_t, $k, $v, $separator='.');
        }
        // print_r($arr_t);
        $body = json_encode($arr_t[$grp], JSON_PRETTY_PRINT);
        // print ($body);
        file_put_contents($baseDir.$grp.".tbl", $body);
        if (!in_array($key, $arr_do)) {
            array_push($arr_do, $key);
        }
    }
    print_r($arr_do);
    doExtra($arr_do);
    // $arr_rs = array();
    // foreach($arr as $key =>$val){
    //     dot2array($arr_rs, $key, $val, $separator='_');
    // }
    

}
else if($_GET['action'] == 'syscmd'){
    print ($_GET['script']);
    sys_shell_script($_GET['script']);
}



?>
