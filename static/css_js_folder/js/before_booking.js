"use strict";
function stateCheckBeforeBooking() {
  const userInfo = localStorage.getItem("userInfo");
  if (userInfo) {
    window.location.href = "/booking";
  } else {
    bookingDisplaySignIn();
  }
}

async function bookingPost() {
  const token = localStorage.getItem("authToken");
  const dateInput = document.getElementById("date").value;
  const timeInput = document.querySelector('input[name="time"]:checked').value;
  const charge = timeInput === "morning" ? 2000 : 2500;
  let journeyForm = { attractionId: urlAttractionId, date: dateInput, time: timeInput, price: charge };

  const response = await fetch("/api/booking", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(journeyForm),
  });
  const result = await response.json();
  if (response.ok) {
    console.log("bookingPost() -> success:", result);
  } else {
    if (response.status === 403) {
      bookingDisplaySignIn();
    } else if (response.status === 400) {
      alert("Facing error booking this trip, please check the submission formate.");
    }
    console.log(result.message);
  }
}

function bookingDisplaySignIn() {
  const signinForm = document.getElementById("signin-form-div");
  const overlay = document.getElementById("overlay");
  signinForm.hidden = false;
  overlay.hidden = false;
}
