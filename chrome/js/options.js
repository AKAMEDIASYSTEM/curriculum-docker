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