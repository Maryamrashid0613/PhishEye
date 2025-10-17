const API_URL = "http://127.0.0.1:5000/predict";

document.getElementById("scanBtn").addEventListener("click", async () => {
  const url = document.getElementById("urlInput").value;
  if (!url) return alert("Enter a URL first");

  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  });

  const data = await response.json();
  document.getElementById("result").textContent =
    `Verdict: ${data.verdict.toUpperCase()} (${(data.score * 100).toFixed(1)}%)`;
});
