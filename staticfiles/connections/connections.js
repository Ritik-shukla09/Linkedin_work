console.log("connections.js loaded");

/* =======================
   CSRF TOKEN
   ======================= */
function getCSRFToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]")?.value;
}

/* =======================
   GLOBAL CLICK HANDLER
   ======================= */
document.addEventListener("click", async (e) => {

  /* =======================
     CONNECT
     ======================= */
  const connectBtn = e.target.closest(".js-connect");
  if (connectBtn) {
    const userId = connectBtn.dataset.userId;

    const res = await fetch("/connections/ajax/connect/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({ user_id: userId }),
    });

    const data = await res.json();

    if (["sent", "already_sent", "resent"].includes(data.status)) {
      connectBtn.textContent = "Pending";
      connectBtn.classList.remove("btn-connect", "js-connect");
      connectBtn.classList.add("btn-pending");
      connectBtn.disabled = true;
    }

    return; // ✅ SAFE (inside listener)
  }

  /* =======================
     FOLLOW
     ======================= */
    /* =======================
   FOLLOW
   ======================= */
const followBtn = e.target.closest(".js-follow");
if (followBtn) {
  console.log("Follow clicked"); // DEBUG (remove later)

  const userId = followBtn.dataset.userId;

  const res = await fetch("/connections/ajax/follow/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
    body: JSON.stringify({ user_id: userId }),
  });

  const data = await res.json();
  console.log("Follow response:", data); // DEBUG

  if (data.status === "followed") {
    followBtn.textContent = "Following";
    followBtn.className = "btn btn-pending js-unfollow";
  }

  return;
}


  /* =======================
     DISCONNECT
     ======================= */
  /* =======================
   DISCONNECT
   ======================= */
const disconnectBtn = e.target.closest(".js-disconnect");
if (disconnectBtn) {
  const userId = disconnectBtn.dataset.userId;

  if (!confirm("Remove connection?")) return;

  const res = await fetch("/connections/ajax/disconnect/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
    body: JSON.stringify({ user_id: userId }),
  });

  const data = await res.json();

  if (data.status === "disconnected") {
    disconnectBtn.textContent = "Connect";
    disconnectBtn.className = "btn btn-connect js-connect";
    disconnectBtn.disabled = false;
  } else {
    alert(data.error || "Failed to disconnect");
  }

  return;
}

  /* =======================
     ACCEPT / REJECT REQUEST
     ======================= */
  const acceptBtn = e.target.closest(".js-accept");
  const rejectBtn = e.target.closest(".js-reject");

  if (acceptBtn || rejectBtn) {
    const btn = acceptBtn || rejectBtn;
    const requestId = btn.dataset.requestId;
    const action = acceptBtn ? "accept" : "reject";

    const res = await fetch("/connections/ajax/respond/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        req_id: requestId,
        action: action,
      }),
    });

    const data = await res.json();

    if (data.status === "accepted" || data.status === "rejected") {
      btn.closest(".request-card").remove();
    }

    return;
  }
    /* =======================
     UNFOLLOW
     ======================= */
  const unfollowBtn = e.target.closest(".js-unfollow");
  if (unfollowBtn) {
    const userId = unfollowBtn.dataset.userId;

    if (!confirm("Unfollow this user?")) return;

    const res = await fetch("/connections/ajax/unfollow/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({ user_id: userId }),
    });

    const data = await res.json();

    if (data.status === "unfollowed") {
      unfollowBtn.textContent = "Follow";
      unfollowBtn.className = "btn btn-follow js-follow";
    }

    return;
  }


});


   