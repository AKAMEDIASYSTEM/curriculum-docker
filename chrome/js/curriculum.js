
// var ec2 = "http://ec2-107-21-88-135.compute-1.amazonaws.com:8888";
// var ec2 = "http://curriculum.nytlabs.com";
var ec2 = "http://ec2-52-0-128-225.compute-1.amazonaws.com"
var ignores = ["curriculum.nytlabs.com","ec2-52-0-128-225.compute-1.amazonaws.com","localhost","192.168.","127.0."]; // do not semantically analyze URLs contining these strings
var path = window.location.href;
var isHttps = path.split(":")[0];
var time = new Date().getTime();
var message = {};
var flagDiscard = false;


if(window.location.protocol == "https:") {
    console.log("It's https");
    // do nothing
    } else {
        for(var i=0; i<ignores.length; i++){
            // check to see if it's an ignorable domain
            if(path.indexOf(ignores[i]) != -1){
                flagDiscard = true;
            }
        }
        if(flagDiscard){
            // do nothing
        } else {
            message.queryData = {
            "url" : path,
            };
            message.ec2 = ec2+"/submit";
            }
    }
            
message.txt = "log_page";

chrome.runtime.sendMessage(message, function(response){
    if(response=="no_creds"){
        alert("Please visit the Options page for your Curriculum extension; we are missing your GroupID and token.");
    }
});
