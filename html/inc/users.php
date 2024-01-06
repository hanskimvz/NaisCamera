<?PHP
header("Content-Type: text/json");
// require_once $_SERVER['DOCUMENT_ROOT']."/inc/json.php";

require_once $_SERVER['DOCUMENT_ROOT']."/inc/functions.php";

foreach($_GET as $key =>$val){
    $_GET[strtolower($key)] = strtolower($val);
}
// print_r($_GET);
function getUser($arr_user, $username){
    for($i=0; $i<count($arr_user); $i++){
        if ($username == trim($arr_user[$i]['username'])) {
            return $arr_user[$i];
        }
    }
    return False;
}
$body = file_get_contents($baseDir."user.tbl");
$arr = json_decode($body, true);
// print_r($arr);

if($_GET['action'] == 'list') {
    if (isset($_GET['username'])){
        $arr = getUser($arr['member'], trim($_GET['username']));
    }
    
    if ($_GET['format'] == 'json'){
        print json_encode($arr, JSON_PRETTY_PRINT);
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
    if (writeFile($fname, $arr['user'])) {
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

?>

