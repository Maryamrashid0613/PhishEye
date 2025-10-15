document.getElementById("checkBtn").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    const url = tabs[0].url;
    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });
    const data = await res.json();
    document.getElementById("result").innerText =
      `Verdict: ${data.verdict.toUpperCase()} (Score: ${data.score})`;
  });
});
