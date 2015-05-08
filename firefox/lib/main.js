// require("sdk/tabs").on("ready", logURL);

var data = require("sdk/self").data;
var pageMod = require("sdk/page-mod");


pageMod.PageMod({
  include: "*",
  contentScriptFile: [data.url("jquery.js"),
                    data.url("submitter.js")],
  onAttach: function(worker) {
    worker.port.emit("pageLoaded", "foo");
    worker.port.on("pageSubmitted", function(url) {
      console.log("submitted "+url);
    });
  }
});