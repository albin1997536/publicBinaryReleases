const generateBtn = document.getElementById('generate');
const copyBtn = document.getElementById('copy');
const labelInput = document.getElementById('label');
const output = document.getElementById('output');

// Request current timestamp and video info from content script
function generate() {
  const label = labelInput.value.trim();
  if (!label) {
    alert('Please enter a label.');
    return;
  }
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tab = tabs[0];
    chrome.tabs.sendMessage(
      tab.id,
      { action: 'getTimestamp', label },
      (response) => {
        if (!response || response.error) {
          output.value = response && response.error ? response.error : 'No response from content script.';
          return;
        }
        output.value = response.markdown;
      }
    );
  });
}

generateBtn.addEventListener('click', generate);

copyBtn.addEventListener('click', () => {
  if (!output.value) return;
  navigator.clipboard.writeText(output.value).then(() => {
    copyBtn.textContent = 'Copied!';
    setTimeout(() => (copyBtn.textContent = 'Copy to Clipboard'), 1500);
  });
});
