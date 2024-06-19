"use strict";
let nextPage = 0;
let nextKeyword = "";
document.addEventListener("DOMContentLoaded", async function () {
  try {
    let response = await fetch(
      `http://52.4.229.207:8000/api/attractions?page=0&keyword=`
    );
    console.log("Response status: ", response.status);
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    let data = await response.json();
    displayHtmlAttrac(data["data"]);
    nextPage = data["nextPage"];
  } catch (error) {
    console.error("Fetch error: ", error);
  }
  waitForDivLoaded();
  try {
    let response = await fetch("http://52.4.229.207:8000/api/mrts");
    console.log("Response status: ", response.status);
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    let data = await response.json();
    displayHtmlMrt(data["data"]);
  } catch (error) {
    console.error("Fetch error: ", error);
  }
  waitForMrtLoaded();

  // 建立一個觀察者， IntersectionObserver ，檢測有沒有rolling到特定的 div
  const observer = new IntersectionObserver(loadMore, {
    root: null,
    rootMargin: "0px",
    threshold: 0.2,
  });
  observer.observe(document.getElementById("load-more-trigger"));

  backtoMain();
});

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("search-btn").addEventListener("click", startSearch);
  document
    .getElementById("search-place")
    .addEventListener("keyup", function (event) {
      if (event.key === "Enter") {
        startSearch();
      }
    });
});

document.addEventListener("DOMContentLoaded", function () {
  const secondMrt = document.getElementById("second-mrt");
  const scrollAmount = 100;
  const leftBtn = document.getElementById("left-mrt-btn");
  const rightBtn = document.getElementById("right-mrt-btn");

  leftBtn.addEventListener("click", function () {
    secondMrt.scrollBy({
      left: -scrollAmount,
      behavior: "smooth",
    });
  });
  rightBtn.addEventListener("click", function () {
    secondMrt.scrollBy({
      left: scrollAmount,
      behavior: "smooth",
    });
  });
});

// 這設定跟先前等待 mrt 載入後才可以點及一樣的問題，一，監聽上一層的div，二，等待載入後再監聽
function waitForDivLoaded() {
  const attractionsContainer = document.getElementById("attracDiv");
  attractionsContainer.addEventListener("click", (event) => {
    const container = event.target.closest(".background-image-container");
    if (container) {
      const attractionId = container.getAttribute("data-id");
      // console.log("Container clicked, the id: " + attractionId);
      // sessionStorage.setItem("attractionId", attractionId);
      window.location.href = `/attraction/${attractionId}`;
      // 我原先是絕對路徑，只會導向api
    }
  });
}
//
function waitForMrtLoaded() {
  const mrtContainer = document.getElementById("second-mrt");
  // 這邊的設定太重要了，不能一次聽多個id，是違法的，只能聽多個class，或者是如現在的作法，一次聽這些同樣名稱class的上一個div
  mrtContainer.addEventListener("click", async function (event) {
    if (event.target.tagName === "A") {
      event.preventDefault();
      let newKeyword = event.target.dataset.keyword;
      document.getElementById("search-place").value = newKeyword;

      try {
        let response = await fetch(
          `http://52.4.229.207:8000/api/attractions?page=0&keyword=${newKeyword}`
        );
        console.log("Response status: ", response.status);
        if (!response.ok) {
          throw new Error("Network response was not ok " + response.statusText);
        }

        let data = await response.json();
        let attracDiv = document.getElementById("attracDiv");
        attracDiv.innerHTML = "";
        displayHtmlAttrac(data["data"]);
        nextKeyword = newKeyword;
        nextPage = data["nextPage"];
        const observer = new IntersectionObserver(loadMore, {
          root: null,
          rootMargin: "0px",
          threshold: 0.2,
        });
        observer.observe(document.getElementById("load-more-trigger"));
      } catch (error) {
        console.error("Fetch error: ", error);
      }
    }
  });
}

async function startSearch() {
  try {
    let searchedAttrac = document.getElementById("search-place").value;
    let response = await fetch(
      `http://52.4.229.207:8000/api/attractions?page=0&keyword=${searchedAttrac}`
    );
    console.log("Response status: ", response.status);
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }

    let data = await response.json();
    console.log("Keyword Fetched data: ", data["data"]);
    let attracDiv = document.getElementById("attracDiv");
    attracDiv.innerHTML = "";
    displayHtmlAttrac(data["data"]);
    nextKeyword = searchedAttrac;
    nextPage = data["nextPage"];
    const observer = new IntersectionObserver(loadMore, {
      root: null,
      rootMargin: "0px",
      threshold: 0.2,
    });
    observer.observe(document.getElementById("load-more-trigger"));
  } catch (error) {
    console.error("Fetch error: ", error);
  }
}

function displayHtmlAttrac(data) {
  let attracDiv = document.getElementById("attracDiv");
  for (let n = 0; n < data.length; n++) {
    attracDiv.innerHTML += `
      <div class="background-image-container" data-id="${data[n]["id"]}">
        <div class="first-part">
          <div class="attraction-pic" id="attraction-pic-${n}">
            <img
              src="${data[n]["images"][0]}"
              alt="Attraction Image"
              class="attraction-pic-hidden lazy"
            />
          </div>
          <div class="attraction-name-div">
            <div class="attraction-name">${data[n]["name"]}</div>
          </div>
        </div>
        <div class="third-part">
          <div class="mrt-name">${data[n]["mrt"]}</div>
          <div class="tag-name">${data[n]["category"]}</div>
        </div>
      </div>
    `;
  }
}
function displayHtmlMrt(data) {
  let mrtDiv = document.getElementById("second-mrt");
  for (let n = 0; n < data.length; n++) {
    mrtDiv.innerHTML += `
    <a href="#" class="mrt-item" id="mrt-keyword" data-keyword=${data[n]}>${data[n]}</a>
    `;
  }
}
async function addUpFetch(page) {
  const url = `http://52.4.229.207:8000/api/attractions?page=${page}&keyword=${nextKeyword}`;
  let response = await fetch(url);
  console.log("Response status: ", response.status);
  if (!response.ok) {
    throw new Error("Network response was not ok " + response.statusText);
  }
  let data = await response.json();
  displayHtmlAttrac(data["data"]);
  nextPage = data["nextPage"];
}

function loadMore(entries, observer) {
  entries.forEach(function (entry) {
    if (entry.isIntersecting) {
      observer.unobserve(entry.target); // 停止觀察當前元素
      console.log(nextPage);
      if (nextPage !== null) {
        addUpFetch(nextPage, nextKeyword).then(() => {
          observer.observe(document.getElementById("load-more-trigger")); // 重新啟動observer，觀察新元素
        });
      } else {
        let attracDiv = document.getElementById("attracDiv");
        attracDiv.innerHTML += `
        <div class="the-empty-block-for-script" data-id="the-empty-block-for-script"></div>
        <div class="the-empty-block-for-script" data-id="the-empty-block-for-script"></div>
        <div class="the-empty-block-for-script" data-id="the-empty-block-for-script"></div>
        `;
      }
    }
  });
}

async function backtoMain() {
  let titleElement = document.getElementById("title");
  titleElement.addEventListener("click", function () {
    window.location.href = "/";
  });
}

// ! New week start
// ! New week start
// ! submitSigninForm
async function submitSigninForm() {
  const form = document.getElementById("signin-form");
  const signinFormData = new FormData(form);
  let ifSuccessMessage = "Sign in successfully.";
  let ifErrorMessage =
    "Invalid user info, please make sure the email and password are correct.";
  await getToken(signinFormData);
  await tokenCheck(ifSuccessMessage, ifErrorMessage);
}

// ! submitSignUpForm
async function submitSignUpForm() {
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
    let ifSuccessMessage = "Sign up successfully and automatically sign in.";
    let ifErrorMessage =
      "Invalid registration, duplicate email or other reasons";
    await getToken(signupFormData);
    await tokenCheck(ifSuccessMessage, ifErrorMessage);
  } else {
    console.error("Error:", result.message);
    displayLoginMessage(result.message);
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
      console.log(
        "tokenCheck() -> check user token, return user_info :",
        result
      );
      localStorage.setItem("userInfo", result["data"]);
      displayLoginMessage(successMessage);
    } else {
      console.error("Error:", result.message);
      localStorage.setItem("userInfo", result["data"]);
      displayLoginMessage(errorMessage);
    }
    const event = new Event("userStatusChange");
    document.dispatchEvent(event);
  } else {
    console.error("Error:", result.message);
    displayLoginMessage(result.message);
  }
}
// ! displayLoginMessage
function displayLoginMessage(message) {
  let errorCatchers = document.querySelectorAll(".error-catcher");
  errorCatchers.forEach((element) => {
    element.textContent = message;
  });
}

// ! login / logout
document.addEventListener("userStatusChange", async function () {
  signinOutSwitch();
});

function signinOutSwitch() {
  let userInfo = localStorage.getItem("userInfo");
  console.log(userInfo);
  const secondBtn = document.getElementById("secondbtn");
  if (userInfo) {
    secondBtn.innerHTML = `
          <a class="second-bar-btn" id="switch-btn" onclick="signout()">登出系統</a>
      `;
  } else {
    secondBtn.innerHTML = `
          <a class="second-bar-btn" id="switch-btn">登入/註冊</a>
      `;
  }
}

function signout() {
  if (
    confirm("You're about to sign out from this page, do you want to sign out?")
  ) {
    localStorage.removeItem("userInfo");
    localStorage.removeItem("authToken");
    const event = new Event("userStatusChange");
    document.dispatchEvent(event);
    window.location.href = "/";
  } else {
    console.log("signout() denied -> token and user_info remained");
  }
}

function signUpInSwitch() {
  const signinForm = document.getElementById("signin-form-div");
  const signupForm = document.getElementById("signup-form-div");
  if (signupForm.hidden) {
    console.log("signinForm set hidden");
    signupForm.hidden = false;
    signinForm.hidden = true;
    displayLoginMessage("");
  } else {
    console.log("signupForm set hidden");
    signupForm.hidden = true;
    signinForm.hidden = false;
    displayLoginMessage("");
  }
}
// switch-btn
document.addEventListener("DOMContentLoaded", function () {
  displaySignIn();
});
function displaySignIn() {
  const loginBtn = document.getElementById("switch-btn");
  const signinForm = document.getElementById("signin-form-div");
  loginBtn.addEventListener("click", async function () {
    signinForm.hidden = false;
  });
}
