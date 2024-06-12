"use strict";

// 嘗試讀取一次，如果沒有就返回首頁？
// fetch(`http://52.4.229.207:8000/api/attraction/${urlAttractionId}`).then(
// 奇怪的是，將fetch放在dom外面作，盡然比放在裡面慢？要多研究

document.addEventListener("DOMContentLoaded", async function () {
  let pathname = window.location.pathname;
  let pathSegments = pathname.split("/");
  let urlAttractionId = pathSegments[pathSegments.length - 1];

  try {
    let response = await fetch(
      `http://52.4.229.207:8000/api/attraction/${urlAttractionId}`
    );
    if (!response.ok) {
      window.location.href = "/";
    } else {
      //   document.getElementById("content").style.display = "block";
      let data = await response.json();
      console.log(data["data"]);
      displayDescribe(data["data"]);
    }
  } catch (error) {
    console.error("Fetch error: ", error);
    window.location.href = "/";
  }
  backtoMain();
});
document.addEventListener("DOMContentLoaded", function () {
  const morningRadio = document.getElementById("morning");
  const afternoonRadio = document.getElementById("afternoon");
  const chargeP = document.getElementById("charge-p");

  morningRadio.addEventListener("change", function () {
    if (morningRadio.checked) {
      chargeP.textContent = "新台幣 2000 元";
      morningRadio.checked = true;
      afternoonRadio.checked = false;
    }
  });
  afternoonRadio.addEventListener("change", function () {
    if (afternoonRadio.checked) {
      chargeP.textContent = "新台幣 2500 元";
      morningRadio.checked = false;
      afternoonRadio.checked = true;
    }
  });
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
function spotDisplay() {
  for (let n = 0; n < data["images"].length; n++) {
    mrtDiv.innerHTML += `
        <a href="#" class="mrt-item" id="mrt-keyword" data-keyword=${data[n]}>${data[n]}</a>
        `;
  }
  data["images"];
}
// function callandDisplay() {
//   let leftPicDiv = document.getElementById("pic-on-left");
//   for (let n = 0; n < data.length; n++) {
//     mrtDiv.innerHTML += `
//     <a href="#" class="mrt-item" id="mrt-keyword" data-keyword=${data[n]}>${data[n]}</a>
//     `;
//   }
//   data["images"];

//   //   讀數列的數字，在回教pic
// }
