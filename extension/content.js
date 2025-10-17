chrome.runtime.onMessage.addListener((message) => {
  if (message.action === "show_warning") {
    if (!document.getElementById("phishing-warning-banner")) {
      
      // Play warning sound
      const audio = new Audio(chrome.runtime.getURL("audio/alert.mp3"));
      audio.play().catch(error => console.log("Audio play blocked:", error));

      // Create warning banner
      const banner = document.createElement("div");
      banner.id = "phishing-warning-banner";
      banner.innerHTML = `
        <div class="warning-container">
          <strong>⚠️ Warning: Suspicious Website Detected!</strong><br>
          This website may be trying to steal your information.<br>
          <button id="leave-site">Leave Site</button>
          <button id="ignore-warning">Ignore Warning</button>
        </div>
      `;
      document.body.prepend(banner);

      // Redirect to Google if user clicks Leave Site
      document.getElementById("leave-site").onclick = () => {
        window.location.href = "https://www.google.com";
      };

      // Remove banner if user ignores
      document.getElementById("ignore-warning").onclick = () => {
        banner.remove();
      };
    }
  }
});
