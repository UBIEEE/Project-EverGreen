let ws = null;
feedPost = {};

function initWS() {
  // is this https?
  const isSecureConnection = window.location.protocol === "https:";

  // choose between ws & wss
  let wsProtocol;

  if (isSecureConnection) {
    wsProtocol = "wss:"; // encrypted baby!!
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

    if (data.type === "like_update") {
      // this updates likes (number of them)
      updateLikeCount(
        data.post_id,
        data.likes,
        data.likers_display,
        data.has_liked,
      );
    } else if (data.type === "feed_update") {
      // broadcast
      updatePosts_Feed(data.posts);

    }
 
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
                  ${post.image.url ? `<img src="${post.image.url}" style="max-width: 300px;">` : ""}
                  <p>${post.caption}</p>
                  <p class="likers-display">${post.likers_display || ""}</p>
                  <div class="likeButton">
                      <button type="button"
                              onclick="likePost('${post.id}')"
                              data-post-id="${post.id}"
                              class="${post.has_liked ? "liked" : ""}">
                          ${post.has_liked ? "Unlike" : "Like"} (${post.likes})
                      </button>
                  </div>
              </div>
          `,
    )
    .join("");
}

function likePost(postId) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(
      JSON.stringify({
        type: "like",
        post_id: postId,
      }),
    );
  } else {
    console.error("WebSocket is not connected");
  }
}

function updateLikeCount(postId, likes, likersDisplay, hasLiked) {
  const postElement = document.querySelector(
    `button[data-post-id="${postId}"]`,
  );
  if (postElement) {

    let buttonText;
    if (hasLiked) {
        buttonText = "Unlike";
    } else {
        buttonText = "Like";
    }

   
    let displayText = buttonText + " (" + likes + ")";

 
    postElement.textContent = displayText;

    // update the likers visual!!!
    const likersElement = postElement
      .closest(".post")
      .querySelector(".likers-display");
    if (likersElement) {
      likersElement.textContent = likersDisplay;
    }
  }
}

function uploadPost() {
  const form = document.getElementById("uploadForm");
  const formData = new FormData(form);
  const caption = formData.get("caption");

  if (!caption || caption.trim() === "") {
    console.error("Caption is required");
    return;
  }

  // make into obj
  const postData = {
    type: "upload_post",
    caption: formData.get("caption"),
  };

  // convert image into proper base64
  const imageFile = formData.get("image_upload");

  if (imageFile) {
    const reader = new FileReader();

    reader.readAsDataURL(imageFile);

    reader.onload = function () {
      postData.image = reader.result;
      sendPostData(postData);
    };
  } else {
    sendPostData(postData);
  }
}

function handleEnterKey(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    uploadPost();
  }
}

function sendPostData(postData) {

  if (ws && ws.readyState === WebSocket.OPEN) {

    ws.send(JSON.stringify(postData));
    document.getElementById("uploadForm").reset();

  } else {
    console.error("WebSocket is not connected");
  }
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

window.addEventListener("unload", function () {
  if (ws) {
    ws.close();
  }
});
