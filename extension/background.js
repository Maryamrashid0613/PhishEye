chrome.runtime.onInstalled.addListener(() => {
  console.log("PhishEye Background Loaded");
});

async function checkURL(url) {
  try {
    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    });
    return await res.json();
  } catch {
    return null;
  }
}

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url.startsWith("http")) {
    checkURL(tab.url).then(result => {
      if (result && result.verdict === "phishing") {
        chrome.tabs.sendMessage(tabId, { action: "warnUser", data: result });

        chrome.notifications.create({
          type: "basic",
          iconUrl: "icon.png",
          title: "⚠️ Phishing Warning",
          message: "This site may be dangerous!"
        });
      }
    });
  }
});
