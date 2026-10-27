var GA_ID = 'G-66R56Y37MQ';
/*
 * AVS site GA4 tracking. Line 1 above is the single source of the GA4 Measurement ID.
 * While line 1 still holds the placeholder (or any value not starting with G-), this file
 * only defines a no-op window.avsTrack: no network request, no listener, nothing else.
 * Plain ES5, no dependencies. Never throws if gtag is blocked.
 */
(function () {
  'use strict';

  var id = (typeof GA_ID === 'string') ? GA_ID : '';

  // Inert: placeholder not replaced yet (an ID made only of X after "G-"), or not a G- ID.
  if (id.indexOf('G-') !== 0 || /^G-X+$/.test(id)) {
    window.avsTrack = function () {};
    return;
  }

  var gtag;
  try {
    window.dataLayer = window.dataLayer || [];
    gtag = function () { window.dataLayer.push(arguments); };
    window.gtag = gtag;

    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
    (document.head || document.documentElement).appendChild(s);

    gtag('js', new Date());
    gtag('config', id);
  } catch (e) {}

  window.avsTrack = function (name, params) {
    try { gtag('event', name, params || {}); } catch (e) {}
  };

  // One delegated listener: any click on (or inside) a link to wa.me, mailto: or tel:
  document.addEventListener('click', function (ev) {
    try {
      var el = ev.target;
      while (el && el !== document) {
        if (el.nodeType === 1 && String(el.tagName).toLowerCase() === 'a') {
          var href = el.getAttribute('href') || '';
          var params = { link_url: href, page_path: location.pathname };
          if (href.indexOf('zaloapp.com/') !== -1 || href.indexOf('zalo.me/') !== -1) {
            window.avsTrack('zalo_click', { channel: 'zalo', page_path: location.pathname });
          } else if (href.indexOf('line.me/') !== -1) {
            window.avsTrack('line_click', { channel: 'line', page_path: location.pathname });
          } else if (href.indexOf('wa.me/') !== -1) {
            window.avsTrack('whatsapp_click', params);
          } else if (href.indexOf('mailto:') === 0) {
            window.avsTrack('email_click', params);
          } else if (href.indexOf('tel:') === 0) {
            window.avsTrack('phone_click', params);
          }
          return;
        }
        el = el.parentNode;
      }
    } catch (e) {}
  }, false);
})();
