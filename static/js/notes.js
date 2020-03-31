var x = new XMLHttpRequest();
x.open("GET", "http://127.0.0.1:5000/api/users/1", true);
x.onload = function (){
    var person = JSON.parse(x.responseText);
    alert(person.about);
}
x.send(null);