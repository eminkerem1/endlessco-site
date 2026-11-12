'use strict';
(function () {
  const form = document.getElementById('en-form');
  if (!form) return;
  const status = document.getElementById('en-status');
  const button = document.getElementById('en-submit');
  const pkg = document.getElementById('en-package');
  const pre = new URLSearchParams(window.location.search).get('package');
  if (pre && Array.from(pkg.options).some(o => o.value === pre)) pkg.value = pre;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    if (form.querySelector('[name="_honey"]').value) return;
    const name = document.getElementById('en-name').value.trim();
    const email = document.getElementById('en-email').value.trim();
    const pkgText = pkg.value ? pkg.options[pkg.selectedIndex].text : 'Not specified';
    const payload = {
      'Name': name, 'Organisation': document.getElementById('en-org').value.trim() || 'Not specified', 'Email': email,
      'Package': pkgText, 'Message': document.getElementById('en-message').value.trim(), 'Privacy notice': 'Read and understood',
      'Language': 'English', 'Page': window.location.href,
      _subject: 'ENDLESS.CO enquiry (EN) — ' + pkgText, _replyto: email, _template: 'table', _captcha: 'false'
    };
    button.disabled = true;
    status.textContent = 'Sending… this can take up to a minute, please keep this page open.';
    const send = async () => {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 90000);
      try {
        const res = await fetch('https://formsubmit.co/ajax/endlesscotr@gmail.com', {
          method: 'POST', headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}, body: JSON.stringify(payload), signal: ctrl.signal
        });
        const out = await res.json().catch(() => ({}));
        if (!res.ok || String(out.success) === 'false') throw new Error('send-failed');
      } finally { clearTimeout(timer); }
    };
    try {
      try { await send(); } catch (first) {
        if (first.name === 'AbortError') throw first;
        status.textContent = 'The connection is slow; trying again…';
        await new Promise(r => setTimeout(r, 3000));
        await send();
      }
      form.classList.add('is-sent');
      form.innerHTML = '<h2>Thank you, your message has reached us.</h2><p>We will reply to the email address you provided.</p><a class="button button-dark" href="/en/services/">Explore our services <span aria-hidden="true">↗</span></a>';
      form.setAttribute('tabindex', '-1');
      form.focus();
    } catch (error) {
      button.disabled = false;
      const body = encodeURIComponent(payload.Message + '\n\n' + name + (payload.Organisation !== 'Not specified' ? ', ' + payload.Organisation : ''));
      status.innerHTML = 'We could not send your message right now. Please try again in a few minutes or <a href="mailto:endlesscotr@gmail.com?subject=' + encodeURIComponent(payload._subject) + '&body=' + body + '">send it by email</a>.';
    }
  });
})();
