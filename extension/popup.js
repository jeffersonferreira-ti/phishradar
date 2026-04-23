const API_BASE_URL = "https://phishradar-production.up.railway.app";
const CACHE_KEY_PREFIX = "analysis:";

const analyzeTabButton = document.getElementById("analyze-tab-button");
const analyzeTextButton = document.getElementById("analyze-text-button");
const manualContentInput = document.getElementById("manual-content");
const statusElement = document.getElementById("status");
const resultElement = document.getElementById("result");
const scoreValueElement = document.getElementById("score-value");
const labelValueElement = document.getElementById("label-value");
const reasonsListElement = document.getElementById("reasons-list");
const GENERIC_ANALYSIS_ERROR = "Could not analyze the content. Please try again.";

function getCacheKey(url) {
  return `${CACHE_KEY_PREFIX}${url}`;
}

function isSupportedUrl(url) {
  return typeof url === "string" && /^https?:\/\//i.test(url);
}

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

function showResult(result, message) {
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
    listItem.textContent = "No risk signals detected.";
    reasonsListElement.appendChild(listItem);
  }

  resultElement.classList.remove("hidden");
  statusElement.textContent = message || "Analysis complete.";
  statusElement.classList.remove("error");
}

function getAnalysisErrorMessage(error) {
  if (!(error instanceof Error)) {
    return GENERIC_ANALYSIS_ERROR;
  }

  if (error.message.startsWith("Analysis request failed with status")) {
    return GENERIC_ANALYSIS_ERROR;
  }

  return error.message;
}

async function getCachedAnalysis(url) {
  const cacheKey = getCacheKey(url);
  const stored = await chrome.storage.local.get(cacheKey);
  return stored[cacheKey] || null;
}

async function saveCachedAnalysis(url, result) {
  const cacheKey = getCacheKey(url);
  await chrome.storage.local.set({
    [cacheKey]: {
      url,
      result,
      analyzedAt: Date.now()
    }
  });
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

async function getCurrentTab() {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  const [activeTab] = tabs;

  if (!activeTab) {
    throw new Error("Could not read the current tab.");
  }

  return activeTab;
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
    showResult(result, "Analysis complete.");
  } catch (error) {
    showError(getAnalysisErrorMessage(error));
  } finally {
    analyzeTabButton.disabled = false;
    analyzeTextButton.disabled = false;
  }
}

async function analyzeUrlWithCache(url, loadingMessage) {
  const cachedAnalysis = await getCachedAnalysis(url);

  if (cachedAnalysis?.result) {
    showResult(cachedAnalysis.result, "Loaded analysis for the current page.");
    return;
  }

  setLoading(true, loadingMessage);
  try {
    const result = await analyzeContent(url);
    await saveCachedAnalysis(url, result);
    showResult(result, "Analysis complete.");
  } catch (error) {
    showError(getAnalysisErrorMessage(error));
  } finally {
    analyzeTabButton.disabled = false;
    analyzeTextButton.disabled = false;
  }
}

async function loadActiveTabAnalysis() {
  try {
    const activeTab = await getCurrentTab();
    const tabUrl = activeTab.url;

    if (!isSupportedUrl(tabUrl)) {
      resultElement.classList.add("hidden");
      statusElement.textContent = "Open an http(s) page to view automatic analysis.";
      statusElement.classList.remove("error");
      return;
    }

    await analyzeUrlWithCache(tabUrl, "Analyzing current page...");
  } catch (error) {
    showError(getAnalysisErrorMessage(error));
  }
}

analyzeTabButton.addEventListener("click", async () => {
  try {
    const activeTab = await getCurrentTab();
    const tabUrl = activeTab.url;

    if (!isSupportedUrl(tabUrl)) {
      showError("Open a valid http(s) tab before analyzing.");
      return;
    }

    await analyzeUrlWithCache(tabUrl, "Analyzing current tab...");
  } catch (error) {
    showError(getAnalysisErrorMessage(error));
  }
});

analyzeTextButton.addEventListener("click", async () => {
  await runAnalysis(manualContentInput.value, "Analyzing text...");
});

loadActiveTabAnalysis();
