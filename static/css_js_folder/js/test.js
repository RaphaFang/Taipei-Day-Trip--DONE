async function tokenCheck(successMessage, errorMessage) {
  const token = localStorage.getItem("authToken");
  if (!token) {
    console.error("tokenCheck() -> auth token no found");
    return;
  }
  const response = await fetch("/api/user/auth", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const result = await response.json();
  if (response.ok) {
    if (result["data"]) {
      console.log("tokenCheck() -> user token checked, return user_info :", result);
      displayLoginMessage(successMessage);
    } else {
      console.error("Error (user_info might be null):", result.message);
      displayLoginMessage(errorMessage);
    }
    localStorage.setItem("userInfo", JSON.stringify(result.data));
  } else {
    console.error("Error:", result.message);
    displayLoginMessage(result.message);
  }
  const event = new Event("userPassTokenCheck");
  document.dispatchEvent(event);
}
