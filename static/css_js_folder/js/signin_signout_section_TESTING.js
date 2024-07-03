"use strict";
// ! submitSigninForm
async function submitSigninForm() {
  let userInfo = JSON.parse(localStorage.getItem("userInfo"));
  if (!userInfo) {
    const form = document.getElementById("signin-form");
    const signinFormData = new FormData(form);
    let ifSuccessMessage = "Sign in successfully.";
    const jsonData = convertToJson(signinFormData);
    await tokenPut(jsonData);
    await tokenGet(ifSuccessMessage);
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
      await tokenGet(ifSuccessMessage);
      displayLoginMessage(ifSuccessMessage);
    } else {
      console.error("Error:", result.message);
      displayLoginMessage(result.message);
    }
  }
}

// ! tokenPut
async function tokenPut(inputJsonHere) {
  const response = await fetch("/api/user/auth", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(inputJsonHere),
    credentials: "include",
  });
  const result = await response.json();
  if (response.ok) {
    console.log("tokenPut() -> user sign-in, return encode.token");
  } else {
    console.error("Error:", result.message);
    displayLoginMessage(result.message);
  }
}

// !  tokenGet
async function tokenGet(successMessage) {
  const response = await fetch("/api/user/auth", {
    method: "GET",
    credentials: "include",
  });
  const result = await response.json();
  if (response.ok) {
    if (result["data"]) {
      console.log("tokenGet() -> user token checked, return user_info :", result);
      displayLoginMessage(successMessage);
      localStorage.setItem("userInfo", JSON.stringify(result.data));
    } else {
      console.log("tokenGet lunched, but there is no token from this user...");
      localStorage.removeItem("userInfo");
    }
  } else {
    console.error("Error:", result.message);
    displayLoginMessage(result.message);
    localStorage.removeItem("userInfo");
  }
  signinOutSwitch();
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
document.addEventListener("DOMContentLoaded", async function () {
  await tokenGet("");
  signinOutSwitch();
});
function signinOutSwitch() {
  let userInfo = JSON.parse(localStorage.getItem("userInfo"));
  let switchFormDiv = document.querySelectorAll(".switch-form");
  const login = document.getElementById("login-btn");
  const logout = document.getElementById("logout-btn");
  if (userInfo) {
    login.hidden = true;
    logout.hidden = false;
    logout.textContent = "登出系統";
    switchFormDiv.forEach((element) => {
      element.hidden = true;
    });
  } else {
    login.hidden = false;
    logout.hidden = true;
    login.textContent = "登入/註冊";
  }
}
// if user state wasn't correct
async function deleteUserInfo() {
  const response = await fetch("/api/user/logout", {
    method: "POST",
    credentials: "include",
  });
  if (response.ok) {
    localStorage.removeItem("userInfo");
    localStorage.removeItem("journeyRaw");
    localStorage.removeItem("journeyVerified");
    window.location.href = "/";
  } else {
    console.error("Failed to log out:", await response.json());
  }
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
  displaySignIn();
});
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