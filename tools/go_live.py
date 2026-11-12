"""Test ortamı ayarlarını geri alır; siteyi endlessco.tr'de yayına hazırlar.

YALNIZCA canlıya geçiş kararı verildiğinde çalıştırın:
    python3 tools/go_live.py
Ardından: commit + push, GitHub Pages > Custom domain = endlessco.tr,
endlessco.tr DNS'inde A kayıtları 185.199.108.153/109.153/110.153/111.153 ve
www CNAME eminkerem1.github.io olacak şekilde güncelleme, HTTPS'i zorunlu kılma.
"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent

n = 0
for f in ROOT.rglob('*.html'):
    if 'tools' in f.relative_to(ROOT).parts:
        continue
    s = f.read_text()
    o = s
    # 404 ve yönlendirme sayfaları noindex,follow kalır
    s = s.replace('<meta name="robots" content="noindex,nofollow">',
                  '<meta name="robots" content="index,follow,max-image-preview:large">')
    if s != o:
        f.write_text(s); n += 1

(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: https://endlessco.tr/sitemap.xml\n')
(ROOT / 'CNAME').write_text('endlessco.tr\n')

app = ROOT / 'app.js'
a = app.read_text()
a = a.replace("const aliasHosts = ['www.endlessco.tr'];",
              "const aliasHosts = ['www.endlessco.tr', 'endlessco.com.tr', 'www.endlessco.com.tr'];")
app.write_text(a)
print(f'{n} sayfa indekslemeye açıldı; robots.txt, CNAME ve app.js güncellendi.')
