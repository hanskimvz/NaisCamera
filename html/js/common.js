
function FillText(str, nSize, align) {
    var newStr = "";
    var strLength = "";
    strLength = str.replace(/&lt;/g, "<");
    if(strLength.length > nSize)    {
        if (align == "right") {
            newStr = "..." + str.substring(0, nSize-3);
        }
        else {
            newStr = str.substring(0, nSize-3) + "...";
        }
    }
    else {
        switch(align) {
			case "left":
				newStr = str;
				for(var j = strLength.length; j < nSize; j++)
					newStr += "&nbsp;";
				break;
			case "right":
				for(var j = strLength.length; j < nSize; j++)
					newStr += "&nbsp;";
				newStr += str;
				break;
			case "center":
				for(var j = 0; j < (nSize-strLength.length)/2; j++)
					newStr += "&nbsp;";
				newStr += str;
				strLength = newStr.replace(/&lt;/g, "<");
				for(j = strLength.length; j < nSize; j++)
					newStr += "&nbsp;";
				break;
			default:
				newStr = str;
				break;
        }
    }
    return newStr;
}

function padLeft(nr, len = 1, padChr = `0`){
	return `${nr < 0 ? `-` : ``}${`${Math.abs(nr)}`.padStart(len, padChr)}`;
}

function toTop(){
    $("html, body").animate({ scrollTop: 0 }, "slow");
}




var options =  { 
    onChange: function(cep, event, currentField, options){
        if(cep){
            var ipArray = cep.split(".");
            for (i in ipArray){
                if(ipArray[i] != "" && parseInt(ipArray[i]) > 255){
                    ipArray[i] =  '255';
                }
            }
            var resultingValue = ipArray.join(".");
            $(currentField).val(resultingValue);
        }
    }
};
// $(".ipv4").mask("099.099.099.099", options);
// $(".date").mask("0000-00-00");
// $(".time").mask("00:00:00");
// $(".datetime").mask("0000-00-00 00:00:00");