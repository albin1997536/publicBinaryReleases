// content.js

function formatTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return [h, m, s]
    .map((n) => String(n).padStart(2, '0'))
    .join(':');
}

function getYouTubeInfo() {
  // For watch pages
  try {
    const url = new URL(window.location.href);
    const titleEl = document.querySelector('h1.title') || document.querySelector('.title.ytd-video-primary-info-renderer');
    const title = titleEl ? titleEl.innerText.trim() : document.title.replace(' - YouTube', '').trim();

    // Try to find current time from the player
    const video = document.querySelector('video');
    if (!video) return { error: 'No video element found on page' };

    const current = Math.floor(video.currentTime);

    // Build timestamped URL
    // Use t param in seconds
    url.searchParams.set('t', current.toString());
    const timestampedUrl = url.toString();

    return { title, current, timestampedUrl };
  } catch (e) {
    return { error: e.message };
  }
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'getTimestamp') {
    const info = getYouTubeInfo();
    if (info.error) return sendResponse({ error: info.error });
    const timeStr = formatTime(info.current);
    const md = `- ${timeStr} - ${msg.label} - [${info.title}](${info.timestampedUrl})`;
    sendResponse({ markdown: md });
  }
});
