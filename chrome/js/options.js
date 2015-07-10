/*
to handle multiple groups:

have plus sign button that causes new line of groupID/token to be added (PLUS server address?)

upon page load, get localStorage.groups and unpack per
http://stackoverflow.com/questions/3357553/how-to-store-an-array-in-localstorage

upon "save" button press, trammel up all groupIDs, tokens, and servers to their respective arrays
commit the stringified arrays to localStorage

upon load background.js, unpack all groupids, servers, and tokens
for each page, iterate through servers and POST

*/




// Saves options to localStorage.
function save_options() {
  
  localStorage.curriculum_groupID = document.getElementById("groupID_input").value;
  localStorage.curriculum_token = document.getElementById("token_input").value;
  // Update status to let user know options were saved.
  var status = document.getElementById("status");
  status.innerHTML = "Options Saved.";
  setTimeout(function() {
    status.innerHTML = "";
  }, 750);
}

// Restores select box state to saved value from localStorage.
function restore_options() {
  var groupID = localStorage.curriculum_groupID;
  if (!groupID) {
    return;
  }
  var token = localStorage.curriculum_token;
  if (!token) {
    return;
  }
  document.getElementById("groupID_input").innerHTML = groupID;
  document.getElementById("token_input").innerHTML = token;
}
document.addEventListener('DOMContentLoaded', restore_options);
document.querySelector('#save').addEventListener('click', save_options);