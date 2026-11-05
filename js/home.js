(function () {
  "use strict";

  // Old root-page links should open the matching section of the massage page.
  var massageAnchors = new Set(["services", "about", "help", "contact", "top"]);
  var anchor = window.location.hash.slice(1);

  if (!massageAnchors.has(anchor)) return;

  var massagePage = new URL("./massage/", window.location.href);
  massagePage.search = window.location.search;
  massagePage.hash = anchor;
  window.location.replace(massagePage.href);
})();
