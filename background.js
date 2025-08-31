//background.js
// Runs when the active tab changes or URL changes
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {
    checkUrlSafety(tabId, tab.url);
  }
});

async function checkUrlSafety(tabId, url) {
  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url }),
    });

    const data = await response.json();

    if (data.prediction === "Malicious") {
      // Show warning badge on extension icon
      chrome.action.setBadgeText({ text: "!", tabId: tabId });
      chrome.action.setBadgeBackgroundColor({ color: "red", tabId: tabId });

      // Show alert message for malicious URLs (similar to content.js)
      chrome.scripting.executeScript({
        target: { tabId: tabId },
        function: (url) => {
          alert("⚠️ Warning: This site is Malicious!\n\nURL: " + url + "\n\nPlease proceed with caution or avoid this site entirely.");
        },
        args: [url]
      });
    } else {
      // Clear badge if benign
      chrome.action.setBadgeText({ text: "", tabId: tabId });
    }
  } catch (error) {
    console.error("Error checking URL safety:", error);
  }
}
