// background.js
// listen for pageload message from content script, submit it to server with creds

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse){
        console.log(request.txt);
        if (request.txt == "log_page") {
            console.log("request contains "+ request.queryData.url);

            if(typeof(localStorage.curriculum_groupID) != "undefined"){
                // if they're already stored, send them back to content script
                request.queryData.groupID = localStorage.curriculum_groupID;
                request.queryData.token = localStorage.curriculum_token;
                console.log("submitting "+request.queryData.url+" to "+request.ec2);
                // console.log("we see "+request.queryData.groupID + " " + request.queryData.token);
                $.post(request.ec2, request.queryData, function(data) {
                    console.log("submitted "+request.queryData.url+" to "+request.ec2);
                }).error(function() {
                    response = "POST failed";
                    console.log("The POST to server failed");
                });
                // also post to any local instances running curriculum
                $.post("http://curriculum.local/submit", request.queryData, function(data) {
                    console.log("submitted to LOCAL"+request.queryData.url+" to http://curriculum.local/submit");
                }).error(function() {
                    response = "POST failed";
                    console.log("The POST to LOCAL server failed");
                });
            } else {
                sendResponse("no_creds");
            }
        
        } else if(request.txt == "ignore me"){
            // do nothing
            console.log("ignoring the page");
        }
    });