
_selected_language = "korean";
url = "/language/"+_selected_language+".json";
// console.log(url);


function txt2Json(txt) {
    let arr =  new Array();
    let body = "";
    lines = txt.split("\n");
    lines.forEach(function(line){
        line = line.split("\/\/")[0];
        line = line.trim();
        if (line) {
            body += line +"\n";
        }
    });

    arr = JSON.parse(body);
    return arr;
}


async function updateLanguage(url) {
    let lang = new Array();
    let response = await fetch(url);
    let data = await response.text();
    
    arr = txt2Json(data);
    // console.log(arr);
    for (x of Object.keys(arr)){
        y = x.replace(/ /g, '').toLowerCase().trim();
        lang[y] = arr[x];
    }
    // console.log(lang);
    $("span, h6, option, button, strong").each(function(){
        x = $(this).text().replace(/ /g, '').toLowerCase().trim();
        $(this).text(lang[x]);
    });

    // $("option").each(function(idx, item){
    //     x = $(this).text().replace(" ","").toLowerCase();
    //     $(this).text(lang[x]);
    // });
    // $("h6").each(function(idx, item){
    //     x = $(this).text().replace(" ","").toLowerCase();
    //     $(this).text(lang[x]);
    // });
    // $("h5").each(function(idx, item){
    //     x = $(this).text().replace(" ","").toLowerCase();
    //     $(this).text(lang[x]);
    // });
    // $("button").each(function(idx, item){
    //     x = $(this).text().replace(" ","").toLowerCase();
    //     $(this).text(lang[x]);
    // });
    // $("label").each(function(idx, item){
    //     x = $(this).text().replace(" ","").toLowerCase();
    //     $(this).text(lang[x]);
    // });


}

updateLanguage(url);

// x = fetchText(url);
// console.log(x.text());

// console.log(x);
//   .then(response => response.text())
//   .then(text => console.log(text))

// console.log(response);



// jsonstr = '{ "setup":            "Setup",  "set up":            "Setup", \
//     "basic":            "Basic", \
//     "videonaudio":      "Video & Audio", \
//     "eventconf":        "Event Configuration", \
//     "networkconf":      "Network Configuration", \
//     "storage":          "Storage" \
// }';

// arr = JSON.parse(jsonstr);

// console.log(arr);
// _selected_language = "Korean";
// var lang = new Array();
// $.getJSON("/inc/lang.json", function(language) {
//     // console.log(language);
//     language.forEach(function(item){
//         // console.log(item);
//         // lang[item.key.toLowerCase()] = item[_selected_language];
//         lang[item.key] = item[_selected_language];
//     });
//     $("span").each(function(idx, item){
//         x = $(this).text().replace(" ","").toLowerCase();
//         $(this).text(lang[x]);
//         // x = item;
//         // console.log(x);
//     });
// });

// _selected_language = "english";
// url = "/language/"+_selected_language+".json"
// let lang = new Array();
// $.getJSON(url, function(response) {
//     // console.log(response);
//     for (x of Object.keys(response)){
//         lang[x.replace(" ","").toLowerCase()] = response[x];
//     }
//     console.log(lang);
//     $("span").each(function(idx, item){
//         x = $(this).text().replace(" ","").toLowerCase();
//         $(this).text(lang[x]);
//     });
//     $("option").each(function(idx, item){
//         x = $(this).text().replace(" ","").toLowerCase();
//         $(this).text(lang[x]);
//     });

// });

