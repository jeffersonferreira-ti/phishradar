const API_BASE_URL = "https://phishradar-production.up.railway.app";

const analyzeTabButton = document.getElementById("analyze-tab-button");
const analyzeTextButton = document.getElementById("analyze-text-button");
const manualContentInput = document.getElementById("manual-content");
const statusElement = document.getElementById("status");
const resultElement = document.getElementById("result");
const scoreValueElement = document.getElementById("score-value");
const labelValueElement = document.getElementById("label-value");
const reasonsListElement = document.getElementById("reasons-list");

function setLoading(isLoading, message) {
  analyzeTabButton.disabled = isLoading;
  analyzeTextButton.disabled = isLoading;
  statusElement.textContent = message || "";
  statusElement.classList.remove("error");
}

function showError(message) {
  resultElement.classList.add("hidden");
  statusElement.textContent = message;
  statusElement.classList.add("error");
}

function showResult(result) {
  scoreValueElement.textContent = String(result.score);
  labelValueElement.textContent = result.label;
  reasonsListElement.innerHTML = "";

  if (Array.isArray(result.reasons) && result.reasons.length > 0) {
    result.reasons.forEach((reason) => {
      const listItem = document.createElement("li");
      listItem.textContent = reason;
      reasonsListElement.appendChild(listItem);
    });
  } else {
    const listItem = document.createElement("li");
    listItem.textContent = "No reasons returned.";
    reasonsListElement.appendChild(listItem);
  }

  resultElement.classList.remove("hidden");
  statusElement.textContent = "Analysis complete.";
  statusElement.classList.remove("error");
}

async function analyzeContent(content) {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ content })
  });

  if (!response.ok) {
    throw new Error(`Analysis request failed with status ${response.status}.`);
  }

  return response.json();
}

async function getCurrentTabUrl() {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  const [activeTab] = tabs;

  if (!activeTab || !activeTab.url) {
    throw new Error("Could not read the current tab URL.");
  }

  return activeTab.url;
}

async function runAnalysis(content, loadingMessage) {
  const normalizedContent = content.trim();

  if (!normalizedContent) {
    showError("Provide some text or open a valid tab before analyzing.");
    return;
  }

  setLoading(true, loadingMessage);

  try {
    const result = await analyzeContent(normalizedContent);
    showResult(result);
  } catch (error) {
    const message =
      error instanceof Error
        ? error.message
        : "Could not complete the analysis.";
    showError(message);
  } finally {
    analyzeTabButton.disabled = false;
    analyzeTextButton.disabled = false;
  }
}

analyzeTabButton.addEventListener("click", async () => {
  try {
    const tabUrl = await getCurrentTabUrl();
    await runAnalysis(tabUrl, "Analyzing current tab...");
  } catch (error) {
    const message =
      error instanceof Error
        ? error.message
        : "Could not read the current tab.";
    showError(message);
  }
});

analyzeTextButton.addEventListener("click", async () => {
  await runAnalysis(manualContentInput.value, "Analyzing text...");
});
