const ws = false;
feedPost = {}

function start() {
    document.getElementById("about").innerHTML += "<br/> We have Javascript, too! 😀"
    document.getElementById("about").innerHTML += "<br/> This probably all gonna be replaced anyway idk"

    updateFeed();
    setInterval(updateFeed, 1000);
}
 
function updateFeed() { //updates both posts and comments
    const request = new XMLHttpRequest();
    request.open("GET", "updateFeed");
    request.send();
}

function updatePosts_Feed(serverPost) {
    
}

function uploadPost() {
    const postImage = document.getElementBy("postImage")
    const img = postImage.value
    postImage.value = "";

    const postCaption = document.getElementById("postCaption")
    const cap = postCaption.value
    postCaption.value = "";

    const postJSON = {"image":img, "caption":cap}
    request.open("POST", "uploadPost");
    request.send(JSON.stringify(postJSON));
}

function addPostToFeed() {

}

function deletePost() {
    const request = new XMLHttpRequest();
    request.open("DELETE", "deletePost");
    request.send();
}

function deleteComment(commentId) {
    const request = new XMLHttpRequest();
    request.open("DELETE", "deleteComment");
    request.send();
}

function post_HTML() {

}

function comment_HTML() {

}

// function likeButton_HTML() {
//  document.getElementsByClassName("likeButton").innerHTML = '<form action="dislikePost" method="post" enctype="application/x-www-form-urlencoded">{{post.likes}}<button id="dislike_button" onclick="dislikeButton_HTML()">Un-Like</button></label>'
// }

// function dislikeButton_HTML() {
//  document.getElementsByClassName("likeButton").innerHTML = '<form action="likePost" method="post" enctype="application/x-www-form-urlencoded">{{post.likes}}<button id="like_button" onclick="likeButton_HTML()">Like</button></label>'
// }

function initWS() {

}
