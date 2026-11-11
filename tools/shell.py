"""Site shell helpers: build a full page from the shared header/footer of an existing page."""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://endlessco.tr'
SHELL_SRC = f'{ROOT}/kurumsal/index.html'

def esc(s):
    return html.escape(s, quote=True)

def _shell():
    h = open(SHELL_SRC, encoding='utf-8').read()
    head_start = h.split('<title>', 1)[0]           # doctype .. charset/viewport
    body_start = h[h.find('</head>'):h.find('<main')]  # </head><body ...><header>...</header>...
    tail = h[h.find('</main>') + len('</main>'):]
    # remove "current page" markers from nav
    body_start = re.sub(r' is-current', '', body_start)
    body_start = body_start.replace(' aria-current="page"', '')
    return head_start, body_start, tail

def build(path, title, desc, crumbs, main_html, extra_ld=None, og_image=f'{BASE}/assets/endless-logo-v2.png'):
    """path like '/paketler/ilk-adim/'; crumbs list of (name, path)."""
    head_start, body_start, tail = _shell()
    url = BASE + path
    t, d = esc(title), esc(desc)
    graph = [
        {"@type": "Organization", "@id": f"{BASE}/#organization", "name": "ENDLESS.CO", "url": f"{BASE}/",
         "logo": {"@type": "ImageObject", "url": f"{BASE}/assets/endless-logo-v2.png", "width": 1942, "height": 809},
         "email": "endlesscotr@gmail.com",
         "address": {"@type": "PostalAddress", "addressLocality": "Çankaya", "addressRegion": "Ankara", "addressCountry": "TR"}},
        {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": "ENDLESS.CO", "inLanguage": "tr-TR",
         "publisher": {"@id": f"{BASE}/#organization"}},
        {"@type": "BreadcrumbList", "@id": f"{url}#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p} for i, (n, p) in enumerate(crumbs)]},
        {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": title, "description": desc, "inLanguage": "tr-TR",
         "isPartOf": {"@id": f"{BASE}/#website"}, "about": {"@id": f"{BASE}/#organization"}, "breadcrumb": {"@id": f"{url}#breadcrumb"}},
    ]
    if extra_ld:
        graph.extend(extra_ld)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    head = (f'<title>{t}</title><meta name="description" content="{d}">\n'
            f'<meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#0b1b32">\n'
            f'<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">\n'
            f'<meta property="og:type" content="website"><meta property="og:locale" content="tr_TR"><meta property="og:site_name" content="ENDLESS.CO">\n'
            f'<meta property="og:image" content="{og_image}"><meta property="og:image:width" content="1942"><meta property="og:image:height" content="809"><meta property="og:image:alt" content="ENDLESS.CO — Proje, Eğitim, Danışmanlık"><meta property="og:url" content="{url}">\n'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{og_image}"><meta name="twitter:image:alt" content="ENDLESS.CO — Proje, Eğitim, Danışmanlık">\n'
            f'<link rel="canonical" href="{url}"><link rel="icon" type="image/png" sizes="96x96" href="/assets/favicon-96.png"><link rel="stylesheet" href="/styles.css"><script src="/app.js" defer></script>'
            f'<script type="application/ld+json">{ld}</script>')
    return head_start + head + body_start + main_html + tail

def breadcrumbs_html(crumbs):
    parts = []
    for i, (n, p) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            parts.append(f'<span aria-current="page">{esc(n)}</span>')
        else:
            parts.append(f'<a href="{p}">{esc(n)}</a><span aria-hidden="true">/</span>')
    return '<div class="breadcrumbs" role="navigation" aria-label="Sayfa yolu">' + ''.join(parts) + '</div>'

def write(path, content):
    import os
    fp = ROOT + path + 'index.html'
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(content)
    return fp
