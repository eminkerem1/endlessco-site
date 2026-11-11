"""Hizmet alanı sayfalarını (/hizmetler/<alan>/) ve /hizmetler/ sayfasını günceller.

Kullanım: python3 tools/build_hizmetler.py
İçerik tools/hizmetler_data.py dosyasındadır. Betik, sayfanın başlık bölümü ile
"Sorularınız ve hazırlık" bölümü arasını <!--area:start--> ... <!--area:end-->
işaretleri arasında yeniden üretir; SSS ve iletişim bölümlerine dokunmaz.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import ROOT, esc
from hizmetler_data import AREA_PAGES, AREA_ORDER
from paketler_data import PACKAGES
from build_paketler import card

ARROW = '<span aria-hidden="true">↗</span>'
START, END = '<!--area:start-->', '<!--area:end-->'


def caps_section(a):
    items = ''.join(
        f'<li><span class="cap-no">{i + 1:02d}</span><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></li>'
        for i, (t, d) in enumerate(a['caps']))
    return (f'<section class="section container area-caps"><div class="section-heading-row"><div><p class="eyebrow">BU ALANDA NE YAPIYORUZ?</p>'
            f'<h2>{esc(a["tagline"])}</h2></div><p>Aşağıdaki başlıklar bu alandaki çalışmalarımızın genel çerçevesidir. Her işin kapsamını kurumunuzun ihtiyacına göre birlikte belirliyoruz.</p></div>'
            f'<ol class="cap-list">{items}</ol></section>')


def approach_section(a):
    items = ''.join(f'<article><h3>{esc(t)}</h3><p>{esc(d)}</p></article>' for t, d in a['approach'])
    who = ''.join(f'<li>{esc(w)}</li>' for w in a['who'])
    return (f'<section class="soft-section section area-approach"><div class="container"><div class="section-intro"><p class="eyebrow">YAKLAŞIMIMIZ</p>'
            f'<h2>Nasıl çalıştığımız,<br>ne yaptığımız kadar önemli.</h2></div><div class="principles-grid">{items}</div>'
            f'<div class="who-row"><span>KİMLERLE ÇALIŞIYORUZ</span><ul>{who}</ul></div></div></section>')


def packages_section(key):
    ps = [p for p in PACKAGES if p['area'] == key]
    return (f'<section class="section container area-packages"><div class="section-heading-row"><div><p class="eyebrow">HAZIR PAKETLER</p>'
            f'<h2>Kapsamı ve teslimi belli<br>paketlerle başlayın.</h2></div><div class="home-program-copy"><p>Bu alandaki işlerin sık talep edilen bölümlerini, ne yapılacağı ve neyin teslim edileceği baştan belli paketler hâline getirdik.</p>'
            f'<a class="text-link" href="/paketler/">Tüm paketleri karşılaştırın {ARROW}</a></div></div>'
            f'<div class="pkg-grid">{"".join(card(p, featured=(p["no"] == "01")) for p in ps)}</div></section>')


def section_bounds(h, start_marker):
    i = h.find(start_marker)
    if i < 0:
        return None
    depth, j = 0, i
    for m in re.finditer(r'<section\b|</section>', h[i:]):
        depth += 1 if m.group(0) == '<section' else -1
        if depth == 0:
            return i, i + m.end()
    raise ValueError('unbalanced section')


def build_area(key):
    a = AREA_PAGES[key]
    path = os.path.join(ROOT, a['file'])
    h = open(path, encoding='utf-8').read()
    head_end = section_bounds(h, '<section class="page-heading')[1]
    if START in h:
        r0, r1 = h.find(START), h.find(END) + len(END)
    else:
        r0 = head_end
        r1 = h.find('<section class="section container editorial-grid service-preparation">')
    region = h[r0:r1]
    prog = ''
    pb = section_bounds(region, '<section id="proje-programlari"')
    if pb:
        prog = region[pb[0]:pb[1]]
    block = START + caps_section(a) + approach_section(a) + prog + packages_section(key) + END
    h = h[:r0] + block + h[r1:]
    # başlık alanı
    h = re.sub(r'(<section class="page-heading[^"]*">.*?<p class="eyebrow">)[^<]*(</p>)', rf'\g<1>HİZMET ALANI · {a["no"]}\2', h, count=1, flags=re.S)
    h = re.sub(r'(<section class="page-heading[^"]*">.*?<p class="page-lead">).*?(</p>)', lambda m: m.group(1) + esc(a['lead']) + m.group(2), h, count=1, flags=re.S)
    d = esc(a['meta'])
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{d}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{d}">', h, count=1)
    h = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{d}">', h, count=1)
    open(path, 'w', encoding='utf-8').write(h)


def build_index():
    path = os.path.join(ROOT, 'hizmetler/index.html')
    h = open(path, encoding='utf-8').read()
    head_end = section_bounds(h, '<section class="page-heading')[1]
    if START in h:
        r0, r1 = h.find(START), h.find(END) + len(END)
    else:
        r0, r1 = head_end, h.find('<section class="section container program-section">')
    cards = []
    for key in AREA_ORDER:
        a = AREA_PAGES[key]
        url = '/' + a['file'][:-len('index.html')]
        tags = ''.join(f'<li>{esc(t)}</li>' for t, _ in a['caps'][:4])
        npk = len([p for p in PACKAGES if p['area'] == key])
        cards.append(f'<article class="svc-card"><span class="cap-no">{a["no"]}</span><h2><a href="{url}">{esc(a["name"])}</a></h2>'
                     f'<p class="svc-card-tag">{esc(a["tagline"])}</p><p>{esc(a["lead"].split(". ")[0].rstrip("."))}.</p><ul>{tags}</ul>'
                     f'<div class="svc-card-foot"><a class="text-link" href="{url}">Alanı inceleyin {ARROW}</a><span>{npk} paket</span></div></article>')
    band = ('<section class="container pkg-band"><div><p class="eyebrow">HAZIR PAKETLER</p><h2>Kapsamı, süresi ve teslimi belli<br>bir başlangıç mı arıyorsunuz?</h2>'
            '<p>Hizmet alanlarımızdaki sık talep edilen işleri dokuz pakete dönüştürdük. İlk Adım 1.900 TL sabit ücretlidir (KDV dahil); diğer paketler için yazılı teklif hazırlıyoruz.</p></div>'
            f'<div class="pkg-band-actions"><a class="button button-light" href="/paketler/">Paketleri inceleyin {ARROW}</a><a class="text-link" href="/paketler/ilk-adim/">İlk Adım · 1.900 TL {ARROW}</a></div></section>')
    block = START + f'<section class="section container"><div class="svc-grid">{"".join(cards)}</div></section>' + band + END
    h = h[:r0] + block + h[r1:]
    h = re.sub(r'(<section class="page-heading container">.*?<p class="page-lead">).*?(</p>)',
               lambda m: m.group(1) + 'Beş alanda çalışıyoruz. Her alanda kurumunuzun ihtiyacını anlamaktan başlıyor, işin gerektirdiği uzmanlığı bir araya getiriyor ve sonucu birlikte değerlendiriyoruz.' + m.group(2), h, count=1, flags=re.S)
    h = re.sub(r'(<section class="page-heading container">.*?<h1>).*?(</h1>)', r'\g<1>Beş hizmet alanı,<br>tek bir çalışma anlayışı.\2', h, count=1, flags=re.S)
    open(path, 'w', encoding='utf-8').write(h)


if __name__ == '__main__':
    for k in AREA_ORDER:
        build_area(k)
    build_index()
    print('built', len(AREA_ORDER) + 1, 'pages')
