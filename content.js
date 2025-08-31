// Very simple suspicious URL check
const suspiciousPatterns = ["login", "verify", "secure", "bank"];

let url = window.location.href.toLowerCase();
if (suspiciousPatterns.some((pattern) => url.includes(pattern))) {
  alert("⚠️ Warning: This site might be phishing!");
}
