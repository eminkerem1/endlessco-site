'use strict';

// Keep bookmarked paths and campaign parameters when visitors use a second domain.
// TEST ORTAMI: endlessco.com.tr bu kopyanın test adresi olduğu için yönlendirmeden çıkarıldı.
// Canlıya alınırken listeye geri eklenebilir: 'endlessco.com.tr', 'www.endlessco.com.tr'
const aliasHosts = ['www.endlessco.tr'];
if (aliasHosts.includes(window.location.hostname)) {
  const destination = new URL(window.location.href);
  destination.protocol = 'https:';
  destination.hostname = 'endlessco.tr';
  destination.port = '';
  window.location.replace(destination.href);
}

const EN_UI = document.documentElement.lang === 'en';
const menuToggle = document.querySelector('.menu-toggle');
const navigation = document.getElementById('main-nav');
const navGroups = Array.from(document.querySelectorAll('[data-nav-group]'));
function closeGroups(except = null) {
  navGroups.forEach(group => { if (group !== except) group.open = false; });
}
function closeMenu() {
  navigation.classList.remove('is-open');
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-label', EN_UI ? 'Open navigation' : 'Gezinme menüsünü aç');
  closeGroups();
}
menuToggle.addEventListener('click', () => {
  const open = menuToggle.getAttribute('aria-expanded') !== 'true';
  if (!open) { closeMenu(); return; }
  menuToggle.setAttribute('aria-expanded', 'true');
  menuToggle.setAttribute('aria-label', EN_UI ? 'Close navigation' : 'Gezinme menüsünü kapat');
  navigation.classList.add('is-open');
});
navGroups.forEach(group => {
  group.addEventListener('toggle', () => { if (group.open) closeGroups(group); });
});
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('click', event => {
  if (!event.target.closest('[data-nav-group]')) closeGroups();
  if (!event.target.closest('.site-header')) closeMenu();
});
document.addEventListener('keydown', event => {
  if (event.key !== 'Escape') return;
  const group = navGroups.find(item => item.open);
  const mobileOpen = menuToggle.getAttribute('aria-expanded') === 'true';
  closeMenu();
  if (mobileOpen) menuToggle.focus();
  else if (group) group.querySelector('summary').focus();
});

const tabGroups = [];
document.querySelectorAll('[data-tabs]').forEach(group => {
  const list = group.querySelector('[role="tablist"]');
  const tabs = Array.from(list.querySelectorAll('[role="tab"]'));
  const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
  function activate(index, focus = false) {
    tabs.forEach((tab, current) => {
      const selected = current === index;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      panels[current].hidden = !selected;
    });
    if (focus) tabs[index].focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activate(index));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); activate(next, true); }
    });
  });
  tabGroups.push({ tabs, panels, activate });
});

function revealHash(scroll = false) {
  let id;
  try { id = decodeURIComponent(window.location.hash.slice(1)); }
  catch { return; }
  if (!id) return;
  const target = document.getElementById(id);
  if (!target) return;
  const panel = target.closest('[role="tabpanel"]');
  if (panel) {
    const group = tabGroups.find(item => item.panels.includes(panel));
    if (group) group.activate(group.panels.indexOf(panel));
  }
  const detail = target.closest('details');
  if (detail) detail.open = true;
  if (scroll) requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
}
revealHash(Boolean(window.location.hash));
window.addEventListener('hashchange', () => revealHash(true));
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', () => {
    const hash = link.getAttribute('href');
    if (hash !== '#' && hash === window.location.hash) revealHash(true);
  });
});

const form = document.getElementById('brief-form');
if (form) {
  const selector = document.getElementById('contact-service');
  const pkg = document.getElementById('contact-package');
  const area = document.getElementById('contact-area');
  const program = document.getElementById('contact-program');
  const programField = document.getElementById('contact-program-field');
  const briefTitle = document.getElementById('brief-title');
  const messageLabel = document.getElementById('contact-message-label');
  const messageField = document.getElementById('contact-message');
  const status = document.getElementById('form-status');
  const submitButton = document.getElementById('brief-submit');
  const defaultMessagePlaceholder = messageField.getAttribute('placeholder');
  const firstStepNote = document.getElementById('first-step-note');
  const packageArea = {'01': 'proje', '02': 'proje', '03': 'proje', '04': 'egitim', '05': 'deneyimsel', '06': 'kurumsal', '07': 'kurumsal', '08': 'akademik', '09': 'akademik'};
  const params = new URLSearchParams(window.location.search);
  function selectKnownOption(element, value) {
    if (element && value && Array.from(element.options).some(option => option.value === value)) element.value = value;
  }
  selectKnownOption(pkg, params.get('paket'));
  selectKnownOption(selector, params.get('hizmet') || packageArea[params.get('paket')]);
  selectKnownOption(area, params.get('alan'));
  selectKnownOption(program, params.get('program'));
  function updateRequestFields() {
    programField.hidden = selector.value !== 'proje';
    const partnership = selector.value === 'uzman-isbirligi';
    const firstStep = !partnership && pkg && pkg.value === '01';
    briefTitle.textContent = partnership ? 'İş birliği talebinizi gönderin' : firstStep ? 'İlk Adım başvurusu' : 'Talebinizi gönderin';
    messageLabel.textContent = partnership ? 'İş birliği yapmak istediğiniz çalışmayı anlatın' : firstStep ? 'Kurumunuzu ve proje fikrinizi kısaca anlatın' : 'İhtiyacınızı kısaca anlatın';
    messageField.setAttribute('placeholder', partnership
      ? 'Uzmanlık alanınız, deneyiminiz ve varsa kendi müşteriniz için planladığınız hizmetin kapsamı ve takvimi…'
      : firstStep ? 'Kurumunuzun türü ve faaliyetleri, proje fikriniz, ulaşmak istediğiniz hedef grup ve varsa aklınızdaki destek programı…'
      : defaultMessagePlaceholder);
    if (firstStepNote) firstStepNote.hidden = !firstStep;
    if (submitButton) submitButton.firstChild.textContent = firstStep ? 'Başvurumu gönder ' : 'Talebimi gönder ';
  }
  updateRequestFields();
  selector.addEventListener('change', updateRequestFields);
  if (pkg) pkg.addEventListener('change', () => { if (packageArea[pkg.value]) selector.value = packageArea[pkg.value]; updateRequestFields(); });
  const optionText = el => (el && el.value ? el.options[el.selectedIndex].text : '');
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const name = document.getElementById('contact-name').value.trim();
    const message = messageField.value.trim();
    if (!name || !message) {
      status.textContent = 'Adınızı ve talebinizi yazın.';
      document.getElementById(!name ? 'contact-name' : 'contact-message').focus();
      return;
    }
    if (form.querySelector('[name="_honey"]').value) return;
    const packageText = optionText(pkg);
    const subject = selector.value === 'uzman-isbirligi'
      ? 'ENDLESS.CO uzman iş ortaklığı talebi'
      : 'ENDLESS.CO talebi — ' + (packageText || optionText(selector) || 'Genel görüşme');
    const payload = {
      'Ad Soyad': name,
      'Kurum': document.getElementById('contact-org').value.trim() || 'Belirtilmedi',
      'E-posta': document.getElementById('contact-email').value.trim(),
      'Paket': packageText || 'Belirtilmedi',
      'Hizmet alanı': optionText(selector) || 'Belirtilmedi',
      'Proje programı': selector.value === 'proje' ? (optionText(program) || 'Belirtilmedi') : '-',
      'Çalışma alanı': optionText(area) || 'Belirtilmedi',
      'Bizi nereden duydu': optionText(document.getElementById('contact-source')) || 'Belirtilmedi',
      'Mesaj': message,
      'KVKK': 'Aydınlatma metni okundu ve anlaşıldı',
      'Sayfa': window.location.href,
      _subject: subject,
      _replyto: document.getElementById('contact-email').value.trim(),
      _template: 'table',
      _captcha: 'false'
    };
    submitButton.disabled = true;
    status.textContent = 'Talebiniz gönderiliyor… Bu işlem bir dakika kadar sürebilir, lütfen sayfayı kapatmayın.';
    const send = async () => {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 90000);
      try {
        const response = await fetch('https://formsubmit.co/ajax/endlesscotr@gmail.com', {
          method: 'POST',
          headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
          body: JSON.stringify(payload),
          signal: ctrl.signal
        });
        const result = await response.json().catch(() => ({}));
        if (!response.ok || String(result.success) === 'false') throw new Error(result.message || 'send-failed');
      } finally {
        clearTimeout(timer);
      }
    };
    try {
      try {
        await send();
      } catch (first) {
        if (first.name === 'AbortError') throw first;
        status.textContent = 'Bağlantı yavaş; talebinizi yeniden göndermeyi deniyoruz…';
        await new Promise(r => setTimeout(r, 3000));
        await send();
      }
      form.reset();
      form.classList.add('is-sent');
      form.innerHTML = '<h2>Talebiniz bize ulaştı.</h2><p>Teşekkür ederiz, ' + name.replace(/[<>&"]/g, '') + '. Talebinizi değerlendirip yazdığınız e-posta adresine dönüş yapacağız.</p><p class="form-note">Acil bir konu için <a href="mailto:endlesscotr@gmail.com">endlesscotr@gmail.com</a> adresine de yazabilirsiniz.</p><a class="button button-dark" href="/paketler/">Hizmet paketlerini inceleyin <span aria-hidden="true">↗</span></a>';
      form.setAttribute('tabindex', '-1');
      form.focus();
    } catch (error) {
      submitButton.disabled = false;
      const body = 'Merhabalar,\n\n' + message + '\n\n' + Object.entries(payload).filter(([k]) => !k.startsWith('_') && k !== 'Mesaj').map(([k, v]) => k + ': ' + v).join('\n');
      const mailto = 'mailto:endlesscotr@gmail.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      status.innerHTML = 'Talebiniz şu an iletilemedi. Lütfen birkaç dakika sonra yeniden deneyin ya da <a href="' + mailto + '">e-posta ile gönderin</a>.';
    }
  });
}
const year = document.getElementById('year');
if (year) year.textContent = String(new Date().getFullYear());

// This is an information notice, not consent for advertising or analytics.
