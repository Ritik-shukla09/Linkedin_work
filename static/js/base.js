document.addEventListener("DOMContentLoaded", () => {
  document.body.classList.add("page-loaded");
});



document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("themeToggle");
  if (!toggleBtn) return;

  const body = document.body;

  // Apply saved theme
  if (localStorage.getItem("theme") === "dark") {
    body.classList.add("dark-mode");
    toggleBtn.textContent = "☀️";
  }

  toggleBtn.addEventListener("click", () => {
    body.classList.toggle("dark-mode");
  


    if (body.classList.contains("dark-mode")) {
      localStorage.setItem("theme", "dark");
      toggleBtn.textContent = "☀️";
    } else {
      localStorage.setItem("theme", "light");
      toggleBtn.textContent = "🌙";
    }
  });
});



function confirmDelete() {
  return confirm(
    "⚠️ Are you sure you want to delete your account?\n\nThis action cannot be undone."
  );
}

function confirmDelete(button) {
  const ok = confirm("Are you sure you want to delete this job?");
  if (ok) {
    button.closest("form").submit();
  }
}
