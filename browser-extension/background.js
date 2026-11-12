const AGENT_ENDPOINT = 'http://localhost:9000/api/website-domain';

async function sendDomain(domain, tabId) {
  if (!domain || domain === 'undefined') {
    return;
  }

  try {
    await fetch(AGENT_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        computer_name: 'PC-01',
        session_id: 1,
        domain,
        tab_id: tabId
      })
    });
  } catch (error) {
    console.warn('Unable to forward domain event:', error);
  }
}

chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status !== 'complete' || !tab.url) {
    return;
  }

  try {
    const url = new URL(tab.url);
    await sendDomain(url.hostname, tabId);
  } catch (error) {
    console.warn('Invalid URL, ignoring tab update:', tab.url);
  }
});
