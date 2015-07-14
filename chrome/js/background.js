// background.js
// listen for pageload message from content script, submit it to server with creds

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse){
        console.log(request.txt);
        if (request.txt == "log_page") {
            console.log("request contains "+ request.queryData.url);

            if(localStorage.curriculum_groupIDs || localStorage.curriculum_tokens || localStorage.curriculum_servers){
                // if these things exist at all
                // go through each and POST to the server
                groupIDs = JSON.parse(localStorage.curriculum_groupIDs);
                tokens = JSON.parse(localStorage.curriculum_tokens);
                servers = JSON.parse(localStorage.curriculum_servers);
                for (var i = groupIDs.length - 1; i >= 0; i--) {
                    request.queryData.groupID = groupIDs[i];
                    request.queryData.token = tokens[i];
                    request.ec2 = "http://" + servers[i] + "/submit";
                    $.post(request.ec2, request.queryData, function(data) {
                            console.log("submitted "+request.queryData.url+" to "+request.ec2);
                        }).error(function() {
                            response = "POST failed";
                            console.log("The POST to server "+ request.ec2 +", groupID "+request.queryData.groupID+" failed");
                        });
                }
            // console.log("submitting "+request.queryData.url+" to "+request.ec2);
            // console.log("we see "+request.queryData.groupID + " " + request.queryData.token);
            // $.post(request.ec2, request.queryData, function(data) {
            //     console.log("submitted to NYTLABS "+request.queryData.url+" to "+request.ec2);
            // }).error(function() {
            //     response = "POST failed";
            //     console.log("The POST to server, groupID NYTLABS failed");
            // });

            // also post to the Slack group instances running curriculum
            // request.queryData.groupID = "slackers";
            // request.queryData.token = "93b2931a2af8dc614dc65563950f7020a";
            // $.post(request.ec2, request.queryData, function(data) {
            //     console.log("submitted to SLACKERS "+request.queryData.url+" to http://curriculum.local/submit");
            // }).error(function() {
            //     response = "POST failed";
            //     console.log("The POST to server, groupID SLACKERS failed");
            // });
            // // also post to any local instances running curriculum
            // $.post("http://curriculum.nytlabs.com/submit", request.queryData, function(data) {
            //     console.log("submitted to LOCAL"+request.queryData.url+" to http://curriculum.local/submit");
            // }).error(function() {
            //     response = "POST failed";
            //     console.log("The POST to LOCAL server failed");
            // });
        } else {
            sendResponse("no_creds");
        }
        
        } else if(request.txt == "ignore me"){
            // do nothing
            console.log("ignoring the page");
        }
    });