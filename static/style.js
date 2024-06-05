const url = `http://52.4.229.207:8000/api/attractions?page=0`;

document.addEventListener("DOMContentLoaded", async function () {
  console.log("start fetching the first page, fetching start...");

  try {
    console.log("Fetching URL: ", url);

    let response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    console.log("Response status: ", response.status);
    console.log("Response ok: ", response.ok);

    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    let data = await response.json();
    console.log("Fetched data: ", data); // 添加调试信息
    console.log(data["data"][0]["name"]);
    // displayAttracItem(data["data"]);
  } catch (error) {
    console.error("Fetch error: ", error);
  }
  console.log("fetching the first page, fetching end...");
});

// function displayAttracItem(data) {
//   let attracDiv = document.getElementById("attracDiv");
//   attracDiv.innerHTML = `
//           <p>${data["name"]}(${data["username"]})</p>

//         <div class="title-1 background-image-container">
//           <div class="first-part">
//             <div class="attraction-pic" id="attraction-pic">
//               <img
//                 src="https://s3-alpha-sig.figma.com/img/cf92/70bb/362e0c2e64c0c59874238a0fcef074d9?Expires=1718582400&Key-Pair-Id=APKAQ4GOSFWCVNEHN3O4&Signature=SzuQSbIeR1oaCsrBc91Pv5WRtl3EOXoLI4Bw~LL8BT92ehkRV6~JY57Vbdx3RXH9AsQr9zgHZWI7-o1t3GIHxgf~3hO3tuPslH6wiLKqRXmV-k5YxjxceOBe~yp3sHX-JZHWpg2LT1lsRhpWaHKOk9Cn2XUkdK33FuBGLeZx3osRvItsMB-R~35y9n5sMk2gfSfyz7FWGFg9nVzOVSbcC0QtzSmKTDLoFh09LZ~p-Pa59GWnk9c9xR8GTNoCDlqu-viHwx4VUFNfKo6gc01hshz8WhIo7DIYu2fKegc7QLrZ34wIdRD-9Y7DI2n0UDBnCaLxV7PazlF1aToBnuPNrg__"
//                 alt="Attraction Image"
//                 class="attraction-pic-hidden"
//               />
//             </div>
//             <div class="attraction-name-div">
//               <div class="attraction-name">平安中</div>
//             </div>
//           </div>
//           <div class="third-part">
//             <div class="mrt-name">忠孝復興</div>
//             <div class="tag-name">公共藝術</div>
//           </div>
//         </div>
//       `;
// }

//   if (data["data"] === null) {
//     userInfoDiv.innerHTML = "<p>No Data.</p>";
//   } else {
//     userInfoDiv.innerHTML = `
//           <p>${data["name"]}(${data["username"]})</p>
//       `;
//   }
