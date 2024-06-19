"use strict";
// ! submitSigninForm
async function submitSigninForm() {
  let userInfo = JSON.parse(localStorage.getItem("userInfo"));
  if (!userInfo) {
    const form = document.getElementById("signin-form");
    const signinFormData = new FormData(form);
    let ifSuccessMessage = "Sign in successfully.";
    let ifErrorMessage = "Invalid user info, please make sure the email and password are correct.";
    await getToken(signinFormData);
    await tokenCheck(ifSuccessMessage, ifErrorMessage);
  }
}

// ! submitSignUpForm
async function submitSignUpForm() {
  let userInfo = JSON.parse(localStorage.getItem("userInfo"));
  if (!userInfo) {
    const form = document.getElementById("signup-form");
    const signupFormData = new FormData(form);
    const response = await fetch("/api/user", {
      method: "POST",
      body: signupFormData,
    });
    const result = await response.json();
    if (response.ok) {
      console.log("submitSignUpForm() -> user sign-up : ", response);
      signupFormData.delete("name");
      let ifSuccessMessage = "Sign up successfully, automatically sign-in.";
      let ifErrorMessage = "Invalid registration, duplicate email or other reasons";
      await getToken(signupFormData);
      await tokenCheck(ifSuccessMessage, ifErrorMessage);
    } else {
      console.error("Error:", result.message);
      displayLoginMessage(result.message);
    }
  }
}

// ! get token
async function getToken(formDataInput) {
  const response = await fetch("/api/user/auth", {
    method: "PUT",
    body: formDataInput,
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
      console.log("tokenCheck() -> check user token, return user_info :", result);
      localStorage.setItem("userInfo", JSON.stringify(result.data));
      displayLoginMessage(successMessage);
    } else {
      console.error("Error:", result.message);
      localStorage.setItem("userInfo", JSON.stringify(result.data));
      displayLoginMessage(errorMessage);
    }
    const event = new Event("userStatusChange");
    document.dispatchEvent(event);
  } else {
    console.error("Error:", result.message);
    displayLoginMessage(result.message);
  }
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
document.addEventListener("DOMContentLoaded", function () {
  signinOutSwitch();
});
document.addEventListener("userStatusChange", function () {
  signinOutSwitch();
});
function signinOutSwitch() {
  let userInfo = JSON.parse(localStorage.getItem("userInfo"));
  let switchFormDiv = document.querySelectorAll(".switch-form");
  const secondBtn = document.getElementById("secondbtn");
  if (userInfo) {
    secondBtn.innerHTML = `
            <a class="second-bar-btn" id="switch-btn" onclick="userSignOut()">登出系統</a>
        `;
    switchFormDiv.forEach((element) => {
      element.hidden = true;
    });
  } else {
    secondBtn.innerHTML = `
            <a class="second-bar-btn" id="switch-btn">登入/註冊</a>
        `;
  }
}

// userSignOut(), delete all the user info, refresh the page
function userSignOut() {
  if (confirm("You're about to sign out from this page, do you want to sign out?")) {
    localStorage.removeItem("userInfo");
    localStorage.removeItem("authToken");
    const event = new Event("userStatusChange");
    document.dispatchEvent(event);
    window.location.href = "/";
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
  const loginBtn = document.getElementById("switch-btn");
  const signinForm = document.getElementById("signin-form-div");
  const overlay = document.getElementById("overlay");

  loginBtn.addEventListener("click", async function () {
    signinForm.hidden = false;
    overlay.hidden = false;
  });
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
