"""Hizmet paketleri sayfalarını üretir: /paketler/ ve /paketler/<paket>/.

Kullanım: python3 tools/build_paketler.py
İçerik tools/paketler_data.py dosyasındadır; üst ve alt bölüm kurumsal/index.html sayfasından alınır.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import build, write, esc, breadcrumbs_html, BASE
from paketler_data import PACKAGES, AREAS

ARROW = '<span aria-hidden="true">↗</span>'

def pkg_url(p):
    return f"/paketler/{p['slug']}/"

def contact_url(p):
    return f"/iletisim/?paket={p['no']}"

def price_badge(p):
    if p.get('price'):
        return f'<span class="pkg-price"><strong>{esc(p["price"])}</strong> {esc(p["price_note"])}</span>'
    return '<span class="pkg-price pkg-price-quote">Kuruma özel teklif</span>'

def card(p, featured=False):
    cls = 'pkg-card pkg-card-featured' if featured else 'pkg-card'
    return (f'<article class="{cls}"><div class="pkg-card-top"><span class="pkg-no">{p["no"]}</span>'
            f'<span class="pkg-area">{esc(AREAS[p["area"]]["short"])}</span></div>'
            f'<h3><a href="{pkg_url(p)}">{esc(p["name"])}</a></h3><p>{esc(p["card"])}</p>'
            f'<div class="pkg-card-foot">{price_badge(p)}<a class="text-link" href="{pkg_url(p)}" aria-label="İnceleyin: {esc(p["name"])}">İnceleyin {ARROW}</a></div></article>')

def package_page(p, prev_p, next_p):
    area = AREAS[p['area']]
    crumbs = [("Ana sayfa", "/"), ("Hizmet paketleri", "/paketler/"), (p['name'], pkg_url(p))]
    # accordion
    acc = []
    for i, (t, txt) in enumerate(p['items']):
        acc.append(f'<details id="icerik-{i+1}" class="service-detail"{" open" if i == 0 else ""}><summary><span>{esc(t)}</span>'
                   f'<span class="detail-plus" aria-hidden="true">+</span></summary><div class="detail-copy"><p>{esc(txt)}</p></div></details>')
    deliv = ''.join(f'<li>{esc(d)}</li>' for d in p['deliverables'])
    sidebar = (f'<aside class="service-sidebar pkg-sidebar"><p class="sidebar-caption">{p["no"]} · {esc(p["name"]).upper()}</p>'
               f'<div class="pkg-sidebar-price">{price_badge(p)}</div>'
               f'<div class="service-deliverables"><h3>Teslim aldıklarınız</h3><ul>{deliv}</ul></div>'
               f'<a class="button button-dark service-cta" href="{contact_url(p)}">{esc(p.get("cta", "Teklif isteyin"))} {ARROW}</a>'
               f'<p class="pkg-sidebar-note">{"Ödeme ve görüşme takvimi başvurunuzdan sonra paylaşılır." if p.get("price") else "Teklif talebi sizi herhangi bir taahhüt altına sokmaz."}</p></aside>')
    sections = []
    # format / options / sample
    if p.get('format'):
        rows = ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in p['format'])
        sections.append(f'<div class="pkg-block"><h2>Standart format</h2><dl class="pkg-format">{rows}</dl><p class="pkg-small">{esc(p["format_note"])}</p></div>')
    if p.get('options'):
        opts = ''.join(f'<article><h3>{esc(a)}</h3><p>{esc(b)}</p></article>' for a, b in p['options'])
        sections.append(f'<div class="pkg-block"><h2>{esc(p["options_title"])}</h2><div class="pkg-options">{opts}</div><p class="pkg-small">Seçenekler örnektir; kapsam teklif aşamasında ihtiyacınıza göre belirlenir.</p></div>')
    if p.get('extra'):
        ex = ''.join(f'<article><h3>{esc(a)}</h3><p>{esc(b)}</p></article>' for a, b in p['extra'])
        sections.append(f'<div class="pkg-block"><h2>{esc(p["extra_title"])}</h2><div class="pkg-options">{ex}</div></div>')
    if p.get('sample'):
        rows = ''.join(f'<li><span>{esc(a)}</span>{esc(b)}</li>' for a, b in p['sample'])
        sections.append(f'<div class="pkg-block"><h2>{esc(p["sample_title"])}</h2><ol class="pkg-sample">{rows}</ol><p class="pkg-small">Toplam 240 dakika. Akış, öğrenme hedeflerinize ve grubunuza göre uyarlanır.</p></div>')
    extra_html = ''.join(sections)
    steps = ''.join(f'<li><span class="service-step-number">{i+1:02d}</span><h3>{esc(a)}</h3><p>{esc(b)}</p></li>' for i, (a, b) in enumerate(p['steps']))
    steps_cls = 'service-approach-grid' + (' pkg-steps-4' if len(p['steps']) == 4 else '')
    # boundaries
    bound = []
    if p.get('safety'):
        bound.append('<div class="pkg-bound"><h3>Uzman ekiplerle güvenli ve kapsayıcı uygulamalar</h3>' + ''.join(f'<p>{esc(s)}</p>' for s in p['safety']) + '</div>')
    if p.get('ethics'):
        bound.append(f'<div class="pkg-bound"><h3>{esc(p.get("ethics_title", "Etik ve veri güvenliği"))}</h3><ul>' + ''.join(f'<li>{esc(s)}</li>' for s in p['ethics']) + '</ul></div>')
    if p.get('excluded'):
        bound.append('<div class="pkg-bound"><h3>Hizmete dahil olmayanlar</h3><ul>' + ''.join(f'<li>{esc(s)}</li>' for s in p['excluded']) + '</ul></div>')
    bound.append(f'<div class="pkg-bound pkg-bound-price"><h3>Ücret</h3><p>{esc(p["pricing"])}</p>' + (f'<p class="pkg-small">{esc(p["note"])}</p>' if p.get('note') else '') + '</div>')
    nav = (f'<div class="pkg-pager" role="navigation" aria-label="Diğer paketler"><a href="{pkg_url(prev_p)}"><small>← Önceki paket</small><strong>{prev_p["no"]} · {esc(prev_p["name"])}</strong></a>'
           f'<a href="/paketler/"><small>Tüm paketler</small><strong>9 hizmet paketi</strong></a>'
           f'<a href="{pkg_url(next_p)}"><small>Sonraki paket →</small><strong>{next_p["no"]} · {esc(next_p["name"])}</strong></a></div>')
    main = (f'<main id="main"><section class="page-heading container illustrated-heading"><div class="illustrated-heading-copy">{breadcrumbs_html(crumbs)}'
            f'<p class="eyebrow">{p["no"]} · {esc(area["name"]).upper()}</p><h1>{esc(p["name"])}</h1>'
            f'<p class="pkg-subtitle">{esc(p["title"])}</p><p class="page-lead">{esc(p["lead"])}</p>'
            f'<div class="hero-actions">{price_badge(p)}<a class="button button-dark" href="{contact_url(p)}">{esc(p.get("cta", "Teklif isteyin"))} {ARROW}</a></div></div>'
            f'<figure class="service-heading-art"><img src="{area["art"]}" alt="{esc(area["art_alt"])}" width="800" height="540"></figure></section>'
            f'<section class="section container service-detail-page"><div class="service-audience"><span>Kimler için?</span><p>{esc(p["audience"])}</p></div>'
            f'<div class="service-layout"><div class="service-detail-list"><h2>Hizmetin içeriği</h2>{"".join(acc)}{extra_html}</div>{sidebar}</div></section>'
            f'<section class="service-approach"><div class="container"><div class="section-heading-row"><div><p class="eyebrow">NASIL ÇALIŞIYORUZ?</p><h2>{esc(p.get("steps_title", "Çalışma süreci"))}</h2></div>'
            f'<p>Kapsamı, takvimi ve teslim edilecekleri çalışma başlamadan önce yazılı olarak netleştiriyoruz.</p></div><ol class="{steps_cls}">{steps}</ol></div></section>'
            f'<section class="section container"><div class="section-intro"><p class="eyebrow">KAPSAM VE KOŞULLAR</p><h2>Açık sınırlar, net teslimler.</h2></div><div class="pkg-bounds">{"".join(bound)}</div>{nav}</section>'
            f'<section id="iletisim" class="closing-cta"><div class="container"><div><p class="eyebrow">{p["no"]} · {esc(p["name"]).upper()}</p>'
            f'<h2>{"Fikrinizi birkaç cümleyle anlatın." if p.get("price") else "İhtiyacınızı anlatın, teklifimizi hazırlayalım."}</h2>'
            f'<p>{"Kurumunuzu ve proje fikrinizi yazın; uygunluğu değerlendirip size dönelim." if p.get("price") else "Kurumunuzu, ihtiyacınızı ve varsa düşündüğünüz tarihleri yazın; kapsamı birlikte netleştirip yazılı teklif hazırlayalım."}</p></div>'
            f'<a class="button button-light" href="{contact_url(p)}">{esc(p.get("cta", "Teklif isteyin"))} {ARROW}</a></div></section></main>')
    title = f'{p["name"]}' + (f' · {p["price"]}' if p.get('price') else '') + ' | ENDLESS.CO'
    desc = p['card'] + (f' Ücret: {p["price"]} ({p["price_note"]}).' if p.get('price') else ' Kuruma özel teklif.')
    service_ld = {"@type": "Service", "@id": f"{BASE}{pkg_url(p)}#service", "name": p['name'], "description": p['lead'],
                  "provider": {"@id": f"{BASE}/#organization"}, "areaServed": "TR", "serviceType": AREAS[p['area']]['name']}
    if p.get('price'):
        service_ld["offers"] = {"@type": "Offer", "price": "1500", "priceCurrency": "TRY", "url": f"{BASE}{pkg_url(p)}"}
    return build(pkg_url(p), title, desc, crumbs, main, extra_ld=[service_ld])

def catalog_page():
    crumbs = [("Ana sayfa", "/"), ("Hizmet paketleri", "/paketler/")]
    first = PACKAGES[0]
    featured = (f'<section class="container pkg-feature"><div class="pkg-feature-copy"><p class="eyebrow">01 · BURADAN BAŞLAYIN</p><h2>İlk Adım</h2>'
                f'<p>{esc(first["lead"])}</p><ul class="pkg-checks">' + ''.join(f'<li>{esc(d)}</li>' for d in first['deliverables']) + '</ul></div>'
                f'<div class="pkg-feature-price"><span class="pkg-feature-amount">1.500 TL</span><span>KDV dahil, sabit ücret</span>'
                f'<a class="button button-light" href="/paketler/ilk-adim/">İlk Adım’ı inceleyin {ARROW}</a>'
                f'<a class="text-link" href="/iletisim/?paket=01">Hemen başvurun {ARROW}</a></div></section>')
    groups = []
    for key in ['proje', 'egitim', 'deneyimsel', 'kurumsal', 'akademik']:
        area = AREAS[key]
        ps = [p for p in PACKAGES if p['area'] == key and p['no'] != '01']
        if not ps:
            continue
        groups.append(f'<div class="pkg-group"><div class="pkg-group-head"><h2>{esc(area["name"])}</h2><a class="text-link" href="{area["url"]}">Hizmet alanını inceleyin {ARROW}</a></div>'
                      f'<div class="pkg-grid">{"".join(card(p) for p in ps)}</div></div>')
    how = ('<section class="soft-section section"><div class="container"><div class="section-intro"><p class="eyebrow">NASIL İLERLİYORUZ?</p><h2>Talebinizden teslime<br>dört adım.</h2></div>'
           '<ol class="service-approach-grid pkg-steps-4"><li><span class="service-step-number">01</span><h3>Talebinizi alıyoruz</h3><p>İlgilendiğiniz paketi seçip ihtiyacınızı birkaç cümleyle anlatıyorsunuz.</p></li>'
           '<li><span class="service-step-number">02</span><h3>Kapsamı netleştiriyoruz</h3><p>Amaç, katılımcılar, süre ve teslim edilecekleri birlikte belirliyoruz.</p></li>'
           '<li><span class="service-step-number">03</span><h3>Yazılı teklif</h3><p>İlk Adım dışındaki hizmetler için kapsamı, ücreti ve koşulları içeren teklif hazırlıyoruz.</p></li>'
           '<li><span class="service-step-number">04</span><h3>Uygulama ve teslim</h3><p>İşin gerektirdiği uzmanları görevlendiriyor, çıktıları kontrol edip teslim ediyoruz.</p></li></ol>'
           '<p class="pkg-small pkg-center">İlk Adım diğer hizmetler için ön koşul değildir; ihtiyacınız olan pakete doğrudan başvurabilirsiniz.</p></div></section>')
    main = (f'<main id="main"><section class="page-heading container">{breadcrumbs_html(crumbs)}<p class="eyebrow">HİZMET PAKETLERİ</p>'
            f'<h1>Dokuz hizmet paketi.<br>Net kapsam, net teslim.</h1><p class="page-lead">Proje, eğitim, deneyimsel öğrenme, kurumsal araştırma ve akademik destek alanlarındaki hizmetlerimizi kapsamı ve teslimleri belli paketler hâlinde sunuyoruz. İlk Adım sabit ücretlidir; diğer paketler için ihtiyacınıza göre yazılı teklif hazırlıyoruz.</p></section>'
            f'{featured}<section class="section container pkg-groups">{"".join(groups)}</section>{how}'
            f'<section id="iletisim" class="closing-cta"><div class="container"><div><p class="eyebrow">TEKLİF İSTEYİN</p><h2>Hangi paketin size uygun olduğundan emin değil misiniz?</h2>'
            f'<p>İhtiyacınızı yazın; size en uygun paketi birlikte belirleyelim.</p></div><a class="button button-light" href="/iletisim/">Bize yazın {ARROW}</a></div></section></main>')
    item_list = {"@type": "ItemList", "name": "ENDLESS.CO hizmet paketleri", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f"{BASE}/paketler/{p['slug']}/", "name": p['name']} for i, p in enumerate(PACKAGES)]}
    return build('/paketler/', 'Hizmet Paketleri: Proje, Eğitim ve Araştırma | ENDLESS.CO',
                 'Dokuz hizmet paketi: İlk Adım (1.500 TL, KDV dahil), proje tasarımı, kurumsal eğitim, deneyimsel öğrenme, araştırma, değerlendirme ve akademik destek.',
                 crumbs, main, extra_ld=[item_list])

if __name__ == '__main__':
    n = len(PACKAGES)
    cur = lambda h: h.replace('<a class="nav-direct" href="/paketler/">Paketler</a>', '<a class="nav-direct is-current" href="/paketler/">Paketler</a>', 1)
    for i, p in enumerate(PACKAGES):
        write(pkg_url(p), cur(package_page(p, PACKAGES[i - 1], PACKAGES[(i + 1) % n])))
    write('/paketler/', cur(catalog_page()))
    print('built', n + 1, 'pages')
