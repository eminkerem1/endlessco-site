'use strict';

// Keep bookmarked paths and campaign parameters when visitors use a second domain.
const aliasHosts = ['www.endlessco.tr', 'endlessco.com.tr', 'www.endlessco.com.tr'];
if (aliasHosts.includes(window.location.hostname)) {
  const destination = new URL(window.location.href);
  destination.protocol = 'https:';
  destination.hostname = 'endlessco.tr';
  destination.port = '';
  window.location.replace(destination.href);
}

const menuToggle = document.querySelector('.menu-toggle');
const navigation = document.getElementById('main-nav');
const navGroups = Array.from(document.querySelectorAll('[data-nav-group]'));
function closeGroups(except = null) {
  navGroups.forEach(group => { if (group !== except) group.open = false; });
}
function closeMenu() {
  navigation.classList.remove('is-open');
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-label', 'Gezinme menüsünü aç');
  closeGroups();
}
menuToggle.addEventListener('click', () => {
  const open = menuToggle.getAttribute('aria-expanded') !== 'true';
  if (!open) { closeMenu(); return; }
  menuToggle.setAttribute('aria-expanded', 'true');
  menuToggle.setAttribute('aria-label', 'Gezinme menüsünü kapat');
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
  const area = document.getElementById('contact-area');
  const program = document.getElementById('contact-program');
  const programField = document.getElementById('contact-program-field');
  const source = document.getElementById('contact-source');
  const briefTitle = document.getElementById('brief-title');
  const messageLabel = document.getElementById('contact-message-label');
  const messageField = document.getElementById('contact-message');
  const defaultMessagePlaceholder = messageField.getAttribute('placeholder');
  const gmailButton = document.getElementById('gmail-draft');
  if (gmailButton) gmailButton.hidden = false;
  const copyButton = document.getElementById('copy-draft');
  const copyPanel = document.getElementById('draft-copy-panel');
  const copyText = document.getElementById('draft-copy-text');
  if (copyButton) copyButton.hidden = false;
  const params = new URLSearchParams(window.location.search);
  function selectKnownOption(element, value) {
    if (value && Array.from(element.options).some(option => option.value === value)) element.value = value;
  }
  selectKnownOption(selector, params.get('hizmet'));
  selectKnownOption(area, params.get('alan'));
  selectKnownOption(program, params.get('program'));
  function updateRequestFields() {
    programField.hidden = selector.value !== 'proje';
    const partnership = selector.value === 'uzman-isbirligi';
    briefTitle.textContent = partnership ? 'İş birliği talebinizi hazırlayın' : 'Talebinizi hazırlayın';
    messageLabel.textContent = partnership ? 'İş birliği yapmak istediğiniz çalışmayı anlatın' : 'İhtiyacınızı kısaca anlatın';
    messageField.setAttribute('placeholder', partnership
      ? 'Uzmanlık alanınız, deneyiminiz ve varsa kendi müşteriniz için planladığınız hizmetin kapsamı ve takvimi…'
      : defaultMessagePlaceholder);
  }
  updateRequestFields();
  selector.addEventListener('change', updateRequestFields);
  function prepareDraft() {
    if (!form.reportValidity()) return null;
    const name = document.getElementById('contact-name').value.trim();
    const organization = document.getElementById('contact-org').value.trim();
    const email = document.getElementById('contact-email').value.trim();
    const service = selector.value ? selector.options[selector.selectedIndex].text : 'Genel görüşme';
    const areaText = area.value ? area.options[area.selectedIndex].text : 'Belirtilmedi';
    const programText = selector.value === 'proje' && program.value ? program.options[program.selectedIndex].text : '';
    const message = document.getElementById('contact-message').value.trim();
    if (!name || !message) {
      document.getElementById('form-status').textContent = 'Adınızı ve talebinizi yazın. Yalnızca boşluk içeren alanlarla taslak hazırlanamıyor.';
      document.getElementById(!name ? 'contact-name' : 'contact-message').focus();
      return null;
    }
    const subject = selector.value === 'uzman-isbirligi'
      ? 'ENDLESS.CO eğitmen ve uzman iş ortaklığı talebi'
      : 'ENDLESS.CO görüşme talebi — ' + service;
    const sourceText = source && source.value ? source.options[source.selectedIndex].text : '';
    const body = 'Merhabalar,\n\n' + message + '\n\nAd Soyad: ' + name + '\nŞirket / Kurum / Üniversite: ' + (organization || 'Belirtilmedi') + '\nE-posta: ' + email + '\nGörüşme konusu: ' + service + (programText ? '\nProje programı: ' + programText : '') + '\nÇalışma alanı: ' + areaText + (sourceText ? '\nBize ulaşma kaynağı: ' + sourceText : '');
    return { subject, body };
  }
  form.addEventListener('submit', event => {
    event.preventDefault();
    const draft = prepareDraft();
    if (!draft) return;
    const { subject, body } = draft;
    if (event.submitter && event.submitter.value === 'gmail') {
      const params = new URLSearchParams({view: 'cm', fs: '1', to: 'endlesscotr@gmail.com', su: subject, body});
      window.open('https://mail.google.com/mail/?' + params.toString(), '_blank', 'noopener,noreferrer');
      document.getElementById('form-status').textContent = 'Gmail’de açılan taslağı kontrol edip gönderebilirsiniz. Yeni pencere açılmadıysa tarayıcınızın pencere ayarlarını kontrol edin.';
    } else {
      window.location.href = 'mailto:endlesscotr@gmail.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      document.getElementById('form-status').textContent = 'Taslağı e-posta uygulamanızdan gönderebilirsiniz. Uygulama açılmadıysa Gmail seçeneğini kullanabilir veya endlesscotr@gmail.com adresine doğrudan yazabilirsiniz.';
    }
  });
  if (copyButton) {
    copyButton.addEventListener('click', async () => {
      const draft = prepareDraft();
      if (!draft) return;
      const text = 'Alıcı: endlesscotr@gmail.com\nKonu: ' + draft.subject + '\n\n' + draft.body;
      copyText.value = text;
      copyPanel.hidden = false;
      copyText.focus();
      copyText.select();
      const status = document.getElementById('form-status');
      status.textContent = 'Taslağınız aşağıda seçili. Metni kopyalayıp e-postanıza yapıştırabilirsiniz; mesaj henüz gönderilmedi.';
      try {
        const clipboard = window.navigator && window.navigator.clipboard;
        if (clipboard && clipboard.writeText) {
          await clipboard.writeText(text);
          if (copyText.value === text) status.textContent = 'Taslak kopyalandı. E-postanıza yapıştırıp alıcı ve konu alanlarını kontrol ederek gönderebilirsiniz. Mesaj henüz gönderilmedi.';
        }
      } catch {
        // Keep the selected, read-only text available when clipboard access is denied.
      }
    });
    function clearCopyPreview() {
      copyPanel.hidden = true;
      copyText.value = '';
      document.getElementById('form-status').textContent = '';
    }
    form.addEventListener('input', clearCopyPreview);
    form.addEventListener('change', clearCopyPreview);
  }
}
const year = document.getElementById('year');
if (year) year.textContent = String(new Date().getFullYear());

// This is an information notice, not consent for advertising or analytics.
const cookieNotice = document.getElementById('cookie-notice');
if (cookieNotice) {
  const noticeKey = 'endless.cookie-notice.v1';
  let dismissed = false;
  try { dismissed = window.sessionStorage.getItem(noticeKey) === '1'; } catch {}
  cookieNotice.hidden = dismissed;
  document.getElementById('cookie-notice-dismiss').addEventListener('click', () => {
    cookieNotice.hidden = true;
    try { window.sessionStorage.setItem(noticeKey, '1'); } catch {}
  });
}
