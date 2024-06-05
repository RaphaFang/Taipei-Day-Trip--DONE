try {
  const url = `http://52.4.229.207:8000/api/attractions?page=0`;
  console.log("Fetching URL: ", url);

  let response = fetch(url, {
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
