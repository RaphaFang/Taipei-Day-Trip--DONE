"use strict";
document.addEventListener("DOMContentLoaded", async function () {
  const attractionId = sessionStorage.getItem("attractionId");
  console.log(attractionId);
  try {
    let response = await fetch(
      `http://52.4.229.207:8000/api/attraction/${attractionId}`
    );
    console.log("Response status: ", response.status);
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    let data = await response.json();
    console.log(data["data"]);
    displayDescribe(data["data"]);
  } catch (error) {
    console.error("Fetch error: ", error);
  }
  backtoMain();
});

// 左右點及
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

//!  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
function displayDescribe(data) {
  let describeBlock = document.getElementById("describe-block");
  describeBlock.innerHTML += `
    <div class="the-discribe-text">${data["description"]}</div>
    <div class="location-title">景點地址：</div>
    <div class="location">${data["address"]}</div>
    <div class="transport-title">交通方式：</div>
    <div class="transport-text">${data["transport"]}</div>
    `;

  let describePic = document.getElementById("pic-on-left");
  describePic.style.backgroundImage = `url(${data["images"][0]})`;

  let describeTitle = document.getElementById("title-of-attrac");
  describeTitle.innerHTML = data["name"];
  let describeTag = document.getElementById("tag-mrt-of-attrac");
  describeTag.innerHTML = `${data["category"]} at ${data["mrt"]}`;
}
function backtoMain() {
  let titleElement = document.getElementById("title");
  titleElement.addEventListener("click", function () {
    window.location.href = "/";
  });
}

function displayHtmlMrt(data) {
  let mrtDiv = document.getElementById("second-mrt");
  for (let n = 0; n < data.length; n++) {
    mrtDiv.innerHTML += `
    <a href="#" class="mrt-item" id="mrt-keyword" data-keyword=${data[n]}>${data[n]}</a>
    `;
  }
}
