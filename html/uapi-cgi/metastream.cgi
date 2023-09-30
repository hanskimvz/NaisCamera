<?php 
Header("Content-type: text/json");
$arr_cat = array(
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck",
    "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
    "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
    "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
    "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop",
    "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
);

$systemid = 0x000f1206; // System ID for the shared memory segment 
$shmid = shmop_open($systemid, "a", 0, 0); 
$sz = shmop_size($shmid);

// print ("shm id:".$shmid.", size:". shmop_size($shmid));
// shmop_write($shmid, "Hello World!", 0);

$old_frame_cnt =0;
while(1) {
    $read_data = shmop_read($shmid, 0, $sz);

    $wp =0;
    $frame_cnt = ord($read_data[$wp++]) | ord($read_data[$wp++]) << 8;
    if ($frame_cnt == $old_frame_cnt) {
        flush();
        usleep(10);
        continue;
    }
    flush();
    $old_frame_cnt = $frame_cnt;
    $ts_m =  ord($read_data[$wp++]) | ord($read_data[$wp++]) <<8;
    $ts   =  ord($read_data[$wp++]) | ord($read_data[$wp++])<<8  | ord($read_data[$wp++])<<16 | ord($read_data[$wp++])<<24;

    $arr_rs = array();
    for ($i =$wp; $i<100; ){
        if (ord($read_data[$i]) == 255) {
            break;
        }
        $cat_no = ord($read_data[$i++]);
        $score  = ord($read_data[$i++]) | ord($read_data[$i++]) << 8;
        $pos_x0 = ord($read_data[$i++]) | ord($read_data[$i++]) << 8;
        $pos_x1 = ord($read_data[$i++]) | ord($read_data[$i++]) << 8;
        $pos_y0 = ord($read_data[$i++]) | ord($read_data[$i++]) << 8;
        $pos_y1 = ord($read_data[$i++]) | ord($read_data[$i++]) << 8;

        $pos_xc = $pos_x0 + ($pos_x1 - $pos_x0)/2;
        $pos_yc = $pos_y0 + ($pos_y1 - $pos_y0)/2;

        array_push($arr_rs, 
            array(
                "cat_no"  => $cat_no,
                "cat_item"=> $arr_cat[$cat_no],
                "score"   => $score,
                "pos_lt"  => [$pos_x0, $pos_y0],
                "pos_rb"  => [$pos_x1, $pos_y1],
                "pos_cen" => [(int)$pos_xc, (int)$pos_yc]

            )
        
        );
    }
    // shmop_delete($shmid);
    $arr_rs_t = array(
        "frame_cnt" => $frame_cnt,
        "timestamp" => $ts + $ts_m/1000,
        "datetime" => date("Y-m-d H:i:s", $ts + 3600*8),
        "data" => $arr_rs
    );

    $json_str = json_encode($arr_rs_t, JSON_NUMERIC_CHECK|JSON_PRETTY_PRINT);
    print $json_str;

}
shmop_close($shmid);
?>

