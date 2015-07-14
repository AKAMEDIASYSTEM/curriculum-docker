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

  var groupIDs = [];
  var tokens = [];
  var servers = [];

function save_options() {
  // trammel up all groupIDs into array, write array to localStorage
  groupIDs = [];
  tokens = [];
  servers = [];

  $('input[name=groupID_input]').each(function(ind){
    console.log(ind+" " + $(this).val());
    groupIDs[ind] = $(this).val();
  });

    $('input[name=token_input]').each(function(ind){
    console.log(ind+" " + $(this).val());
    tokens[ind] = $(this).val();
  });

  $('input[name=server_input]').each(function(ind){
    console.log(ind+" " + $(this).val());
    servers[ind] = $(this).val();
  });

  localStorage.curriculum_groupIDs = JSON.stringify(groupIDs);
  localStorage.curriculum_tokens = JSON.stringify(tokens);
  localStorage.curriculum_servers = JSON.stringify(servers);
    
  console.log(JSON.stringify(groupIDs));
  console.log(JSON.stringify(tokens));
  console.log(JSON.stringify(servers));

  // Update status to let user know options were saved.
  var status = document.getElementById("status");
  status.innerHTML = "Options Saved.";
  setTimeout(function() {
    status.innerHTML = "";
  }, 1000);
}

// Restores select box state to saved value from localStorage.
function restore_options() {
  var groupIDs_out = localStorage["curriculum_groupIDs"];
  console.log(groupIDs_out);
  var tokens_out = localStorage["curriculum_tokens"];
  console.log(tokens_out);
  var servers_out = localStorage["curriculum_servers"];
  console.log(servers_out);

  // restore from localStorage if extant, show blank line if not
  if(groupIDs_out || tokens_out || servers_out){
  groupIDs_out = JSON.parse(groupIDs_out);
  tokens_out = JSON.parse(tokens_out);
  servers_out = JSON.parse(servers_out);
    for (var i = groupIDs_out.length - 1; i >= 0; i--) {
      add_saved_field(groupIDs_out[i], tokens_out[i], servers_out[i]);
      }
    } else {
      add_blank_field();
    }
}

function remove_field(){
  $(this).parent().remove();
  save_options();
}

function add_blank_field(){
  // add one new credentials field
  // get index of last current field
  // concoct div with new name (index+1) and children (the inputs) and append correct attrs
  // append concoction to parent
  var newLine = document.createElement("div");
  newLine.id = "line_"+1;
  var id_in = document.createElement("input");
  id_in.type = "text";
  id_in.name = "groupID_input";
  id_in.value = "new GroupID";
  newLine.appendChild(id_in);

  var tok_in = document.createElement("input");
  tok_in.type = "text";
  tok_in.name = "token_input";
  tok_in.value = "new Token";
  newLine.appendChild(tok_in);

  var serv_in = document.createElement("input");
  serv_in.type = "text";
  serv_in.name = "server_input";
  serv_in.value = "new Server";
  newLine.appendChild(serv_in);

  var del_but = document.createElement("button");
  del_but.id = "remove";
  del_but.innerHTML = "Delete";

  newLine.appendChild(del_but);

  $('div[id=server_info]').append(newLine);
  $('button[id=remove]').on('click',remove_field);
}

function add_saved_field(grp, tok, ser){

  var newLine = document.createElement("div");
  newLine.id = "line_"+1;
  var id_in = document.createElement("input");
  id_in.type = "text";
  id_in.name = "groupID_input";
  id_in.value = grp;
  newLine.appendChild(id_in);

  var tok_in = document.createElement("input");
  tok_in.type = "text";
  tok_in.name = "token_input";
  tok_in.value = tok;
  newLine.appendChild(tok_in);

  var serv_in = document.createElement("input");
  serv_in.type = "text";
  serv_in.name = "server_input";
  serv_in.value = ser;
  newLine.appendChild(serv_in);

  var del_but = document.createElement("button");
  del_but.id = "remove";
  del_but.innerHTML = "Delete";

  newLine.appendChild(del_but);

  $('div[id=server_info]').append(newLine);
  $('button[id=remove]').on('click',remove_field);
}

document.addEventListener('DOMContentLoaded', restore_options);
$('button[id=save]').on('click', save_options);
$('button[id=add]').on('click', add_blank_field);
$('button[id=remove]').on('click', remove_field);