"""İngilizce sayfaları üretir: /en/, /en/services/, /en/about/, /en/contact/, /en/privacy/.

Kullanım: python3 tools/build_en.py
Ayrıca Türkçe sayfaların üst menüsüne "EN" dil bağlantısını ekler.
"""
import glob, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import ROOT

BASE = 'https://endlessco.tr'
A = '<span aria-hidden="true">↗</span>'
e = lambda s: html.escape(s, quote=True)
LOGO = ('<span class="logo-window"><img src="/assets/endless-logo-web-600.webp" srcset="/assets/endless-logo-web-600.webp 600w, /assets/endless-logo-web-900.webp 900w" '
        'sizes="275px" alt="ENDLESS.CO — Projects · Training · Consultancy" width="1942" height="809"></span>')

PAGES = [('/en/', 'Home'), ('/en/services/', 'Services'), ('/en/about/', 'About'), ('/en/contact/', 'Contact')]
TR_OF = {'/en/': '/', '/en/services/': '/hizmetler/', '/en/about/': '/kurumsal/', '/en/contact/': '/iletisim/', '/en/privacy/': '/kvkk-aydinlatma-metni/'}

AREAS = [
    ('projects', 'Project Development and Management', 'From an idea to a funded project, and from a project to lasting results.',
     ['Reviewing national and international funding programmes against your organisation and goals',
      'Building a coherent project logic: needs, target groups, objectives and activities',
      'Planning partnerships, roles, timelines and resources realistically',
      'Delivering training, workshops and expert coordination for funded projects, within programme rules']),
    ('training', 'Training Programmes', 'Tailored, practice-based training that people use at work the next day.',
     ['AI tools and digital productivity', 'Office and collaboration tools, digital content',
      'Project Cycle Management (PCM), planning and reporting', 'Communication, time management, problem solving and entrepreneurship']),
    ('experiential', 'Experiential Learning', 'Teams that learn by doing, and by reflecting on what they did.',
     ['Team development and group dynamics', 'Leadership and decision-making experiences',
      'Business simulations', 'Low-risk outdoor and adventure-based learning, also deliverable indoors']),
    ('research', 'Organisational Research and Consultancy', 'The right questions, reliable data, actionable recommendations.',
     ['Needs and stakeholder research with surveys, interviews and focus groups', 'Participatory workshops',
      'Monitoring and evaluation of projects and training programmes', 'Turning findings into practical action plans']),
    ('academic', 'Academic Support', 'Your research, your work; done with the right method.',
     ['Research design and methodology guidance', 'Selection and adaptation of measurement tools',
      'Quantitative and qualitative data analysis', 'Methodological feedback on theses, papers and conference submissions']),
]
PACKAGES = [
    ('01', 'projects', 'First Step', 'Two online meetings, a review of up to three funding opportunities and a written 2–3 page project roadmap.', 'Fixed fee: TRY 1,900 (VAT included)'),
    ('02', 'projects', 'Project Design Workshop', 'A hands-on workshop in which your team turns its own idea into a structured project design.', None),
    ('03', 'projects', 'Project Implementation and Training', 'Training, workshops, expert coordination and evaluation for funded projects.', None),
    ('04', 'training', 'Applied Competence Programmes', 'Tailored training on AI and digital productivity, office tools, PCM, communication and entrepreneurship.', None),
    ('05', 'experiential', 'Experiential Learning and Adventure Education', 'Workshops, outdoor programmes and development series run by qualified facilitators.', None),
    ('06', 'research', 'Organisational Needs and Stakeholder Research', 'Research that turns stakeholder views into actionable recommendations.', None),
    ('07', 'research', 'Impact and Evaluation', 'Monitoring and evaluation frameworks, pre/post assessments and outcome reports, with clear limits on impact claims.', None),
    ('08', 'academic', 'Academic Mentoring', 'Research design and methodology guidance. We never write theses or papers on anyone’s behalf.', None),
    ('09', 'academic', 'Qualitative and Quantitative Data Analysis', 'Statistical and thematic analysis of research data, with results explained to the researcher.', None),
]


def shell(path, title, desc, main):
    nav = ''.join(f'<a class="nav-direct{" is-current" if p == path else ""}" href="{p}"{" aria-current=\"page\"" if p == path else ""}>{n}</a>'
                  for p, n in PAGES[1:3])
    nav += f'<a class="nav-direct nav-lang" href="{TR_OF[path]}" hreflang="tr" lang="tr" aria-label="Türkçe">TR</a>'
    nav += f'<a class="nav-cta" href="/en/contact/">Contact {A}</a>'
    header = (f'<header class="site-header"><div class="container header-inner"><a class="brand" href="/en/" aria-label="ENDLESS.CO home">{LOGO}</a>'
              '<button class="menu-toggle" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="main-nav"><span></span><span></span></button>'
              f'<nav id="main-nav" aria-label="Main navigation">{nav}</nav></div></header>')
    footer = (f'<footer class="full-footer"><div class="container footer-grid"><div class="footer-brand"><a class="brand" href="/en/" aria-label="ENDLESS.CO home">{LOGO}</a>'
              '<p>Projects · Training · Consultancy</p><p>Çankaya, Ankara, Türkiye</p><a href="mailto:endlesscotr@gmail.com">endlesscotr@gmail.com</a></div>'
              '<div class="footer-column"><h3>ENDLESS.CO</h3><a href="/en/about/">About us</a><a href="/en/services/">Services</a><a href="/en/contact/">Contact</a></div>'
              '<div class="footer-column"><h3>Services</h3>' + ''.join(f'<a href="/en/services/#{i}">{n}</a>' for i, n, _, _ in AREAS) + '</div>'
              '<div class="footer-column"><h3>Türkçe</h3><a href="/" hreflang="tr" lang="tr">Türkçe site</a><a href="/paketler/" hreflang="tr" lang="tr">Hizmet paketleri</a></div></div>'
              '<div class="container footer-bottom"><span>© <span id="year">2026</span> ENDLESS.CO</span><span>Beyond development.</span></div>'
              '<div class="container footer-legal"><p>Business owner: Aleyna ERKADAM</p><nav aria-label="Legal"><a href="/en/privacy/">Privacy notice</a></nav></div></footer>')
    url = BASE + path
    ld = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "url": url, "name": title, "description": desc, "inLanguage": "en",
                     "publisher": {"@type": "Organization", "name": "ENDLESS.CO", "url": f"{BASE}/"}}, ensure_ascii=False)
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f'<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#0b1b32">'
            f'<link rel="canonical" href="{url}"><link rel="alternate" hreflang="en" href="{url}"><link rel="alternate" hreflang="tr" href="{BASE}{TR_OF[path]}">'
            f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:locale" content="en_GB">'
            f'<meta property="og:image" content="{BASE}/assets/endless-logo-v2.png"><meta property="og:url" content="{url}">'
            '<link rel="icon" type="image/png" sizes="96x96" href="/assets/favicon-96.png"><link rel="stylesheet" href="/styles.css"><script src="/app.js" defer></script>'
            f'<script type="application/ld+json">{ld}</script></head>'
            f'<body class="site-multipage"><a class="skip-link" href="#main">Skip to content</a>{header}{main}{footer}</body></html>')


def heading(eyebrow, h1, lead, crumbs=None, actions=''):
    bc = ''
    if crumbs:
        bc = ('<div class="breadcrumbs" role="navigation" aria-label="Breadcrumb"><a href="/en/">Home</a><span aria-hidden="true">/</span>'
              f'<span aria-current="page">{crumbs}</span></div>')
    return f'<section class="page-heading container">{bc}<p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="page-lead">{lead}</p>{actions}</section>'


def cta(title, text, href='/en/contact/', label='Get in touch'):
    return (f'<section class="closing-cta"><div class="container"><div><p class="eyebrow">CONTACT</p><h2>{title}</h2><p>{text}</p></div>'
            f'<a class="button button-light" href="{href}">{label} {A}</a></div></section>')


def page_home():
    cards = ''.join(f'<article class="pkg-card"><div class="pkg-card-top"><span class="pkg-no">{k + 1:02d}</span></div><h3><a href="/en/services/#{i}">{n}</a></h3>'
                    f'<p>{t}</p><div class="pkg-card-foot"><span class="pkg-price pkg-price-quote">{(lambda c: f"{c} package" + ("s" if c > 1 else ""))(sum(1 for p in PACKAGES if p[1] == i))}</span>'
                    f'<a class="text-link" href="/en/services/#{i}">Explore {A}</a></div></article>' for k, (i, n, t, _) in enumerate(AREAS))
    main = ('<main id="main">' + heading('ENDLESS.CO · ANKARA, TÜRKİYE', 'Projects, training<br>and research consultancy.',
            'We help organisations turn ideas into well-designed projects, build their people’s skills and make decisions based on evidence. For each piece of work we bring together the right academics, trainers, researchers and project specialists.',
            actions=f'<div class="hero-actions"><a class="button button-dark" href="/en/services/">Explore our services {A}</a><a class="text-link" href="/en/contact/">Get in touch {A}</a></div>') +
            f'<section class="section container"><div class="section-intro"><p class="eyebrow">WHAT WE DO</p><h2>Five areas of work,<br>one way of working.</h2></div><div class="pkg-grid home-pkg-grid">{cards}</div></section>'
            '<section class="soft-section section"><div class="container"><div class="section-intro"><p class="eyebrow">INTERNATIONAL COOPERATION</p><h2>A reliable partner<br>for European projects.</h2></div>'
            '<div class="principles-grid"><article><h3>Erasmus+ and ESC</h3><p>Our team has hands-on experience with Erasmus+ (KA1, KA2, Youth and Sport) and European Solidarity Corps projects, from project design to coordination and training.</p></article>'
            '<article><h3>Training and evaluation</h3><p>We can contribute non-formal and experiential learning activities, training design, and monitoring and evaluation to international partnerships, within each programme’s rules.</p></article>'
            '<article><h3>Sport and youth</h3><p>Sport management, youth participation, social inclusion and social entrepreneurship are among our main fields of work.</p></article></div></div></section>'
            '<section class="section container"><div class="section-intro"><p class="eyebrow">HOW WE WORK</p><h2>Clear scope before we start,<br>close follow-up while we work.</h2></div>'
            '<ol class="service-approach-grid"><li><span class="service-step-number">01</span><h3>We listen</h3><p>We discuss your goals, the people involved and any deadlines.</p></li>'
            '<li><span class="service-step-number">02</span><h3>We agree the scope</h3><p>We put the team, timeline, fee and deliverables in a written proposal.</p></li>'
            '<li><span class="service-step-number">03</span><h3>We deliver and follow up</h3><p>We coordinate the work, check the outputs and review the results with you.</p></li></ol></section>' +
            cta('Tell us about your project.', 'Write to us in English or Turkish. We will get back to you by email.') + '</main>')
    return shell('/en/', 'ENDLESS.CO | Projects, Training and Research Consultancy, Ankara',
                 'Ankara-based project, training and research consultancy: project design, tailored training, experiential learning, research, evaluation and academic support.', main)


def page_services():
    blocks = []
    for i, n, t, caps in AREAS:
        lis = ''.join(f'<li>{c}</li>' for c in caps)
        pk = ''.join(f'<article class="pkg-card{" pkg-card-featured" if no == "01" else ""}"><div class="pkg-card-top"><span class="pkg-no">{no}</span></div><h3>{name}</h3><p>{d}</p>'
                     f'<div class="pkg-card-foot"><span class="pkg-price{"" if price else " pkg-price-quote"}">{price or "Tailored proposal"}</span>'
                     f'<a class="text-link" href="/en/contact/?package={no}">Enquire {A}</a></div></article>'
                     for no, a, name, d, price in PACKAGES if a == i)
        blocks.append(f'<div class="pkg-group en-area" id="{i}"><div class="pkg-group-head"><h2>{n}</h2><p class="en-area-tag">{t}</p><ul class="en-caps">{lis}</ul></div>'
                      f'<div class="pkg-grid">{pk}</div></div>')
    main = ('<main id="main">' + heading('SERVICES', 'Five areas of work,<br>nine service packages.',
            'Each area below describes what we do in general. The packages next to it are ready-made, clearly scoped services. First Step has a fixed fee; for all other packages we prepare a written, tailored proposal.', 'Services') +
            f'<section class="section container pkg-groups">{"".join(blocks)}</section>'
            '<section class="container"><p class="pkg-small">Detailed descriptions of each package, including deliverables and what is not included, are available on our <a href="/paketler/" hreflang="tr" lang="tr">Turkish package pages</a>.</p></section>' +
            cta('Not sure which package fits?', 'Describe what you need and we will suggest the right starting point.') + '</main>')
    return shell('/en/services/', 'Services and Packages | ENDLESS.CO',
                 'Project development, training programmes, experiential learning, organisational research and academic support. Nine clearly scoped service packages.', main)


def page_about():
    main = ('<main id="main">' + heading('ABOUT US', 'Bringing knowledge, experience<br>and cooperation together<br>for organisations to grow.',
            'ENDLESS.CO is an Ankara-based professional services brand working in projects, training and consultancy. We bring together academics, trainers, researchers and project specialists as each piece of work requires.', 'About us') +
            '<section class="soft-section section"><div class="container"><div class="section-intro"><p class="eyebrow">MISSION AND VISION</p><h2>Beyond development:<br>creating lasting value.</h2></div>'
            '<div class="mv-grid"><article class="mv-card"><span class="mv-label">Our mission</span><p>To identify organisations’ development needs accurately, bring together the expertise each task requires, design practical projects, training and research, and measure their results to contribute to lasting change.</p></article>'
            '<article class="mv-card mv-card-dark"><span class="mv-label">Our vision</span><p>To be a development partner that organisations in Türkiye and in international projects turn to with confidence, combining a scientific approach, field experience and cooperation.</p></article></div>'
            '<p class="mv-approach"><strong>“Beyond development.”</strong> Our motto sums up this idea: the value of a training programme, a project or a study is measured not on the day it ends, but by the lasting difference it leaves behind.</p></div></section>'
            '<section class="section container"><div class="section-intro"><p class="eyebrow">WHAT SETS US APART</p><h2>Three things,<br>at the same time.</h2></div><div class="principles-grid diff-grid">'
            '<article><span class="cap-no">01</span><h3>A scientific approach</h3><p>We base our recommendations on research, analysis and up-to-date sources rather than assumptions.</p></article>'
            '<article><span class="cap-no">02</span><h3>Field experience</h3><p>We make sure that what we design can actually be delivered, combining academic knowledge with practical experience.</p></article>'
            '<article><span class="cap-no">03</span><h3>Coordination</h3><p>We bring the right experts together and manage scope, timeline and responsibilities through a single point of contact.</p></article></div>'
            '<p class="values-line"><strong>Our values:</strong> cooperation, reliability, scientific rigour, practicality, continuous learning, transparency, ethics and a focus on impact.</p></section>'
            '<section class="soft-section section"><div class="container"><div class="section-intro"><p class="eyebrow">OUR NAME</p><h2>Built to work together.</h2></div><div class="principles-grid">'
            '<article><h3>Why we started</h3><p>We wanted to bring the experience we gained in project management, education, research and sport sciences into a shared structure where different kinds of expertise complement each other.</p></article>'
            '<article><h3>ENDLESS</h3><p>Stands for the continuity of learning, growth and working together, and for the value we place on work and the effort behind it.</p></article>'
            '<article><h3>.CO</h3><p>Stands for cooperation, collaboration and co-working: experts working together with clear roles and shared responsibility.</p></article></div></div></section>' +
            cta('Let’s talk about what you need.', 'Write to us in English or Turkish.') + '</main>')
    return shell('/en/about/', 'About Us: Mission, Vision and Values | ENDLESS.CO',
                 'ENDLESS.CO is an Ankara-based professional services brand in projects, training and consultancy. Our mission, vision, values and story.', main)


def page_contact():
    opts = ''.join(f'<option value="{no}">{no} · {name}</option>' for no, _, name, _, _ in PACKAGES)
    form = ('<form id="en-form" class="brief-form" action="https://formsubmit.co/endlesscotr@gmail.com" method="post" novalidate>'
            '<h2>Send us a message</h2><p class="form-privacy-note">The data controller, Aleyna ERKADAM, processes the information in this form to respond to your enquiry. '
            'Because our form and email service providers are located outside Türkiye, your information is transferred abroad for this purpose. Details: '
            '<a href="/en/privacy/" target="_blank" rel="noopener noreferrer">Privacy notice</a>.</p>'
            '<div class="form-row"><label>Full name<input id="en-name" name="name" autocomplete="name" required></label>'
            '<label>Organisation (optional)<input id="en-org" name="organisation" autocomplete="organization"></label></div>'
            '<label>Email<input id="en-email" type="email" name="email" autocomplete="email" required></label>'
            f'<label>Which package are you interested in? (optional)<select id="en-package" name="package"><option value="">Not sure yet</option>{opts}</select></label>'
            '<label>Your message<textarea id="en-message" name="message" rows="6" required placeholder="What would you like to do, who is it for, and when?"></textarea></label>'
            '<label class="form-consent"><input id="en-consent" type="checkbox" required><span>I have read and understood the <a href="/en/privacy/" target="_blank" rel="noopener noreferrer">Privacy notice</a>.</span></label>'
            '<input type="text" name="_honey" class="form-honey" tabindex="-1" autocomplete="off" aria-hidden="true">'
            f'<button id="en-submit" class="button button-blue" type="submit">Send message {A}</button><p id="en-status" class="form-status" role="status" aria-live="polite"></p>'
            '<p class="form-note">You can also write directly to <a href="mailto:endlesscotr@gmail.com">endlesscotr@gmail.com</a>.</p></form>')
    main = ('<main id="main">' + heading('CONTACT', 'Tell us about<br>your project.', 'Write to us in English or Turkish. We will reply by email.', 'Contact') +
            '<section class="section container en-contact"><div class="en-contact-info"><h2>Contact details</h2><p><a href="mailto:endlesscotr@gmail.com">endlesscotr@gmail.com</a></p>'
            '<p>Çankaya, Ankara, Türkiye</p><p class="pkg-small">For Erasmus+ and other international partnerships, please mention the programme, action and deadline you have in mind.</p></div>'
            f'{form}</section></main><script src="/en/en.js" defer></script>')
    return shell('/en/contact/', 'Contact | ENDLESS.CO', 'Contact ENDLESS.CO in English or Turkish about projects, training, research and academic support.', main)


def page_privacy():
    S = lambda t, b: f'<section><h2>{t}</h2>{b}</section>'
    body = ''.join([
        S('About this notice', '<p>This is an English summary of our Turkish privacy notice (KVKK Aydınlatma Metni), prepared under Article 10 of the Turkish Personal Data Protection Law No. 6698 (KVKK). If the two versions differ, the <a href="/kvkk-aydinlatma-metni/" hreflang="tr" lang="tr">Turkish version</a> prevails.</p>'),
        S('Data controller', '<p>Aleyna ERKADAM, owner of the sole proprietorship operating under the ENDLESS.CO brand. Contact: <a href="mailto:endlesscotr@gmail.com">endlesscotr@gmail.com</a> · Çankaya, Ankara, Türkiye.</p>'),
        S('What we process and how', '<p>Name, email address, organisation, the package or service you are interested in and the content of your message, collected directly from you through the contact form or by email; and technical records such as IP address and time of request, created automatically by our hosting and form service providers.</p>'),
        S('Purposes and legal bases', '<ul><li>Responding to your enquiry and preparing proposals (KVKK Art. 5(2)(c)).</li><li>Answering general questions and keeping our services secure (KVKK Art. 5(2)(f), legitimate interest).</li><li>Meeting legal obligations and protecting our rights (KVKK Art. 5(2)(ç) and (e)).</li></ul><p>We do not use your data for marketing.</p>'),
        S('Recipients and transfers abroad', '<p>We share only what is necessary with the experts working on your request, and use FormSubmit (form delivery), Google (email) and GitHub (website hosting) as service providers. Their servers are located outside Türkiye, so your data is transferred abroad solely to provide these services, subject to Article 9 of the KVKK.</p>'),
        S('Retention', '<p>Enquiries that do not lead to a contract are kept for up to two years from our last correspondence. If a contract is concluded, records are kept for the periods required by Turkish commercial and tax law.</p>'),
        S('Cookies', '<p>Our website does not use cookies or tracking tools.</p>'),
        S('Your rights', '<p>Under Article 11 of the KVKK you may ask whether your data is processed, request information, correction or deletion, learn who it has been shared with, object to certain automated decisions and claim compensation for unlawful processing. To exercise your rights, write to <a href="mailto:endlesscotr@gmail.com">endlesscotr@gmail.com</a> from the email address you used to contact us. You also have the right to complain to the Turkish Personal Data Protection Board.</p>'),
    ])
    main = ('<main id="main">' + heading('LEGAL', 'Privacy notice', 'How we process personal data when you visit our website or contact us. Last updated: 11 November 2026.', 'Privacy notice') +
            f'<div class="container section legal-layout"><article class="legal-prose">{body}</article></div></main>')
    return shell('/en/privacy/', 'Privacy Notice | ENDLESS.CO', 'How ENDLESS.CO processes personal data under the Turkish Personal Data Protection Law (KVKK).', main)


EN_JS = r"""'use strict';
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
    status.textContent = 'Sending…';
    try {
      const res = await fetch('https://formsubmit.co/ajax/endlesscotr@gmail.com', {
        method: 'POST', headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}, body: JSON.stringify(payload)
      });
      const out = await res.json().catch(() => ({}));
      if (!res.ok || String(out.success) === 'false') throw new Error('send-failed');
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
"""

# Türkçe sayfalar için İngilizce karşılıklar
EN_OF = {'index.html': '/en/', 'kurumsal/index.html': '/en/about/', 'hizmetler/index.html': '/en/services/', 'paketler/index.html': '/en/services/',
         'iletisim/index.html': '/en/contact/', 'kvkk-aydinlatma-metni/index.html': '/en/privacy/', 'cerez-politikasi/index.html': '/en/privacy/'}


def add_lang_switch():
    n = 0
    for fp in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
        rel = os.path.relpath(fp, ROOT)
        if rel.startswith(('en/', 'ilk-adim/')):
            continue
        h = open(fp, encoding='utf-8').read()
        o = h
        target = EN_OF.get(rel) or ('/en/services/' if rel.startswith(('hizmetler/', 'paketler/')) else '/en/')
        link = f'<a class="nav-direct nav-lang" href="{target}" hreflang="en" lang="en" aria-label="English">EN</a>'
        h = re.sub(r'<a class="nav-direct nav-lang" href="[^"]*" hreflang="en" lang="en" aria-label="English">EN</a>', '', h)
        h = h.replace('<a class="nav-cta" href="/iletisim/"', link + '<a class="nav-cta" href="/iletisim/"', 1)
        h = h.replace('<a href="/en/" hreflang="en" lang="en">English</a>', '')
        if h != o:
            open(fp, 'w', encoding='utf-8').write(h)
            n += 1
    return n


if __name__ == '__main__':
    out = {'/en/': page_home(), '/en/services/': page_services(), '/en/about/': page_about(), '/en/contact/': page_contact(), '/en/privacy/': page_privacy()}
    for p, c in out.items():
        fp = os.path.join(ROOT, p.strip('/'), 'index.html')
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, 'w', encoding='utf-8').write(c)
    open(os.path.join(ROOT, 'en', 'en.js'), 'w', encoding='utf-8').write(EN_JS)
    print('english pages', len(out), '| language links on', add_lang_switch(), 'pages')
