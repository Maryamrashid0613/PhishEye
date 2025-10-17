chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "loading" && tab.url.startsWith("http")) {
    console.log("[PhishEye] Checking URL:", tab.url);

    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: tab.url })
    })
      .then(res => res.json())
      .then(data => {
        console.log("[PhishEye] Prediction result:", data);

        if (data.verdict === "phishing") {
          chrome.tabs.update(tabId, { url: "warning.html?url=" + encodeURIComponent(tab.url) });
        }
      })
      .catch(err => console.error("[PhishEye] Error contacting backend:", err));
  }
});
