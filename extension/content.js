chrome.runtime.onMessage.addListener((msg) => {
  if (msg.action === "warnUser") {
    const banner = document.createElement("div");
    banner.style.position = "fixed";
    banner.style.top = "0";
    banner.style.left = "0";
    banner.style.width = "100%";
    banner.style.background = "red";
    banner.style.color = "white";
    banner.style.padding = "15px";
    banner.style.textAlign = "center";
    banner.style.zIndex = "10000";
    banner.innerText = `⚠️ WARNING: This site may be a phishing attempt! (${msg.data.url})`;

    document.body.prepend(banner);

    if (!confirm("WARNING: This site is unsafe. Do you still want to continue?")) {
      window.location.href = "about:blank";
    }
  }
});
