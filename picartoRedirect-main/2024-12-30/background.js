chrome.browserAction.onClicked.addListener(function(tab) {
    var currentUrl = tab.url;
    var regex = /https:\/\/picarto\.tv\/(.*)/;
    var match = currentUrl.match(regex);
    
    if (match) {
      var newUrl = "https://picarto.tv/chatpopout/" + match[1] + "/public";
      chrome.tabs.update({url: newUrl});
    }
  });
  
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message == "reverse") {
      var currentUrl = sender.tab.url;
      var regex = /https:\/\/picarto\.tv\/chatpopout\/(.*)\/public/;
      var match = currentUrl.match(regex);
      
      if (match) {
        var newUrl = "https://picarto.tv/" + match[1];
        chrome.tabs.update({url: newUrl});
      }
    }
  });
  