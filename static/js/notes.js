const API_SERVER = document.location.protocol + '//' + document.location.host
var count = 10
var search = null
var last_start_id = null
var start_id = null
var cateogry = null
var subscribe = null
var this_user_id = null
var xhr = new XMLHttpRequest();


function containsObject(obj, list) {
    var i;
    for (i = 0; i < list.length; i++) {
        if (list[i].id == obj.id) {
            return true;
        }
    }
    return false;
}


function add_data(notes, subscribe_users) {
    if (!("message" in notes) && notes.notes.length) {
        last_start_id = start_id
        start_id = notes.notes[notes.notes.length - 1].note.id - 1;
        var notes_list = document.getElementById("notes-list");
        for (let i = 0; i < notes.notes.length; i++) {
            this_note = notes.notes[i];
            var div = document.createElement("div");
            div.className = "note rounded"
            html = "<h5 class='nickname'><a href='/profile/"+this_note.author.id+"'>"+this_note.author.nickname+"</a></h5>"+this_note.note.text+"<br>";
            if (this_note.note.img_file) {
                html += "<img src='/static/img/notes/"+this_note.note.img_file+"' width='100%'>"
            }
            if (this_note.note.audio_file) {
                html += "<audio class='player' src='/static/audio/notes/"+this_note.note.audio_file+"' controls></audio>"
            }
            if (this_note.author.id == this_user_id) {
                html += "<a class='text-right' href='/delete_note/"+this_note.note.id+"'><button type='button' class='btn btn-outline-danger'>Удалить</button></a>";
                html += "<a class='text-right' href='/edit_note/"+this_note.note.id+"'><button type='button' class='btn btn-outline-secondary'>Изменить</button></a>";
            } else if (subscribe_users != null && !containsObject(this_note.author, subscribe_users.users)) {
                html += "<a class='text-right' href='/subscribe/"+this_note.author.id+"'><button type='button' class='btn btn-outline-secondary'>Подписаться</button></a>";
            }
            div.innerHTML = html;
            notes_list.appendChild(div);
        };
    };
};


function update_data(is_new){
    var category_select = document.getElementById("category");
    if (is_new) {
        start_id = null;
    }
    category = category_select.value;
    data = "count=" + count;
    if (category != "null") {
        data += "&category=" + category;
    }
    if (start_id != null) {
        data += "&start_id=" + start_id
    }
    if (subscribe != null) {
        data += "&subscribe=" + subscribe
    }
    if (search != null) {
        data += "&search=" + search
    }
    xhr.open("GET", API_SERVER + "/api/notes?" + data, true);
    xhr.onload = function (){
        var notes_list = document.getElementById("notes-list");
        if (is_new) {
            notes_list.innerHTML = "";
        }
        var notes = JSON.parse(xhr.responseText);
        if (this_user_id != null) {
            xhr.open("GET", API_SERVER + "/api/users/subscribe/" + this_user_id, true);
            xhr.onload = function() {
                var subscribe_users = JSON.parse(xhr.responseText);
                add_data(notes, subscribe_users);
            }
            xhr.send();
        } else {
            add_data(notes, null);
        }
    };
    xhr.send();
}


function show_all() {
    subscribe = null;
    search = null
    update_data(true)
}


function show_subscribe(user_id) {
    subscribe = user_id;
    update_data(true)
}


function remember_id(user_id) {
    this_user_id = user_id;
}


const search_input = document.getElementById("search_input");
search_input.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        if (search_input.value != '') {
            search = search_input.value;
        }
        else {
            search = null
        }
        update_data(true)
    }
});


update_data();


document.onscroll = function (event){
    var scrollHeight = Math.max(
        document.body.scrollHeight, document.documentElement.scrollHeight,
        document.body.offsetHeight, document.documentElement.offsetHeight,
        document.body.clientHeight, document.documentElement.clientHeight);
    if (scrollHeight - window.pageYOffset <= 660) {
        if (start_id > 0 && start_id != last_start_id) {
            update_data(false);
        }
    }
};
