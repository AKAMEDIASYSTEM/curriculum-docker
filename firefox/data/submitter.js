// CHANGE THIS TO YOUR CURRICULUM SERVER
var ec2 = "http://curriculum.nytlabs.com/submit";
var lcl = "http://curriculum.local/submit";


// CHANGE THESE TO REFLECT YOUR GROUPID AND TOKEN
var tok = "demo_token";
var group = "demo_groupID";
var request = {};
request.token = tok;
request.groupID = group;

self.port.on("pageLoaded", function(url) {
  console.log("worker got "+url);
  if(window.location.protocol == "https:"){
    console.log("ignoring an https page");
  } else {
    request.url = window.location.href;
    // post to nytlabs-hosted curriculum instance
  $.post(ec2, request, function(data){
    self.port.emit("pageSubmitted", url);
    console.log("worker reporting submission");
        }).error(function(){
            console.log("failed to submit");
        });
        // now post to any subnet-resident curriculum instances
  $.post(lcl, request, function(data){
    self.port.emit("pageSubmitted", url);
    console.log("worker reporting submission");
        }).error(function(){
            console.log("failed to submit");
        });
    }

});