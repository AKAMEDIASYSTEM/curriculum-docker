// background.js
// listen for pageload message from content script, submit it to server with creds

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse){
        
        if (request.txt == "log_page") {
            console.log("request contains "+ request.queryData.url);

            if(typeof(localStorage.curriculum_groupID) != "undefined"){
                // if they're already stored, send them back to content script
                request.queryData.groupID = localStorage.curriculum_groupID;
                request.queryData.token = localStorage.curriculum_token;
                console.log("submitting "+request.queryData.url+" to "+request.ec2);
                console.log("we see "+request.queryData.groupID + " " + request.queryData.token);
                $.post(request.ec2, request.queryData, function(data) {
                    console.log("submitted "+request.queryData.url+" to "+request.ec2);
                }).error(function() {
                    response = "POST failed";
                    console.log("The POST to server failed");
                });
            } else {
                // should make an html layout for popup window
                // like: window.open("path to layout.html")
                // localStorage.curriculum_groupID = "nytlabs";
                // localStorage.curriculum_token = "frankd0g_is_the_raddest";
                sendResponse("no_creds");
            }
        
        }
    });