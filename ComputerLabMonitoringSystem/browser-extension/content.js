(() => {
  try {
    const hostname = window.location.hostname;
    if (!hostname) {
      return;
    }

    chrome.runtime.sendMessage({
      type: 'domain-update',
      domain: hostname
    });
  } catch (error) {
    console.warn('Content script failed:', error);
  }
})();
