document.addEventListener("DOMContentLoaded", function () {
  //
  document.querySelectorAll(".like-btn").forEach((item) => {
    item.addEventListener("click", like_clicked);
  });
  document.querySelectorAll(".edit-btn").forEach((item) => {
    item.addEventListener("click", edit_post);
  });
  const follow_btn = document.querySelector("#follow-btn");
  follow_btn.addEventListener("click", follow_user);
  //
});

function like_clicked() {
  fetch(`/like/${this.name}`, {
    method: "POST",
    // body: this.name,
  })
    .then((response) => response.json())
    .then((data) => {
      const like_btn = document.getElementById(`like-btn-${this.name}`);

      if (data.likes_this) {
        like_btn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-heart-fill" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
                    </svg>`;
        document.getElementById(`num-likes-${this.name}`).textContent =
          data.likes_count;
      } else {
        like_btn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-heart" viewBox="0 0 16 16">
        <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
    </svg>`;
        document.getElementById(`num-likes-${this.name}`).textContent =
          data.likes_count;
      }
    });
}

function follow_user() {
  fetch(`/follow/${this.name}`, {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      const follow_btn = document.querySelector("#follow-btn");

      if (data.is_following) {
        follow_btn.innerHTML =
          '<i class="bi bi-person-dash-fill"></i> Unfollow';
      } else {
        follow_btn.innerHTML = '<i class="bi bi-person-plus-fill"></i> Follow';
      }
      document.querySelector("#followers_count").textContent = data.followers;
    });
}

function edit_post() {
  // Create variables and elements to manipulate the edit function
  post_id = this.name;
  let current_text = document.querySelector(`#post-body-${post_id}`);
  let body_edit_box = document.querySelector(`#post-edit-${post_id}`);
  body_edit_box.style.display = "block";
  current_text.style.display = "none";

  //  Fetch Data
  fetch(`/edit/${post_id}`)
    .then((response) => response.json())
    .then((data) => {
      body_edit_box.innerHTML = `<textarea id="edit-text-${post_id}">${data.body}</textarea>
      <div  style="margin-left: auto;">
          <button type="submit" id="edit-cancel-${post_id}" class="btn btn-outline-secondary btn-sm">Cancel</button>
          <button type="submit" id="edit-save-${post_id}" class="btn btn-dark btn-sm" name="post-btn">Save</button>
      </div>`;
      current_text.style.display = "none";
      //  Add eventlistener to cancel button
      document
        .querySelector(`#edit-cancel-${post_id}`)
        .addEventListener("click", function () {
          body_edit_box.style.display = "none";
          current_text.style.display = "block";
        });
      // Add eventlistener to save button / save changes
      new_text = document.querySelector(`#edit-text-${post_id}`).value;
      document
        .querySelector(`#edit-save-${post_id}`)
        .addEventListener("click", function () {
          //
          fetch(`/edit/${post_id}`, {
            method: "POST",
            body: JSON.stringify({
              text: document.querySelector(`#edit-text-${post_id}`).value,
            }),
          })
            .then((response) => response.json())
            .then((data) => {
              body_edit_box.style.display = "none";
              current_text.style.display = "block";
              current_text.textContent = data.body;
            });
        });
    });
}
