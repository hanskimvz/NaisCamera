<!DOCTYPE html>
<!-- origin: https://startbootstrap.com/previews/sb-admin-2 -->
<html lang="en">
<?php
// $_COOKIE['selected_language'] = "korean";
// print_r($_COOKIE);
include ("../inc/common.php");
echo $header;

require_once $_SERVER['DOCUMENT_ROOT']."/inc/json.php";
$json = new Services_JSON();
$json_str = file_get_contents($_SERVER['DOCUMENT_ROOT']."/inc/menu.json");
$objmenu = $json->decode($json_str);

$top_left_menu= '';
foreach(($objmenu->top_left_menu) as $menu ){
    if ($menu->flag =='n') {
        continue;
    }
    $disabled =  $menu->id == "setting" ? "disabled" : "";
    $top_left_menu.= '<button class="btn btn-white" onClick="location.href=(\''.$menu->href.'\')" style="padding:10px 0px 10px 0px; text-align:center;" '.$disabled.'>'.$menu->display.'</button>';
}
$top_left_menu = '<div id="topmenu" class="btn-group btn-group text-center mt-3 pl-2 pr-2" role="group">'.$top_left_menu.'</div>';

// $top_left_menu = '<div id="topmenu" class="btn-group btn-group text-center mt-3 pl-2 pr-2" role="group">
//         <button class="btn btn-white" onClick="location.href=(\'/\')" style="padding:10px 0px 10px 0px; text-align:center;">Live</button>    
//         <button class="btn btn-white" onClick="location.href=(\'/config/\')" style="padding:10px 0px 10px 0px; text-align:center;" >Setup</button>
//         <button class="btn btn-white" onClick="location.href=(\'/storage/\')" style="padding:10px 0px 10px 0px; text-align:center;">Search</button>
// </div>';


$leftMenu = '<li class="nav-item">';
foreach(($objmenu->config) as $grp=>$obj){
    if ($obj->display =='n') {
        continue;
    }
    $leftMenu .= '<a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#'.$grp.'" style="padding-bottom:0px;"><span>'.($obj->display).'</span></a>';
    // $leftMenu .= '<a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#'.$grp.'" aria-expanded="false" aria-controls="'.$grp.'"><span>'.($obj->display).'</span></a>';

	$leftMenu .= '<div id="'.$grp.'" class="collapse" data-parent="#accordionSidebar"><div class="bg-white py-2 collapse-inner rounded">';

    foreach(($obj->submenus) as $page => $param){
        if ($param->flag == 'n'){
            continue;
        }
		$leftMenu .= '<a id="'.($param->id).'" class="collapse-item" href="'.$param->href.'"  target="contentFrame"><span>'.($param->display).'</span></a>';
        // $leftMenu .= "\n";
	}
	$leftMenu .= '</div></div>';
}
$leftMenu .= '</li>';

$href = 'users.html';

// print_r($_SERVER);

?>
<style>
.btn-white{
    background-color:#eee;
    width:160px;
}
/* body {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
} */
</style>
<body>
    <div id="wrapper" >
        <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">
            <?=$top_left_menu?>
            <?=$leftMenu?>
        </ul>
        <div id="content-wrapper" class="d-flex flex-column">
            <div id="content">
                <nav class="navbar navbar-expand navbar-light bg-white topbar mb-2 static-top shadow"><h3 class="ml-5">NiceHans</h3></nav>

                <div class="container-fluid">
                    <iframe src="<?=$href?>" name="contentFrame" width="100%" height="1800px" scrolling="no" marginheight="1" marginwidth="2" frameborder="0"></iframe>
                </div>
            </div>
        </div>
        <!-- End of Content Wrapper -->
    </div>
</body>
<?php
echo $footer
?>

<script>

$("#basic").addClass("show");
$("#basic_user").addClass("active");

$(".collapse-item").on("click", function () {
	// console.log(this);
	$(".collapse-item").removeClass("active");
    $(this).addClass("active");
    toTop();
});


</script>
</html>