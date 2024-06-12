"use strict";
// 嘗試讀取一次，如果沒有就返回首頁？
// fetch(`http://52.4.229.207:8000/api/attraction/${urlAttractionId}`).then(
// 奇怪的是，將fetch放在dom外面作，盡然比放在裡面慢？要多研究

const picDataAll = [];
document.addEventListener("DOMContentLoaded", async function () {
  let pathname = window.location.pathname;
  let pathSegments = pathname.split("/");
  let urlAttractionId = pathSegments[pathSegments.length - 1];
  let picDataAll = []; // 這邊不能用const，很蠢的初級問題，但是真的忘了還找不到錯在哪

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
      picDataAll = data["data"]["images"];
    }
  } catch (error) {
    console.error("Fetch error: ", error);
    window.location.href = "/";
  }
  backtoMain();

  let currentPic = 0;
  const leftBtn = document.getElementById("left-mrt-btn");
  const rightBtn = document.getElementById("right-mrt-btn");

  spotDisplay(picDataAll);

  leftBtn.addEventListener("click", function () {
    currentPic -= 1;
    picAndDisplay(currentPic, picDataAll);
  });
  rightBtn.addEventListener("click", function () {
    currentPic += 1;
    picAndDisplay(currentPic, picDataAll);
  });
});

function picAndDisplay(currentPic, picDataAll) {
  //處理variable傳遞的問題，最快的方式就是丟進()傳遞
  const theLength = picDataAll.length;
  console.log("theLength at 48: " + theLength);
  let theNum = 0;
  if (currentPic >= 0) {
    theNum = currentPic % theLength;
  } else {
    theNum = (currentPic % theLength) + theLength;
  }
  console.log("The Num:", theNum);
  let describePic = document.getElementById("pic-on-left");
  describePic.style.backgroundImage = `url(${picDataAll[theNum]})`;

  let boxElements = document.querySelectorAll(".choose-all-box");
  boxElements.forEach(function (boxElements) {
    boxElements.className = "box-1 choose-all-box";
  });
  document.getElementById(`dot-id-${theNum}`).className =
    "box-2 choose-all-box";
  //   只要在每次更新全部class name時，同時也附加上choose-all-box就可以解決全部取代，後面選不上的問題
}

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

function spotDisplay(picDataAll) {
  const lenAll = picDataAll.length;
  let indicator = document.getElementById("indicator");
  for (let n = 0; n < lenAll; n++) {
    indicator.innerHTML += `
    <div class="box-1 choose-all-box" id="dot-id-${n}"></div>
    `;
  }
  document.getElementById(`dot-id-0`).className = "box-2 choose-all-box";
  //   只要在每次更新全部class name時，同時也附加上choose-all-box就可以解決全部取代，後面選不上的問題
}
