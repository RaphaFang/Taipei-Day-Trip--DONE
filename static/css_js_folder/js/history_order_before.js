"use strict";
function redirectBookingHistory() {
  const orderBtn = document.getElementById("bookingGetAll");
  const userInfo = localStorage.getItem("userInfo");
  if (userInfo) {
    window.location.href = "/history_orders";
  } else {
    bookingDisplaySignIn();
  }
}
