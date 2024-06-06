"use strict";
let nextPage = 0;
document.addEventListener("DOMContentLoaded", async function () {
  console.log(">>>>>>>> fetching start...");

  try {
    const url = `http://52.4.229.207:8000/api/attractions?page=0`;
    let response = await fetch(url);
    console.log("Response status: ", response.status);
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    let data = await response.json();
    console.log("Fetched data: ", data["data"]);
    displayHtml(data["data"]);
    nextPage = data["nextPage"];
    console.log(nextPage);

    // 建立一個觀察者， IntersectionObserver ，檢測有沒有拱動到特定的 div
    const observer = new IntersectionObserver(loadMore, {
      root: null, // 視窗
      rootMargin: "0px",
      threshold: 1.0, // 完全可見時觸發，調用下方的 addUpFetch()
    });
    observer.observe(document.getElementById("load-more-trigger")); // 開始觀察
  } catch (error) {
    console.error("Fetch error: ", error);
  }
  console.log(">>>>>>>> fetching end...");
});

function displayHtml(data) {
  let attracDiv = document.getElementById("attracDiv");
  // attracDiv.innerHTML = "";
  for (let n = 0; n < data.length; n++) {
    // console.log(`Adding item ${n}: `, data[n]["images"][0]);
    attracDiv.innerHTML += `
      <div class="background-image-container">
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

async function addUpFetch(page) {
  const url = `http://52.4.229.207:8000/api/attractions?page=${page}`;
  let response = await fetch(url);
  console.log("Response status: ", response.status);
  if (!response.ok) {
    throw new Error("Network response was not ok " + response.statusText);
  }
  let data = await response.json();
  console.log("Fetched data: ", data["data"]);
  displayHtml(data["data"]);
  nextPage = data["nextPage"];
  console.log(nextPage);
}

function loadMore(entries, observer) {
  entries.forEach(function (entry) {
    if (entry.isIntersecting) {
      observer.unobserve(entry.target); // 停止觀察當前元素
      addUpFetch(nextPage).then(() => {
        if (nextPage !== null) {
          observer.observe(document.getElementById("load-more-trigger")); // 重新啟動observer，觀察新元素
        }
      });
    }
  });
}
