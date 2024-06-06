"use strict";
let nextPage = 0;
let nextKeyword = "";
document.addEventListener("DOMContentLoaded", async function () {
  console.log(">>>>>>>> Attractions, fetching start...");
  try {
    let response = await fetch(
      `http://52.4.229.207:8000/api/attractions?page=0&keyword=`
    );
    console.log("Response status: ", response.status);
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    let data = await response.json();
    console.log("Fetched data: ", data["data"]);
    displayHtmlAttrac(data["data"]);
    nextPage = data["nextPage"];
    console.log(nextPage);
  } catch (error) {
    console.error("Fetch error: ", error);
  }

  console.log(">>>>>>>> Mrts, fetching start...");
  try {
    let response = await fetch("http://52.4.229.207:8000/api/mrts");
    console.log("Response status: ", response.status);
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    let data = await response.json();
    console.log("Fetched data: ", data["data"]);
    displayHtmlMrt(data["data"]);
    console.log(nextPage);
  } catch (error) {
    console.error("Fetch error: ", error);
  }
  console.log(">>>>>>>> first loading fetching end...");
  waitForMrtLoaded();

  // 建立一個觀察者， IntersectionObserver ，檢測有沒有rolling到特定的 div
  const observer = new IntersectionObserver(loadMore, {
    root: null, // 視窗
    rootMargin: "0px",
    threshold: 0.2, // 完全可見時觸發，調用下方的 addUpFetch()
  });
  observer.observe(document.getElementById("load-more-trigger")); // 開始觀察
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
        console.log("Keyword Fetched data: ", data["data"]);
        let attracDiv = document.getElementById("attracDiv");
        attracDiv.innerHTML = "";
        displayHtmlAttrac(data["data"]);

        nextKeyword = newKeyword;
        nextPage = data["nextPage"];

        console.log(nextKeyword);
        console.log(nextPage);

        const observer = new IntersectionObserver(loadMore, {
          root: null,
          rootMargin: "0px",
          threshold: 0.2, // 完全可見時觸發，調用下方的 addUpFetch()
        });
        observer.observe(document.getElementById("load-more-trigger")); // 開始觀察
      } catch (error) {
        console.error("Fetch error: ", error);
      }
    }
  });
}

async function startSearch() {
  try {
    let searchedAttrac = document.getElementById("search-place").value;
    console.log(searchedAttrac);
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
    console.log(nextKeyword);
    console.log(nextPage);

    const observer = new IntersectionObserver(loadMore, {
      root: null,
      rootMargin: "0px",
      threshold: 0.2, // 完全可見時觸發，調用下方的 addUpFetch()
    });
    observer.observe(document.getElementById("load-more-trigger")); // 開始觀察
  } catch (error) {
    console.error("Fetch error: ", error);
  }
}

function displayHtmlAttrac(data) {
  let attracDiv = document.getElementById("attracDiv");
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
function displayHtmlMrt(data) {
  let mrtDiv = document.getElementById("second-mrt");
  // mrtDiv.innerHTML = "";
  for (let n = 0; n < data.length; n++) {
    mrtDiv.innerHTML += `
    <a href="#" class="mrt-item" id="mrt-keyword" data-keyword=${data[n]}>${data[n]}</a>
    `;
  }
}
async function addUpFetch(page) {
  console.log();
  const url = `http://52.4.229.207:8000/api/attractions?page=${page}&keyword=${nextKeyword}`;
  let response = await fetch(url);
  console.log("Response status: ", response.status);
  if (!response.ok) {
    throw new Error("Network response was not ok " + response.statusText);
  }
  let data = await response.json();
  console.log("Fetched data: ", data["data"]);
  displayHtmlAttrac(data["data"]);
  nextPage = data["nextPage"];
  console.log(nextPage);
}

function loadMore(entries, observer) {
  entries.forEach(function (entry) {
    if (entry.isIntersecting) {
      observer.unobserve(entry.target); // 停止觀察當前元素
      console.log("nextPage at loadMore() :" + nextPage);
      console.log("nextKeyword at loadMore() :" + nextKeyword);
      if (nextPage !== null) {
        addUpFetch(nextPage, nextKeyword).then(() => {
          observer.observe(document.getElementById("load-more-trigger")); // 重新啟動observer，觀察新元素
        });
      }
    }
  });
}
