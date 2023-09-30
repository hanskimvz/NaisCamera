<?php


// require_once $_SERVER['DOCUMENT_ROOT']."/inc/json.php";
// if (strpos(" ".$_SERVER['REQUEST_URI'], "/config/") >0 ){
$header = <<<EOBLOCK
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="description" content="">
        <meta name="author" content="">
        <title></title>
        <link href="/css/fontawesome-free.css" rel="stylesheet" type="text/css">
        <link href="/css/config.css" rel="stylesheet">
    </head>
EOBLOCK;

$footer = <<<EOBLOCK
    <script src="/js/jquery-3.6.0.min.js"></script>
    <script src="/js/jquery.mask.js"></script>
    <script src="/js/bootstrap.bundle.min.js"></script>
    <script src="/js/bootstrap.js"></script>
    <script src="/js/language.js"></script>
    <script src="/js/common.js"></script>
EOBLOCK;
// <!--script src="/js/bootstrap.bundle.js"></script-->
// }
// else {   
//     $header = '<head>
//     <meta charset="utf-8">
//     <meta http-equiv="X-UA-Compatible" content="IE=edge">
//     <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
//     <meta name="description" content="">
//     <meta name="author" content="">
//     <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
//     <meta http-equiv="Cache-Control" content="no-cache"/>
//     <meta http-equiv="Expires" content="0"/>
//     <meta http-equiv="Pragma" content="no-cache"/>
//     <title></title>
//     <link type="text/css" href="/css/common.css" rel="stylesheet" />

// </head>';
// $footer = '
//     <script type="text/javascript" src="/js/jquery-1.4.2.min.js"></script>
//     <script type="text/javascript" src="/js/jquery-ui-1.8.4.min.js"></script>
// ';
// }


// EOBLOCK;
/*

    <script type="text/javascript" src="/js/jquery-ui-1.8.4.min.js"></script>
    <script type="text/javascript" src="/js/jquery.ui.mouse.js"></script>
    <script type="text/javascript" src="/js/jquery.ui.slider.js"></script>
    <script type="text/javascript" src="/js/jquery.ui.slider-rtl.js"></script>
    <script type="text/javascript" src="/js/jquery.corner.js?v2.09"></script>
    <script type="text/javascript" src="/js/jquery.cookie.js"></script>
    <script type="text/javascript" src="/js/fafu_util.js"></script>
    <script type="text/javascript" src="/js/common.js"></script>
    <script type="text/javascript" src="./js/utils/log.js"></script>
    <script type="text/javascript" src="./js/utils/jq_control.js"></script>
    <script type="text/javascript" src="./js/utils/jq_string.js"></script>
    <script type="text/javascript" src="./js/uapi.ajax.js"></script>

    <script type="text/javascript" src="./js/jquery.browser.js"></script>
    <script type="text/javascript" src="./js/jquery.alphanumeric.pack.js"></script>
    <script type="text/javascript" src="./js/uapi.player.js"></script>
    <script type="text/javascript" src="./js/activexobject.js"></script>
    <script type="text/javascript" src="./js/activexptz.js"></script>
    <!--script type="text/javascript" src="./js/defstring/defbrand.js"></script-->
    <script type="text/javascript" src="./js/plat_utils/string.js"></script>
    <!--script type="text/javascript" src="./js/plat_utils/control.js"></script-->
    <!--script type="text/javascript" src="./js/plat_utils/brand.js"></script-->
    <!--script type="text/javascript" src="./js/plat_utils/uconfig.js"></script-->
    <!--script type="text/javascript" src="./js/brand.js"></script-->
    <!--script type="text/javascript" src="./js/main.js"></script-->

    <!--[If lte IE 8]>
        <link type="text/css" href="./css/ie8.css" rel="stylesheet" />
    <![endif]-->
    <!--[If lte IE 7]>
        <script type="text/javascript" src="./js/ie_exception.js"></script>
    <![endif]-->
    <!--[If lte IE 5]>
        <table bgcolor="#FF5555" width="100%" border="0" cellspacing="8">
            <tr>
                <th align="center">
                    <font size="3" color="#FFF7F7" face="Verdana, Geneva, Arial, Helvetica, sans-serif">
                        Your web browser does not support.<br>Please try one of these more modern browsers.
                    </font>
                </th>
            <tr>
                <th align="center">
                    <font size="2" color="#FFDCD4" face="Arial, Helvetica, sans-serif, Verdana, Geneva">
                        IE8 or later &nbsp; Firefox &nbsp; Chrome &nbsp; Safari
                    </font>
                </th>
            </tr>
        </table>
    <![endif]-->

    */

$top_menu = '<div id="top">
    <div id="logomenu"><a href="/"><img id="logo" class="mainLogoLink" alt="" /></a></div>
    <div id="topmenu" class="ui-widget-header" style="display:block">
        <ul id="list">
            <li><a href="/config/" class="0103">Setup</a></li>
            <li class="storage_TopMenu"><a href="/storage/" class="0109">Search</a></li>
            <li class="ui-state-hover-top"><a href="/">Live</a></li>
        </ul>
    </div>
    <div id="brandname">Nicehans</div>
</div>';



// $footer = '
//     <script type="text/javascript" src="/js/jquery-1.4.2.min.js"></script>
//     <script type="text/javascript" src="/js/jquery-ui-1.8.4.min.js"></script>
//     <script type="text/javascript" src="/js/common.js"></script>
// ';

// $footer="";

$PTZ_CONTROL_PAD= <<<EOBLOCK
<div class="card justify-content-center" style="width:200px;">
    <div class="card-header">
    	<h6 class="card-title m-0 font-weight-bold text-primary">PTZ control</h6>
	</div>
    <div class="card-body justify-content-center">
        <span class="text-center">Movement</span>
        <div class="form-group mt-1 ">
            <div class="form-inline justify-content-center">
                <button id="_lu" class="btn btn-mini btn-outline-warning"><img src="../images/pt_lu.gif" width="18" height="16" /></button>
                <button id="_cu" class="btn btn-mini btn-outline-warning"><img src="../images/pt_cu.gif" width="18" height="16" /></button>
                <button id="_ru" class="btn btn-mini btn-outline-warning"><img src="../images/pt_ru.gif" width="18" height="16" /></button>
            </div>
            <div class="form-inline  justify-content-center">
                <button id="_lm" class="btn btn-mini btn-outline-warning"><img src="../images/pt_lm.gif" width="18" height="16" /></button>
                <button id="_cm" class="btn btn-mini btn-outline-warning"><img src="../images/pt_cm.gif" width="18" height="16" /></button>
                <button id="_rm" class="btn btn-mini btn-outline-warning"><img src="../images/pt_rm.gif" width="18" height="16" /></button>
            </div>
            <div class="form-inline  justify-content-center">
                <button id="_ld" class="btn btn-mini btn-outline-warning"><img src="../images/pt_ld.gif" width="18" height="16" /></button>
                <button id="_cd" class="btn btn-mini btn-outline-warning"><img src="../images/pt_cd.gif" width="18" height="16" /></button>
                <button id="_rd" class="btn btn-mini btn-outline-warning"><img src="../images/pt_rd.gif" width="18" height="16" /></button>
            </div>						
        </div>

        <div class="form-group">
            <div class="form-inline">
                <span style="width:70px;";>Zoom</span>
                <button id="_zIn" class="btn btn-mini btn-outline-warning"><img src="../images/pt_fnear.gif" /></button>
                <button id="_zOut" class="btn btn-mini btn-outline-warning ml-2"><img src="../images/pt_ffar.gif" /></button>
            </div>
            <div class="form-inline mt-1">
                <span style="width:70px;">Focus</span>
                <button id="_fNear" class="btn btn-mini btn-outline-warning"><img src="../images/pt_fnear.gif" /></button>
                <button id="_fFar" class="btn btn-mini btn-outline-warning ml-2"><img src="../images/pt_ffar.gif" /></button>
            </div>
            <div class="form-inline mt-1">
                <span style="width:70px;">Speed</span>
                <input type="text" size="1" id="formSpeedbar" class="form-control-custom text-center"/>
                <input type="range" id="sliderSpeedbar" style="width:200px;" class="slider" />
            </div>
        </div>
        <div class="form-group">
            <div class="form-inline mb-1">
                <span>Pre-position</span>
                <input type="text" size="1" id="preset_number" class="form-control-custom ml-2 mr-2"/>
                <label>(1 ... 255)</label>
            </div>
            <button id="btnSet" class="btn btn-mini btn-warning">Set</button>
            <button id="btnClear" class="btn btn-mini btn-warning">Clear</button>
        </div>
        <div class="form-group">
            <div class="form-inline">
                <span>Preset number</span>
                <input type="text" size="1" id="preset_number" class="form-control-custom ml-1"/>
                <button id="btnGo" class="btn btn-mini btn-warning ml-1">Go</button>
            </div>
        </div>
        <div class="form-group mb-0">
            <div class="form-inline mb-1">
                <span>Tour</span>
                <select id="bottomTourListContents" class="form-control-custom ml-2" style="width:40px;">
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                    <option value="6">6</option>
                </select>
            </div>
            <button id="btnTourStart" class="btn btn-mini btn-warning">Start</button>
            <button id="btnTourSop" class="btn btn-mini btn-warning">Stop</button>
        </div>
    </div>
</div>

EOBLOCK;




?>