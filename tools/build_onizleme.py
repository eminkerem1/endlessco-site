"""Ana sayfadan tasarım önizlemesi üretir: /onizleme/index.html (yalnızca test, noindex)."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
s = (ROOT / 'index.html').read_text()

def sub(old, new):
    global s
    assert old in s, old[:60]
    s = s.replace(old, new, 1)

sub('<link rel="stylesheet" href="/styles.css">',
    '<link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/onizleme/onizleme.css">'
    '<link rel="preload" href="/assets/fonts/jetbrains-mono-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>')
s = re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="https://endlessco.tr/">', s, count=1)
if 'noindex' not in s:
    sub('<head>', '<head><meta name="robots" content="noindex,nofollow">')
sub('<body class="', '<body class="kv ')
sub('<a class="skip-link"', '<div class="kv-note">TASARIM ÖNİZLEMESİ · Şu anki ana sayfa için: <a href="/">endlessco.com.tr</a></div><a class="skip-link"')

m = re.search(r'<section id="iletisim" class="closing-cta">.*?</section>', s, re.S)
s = s[:m.start()] + (
    '<section id="iletisim" class="closing-cta"><div class="container"><div class="kv-cta">'
    '<div class="kv-slogan" aria-hidden="true"><small>ENDLESS.CO</small><strong>Gelişimin<br>ötesinde.</strong></div>'
    '<div class="kv-cta-copy"><p class="eyebrow">İLETİŞİM</p><h2>Çalışmanızı birkaç cümleyle anlatın.</h2>'
    '<p>Konuyu, neye ihtiyaç duyduğunuzu ve varsa düşündüğünüz tarihleri yazın.</p>'
    '<a class="button button-light" href="/iletisim/">Bize yazın <span aria-hidden="true">↗</span></a></div>'
    '</div></div></section>') + s[m.end():]

out = ROOT / 'onizleme' / 'index.html'
out.parent.mkdir(exist_ok=True)
out.write_text(s)
print('ok', out)
