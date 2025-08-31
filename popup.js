document.getElementById("checkBtn").addEventListener("click", async () => {
  const url = document.getElementById("urlInput").value;
  const resultDiv = document.getElementById("result");
  const resultImage = document.getElementById("resultImage");

  if (!url) {
    resultDiv.textContent = "Please enter a URL.";
    resultDiv.className = "result";

    // Show default image when no input
    resultImage.src = "NangoCat/cat34green-01.png";
    resultImage.alt = "Default";
    resultImage.style.display = "block";
    return;
  }

  resultDiv.textContent = "Checking...";
  resultDiv.className = "result";

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();

    if (data.prediction === "Benign") {
      resultDiv.textContent = "✅ Safe";
      resultDiv.className = "result safe";

      resultImage.src = "NangoCat/cat34yellow-01.png";
      resultImage.alt = "Safe site";
      resultImage.style.display = "block";
    } else {
      resultDiv.textContent = "⚠️ Malicious!";
      resultDiv.className = "result malicious";

      resultImage.src = "NangoCat/cat34red-01.png";
      resultImage.alt = "Malicious site";
      resultImage.style.display = "block";
    }
  } catch (error) {
    resultDiv.textContent = "❌ Error: Backend not running.";
    resultDiv.className = "result";

    // Show default image on error
    resultImage.src = "NangoCat/cat34green-01.png";
    resultImage.alt = "Default";
    resultImage.style.display = "block";
  }
});
