<?PHP

header("Content-Type: text/json");
include $_SERVER['DOCUMENT_ROOT']."/inc/functions.php";
$arr_rs = array();


# Temperature
function get_server_temperature() {
    $fname = "/sys/class/thermal/thermal_zone0/mode";
    if (strcmp(file_get_contents($fname), "enabled")) {
        $fp = fopen($fname, "w");
        fwrite($fp, "enabled");
        fclose($fp);
    }

    $fname = "/sys/class/thermal/thermal_zone0/temp";
    $temp = file_get_contents($fname);
    return round($temp/1000,2);
}

# Resource
function get_server_cpu_usage() {
    $load = sys_getloadavg();
    return round($load[0]*100,2);
}

function get_server_memory_usage() {

    $free         = shell_exec('free');
    $free         = (string) trim($free);
    $free_arr     = explode("\n", $free);
    $mem          = explode(" ", $free_arr[1]);
    $mem          = array_filter($mem);
    $mem          = array_merge($mem);
    $memory_usage = $mem[2] / $mem[1] * 100;

    $report['total']         = (int) $mem[1];
    $report['used']          = (int) $mem[2];
    $report['usage_percent'] = round($memory_usage,2);

    return $report;
}

# uptime
function get_server_uptime(){
    $fname = "/proc/uptime";
    $str = file_get_contents($fname);
    $ts = intval($str);
    $report['ts'] = $ts;
    $report['str'] = floor($ts/(3600*24))." day, ".date("H:i:s", $ts) ;
    return $report;
}

# rtsp connection
function get_connection(){
    $report = array();
    $netstat = shell_exec('netstat -atn | grep ESTABLISHED');
    $netstat = (string) trim($netstat);
    $lines = explode("\n", $netstat);
    foreach($lines as $line){
        $tabs = explode(" ", $line);
        $tabs = array_merge(array_filter($tabs));
        for($i=0; $i<count($tabs); $i++){
            preg_match('/(\d+.\d+.\d+.\d+):(\d+)/', $tabs[$i], $matches, PREG_OFFSET_CAPTURE);
            if ($matches) {
                preg_match('/(\d+.\d+.\d+.\d+):(\d+)/', $tabs[$i+1], $matches2, PREG_OFFSET_CAPTURE);
                array_push($report, array("address"=>$matches2[1][0],"port"=>$matches[2][0] ));
                break;
            }
        }
    }
    
    return $report;
}

function get_rtsp_connection(){
    $rtsp_ports = [554, 556];
    $result = array();
    $arr =  get_connection();
    foreach($arr as $a){
        if (in_array($a['port'], $rtsp_ports)){
            $result[] = $a;
        }
    }
    return $result;
}

if ($_GET['item'] == 'datetime'){
    $arr = getArrayFromFile('system', true);
    $offset = $arr['system.datetime.tz.utcoffset'];
    $arr_rs['datetime'] = date("Y/m/d H:i:s", time()+ intval($offset));
}
else {
    $arr_rs['datetime'] = date("Y/m/d H:i:s");
    $arr_rs['temperature'] =  get_server_temperature();
    $arr_rs['cpu'] = get_server_cpu_usage();
    $arr_rs['memory'] = get_server_memory_usage();
    $arr_rs['uptime'] = get_server_uptime();
    $arr_rs['connection'] = get_rtsp_connection();
}
$json_str = json_encode($arr_rs, JSON_PRETTY_PRINT);
print $json_str;

?>
