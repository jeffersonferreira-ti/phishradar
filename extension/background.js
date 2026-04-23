const API_BASE_URL = "https://phishradar-production.up.railway.app";
const CACHE_KEY_PREFIX = "analysis:";

const BADGE_CONFIG = {
  LOW_RISK: {
    text: "LOW",
    color: "#15803d"
  },
  MODERATE: {
    text: "MOD",
    color: "#ea580c"
  },
  SUSPICIOUS: {
    text: "WARN",
    color: "#ca8a04"
  },
  HIGH_RISK: {
    text: "HIGH",
    color: "#b91c1c"
  }
};

function getCacheKey(url) {
  return `${CACHE_KEY_PREFIX}${url}`;
}

function isSupportedUrl(url) {
  return typeof url === "string" && /^https?:\/\//i.test(url);
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

async function updateBadgeForTab(tabId, result) {
  if (!Number.isInteger(tabId)) {
    return;
  }

  const badge = BADGE_CONFIG[result?.label];

  if (!badge) {
    await chrome.action.setBadgeText({ tabId, text: "" });
    return;
  }

  await chrome.action.setBadgeText({ tabId, text: badge.text });
  await chrome.action.setBadgeBackgroundColor({ tabId, color: badge.color });
}

async function clearBadge(tabId) {
  if (!Number.isInteger(tabId)) {
    return;
  }

  await chrome.action.setBadgeText({ tabId, text: "" });
}

async function analyzeUrlWithCache(url) {
  const cachedAnalysis = await getCachedAnalysis(url);

  if (cachedAnalysis) {
    return cachedAnalysis.result;
  }

  const result = await analyzeContent(url);
  await saveCachedAnalysis(url, result);
  return result;
}

async function processTab(tabId, url) {
  if (!isSupportedUrl(url)) {
    await clearBadge(tabId);
    return;
  }

  try {
    const result = await analyzeUrlWithCache(url);
    await updateBadgeForTab(tabId, result);
  } catch {
    await clearBadge(tabId);
  }
}

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status !== "complete" || !tab.active) {
    return;
  }

  processTab(tabId, tab.url);
});

chrome.tabs.onActivated.addListener(async ({ tabId }) => {
  try {
    const tab = await chrome.tabs.get(tabId);
    await processTab(tabId, tab.url);
  } catch {
    await clearBadge(tabId);
  }
});
