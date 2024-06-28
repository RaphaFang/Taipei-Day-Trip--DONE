"use strict";
// ! submitSigninForm
async function submitSigninForm() {
  let userInfo = JSON.parse(localStorage.getItem("userInfo"));
  if (!userInfo) {
    const form = document.getElementById("signin-form");
    const signinFormData = new FormData(form);
    let ifSuccessMessage = "Sign in successfully.";
    let ifErrorMessage = "Invalid user info, please make sure the email and password are correct.";
    const jsonData = convertToJson(signinFormData);
    await getToken(jsonData);
    await tokenCheck(ifSuccessMessage, ifErrorMessage);
  }
}

// ! submitSignUpForm
async function submitSignUpForm() {
  let userInfo = JSON.parse(localStorage.getItem("userInfo"));
  if (!userInfo) {
    const form = document.getElementById("signup-form");
    const signupFormData = new FormData(form);
    const jsonData = convertToJson(signupFormData);
    const response = await fetch("/api/user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(jsonData),
    });
    const result = await response.json();
    if (response.ok) {
      console.log("submitSignUpForm() -> user sign-up : ", response);
      let ifSuccessMessage = "Sign up successfully, automatically sign-in.";
      let ifErrorMessage = "Invalid registration, duplicate email or other reasons";
      await getToken({ email: jsonData.email, password: jsonData.password });
      await tokenCheck(ifSuccessMessage, ifErrorMessage);
    } else {
      console.error("Error:", result.message);
      displayLoginMessage(result.message);
    }
  }
}

// ! get token
async function getToken(inputJsonHere) {
  const response = await fetch("/api/user/auth", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(inputJsonHere),
  });
  const result = await response.json();
  if (response.ok) {
    const token = result.access_token;
    localStorage.setItem("authToken", token);
    console.log("getToken() -> user sign-in, return encode.token: ", token);
  } else {
    console.error("Error:", result.message);
    displayLoginMessage(result.message);
  }
}
// !  tokenCheck
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
// convertToJson(), convert form data to json
function convertToJson(formDataInput) {
  const jsonData = {};
  formDataInput.forEach((value, key) => {
    jsonData[key] = value;
  });
  return jsonData;
}
//  displayLoginMessage(), display the correct or error below the form section
function displayLoginMessage(message) {
  let errorCatchers = document.querySelectorAll(".error-catcher");
  errorCatchers.forEach((element) => {
    element.hidden = false;
    element.textContent = message;
  });
}
// signinOutSwitch(), switch the btn at the up-right corner, and hide the signUpInSwitch()
// right after user login or sign-up,
document.addEventListener("userPassTokenCheck", function () {
  signinOutSwitch();
});
// fetch the user_Api to check token, right after enter any page(e.g. attraction page)
document.addEventListener("DOMContentLoaded", async function () {
  signinOutSwitch();
  await tokenCheck("", ""); // lunch 'userPassTokenCheck' event inside the func.
});
// for future user token check
// document.addEventListener("requireAuthEvent", async function () {
//   await tokenCheck("", "");
// });
function signinOutSwitch() {
  let userInfo = JSON.parse(localStorage.getItem("userInfo"));
  let switchFormDiv = document.querySelectorAll(".switch-form");
  const login = document.getElementById("login-btn");
  const logout = document.getElementById("logout-btn");

  if (userInfo) {
    login.hidden = true;
    logout.hidden = false;
    switchFormDiv.forEach((element) => {
      element.hidden = true;
    });
  } else {
    login.hidden = false;
    logout.hidden = true;
  }
}
// if user state wasn't correct
function deleteUserInfo() {
  localStorage.removeItem("userInfo");
  localStorage.removeItem("authToken");
  localStorage.removeItem("journeyRaw");
  localStorage.removeItem("journeyVerified");

  window.location.href = "/";
}
// userSignOut(), delete all the user info, refresh the page
function userSignOut() {
  if (confirm("You're about to sign out from this page, do you want to sign out?")) {
    deleteUserInfo();
  } else {
    console.log("userSignOut() denied -> token and user_info remained");
  }
}
// signUpInSwitch(), switch the form to display
function signUpInSwitch() {
  const signinForm = document.getElementById("signin-form-div");
  const signupForm = document.getElementById("signup-form-div");
  if (signupForm.hidden) {
    console.log("signinForm set hidden");
    signupForm.hidden = false;
    signinForm.hidden = true;
    hideErrorCatcher();
  } else {
    console.log("signupForm set hidden");
    signupForm.hidden = true;
    signinForm.hidden = false;
    hideErrorCatcher();
  }
}
// displaySignIn() login btn trigger, display sign in form
document.addEventListener("DOMContentLoaded", function () {
  function displaySignIn() {
    const loginBtn = document.getElementById("login-btn");
    const signinForm = document.getElementById("signin-form-div");
    const overlay = document.getElementById("overlay");
    if (loginBtn) {
      loginBtn.addEventListener("click", async function () {
        signinForm.hidden = false;
        overlay.hidden = false;
      });
    }
  }
  displaySignIn();
});

// cancelFormDisplay() close the form and reset the 'error-catcher' to empty
function cancelFormDisplay() {
  const signinForm = document.getElementById("signin-form-div");
  const signupForm = document.getElementById("signup-form-div");
  const overlay = document.getElementById("overlay");
  signupForm.hidden = true;
  signinForm.hidden = true;
  overlay.hidden = true;
  hideErrorCatcher();
}
function hideErrorCatcher() {
  const errorCatchers = document.querySelectorAll(".error-catcher");
  errorCatchers.forEach((element) => {
    element.hidden = true;
  });
}
