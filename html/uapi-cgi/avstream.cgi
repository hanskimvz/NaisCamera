<img id="img" src="" style="position: absolute; left: 0; top: 0; z-index: 0;"></img>
<script>
    var img = document.getElementById("img");
</script>
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

for ($i=0; $i<300; $i++) {
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
    $frame_cnt = ord($read_data[4]) | ord($read_data[5]) <<8;
    // print($p.": ".$frame_cnt);
    // header("Content-Type: image/jpeg");
    // echo $img;
    flush();
    $img_b64 = base64_encode($img);
    // print '<img id="img" src="data:image/jpg;base64,'.$img_b64.'" style="position: absolute; left: 0; top: 0; z-index: 0;"></img>';
    echo '<script>img.src="data:image/jpg;base64,'.$img_b64.'";</script>';
    usleep(100);
    ob_flush();
    flush();
}
shmop_close($shmid);
?>

