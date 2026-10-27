var META_PIXEL_ID = 'PIXEL_ID_PENDING';
/*
 * AVS Meta Pixel, loaded only on pages that receive paid Meta traffic (Vietnamese PCU landing page).
 * Line 1 above is the single source of the Pixel ID. While it is not all digits, this file does nothing.
 * Fires PageView on load, and the standard Contact event when a visitor taps a Zalo or LINE link,
 * so the ad set can optimise for people who open a chat. Sends no link URL and no personal data.
 * Plain ES5, no dependencies. Never throws if Meta is blocked.
 */
(function () {
  'use strict';

  var id = (typeof META_PIXEL_ID === 'string') ? META_PIXEL_ID : '';
  if (!/^\d+$/.test(id)) { return; }

  try {
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () {
        n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
      };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0';
      n.queue = []; t = b.createElement(e); t.async = !0; t.src = v;
      s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', id);
    window.fbq('track', 'PageView');
  } catch (e) { return; }

  document.addEventListener('click', function (ev) {
    try {
      var el = ev.target;
      while (el && el !== document) {
        if (el.nodeType === 1 && String(el.tagName).toLowerCase() === 'a') {
          var href = el.getAttribute('href') || '';
          if (href.indexOf('zaloapp.com/') !== -1 || href.indexOf('zalo.me/') !== -1) {
            window.fbq('track', 'Contact', { content_name: 'zalo' });
          } else if (href.indexOf('line.me/') !== -1) {
            window.fbq('track', 'Contact', { content_name: 'line' });
          }
          return;
        }
        el = el.parentNode;
      }
    } catch (e) {}
  }, false);
})();
