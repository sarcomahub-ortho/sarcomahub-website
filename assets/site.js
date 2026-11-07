(function () {
  var nav = document.getElementById('mainNav'), btn = document.getElementById('menuBtn');
  if (btn) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
  });

  // Mandala with the yellow sarcoma ribbon, drawn to match the logo
  function drawMandala(id) {
    var c = document.getElementById(id); if (!c) return;
    var x = c.getContext('2d'), s = c.width, m = s / 2, onTeal = id === 'mandala';
    var ink = getComputedStyle(document.documentElement).getPropertyValue('--ink').trim() || '#0B2E2A';
    x.clearRect(0, 0, s, s);
    x.lineWidth = s / 340;
    for (var ring = 0; ring < 5; ring++) {
      var r = m * (0.32 + ring * 0.135);
      x.globalAlpha = onTeal ? 1 : 0.25 + ring * 0.12;
      x.strokeStyle = onTeal ? 'rgba(255,247,242,' + (0.25 + ring * 0.12) + ')' : ink;
      x.beginPath(); x.arc(m, m, r, 0, Math.PI * 2); x.stroke();
      var n = 12 + ring * 6;
      for (var i = 0; i < n; i++) {
        var a = i / n * Math.PI * 2 + (ring % 2 ? Math.PI / n : 0), r2 = r - m * 0.06;
        x.beginPath(); x.moveTo(m + Math.cos(a) * r2, m + Math.sin(a) * r2); x.lineTo(m + Math.cos(a) * r, m + Math.sin(a) * r); x.stroke();
        if (ring % 2 === 0) { x.beginPath(); x.arc(m + Math.cos(a) * (r - m * 0.075), m + Math.sin(a) * (r - m * 0.075), s / 170, 0, Math.PI * 2); x.stroke(); }
      }
    }
    x.globalAlpha = 1; x.strokeStyle = '#E9B425'; x.lineCap = 'round'; x.lineWidth = s / 26;
    var k = m * 0.0105;
    x.beginPath(); x.moveTo(m, m - 24 * k); x.bezierCurveTo(m - 16 * k, m - 24 * k, m - 20 * k, m - 8 * k, m - 12 * k, m + 4 * k); x.lineTo(m + 10 * k, m + 28 * k); x.stroke();
    x.beginPath(); x.moveTo(m, m - 24 * k); x.bezierCurveTo(m + 16 * k, m - 24 * k, m + 20 * k, m - 8 * k, m + 12 * k, m + 4 * k); x.lineTo(m - 10 * k, m + 28 * k); x.stroke();
  }
  drawMandala('mandala'); drawMandala('mandala2');
  if (window.matchMedia) {
    var mq = matchMedia('(prefers-color-scheme: dark)');
    if (mq.addEventListener) mq.addEventListener('change', function () { drawMandala('mandala2'); });
  }

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
