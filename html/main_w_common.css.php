<!DOCTYPE html lang="en">
<?php
include ("inc/common.php");
?>
<html lang="en" >
<?php
echo $header;

$tab_option = '<div id="tab_0">
    <dl class="box">
        <dd class="box-title"><h2>Stream</h2></dd>
        <dd class="box-content" id="streamSector">
            <dl>
                <dd class="item">
                    <select id="transmission" onchange="ChangeVideo()" style="width: 165px"></select>
                </dd>
                <input type="checkbox" id="videoStreamEnableCheckBox" /><label for="videoStreamEnableCheckBox" class="020185">Video</label>
                <input type="checkbox" id="audioStreamEnableCheckBox" class="audioContents"/><label for="audioStreamEnableCheckBox" class="audioContents 020186">Audio</label>
            </dl>
        </dd>
    </dl>
    <dl class="box">
        <dd class="box-title"><h2>Size</h2></dd>
        <dd id="sizeSector" class="box-content"></dd>
            <dl>
                <dd class="item">
                    <select id="screen_size" style="width: 100">
                        <option value="0" selected>Fit</option>
                        <option value="0.25">25%</option>
                        <option value="0.5">50%</option>
                        <option value="0.75">75%</option>
                        <option value="1">100%</option>
                        <option value="1.5">150%</option>
                    </select>
                </dd>
            </dl>
        </dd>
    </dl>
    <dl class="box" id="trigAlarmContents">
        <dd class="box-title"><h2>Trigger-Alarm(DO)</h2></dd>
        <dd class="box-content" id="triggerSector">
            <dl>
                <dd class="item">
                    <select id="doChannel" class="dsp_hide">
                        <option value="0">Channel1</option>
                    </select>
                    <input type="radio" name="formMainTrigger" id="trig_on" value="on" />
                    <label for="trig_on"> On</label>
                    <input type="radio" name="formMainTrigger" id="trig_off" value="off" />
                    <label for="trig_off"> Off</label>
                </dd>
            </dl>
        </dd>
    </dl>
    <dl class="box" id="audioContents">
        <dd class="box-title"><h2 class="020107">Audio</h2></dd>
        <dd id="audioSector" class="box-content">
            <dl>
                <dd class="item">
                    <input type="checkbox" id="audioSpeaker" /><label for="audioSpeaker">Speaker</label>
                    <div id="audioSpeakerVolumeSlider" class="slider-bar">---</div>
                </dd>
                <dd class="item">
                    <input type="checkbox" id="audioMicrophone" /><label for="audioMicrophone" class="020109">Microphone</label>
                </dd>
            </dl>
        </dd>
    </dl>
    <dl class="box" id="recordContents">
        <dd class="box-title"><h2>Video Control</h2></dd>
        <dd id="controlSector" class="box-content">
            <dl class="item">
                <dd>
                    <button id="recording"><span id="txtRec">Record</span></button>
                    <button id="snapshot"><span>Snapshot</span></button>
                </dd>
                <dd>
                    <button id="pause"><span id="txtPause">Pause</span></button>
                    <button id="controlSetting"><span>Setting</span></button>
                </dd>
            </dl>
        </dd>
    </dl>
</div>';

$tab_status = '<div id="tab_1">
    <dl class="box">
        <dd class="box-title h2BottomSpace"><h2 class="020157">System</h2></dd>
        <dd class="box-content">
            <dl class="item">
                <dd>
                    <span>CPU : </span>
                    <span id="status_CpuUsed">-</span>%
                </dd>
                <dd>
                    <span>Memory : </span>
                    <span id="status_MemUsed">-</span>%
                </dd>
            </dl>
        </dd>
    </dl>
    <dl class="box">
        <dd class="box-title h2BottomSpace"><h2 class="020115">Time</h2></dd>
        <dd class="box-content adjustStatus">
            <dl>
                <dd class="item">
                    <span>Uptime : </span>
                    <span id="status_TimeUptime">-</span>
                </dd>
            </dl>
        </dd>
    </dl>';

$msg["stream0"] = "Main Stream";
$msg["stream1"] = "Sub Stream";
$msg["stream2"] = "Snapshot";
for ($i=0; $i<3; $i++) {
$tab_status .= '
    <dl class="box" stream'.$i.'StatusContents">
        <dd class="box-title h2BottomSpace"><h2>'.$msg["stream".$i].'</h2></dd>
        <dd class="box-content adjustStatus">
            <dl class="item">
                <dd style="padding-bottom:2px;"><span>Type: </span><span id="status_streamType'.$i.'">-</span></dd>
                <dd style="padding-bottom:2px;"><span>Resolution : </span><span id="status_streamResolution'.$i.'">-</span></dd>
                <dd style="padding-bottom:2px;"><span>Fps : </span><span id="status_streamFps'.$i.'">-</span></dd>
                <dd style="padding-bottom:2px;"><span>Bitrate : </span><span id="status_streamBitrate'.$i.'">-</span></dd>
            </dl>
        </dd>
    </dl>';
}

$tab_status .= '
    <dl class="box">
        <dd class="box-title"><h2>RTSP Connect List</h2></dd>
        <dd class="box-content">
            <dl>
                <dd class="item">
                    <span>Total : </span> 
                    <span id="status_ConnectNum">-</span>
                </dd>
                <dd style="padding:0px;">
                    <select size="6" id="formConnectList" class="select-list" style="width:13em"><option>192.168.1.2</option></select>
                </dd>
            </dl>
        </dd>
    </dl>
</div>';

$tab_ptz = '<div id="tab_2">
    <div id="loading_ptz" class="dsp_show_block margin_top_step2 text_cen">
        <img src="./images/loading.gif" alt="in" />
    </div>
    <div id="panel_ptz">
        <dl class="box">
            <dd class="box-title"><h2 class="020139">Movement</h2></dd>
            <dd id="ptz" class="box-content">
                <dl>
                    <dd id="ptz_panel" class="item">
                        <dl>
                            <dd id="pt_lu" class="ui-button"></dd>
                            <dd id="pt_cu" class="ui-button"></dd>
                            <dd id="pt_ru" class="ui-button"></dd>
                            <dd id="pt_lm" class="ui-button"></dd>
                            <dd id="pt_cm" class="ui-button"></dd>
                            <dd id="pt_rm" class="ui-button"></dd>
                            <dd id="pt_ld" class="ui-button"></dd>
                            <dd id="pt_cd" class="ui-button"></dd>
                            <dd id="pt_rd" class="ui-button"></dd>
                        </dl>
                    </dd>
                    <dd id="ptz_zoomfocus">
                        <dl>
                            <dd id="main_ptz_zoom" class="020140">Zoom</dd>
                            <dd>
                                <img id="_zIn" class="ui-button" width="16" height="16" src="images/pt_fnear.gif" alt="zoom in" />
                                <img id="_zOut" class="ui-button" width="16" height="16" src="images/pt_ffar.gif" alt="zoom out" />
                            </dd>
                        </dl>
                        <dl>
                            <dd id="main_ptz_focus" class="020141">Focus</dd>
                            <dd>
                                <img id="_fNear" class="ui-button" width="16" height="16" src="images/pt_fnear.gif" alt="focus near" />
                                <img id="_fFar" class="ui-button" width="16" height="16" src="images/pt_ffar.gif" alt="focus far" />
                            </dd>
                        </dl>
                    </dd>
                </dl>
            </dd>
        </dl>
        <dl class="box">
            <dd class="box-title"><h2 class="020142">Speed</h2></dd>
            <dd class="box-content">
                <dl>
                    <dd class="item">
                        <dl>
                            <dd id="ptz_speedbar">
                                <dl>
                                    <dd><div id="slider_speedbar" class="slider-bar"></div></dd>
                                    <dd>
                                        <input type="text" size="3" id="text_speedbar" value=20></input>
                                    </dd>
                                </dl>
                            </dd>
                        </dl>
                    </dd>
                </dl>
            </dd>
        </dl>
        <dl class="box">
            <dd class="box-title"><h2 class="020143">Pre Position</h2></dd>
            <dd class="box-content">
                <dl>
                    <dd class="item">
                        <dl>
                            <dd id="ptz_numberbar">
                                <dl>
                                    <dd>
                                        <input type="text" size="1" id="preset_number" value=20></input>
                                        <label for="preset_number">(1 ... 255)</label>
                                    </dd>
                                </dl>
                            </dd>
                            <dd class="setclear_button">
                                <button id="btnSet"><span class="020144">Set</span></button>
                                <button id="btnClear"><span class="020146">Clear</span></button>
                            </dd>
                            <dd class="preset_Number_contents">
                                <dl>
                                    <dd>
                                        <span class="020147">Preset Number :</span>
                                        <select class="select" id="setPresetList"></select>
                                        <input type="text" size="1" id="setPresetText" class="dsp_hide"></input>
                                    </dd>
                                </dl>
                            </dd>
                            <dd class="go_button">
                                <button id="btnGo"><span class="020145">Go</span></button>
                            </dd>
                        </dl>
                    </dd>
                </dl>
            </dd>
        </dl>
        <dl class="box TourContents dsp_hide">
            <dd class="box-title"><h2 class="020148">Tour</h2></dd>
            <dd class="box-content">
                <dl>
                    <dd class="item">
                        <dl>
                            <dd>
                                <span class="020149">Touring Number :</span>
                                <select class="select" id="bottomTourListContents">
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3">3</option>
                                    <option value="4">4</option>
                                    <option value="5">5</option>
                                    <option value="6">6</option>
                                </select>
                            </dd>
                        </dl>
                        <dl>
                            <dd class="tourStartStop_button">
                                <button id="btnTourStart"><span class="020150">Start</span></button>
                                <button id="btnTourStop"><span class="020151">Stop</span></button>
                            </dd>
                        </dl>
                    </dd>
                </dl>
            </dd>
        </dl>
        <dl class="box HomePositionContents dsp_hide">
            <dd class="box-title"><h2 class="020152">Home Position</h2></dd>
            <dd class="box-content">
                <dl>
                    <dd class="item">
                        <dl>
                            <dd class="homeSetGo_button">
                                <button id="btnHomeSet"><span class="020153">Set</span></button>
                                <button id="btnHomeGo"><span class="020154">Go</span></button>
                            </dd>
                        </dl>
                    </dd>
                </dl>
            </dd>
        </dl>
        <dl class="box ptzCtrlContents dsp_hide">
            <dd class="box-title"><h2 class="020181">PTZ Control</h2></dd>
            <dd id="" class="box-content">
                <dl>
                    <dd class="item">
                        <dl>
                            <dd>
                                <button id="ptzCtrlShow"><span class="020182">Show</span></button>
                                <button id="ptzCtrlHide"><span class="020183">Hide</span></button>
                            </dd>
                        </dl>
                    </dd>
                </dl>
            </dd>
        </dl>
        <dl class="box wiperContents dsp_hide">
            <dd class="box-title"><h2 class="020184">Wiper</h2></dd>
            <dd id="" class="box-content">
                <dl>
                    <dd class="item">
                        <dl>
                            <dd>
                                <button id="btnWiperStart"><span class="020150">Start</span></button>
                                <button id="btnWiperStop"><span class="020151">Stop</span></button>
                            </dd>
                        </dl>
                    </dd>
                </dl>
            </dd>
        </dl>
    </div>
</div>';
?>


<body>
    <div id="compatible_ie"></div>
    <div class="container">
        <?=$top_menu?>
        <div class="main">
            <div class="sidebar">
                <div class="box">
                    <div class="tab-wrap">
                        <!-- active tab on page load gets checked attribute -->
                        <input type="radio" id="tab1" name="tabGroup1" class="tab" checked>
                        <label for="tab1">Option</label>

                        <input type="radio" id="tab2" name="tabGroup1" class="tab" >
                        <label for="tab2">Status</label>

                        <input type="radio" id="tab3" name="tabGroup1" class="tab">
                        <label for="tab3" id="tab_ptz" style="display:">PTZ</label>

                        <div class="tab__content"><?=$tab_option?></div>
                        <div class="tab__content"><?=$tab_status?></div>
                        <div class="tab__content"><?=$tab_ptz?></div>
                    </div>
                </div>
            </div>
            <div class="content">
                <div class="box">
                    <div id="screen">
                        <img src="http://49.235.119.5/a.jpg" width="500"></img>
                        <!-- <canvas height="600"></canvas> -->
                    </div>
                    <div id="screen_tools"></div>
                </div>
            </div>
            <div class="clear">&nbsp;</div>            
        </div>
    </div>
</body>
</html>

<?PHP
echo $footer;
exit();
?>
