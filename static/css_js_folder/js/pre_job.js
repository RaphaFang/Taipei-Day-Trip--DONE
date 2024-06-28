"use strict";
// backtoMain
document.addEventListener("DOMContentLoaded", async function () {
  backtoMain();
});
function backtoMain() {
  let titleElement = document.getElementById("title");
  titleElement.addEventListener("click", function () {
    window.location.href = "/";
  });
}

// document.addEventListener("DOMContentLoaded", async function () {
//   signinOutSwitch();
// });

// function signinOutSwitch() {
//   let userInfo = JSON.parse(localStorage.getItem("userInfo"));
//   let switchFormDiv = document.querySelectorAll(".switch-form");
//   const secondBtn = document.getElementById("secondbtn");
//   if (userInfo) {
//     secondBtn.innerHTML = `
//           <a class="second-bar-btn" id="switch-btn" onclick="userSignOut()">登出系統</a>
//       `;
//     switchFormDiv.forEach((element) => {
//       element.hidden = true;
//     });
//   } else {
//     secondBtn.innerHTML = `
//           <a class="second-bar-btn" id="switch-btn">登入/註冊</a>
//       `;
//   }
// }
