/* AVS site — header interactions */
(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');

  // mobile menu open/close
  if (toggle && header) {
    toggle.addEventListener('click', function () {
      header.classList.toggle('open');
      var exp = header.classList.contains('open');
      toggle.setAttribute('aria-expanded', exp ? 'true' : 'false');
    });
  }

  // dropdowns: tap to expand on mobile (<=768px)
  document.querySelectorAll('.has-dd > a').forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (window.innerWidth <= 768) {
        e.preventDefault();
        a.parentElement.classList.toggle('open');
      }
    });
  });

  // sticky header shadow on scroll
  if (header) {
    var onScroll = function () {
      header.classList.toggle('scrolled', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // close mobile menu when a real link is clicked
  document.querySelectorAll('.nav-menu a').forEach(function (a) {
    a.addEventListener('click', function () {
      if (!a.parentElement.classList.contains('has-dd') || window.innerWidth > 768) {
        header && header.classList.remove('open');
      }
    });
  });

  // Enhanced conversions: read email + phone from the form before it is reset.
  // gtag hashes these (SHA-256) before sending; GA4 only uses them when
  // "User-provided data collection" is on. Returns null when nothing usable.
  var avsUserData = function (f) {
    try {
      var get = function (n) {
        var el = f.querySelector('[name="' + n + '"]');
        return el ? String(el.value || '').trim() : '';
      };
      var ud = {};
      var email = get('email').toLowerCase();
      if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { ud.email = email; }
      var country = get('country').toLowerCase();
      var d = get('phone').replace(/[^\d+]/g, '');
      var phone = '';
      if (/^\+\d{8,15}$/.test(d)) { phone = d; }
      else if (/^00\d{8,15}$/.test(d)) { phone = '+' + d.slice(2); }
      else if (/^60\d{8,11}$/.test(d)) { phone = '+' + d; }
      else if (/^0\d{8,10}$/.test(d) && (country === '' || country === 'my' || country.indexOf('malaysia') !== -1)) { phone = '+6' + d; }
      if (phone) { ud.phone_number = phone; }
      return (ud.email || ud.phone_number) ? ud : null;
    } catch (e) { return null; }
  };

  // Formspree AJAX form handling (quote + contact)
  document.querySelectorAll('form[data-formspree]').forEach(function (f) {
    var note = f.querySelector('.form-note');
    var err = f.querySelector('.form-error');
    var btn = f.querySelector('[type="submit"]');
    var label = btn ? btn.textContent : '';
    var showErr = function (m) { if (err) { err.textContent = m; err.hidden = false; } };
    var hideErr = function () { if (err) { err.hidden = true; } };

    f.addEventListener('submit', function (e) {
      e.preventDefault();
      hideErr();
      var action = f.getAttribute('action') || '';
      if (action.indexOf('YOUR_FORMSPREE_ID') !== -1) {
        showErr('This form isn’t connected yet. Add your Formspree form ID to activate it (see FORMS-SETUP.md).');
        return;
      }
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
      var userData = avsUserData(f);
      fetch(action, {
        method: 'POST',
        body: new FormData(f),
        headers: { 'Accept': 'application/json' }
      }).then(function (res) {
        if (res.ok) {
          f.reset();
          if (note) { note.hidden = false; }
          f.querySelectorAll('input,textarea,select').forEach(function (el) { el.disabled = true; });
          if (btn) { btn.textContent = 'Sent ✓'; }
          if (userData && window.gtag) { try { window.gtag('set', 'user_data', userData); } catch (e) {} }
          if (window.avsTrack) { window.avsTrack('generate_lead', {form_page: location.pathname}); }
        } else {
          return res.json().then(function (d) {
            var m = (d && d.errors && d.errors.length)
              ? d.errors.map(function (x) { return x.message; }).join(', ')
              : 'Sorry, something went wrong. Please try again or email info@avs.my.';
            showErr(m);
            if (btn) { btn.disabled = false; btn.textContent = label; }
          });
        }
      }).catch(function () {
        showErr('Network error — please check your connection or email info@avs.my.');
        if (btn) { btn.disabled = false; btn.textContent = label; }
      });
    });
  });
})();
