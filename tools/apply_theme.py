"""Site temasını tüm sayfalara uygular (her üretimden sonra en son çalıştırın).

- <body> etiketine `kv` sınıfını ekler (tema CSS'i styles.css sonunda, body.kv ile sınırlı).
- "closing-cta" kapanış bandını slogan karolu düzene çevirir.
Tekrar çalıştırmak güvenlidir.
"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {'node_modules', '.git', 'tools'}

CTA = re.compile(r'(<section[^>]*class="closing-cta[^"]*"[^>]*>)<div class="container"><div>(.*?)</div>(.*?)</div></section>', re.S)

def slogan(lang):
    text = 'Beyond<br>growth.' if lang == 'en' else 'Gelişimin<br>ötesinde.'
    return f'<div class="kv-slogan" aria-hidden="true"><small>ENDLESS.CO</small><strong>{text}</strong></div>'

n_body = n_cta = 0
for f in ROOT.rglob('*.html'):
    if SKIP & set(f.relative_to(ROOT).parts):
        continue
    s = f.read_text()
    o = s
    lang = 'en' if '<html lang="en"' in s else 'tr'
    m = re.search(r'<body class="([^"]*)"', s)
    if m and 'kv' not in m.group(1).split():
        s = s.replace(m.group(0), f'<body class="kv {m.group(1)}"', 1); n_body += 1
    elif not m and '<body>' in s:
        s = s.replace('<body>', '<body class="kv">', 1); n_body += 1
    if 'kv-cta' not in s:
        def rep(mm):
            return (f'{mm.group(1)}<div class="container"><div class="kv-cta">{slogan(lang)}'
                    f'<div class="kv-cta-copy">{mm.group(2)}{mm.group(3)}</div></div></div></section>')
        s, k = CTA.subn(rep, s); n_cta += k
    # sekme simgeleri
    if 'apple-touch-icon' not in s and '</head>' in s:
        icons = '<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">'
        if 'rel="icon"' not in s:
            icons = '<link rel="icon" type="image/png" sizes="96x96" href="/assets/favicon-96.png">' + icons
        s = s.replace('</head>', icons + '</head>', 1)
    # alt bilgide kullanım koşulları bağlantısı
    kk = ('Terms of use', '/kullanim-kosullari/') if lang == 'en' else ('Kullanım Koşulları', '/kullanim-kosullari/')
    lab = 'aria-label="Legal">' if lang == 'en' else 'aria-label="Yasal bilgiler">'
    if lab in s and '/kullanim-kosullari/"' not in s.split(lab, 1)[1][:600]:
        s = re.sub(r'(<nav ' + re.escape(lab) + r'.*?)(</nav>)', lambda mm: mm.group(1) + f'<a href="{kk[1]}">{kk[0]}</a>' + mm.group(2), s, count=1, flags=re.S)
    if s != o:
        f.write_text(s)
print(f'body: {n_body}, cta: {n_cta}')
