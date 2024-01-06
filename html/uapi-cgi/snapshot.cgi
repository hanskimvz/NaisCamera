<meta http-equiv='cache-control' content='no-cache'>
<meta http-equiv='expires' content='0'>
<meta http-equiv='pragma' content='no-cache'>
<?php 
$systemid = 0x000f6085; // System ID for the shared memory segment 
$shmid = shmop_open($systemid, "a", 0, 0); 
$offset = 524288;

// read_data[4:5] frame_cnt
// read_data[6:7] timestamp_microsecond
// read_data[8:11] timestamp_second
// read_data[12:15] sizeof snapshot
// read_data[16~] snapshot data

// $read_data = shmop_read($shmid, 0, 200); for ($i=0; $i<200; $i++) {  print (ord($read_data[$i]).",");} shmop_close($shmid); exit();
$read_data = shmop_read($shmid, 0, 1);
$p = (ord($read_data[0]) +3) %4;

$p_x = $offset * $p;

$read_data = shmop_read($shmid, $p_x, 16);
$sz = ord($read_data[12]) | ord($read_data[13]) <<8 | ord($read_data[14]) <<16 | ord($read_data[15])<<24;
if (!$sz) {
    $sz = 300000;
}
// print ($sz);
// // string shmop_read ( int shmid, int start, int count)

$img = shmop_read($shmid, $p_x + 16, $sz+4);
$ts = ord($read_data[8]) | ord($read_data[9]) <<8 | ord($read_data[10]) <<16 | ord($read_data[11])<<24;
$ts_m = ord($read_data[6]) | ord($read_data[7]) <<8; 
ob_get_clean();
flush();
// header("Content-Type: image/jpeg");
echo $img.$ts.".".$ts_m;
flush();
ob_clean();
// $img_b64 = base64_encode($img);
// print '<img id="img" src="data:image/jpg;base64,'.$img_b64.'" width="640" height="320"></img>';

shmop_close($shmid);
?>

