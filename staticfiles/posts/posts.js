// ================= CSRF =================
function getCookie(name) {
  let cookieValue = null;
  document.cookie.split(";").forEach(cookie => {
    cookie = cookie.trim();
    if (cookie.startsWith(name + "=")) {
      cookieValue = decodeURIComponent(cookie.split("=")[1]);
    }
  });
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

// ================= CLICK HANDLER =================
document.addEventListener("click", function (e) {

  // ❤️ LIKE / UNLIKE POST
  const likeBtn = e.target.closest(".like-btn");
  if (likeBtn) {
    const postId = likeBtn.dataset.id;

    fetch(`/posts/${postId}/like/`, {
  method: "POST",
  headers: {
    "X-CSRFToken": csrftoken
  }
})
  .then(res => res.json())
  .then(data => {
    likeBtn.querySelector(".like-count").innerText = data.like_count;
  });

    return;
  }

  // 🗑️ DELETE COMMENT / REPLY
  const deleteComment = e.target.closest(".delete-comment");
  if (deleteComment) {
    e.preventDefault();
    e.stopPropagation();

    if (!confirm("Delete this comment?")) return;

    const commentId = deleteComment.dataset.id;
    const commentEl = deleteComment.closest(".comment");

    fetch(`/posts/comment/${commentId}/delete/`, {

      method: "POST",
      headers: { "X-CSRFToken": csrftoken }
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          commentEl.remove();
        }
      });
    return;
  }

  // 💬 SHOW REPLY FORM
  const replyBtn = e.target.closest(".reply-btn");
  if (replyBtn) {
    e.preventDefault();
    e.stopPropagation();

    const commentEl = replyBtn.closest(".comment");
    const form = commentEl.querySelector(".reply-form");

    if (form) {
      form.classList.toggle("hidden");
      form.querySelector("input").focus();
    }
  }

});

// ================= SUBMIT HANDLER =================
document.addEventListener("submit", function (e) {

  // ➕ ADD COMMENT
  const commentForm = e.target.closest(".comment-form");
  if (commentForm) {
    e.preventDefault();

    const postId = commentForm.dataset.postId;
    const input = commentForm.querySelector("input[name='comment']");
    const text = input.value.trim();
    if (!text) return;
fetch(`/posts/${postId}/comment/`, {
  method: "POST",
  headers: {
    "X-CSRFToken": csrftoken,
    "Content-Type": "application/x-www-form-urlencoded"
  },
  body: `comment=${encodeURIComponent(text)}`
})
.then(() => {
  input.value = "";
  location.reload();
});


    return;
  }

  // ↩️ SUBMIT REPLY
  const replyForm = e.target.closest(".reply-form");
  if (replyForm) {
    e.preventDefault();

    const input = replyForm.querySelector("input[name='comment']");
    const text = input.value.trim();
    if (!text) return;

    const parentId = replyForm.dataset.commentId;
    const postCard = replyForm.closest(".post-card");
    const postId = postCard.dataset.postId;
    fetch(`/posts/${postId}/comment/`, {
  method: "POST",
  headers: {
    "X-CSRFToken": csrftoken,
    "Content-Type": "application/x-www-form-urlencoded"
  },
  body: `comment=${encodeURIComponent(text)}&parent_id=${parentId}`
})
.then(() => location.reload());

    

  }

});


// backbutton 
document.getElementById("backBtn")?.addEventListener("click", () => {
  window.location.href = "/posts/feed/";
});

// deletepost
document.addEventListener("click", function (e) {

  const deleteBtn = e.target.closest(".delete-post");
  if (!deleteBtn) return;

  const postId = deleteBtn.dataset.id;
  if (!postId) return;

  if (!confirm("Delete this post?")) return;

  fetch(`/posts/${postId}/delete/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken
    }
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      deleteBtn.closest(".post-card").remove();
    }
  });

});
