function googleLogin() {
  window.location.href = "https://raphaelfang.com/auth/login";
}

window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  const status = urlParams.get("status");
  const message = urlParams.get("message");

  if (status === "success") {
    alert("Login successful!");
  }
  if (status === "error") {
    alert("Login failed: " + message);
  }
};
