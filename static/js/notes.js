var xhr = new XMLHttpRequest();
start_id = null
count = 15
xhr.open("GET", "http://127.0.0.1:5000/api/notes?count=4", true);
xhr.onload = function (){
    var notes = JSON.parse(xhr.responseText);
    //
    start_id = notes.notes[notes.notes.length - 1].note.id - 1;
    var notes_list = document.getElementById("notes-list");
    for (let i = 0; i < notes.notes.length; i++) {
        this_note = notes.notes[i];
        var div = document.createElement("div");
        div.className = "note rounded"
        html = "<h5 class='nickname'>"+this_note.author.nickname+"</h5><h6>"+this_note.note.title+"</h6>"+this_note.note.text+"<br>";
        if (this_note.note.img_file) {
            html += "<img src='http://127.0.0.1:5000/static/img/notes/"+this_note.note.img_file+"' width='100%'>"
        }
        if (this_note.note.audio_file) {
            html += "<audio class='player' src='http://127.0.0.1:5000/static/audio/notes/"+this_note.note.audio_file+"' controls></audio>"
        }
        html += "<p class='text-right'><a href='/subscribe/"+this_note.author.id+"'><button type='button' class='btn btn-info'>Подписаться</button></a></p>";
        div.innerHTML = html;
        notes_list.appendChild(div);
    };
};
xhr.send();


document.onscroll = function (event){
    var scrollHeight = Math.max(
        document.body.scrollHeight, document.documentElement.scrollHeight,
        document.body.offsetHeight, document.documentElement.offsetHeight,
        document.body.clientHeight, document.documentElement.clientHeight);
    if (scrollHeight - window.pageYOffset <= 660) {
        if (start_id > 0) {
            data = "start_id=" + start_id + "&count=" + count;
            xhr.open("GET", "http://127.0.0.1:5000/api/notes?" + data, true);
            xhr.onload = function (){
                var notes = JSON.parse(xhr.responseText);
                //
                start_id = notes.notes[notes.notes.length - 1].note.id - 1;
                var notes_list = document.getElementById("notes-list");
                for (let i = 0; i < notes.notes.length; i++) {
                    this_note = notes.notes[i];
                    var div = document.createElement("div");
                    div.className = "note rounded"
                    html = "<h5 class='nickname'>"+this_note.author.nickname+"</h5><h6>"+this_note.note.title+"</h6>"+this_note.note.text+"<br>";
                    if (this_note.note.img_file) {
                        html += "<img src='http://127.0.0.1:5000/static/img/notes/"+this_note.note.img_file+"' width='100%'>"
                    }
                    if (this_note.note.audio_file) {
                        html += "<audio class='player' src='http://127.0.0.1:5000/static/audio/notes/"+this_note.note.audio_file+"' controls></audio>"
                    }
                    html += "<p class='text-right'><a href='/subscribe/"+this_note.author.id+"'><button type='button' class='btn btn-info'>Подписаться</button></a></p>";
                    div.innerHTML = html;
                    notes_list.appendChild(div);
                };
            };
            xhr.send();}
    }
};
