(function () {
  var nav = document.getElementById('mainNav'), btn = document.getElementById('menuBtn');
  if (btn) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
  });

  var copy = document.getElementById('copyPhone');
  if (copy) copy.addEventListener('click', function () {
    var num = '+91 9111 60 9222';
    var fallback = function () {
      var r = document.createRange(); r.selectNodeContents(document.getElementById('phone'));
      var sel = getSelection(); sel.removeAllRanges(); sel.addRange(r); copy.textContent = 'Selected, press copy';
    };
    if (navigator.clipboard) navigator.clipboard.writeText(num).then(function () { copy.textContent = 'Copied'; }, fallback);
    else fallback();
  });

  // Contact form: sends to Formspree without leaving the page
  var form = document.getElementById('contactForm');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var msg = document.getElementById('formMsg'), ok = true;
    form.querySelectorAll('[required]').forEach(function (i) {
      var bad = !i.value.trim(); i.style.borderColor = bad ? '#C4492F' : ''; if (bad) ok = false;
    });
    var show = function (text, cls) { msg.textContent = text; msg.className = 'formmsg ' + cls; msg.hidden = false; };
    if (!ok) { show('Please fill in your name, how to reach you, and your message.', 'err'); return; }
    var submit = form.querySelector('button[type="submit"]'); submit.disabled = true; submit.textContent = 'Sending…';
    fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
      .then(function (r) {
        if (!r.ok) throw new Error();
        form.reset(); show('Thank you. Your message has reached us and we will get back to you soon.', 'ok');
      })
      .catch(function () { show('Your message could not be sent. Please try again, or call +91 9111 60 9222.', 'err'); })
      .then(function () { submit.disabled = false; submit.textContent = 'Send message'; });
  });
})();
