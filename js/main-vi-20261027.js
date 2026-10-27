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

  // Formspree AJAX form handling (quote + contact)
  document.querySelectorAll('form[data-formspree]').forEach(function (f) {
    // Local validation messages do not depend on the visitor's browser language.
    f.querySelectorAll('input,textarea,select').forEach(function (el) {
      el.addEventListener('invalid', function () {
        if (el.validity.valueMissing) el.setCustomValidity('Vui lòng điền thông tin này.');
        else if (el.validity.typeMismatch && el.type === 'email') el.setCustomValidity('Vui lòng nhập địa chỉ email hợp lệ.');
        else el.setCustomValidity('Vui lòng kiểm tra thông tin đã nhập.');
      });
      el.addEventListener('input', function () { el.setCustomValidity(''); });
      el.addEventListener('change', function () { el.setCustomValidity(''); });
    });
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
        showErr('Biểu mẫu hiện chưa sẵn sàng. Vui lòng gửi email đến info@avs.my.');
        return;
      }
      if (btn) { btn.disabled = true; btn.textContent = 'Đang gửi…'; }
      fetch(action, {
        method: 'POST',
        body: new FormData(f),
        headers: { 'Accept': 'application/json' }
      }).then(function (res) {
        if (res.ok) {
          f.reset();
          if (note) { note.hidden = false; }
          f.querySelectorAll('input,textarea,select').forEach(function (el) { el.disabled = true; });
          if (btn) { btn.textContent = 'Đã gửi ✓'; }
          if (window.avsTrack) { window.avsTrack('generate_lead', {form_page: location.pathname}); }
        } else {
          return res.json().then(function (d) {
            var m = 'Không thể gửi yêu cầu. Vui lòng kiểm tra thông tin, thử lại hoặc gửi email đến info@avs.my.';
            showErr(m);
            if (btn) { btn.disabled = false; btn.textContent = label; }
          });
        }
      }).catch(function () {
        showErr('Lỗi kết nối — vui lòng kiểm tra mạng hoặc gửi email đến info@avs.my.');
        if (btn) { btn.disabled = false; btn.textContent = label; }
      });
    });
  });
})();
