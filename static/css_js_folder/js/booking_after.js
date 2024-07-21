"use strict";
document.addEventListener("DOMContentLoaded", async function () {
  const bookingInfo = document.getElementById("detect-display");
  const firstBookingInfo = document.getElementById("first-block");
  const nullP = document.getElementById("prevent-null-p");
  const nullDiv = document.getElementById("prevent-null");
  const footer = document.getElementById("footer");

  const startRender = await bookingGet();
  if (startRender) {
    bookingInfo.hidden = false;
    firstBookingInfo.hidden = false;
    await renderUserName();
    await renderJourneyVerified();
  } else {
    await renderUserName();
    nullDiv.hidden = false;
    nullP.textContent = `目前沒有任何待預訂的行程`;
  }
  await footerCreator(startRender);
});

// render UserName to page
async function renderUserName() {
  const userInfo = JSON.parse(localStorage.getItem("userInfo"));
  const welcomeParagraph = document.getElementById("wel-booking-p");
  welcomeParagraph.textContent = `您好，${userInfo.name}，待預訂的行程如下：`;
}

// render Journey to page, only if it pass the token check inside the bookingGet()
async function renderJourneyVerified() {
  const verData = JSON.parse(localStorage.getItem("journeyVerified"));
  const bookInfoDiv = document.getElementById("book-info-div");
  bookInfoDiv.innerHTML = `
    <p class="book-info-title">台北一日遊：${verData.attraction.name}</p>
    <p class="book-info-text"><span class="custom-bold">日期：</span>${verData.date}</p>
    <p class="book-info-text" id='morning-or-evening'><span class="custom-bold">時間：</span>${verData.time}</p>
    <p class="book-info-text"><span class="custom-bold">費用：</span>新台幣${verData.price}元</p>
    <p class="book-info-text"><span class="custom-bold">地點：</span>${verData.attraction.address}</p>
  `;
  const bookInfoPic = document.getElementById("book-info-div-pic");
  bookInfoPic.innerHTML = `
  <img src="${verData.attraction.image}"  alt="Booking Image" class="booking-pic" />`;

  const finalPrice = document.getElementById("finalPrice");
  finalPrice.textContent = `總價：新台幣 ${verData.price} 元`;
}

// ! bookingGet()
async function bookingGet() {
  const response = await fetch("/tdt/v1/api/booking", {
    method: "GET",
    credentials: "include",
  });
  const result = await response.json();
  if (response.ok) {
    localStorage.setItem("journeyVerified", JSON.stringify(result.data));
    if (result.data !== null) {
      return true;
    } else {
      return false;
    }
  } else {
    console.log(result.message);
    window.location.href = "/tdt/v1/";
    return false;
  }
}
// create footer
async function footerCreator(typeState) {
  const footer1 = document.getElementById("type-1-footer");
  const footer2 = document.getElementById("type-2-footer");
  if (typeState) {
    footer2.innerHTML = `  
    <footer hidden class="foot foot-v2" id="footer-v2">
      <p class="foot-p">COPYRIGHT © 2024 Taipei-Day-Trip</p>
    </footer>`;
  } else {
    footer1.innerHTML = `
    <footer class="foot" id="foot">
      <p class="foot-p">COPYRIGHT © 2024 Taipei-Day-Trip</p>
    </footer>
    `;
  }
}

// ! deleteCurrentData
async function bookingDelete() {
  const response = await fetch("/tdt/v1/api/booking", {
    method: "DELETE",
    credentials: "include",
  });
  const result = await response.json();
  if (response.ok) {
    console.log(result);
    window.location.href = "/tdt/v1/booking";
  } else {
    console.log(result.message);
    alert("Cannot delete current journey, please retry");
  }
}
