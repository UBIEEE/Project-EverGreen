const ws = false;
feedPost = {}

function start() {
	document.getElementById("about").innerHTML += "<br/> We have Javascript, too! 😀"
	document.getElementById("about").innerHTML += "<br/> This probably all gonna be replaced anyway idk"
}


function login() {
	document.getElementById("loggedin").innerHTML = '<form action="/logout" method="post" enctype="application/x-www-form-urlencoded">{% csrf_token %}<input type="submit" value="Logout"></form>'
}

function logout() {
	document.getElementById("loggedin").innerHTML = '<form action="/logout" method="post" enctype="application/x-www-form-urlencoded">{% csrf_token %}<input type="submit" value="Logout" disabled></form>'
}


