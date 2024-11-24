//const ws = false;
let ws = null;
feedPost = {};

function initWS() {

  // is this https?
  const isSecureConnection = window.location.protocol === "https:";

  // choose between ws & wss
  let wsProtocol = "ws";

  if (isSecureConnection) {
      wsProtocol = "wss:";  // encrypted baby!!
  } else {
      wsProtocol = "ws:";   
  }
  
  const host = window.location.host;
  const wsPath = `${wsProtocol}//${host}/ws/feed/`; 

  console.log("Attempting WebSocket connection to:", wsPath);

  ws = new WebSocket(wsPath);

  ws.onopen = function () {
    console.log("WebSocket connection established!");
  };

  ws.onmessage = function (event) {
    console.log("Received message:", event.data);
    const data = JSON.parse(event.data);
    updatePosts_Feed(data.posts);
  };

  ws.onclose = function () {
    console.log("WebSocket CLOSED, attempting to RECONNECT!!!!...");
    setTimeout(initWS, 1000); // reconnecting after 1 sec, 1000 ms
  };

  ws.onerror = function (error) {
    console.error("WebSocket Error:", error);
  };
}

function start() {
  document.getElementById("about").innerHTML +=
    "<br/> We have Javascript, too! 😀";
  document.getElementById("about").innerHTML +=
    "<br/> This probably all gonna be replaced anyway idk";

  updateFeed();
  initWS();
  //setInterval(updateFeed, 1000);
}

function updateFeed() {
  //updates both posts and comments
  const request = new XMLHttpRequest();

  request.onload = function () {
    if (this.status === 200) {
      const data = JSON.parse(this.responseText);
      updatePosts_Feed(data.posts);
    }
  };
  request.open("GET", "updateFeed");
  request.send();
}

function updatePosts_Feed(posts) {
  if (!posts) {
    return;
  }
  const feedBox = document.getElementById("feed-box");
  feedBox.innerHTML = posts
    .map(
      (post) => `
          <div class="post">
              <p>${post.user}</p>
              <img src="${post.image.url}" style="max-width: 300px;">
              <p>${post.caption}</p>
              <p>${post.likes} likes</p>
              <div class="likeButton">
                  <form action="likePost/${post.id}" method="post" enctype="application/x-www-form-urlencoded">
                      <button type="button" onclick="likePost('${post.id}')">${post.likes} Like</button>
                  </form>
              </div>

          </div>
          `,
    )
    .join("");
}

function uploadPost() {
  const form = document.getElementById("uploadForm");
  const formData = new FormData(form);

  // Add the frickinCSRF token
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  const request = new XMLHttpRequest();
  request.open("POST", "uploadPost");
  request.setRequestHeader("X-CSRFToken", csrfToken);

  request.onload = function () {
    if (this.status === 200) {
      form.reset();
      updateFeed();
    }
  };

  request.send(formData);
}

// WE DO NOT NEED THIS METHOD
//function addPostToFeed() {}

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

// function likeButton_HTML() {
//  document.getElementsByClassName("likeButton").innerHTML = '<form action="dislikePost" method="post" enctype="application/x-www-form-urlencoded">{{post.likes}}<button id="dislike_button" onclick="dislikeButton_HTML()">Un-Like</button></label>'
// }

// function dislikeButton_HTML() {
//  document.getElementsByClassName("likeButton").innerHTML = '<form action="likePost" method="post" enctype="application/x-www-form-urlencoded">{{post.likes}}<button id="like_button" onclick="likeButton_HTML()">Like</button></label>'
// }

// function likeButton_HTML() {
//  document.getElementsByClassName("likeButton").innerHTML = '<form action="dislikePost" method="post" enctype="application/x-www-form-urlencoded">{{post.likes}}<button id="dislike_button" onclick="dislikeButton_HTML()">Un-Like</button></label>'
// }

// function dislikeButton_HTML() {
//  document.getElementsByClassName("likeButton").innerHTML = '<form action="likePost" method="post" enctype="application/x-www-form-urlencoded">{{post.likes}}<button id="like_button" onclick="likeButton_HTML()">Like</button></label>'
// }
//
function likePost(postId) {
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  const request = new XMLHttpRequest();
  request.open("POST", `likePost/${postId}`);

  request.setRequestHeader("X-CSRFToken", csrfToken);
  request.setRequestHeader("Content-Type", "application/json");

  request.onload = function () {
    if (this.status === 200) {
      updateFeed(); // Refresh the feed to show updated likes
    } else {
      console.error("Like failed");
    }
  };

  request.send();
}

window.addEventListener("unload", function () {
  if (ws) {
    ws.close();
  }
});
