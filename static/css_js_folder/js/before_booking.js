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
  const attrName = document.getElementById("title-of-attrac").innerText;
  const locId = document.getElementById("location-id").innerText;
  const dateInput = document.getElementById("date").value;
  const timeInput = document.querySelector('input[name="time"]:checked').value;
  const charge = timeInput === "morning" ? 2000 : 2500;
  let journeyForm = {
    attractionId: urlAttractionId,
    name: attrName,
    address: locId,
    image: picDataAll[0].toString(),
    date: dateInput,
    time: timeInput,
    price: charge,
  };
  console.log(journeyForm);

  // const response = await fetch("/api/booking", {
  //   method: "POST",
  //   headers: {
  //     "Content-Type": "application/json",
  //   },
  //   credentials: "include",
  //   body: JSON.stringify(journeyForm),
  // });
  // const result = await response.json();
  // if (response.ok) {
  //   console.log("bookingPost() -> success:", result);
  // } else {
  //   if (response.status === 403) {
  //     bookingDisplaySignIn();
  //   } else if (response.status === 400) {
  //     alert("Facing error booking this trip, please check the submission formate.");
  //   }
  //   console.log(result.message);
  // }
  // //
  const response2 = await fetch("/api/booking", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify(journeyForm),
  });
  const result2 = await response2.json();
  if (response2.ok) {
    console.log("bookingPost() -> success:", result2);
  } else {
    if (response2.status === 403) {
      bookingDisplaySignIn();
    } else if (response2.status === 400) {
      alert("Facing error booking this trip, please check the submission formate.");
    }
    console.log(result2.message);
  }
}

function bookingDisplaySignIn() {
  const signinForm = document.getElementById("signin-form-div");
  const overlay = document.getElementById("overlay");
  signinForm.hidden = false;
  overlay.hidden = false;
}

// async function bookingPost() {
//   const dateInput = document.getElementById("date").value;
//   const timeInput = document.querySelector('input[name="time"]:checked').value;
//   const charge = timeInput === "morning" ? 2000 : 2500;
//   let journeyForm = { attractionId: urlAttractionId, date: dateInput, time: timeInput, price: charge };

//   console.log(journeyForm);
//   const response = await fetch("/api/booking", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify(journeyForm),
//   });
//   const result = await response.json();
//   if (response.ok) {
//     console.log("bookingPost() -> success:", result);
//   } else {
//     if (response.status === 403) {
//       bookingDisplaySignIn();
//     } else if (response.status === 400) {
//       alert("Facing error booking this trip, please check the submission formate.");
//     }
//     console.log(result.message);
//   }
// }
