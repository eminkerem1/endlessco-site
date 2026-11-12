"""Yasal sayfaları (KVKK aydınlatma metni, çerez politikası, KVKK başvuru) günceller.

Kullanım: python3 tools/build_yasal.py
Sayfanın düzeni korunur; yalnızca <article class="legal-prose"> içeriği, yan menü
bağlantıları, sayfa girişi ve güncelleme tarihi yeniden yazılır.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shell import ROOT

TARIH = '11 Kasım 2026'
A = '<span aria-hidden="true">↗</span>'
MAIL = '<a href="mailto:endlesscotr@gmail.com">endlesscotr@gmail.com</a>'


def table(caption, head, rows):
    th = ''.join(f'<th scope="col">{h}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return (f'<div class="legal-table-wrap" role="region" aria-label="{caption}" tabindex="0"><table class="legal-table">'
            f'<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>')


def sec(i, title, body):
    return f'<section id="{i}"><h2>{title}</h2>{body}</section>'


HAKLAR = ('<ul><li>Kişisel verilerinizin işlenip işlenmediğini öğrenme,</li><li>İşlenmişse buna ilişkin bilgi talep etme,</li>'
          '<li>İşlenme amacını ve amacına uygun kullanılıp kullanılmadığını öğrenme,</li><li>Yurt içinde veya yurt dışında aktarıldığı üçüncü kişileri bilme,</li>'
          '<li>Eksik veya yanlış işlenmişse düzeltilmesini isteme,</li><li>Kanun’un 7. maddesindeki şartlar çerçevesinde silinmesini veya yok edilmesini isteme,</li>'
          '<li>Düzeltme, silme ve yok etme işlemlerinin verilerin aktarıldığı üçüncü kişilere bildirilmesini isteme,</li>'
          '<li>Münhasıran otomatik sistemlerle analiz edilmesi suretiyle aleyhinize bir sonuç ortaya çıkmasına itiraz etme,</li>'
          '<li>Kanuna aykırı işlenmesi sebebiyle zarara uğramanız hâlinde zararın giderilmesini talep etme.</li></ul>')

SIKAYET = ('<p>Başvurunuz reddedilirse, verilen cevabı yetersiz bulursanız veya başvurunuza 30 gün içinde cevap verilmezse; '
           'cevabı öğrendiğiniz tarihten itibaren 30 gün ve her hâlde başvuru tarihinden itibaren 60 gün içinde Kişisel Verileri Koruma Kurulu’na şikâyette bulunabilirsiniz (KVKK m.14).</p>')

# ---------------------------------------------------------------- aydınlatma
AYD_SECTIONS = [
    ('veri-sorumlusu', 'Veri sorumlusu', 'Veri sorumlusu',
     '<p>Bu metin, 6698 sayılı Kişisel Verilerin Korunması Kanunu’nun (“KVKK”) 10. maddesi ve Aydınlatma Yükümlülüğünün Yerine Getirilmesinde Uyulacak Usul ve Esaslar Hakkında Tebliğ uyarınca hazırlanmıştır.</p>'
     f'<p>ENDLESS.CO markasıyla yürütülen faaliyetlerde veri sorumlusu, işletme sahibi <strong>Aleyna ERKADAM</strong>’dır. Adres: Kızılırmak Mahallesi, 1450. Sokak No: 16, Çankaya/Ankara · E-posta: {MAIL}</p>'),
    ('kapsam', 'Bu metnin kapsamı', 'Kapsam',
     '<p>Bu metin; internet sitemizi ziyaret etmeniz, iletişim formunu kullanmanız, bize e-posta göndermeniz ve uzman iş ortaklığı başvurusunda bulunmanız sırasında işlenen kişisel verileri kapsar.</p>'
     '<p>Bir hizmet sözleşmesi kurduğumuzda veya bir araştırma ya da eğitim programı yürüttüğümüzde, o süreçte işlenecek veriler için ayrıca bilgilendirme yaparız.</p>'),
    ('islenen-veriler', 'Hangi kişisel verileri işliyoruz?', 'İşlenen veriler',
     table('İşlenen kişisel veri kategorileri', ['Veri kategorisi', 'Örnek veriler'], [
         ['Kimlik', 'Ad, soyad'],
         ['İletişim', 'E-posta adresi; paylaşırsanız telefon numarası'],
         ['Mesleki ve kurumsal bilgi', 'Kurum adı; uzman başvurularında uzmanlık alanı, deneyim ve paylaştığınız mesleki profil veya portföy bağlantısı'],
         ['Talep bilgisi', 'İlgilendiğiniz paket veya hizmet alanı, proje programı, çalışma alanı, mesajınızın içeriği, isteğe bağlı olarak bizi nereden duyduğunuz'],
         ['İşlem güvenliği', 'IP adresi, işlem tarihi ve saati, tarayıcı bilgisi gibi teknik kayıtlar'],
     ]) +
     '<p>Formda T.C. kimlik numarası, kimlik belgesi veya banka bilgisi istemiyoruz. Lütfen sağlık bilgisi gibi özel nitelikli kişisel verileri ve araştırma katılımcılarına ait kişisel verileri formda veya ilk yazışmada paylaşmayın.</p>'),
    ('toplama-yontemi', 'Verileri nasıl topluyoruz?', 'Toplama yöntemi',
     '<p>Kişisel verileriniz; iletişim formunu doldurmanız veya bize e-posta göndermeniz yoluyla doğrudan sizden, elektronik ortamda toplanır. İşlem güvenliğine ilişkin teknik kayıtlar ise siteyi ziyaret ettiğinizde ve formu gönderdiğinizde, barındırma ve form iletim hizmeti sağlayıcılarının sistemlerinde otomatik yollarla oluşur.</p>'
     '<p>Verileriniz, aşağıda belirtilen amaçlar ve KVKK’nın 5. maddesinde sayılan hukuki sebepler doğrultusunda işlenir.</p>'),
    ('amac-ve-hukuki-sebep', 'İşleme amaçları ve hukuki sebepler', 'Amaçlar ve hukuki sebepler',
     table('İşleme amaçları ve hukuki sebepler', ['İşleme amacı', 'Hukuki sebep'], [
         ['Hizmet talebinizi değerlendirmek, sorularınızı yanıtlamak, görüşme planlamak ve teklif hazırlamak', 'KVKK m.5/2-c: Bir sözleşmenin kurulması veya ifasıyla doğrudan ilgili olması'],
         ['Bir hizmetle doğrudan ilgili olmayan genel sorularınızı yanıtlamak', 'KVKK m.5/2-f: Temel hak ve özgürlüklerinize zarar vermemek kaydıyla veri sorumlusunun meşru menfaati'],
         ['Uzman iş ortaklığı başvurularını değerlendirmek', 'KVKK m.5/2-c: Bir sözleşmenin kurulması veya ifasıyla doğrudan ilgili olması'],
         ['Bilgi güvenliğini sağlamak, istenmeyen ve otomatik gönderimleri önlemek', 'KVKK m.5/2-f: Veri sorumlusunun meşru menfaati'],
         ['Yetkili kurumların taleplerini ve KVKK başvurularını yerine getirmek', 'KVKK m.5/2-ç: Veri sorumlusunun hukuki yükümlülüğü'],
         ['Olası uyuşmazlıklarda hakların tesisi, kullanılması ve korunması', 'KVKK m.5/2-e: Bir hakkın tesisi, kullanılması veya korunması için zorunlu olması'],
     ]) +
     '<p>Verilerinizi pazarlama amacıyla kullanmıyor, size ticari elektronik ileti göndermiyoruz. Yukarıdaki işlemler açık rızanıza dayanmadığı için sizden ayrıca açık rıza istemiyoruz.</p>'),
    ('alici-gruplari', 'Verileri kimlere ve hangi amaçla aktarıyoruz?', 'Aktarım ve alıcılar',
     table('Aktarılan alıcı grupları ve amaçlar', ['Alıcı grubu', 'Aktarım amacı'], [
         ['İşin yürütülmesinde görev alacak uzmanlar ve eğitmenler (yurt içi)', 'Talebinize uygun teklif ve hizmet hazırlığı; yalnızca işin gerektirdiği bilgiler paylaşılır'],
         ['Bilişim hizmet sağlayıcıları: FormSubmit (form iletimi), Google LLC (e-posta), GitHub, Inc. (site barındırma)', 'Formun iletilmesi, e-posta yazışmalarının yürütülmesi ve sitenin yayınlanması; bu sağlayıcılar verileri bizim adımıza ve hizmetleri kapsamında işler'],
         ['Yetkili kamu kurum ve kuruluşları, hukuk danışmanları', 'Kanuni yükümlülüklerin yerine getirilmesi ve hakların korunması'],
     ])),
    ('yurt-disi', 'Yurt dışına aktarım', 'Yurt dışına aktarım',
     '<p>Form iletimi, e-posta ve site barındırma için kullandığımız hizmet sağlayıcıların sunucuları Türkiye dışında bulunmaktadır. Bu nedenle formla veya e-postayla ilettiğiniz kimlik, iletişim, talep ve işlem güvenliği verileriniz, yalnızca bu hizmetlerin sunulması amacıyla yurt dışına aktarılır.</p>'
     '<p>Yurt dışına aktarım, KVKK’nın 9. maddesi ve Kişisel Verilerin Yurt Dışına Aktarılmasına İlişkin Usul ve Esaslar Hakkında Yönetmelik hükümlerine tabidir. Hangi hizmet sağlayıcılarla çalıştığımızı ve aktarımın dayanağını öğrenmek için bize yazabilirsiniz.</p>'),
    ('saklama', 'Verileri ne kadar süre saklıyoruz?', 'Saklama süreleri',
     table('Saklama süreleri', ['Veri', 'Saklama süresi'], [
         ['Sözleşmeye dönüşmeyen talepler ve yazışmalar', 'Son yazışma tarihinden itibaren en fazla 2 yıl'],
         ['Sonuçlanan uzman iş ortaklığı başvuruları (iş birliği kurulmazsa)', 'Değerlendirmenin tamamlanmasından itibaren en fazla 2 yıl'],
         ['Sözleşmeye dönüşen talepler', 'Sözleşme süresince ve ticari ve vergisel kayıtlar için mevzuatta öngörülen süreler boyunca (ticari defter ve belgeler için 10 yıl)'],
         ['Hizmet sağlayıcıların teknik kayıtları', 'İlgili sağlayıcının güvenlik ve saklama politikalarında belirtilen süreler'],
     ]) +
     '<p>Süre dolduğunda veya işleme amacı ortadan kalktığında verileriniz silinir, yok edilir veya anonim hâle getirilir. Bir uyuşmazlık söz konusuysa ilgili kayıtlar, uyuşmazlık sonuçlanana kadar saklanabilir.</p>'),
    ('haklariniz', 'Haklarınız', 'Haklarınız',
     '<p>KVKK’nın 11. maddesi uyarınca bize başvurarak:</p>' + HAKLAR +
     f'<p>Başvuru yöntemleri, başvuruda bulunması gereken bilgiler ve cevap süresi <a href="/kvkk-basvuru/">KVKK Başvuru</a> sayfasında yer alır.</p>' + SIKAYET),
    ('degisiklikler', 'Bu metindeki değişiklikler', 'Değişiklikler',
     '<p>Veri işleme süreçlerimiz veya mevzuat değiştiğinde bu metni güncelleriz. Güncel metin her zaman bu sayfada yayımlanır; son güncelleme tarihi sayfanın başında yer alır.</p>'),
]

AYD_SOURCES = ('<details class="legal-sources"><summary>Mevzuat ve kaynaklar</summary>'
               f'<a class="text-link" href="https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6698&amp;MevzuatTur=1&amp;MevzuatTertip=5" target="_blank" rel="noopener noreferrer">6698 sayılı Kişisel Verilerin Korunması Kanunu {A}</a>'
               f'<a class="text-link" href="https://www.kvkk.gov.tr/Icerik/4132/aydinlatma-yukumlulugunun-yerine-getirilmesinde-uyulacak-usul-ve-esaslar-hakkinda-teblig" target="_blank" rel="noopener noreferrer">Aydınlatma Yükümlülüğü Tebliği {A}</a>'
               f'<a class="text-link" href="https://www.kvkk.gov.tr/Icerik/7938/Standart-Sozlesmeler-ve-Baglayici-Sirket-Kurallarina-Iliskin-Dokumanlar-Hakkinda-Kamuoyu-Duyurusu" target="_blank" rel="noopener noreferrer">KVKK — Yurt dışına aktarım belgeleri {A}</a></details>')

# ---------------------------------------------------------------- çerez
CEREZ_SECTIONS = [
    ('kisaca', 'Kısaca', 'Kısaca',
     '<p><strong>ENDLESS.CO internet sitesi çerez kullanmaz.</strong> Sitede reklam, ziyaretçi analizi veya takip aracı bulunmaz; tarayıcınıza herhangi bir bilgi kaydetmeyiz. Bu nedenle sitede çerez onayı istenmez.</p>'),
    ('kapsam', 'Bu politikanın kapsamı', 'Kapsam',
     '<p>Bu politika, veri sorumlusu Aleyna ERKADAM’ın ENDLESS.CO markasıyla yayımladığı internet sitesinde çerez ve benzeri teknolojilerin kullanımını açıklar. Çerezler, ziyaret ettiğiniz siteler tarafından tarayıcınıza kaydedilen küçük metin dosyalarıdır.</p>'),
    ('teknik-kayitlar', 'Barındırma altyapısının teknik kayıtları', 'Teknik kayıtlar',
     '<p>Sitemiz GitHub Pages altyapısında yayınlanır. Siteyi ziyaret ettiğinizde GitHub, hizmetin güvenliğini sağlamak ve kötüye kullanımı önlemek amacıyla IP adresi, istek zamanı ve tarayıcı bilgisi gibi teknik kayıtları kendi sistemlerinde tutar. Bu kayıtlar tarayıcınıza yerleştirilen çerezler değildir.</p>'
     '<p>Bu işleme ilişkin ayrıntılar <a href="/kvkk-aydinlatma-metni/">KVKK Aydınlatma Metni</a>’nde yer alır.</p>'),
    ('form-ve-baglantilar', 'İletişim formu ve dış bağlantılar', 'Form ve dış bağlantılar',
     '<p>İletişim formu, FormSubmit hizmeti aracılığıyla gönderilir; gönderim tarayıcınıza çerez kaydetmez. Sitedeki e-posta, sosyal medya veya resmî kurum bağlantılarını açtığınızda ilgili sitelerin kendi çerez ve gizlilik politikaları geçerli olur.</p>'),
    ('gelecek', 'Çerez kullanmaya başlarsak', 'İleride',
     '<p>İleride ziyaretçi analizi gibi zorunlu olmayan çerezler kullanmaya karar verirsek, bunları açık rızanızı almadan çalıştırmayız. Bu durumda sitede bir tercih paneli sunar ve bu politikayı güncelleriz.</p>'),
    ('tarayici', 'Tarayıcı ayarlarınız', 'Tarayıcı ayarları',
     '<p>Tarayıcınızın gizlilik ayarlarından çerezleri ve site verilerini dilediğiniz zaman görüntüleyebilir, silebilir veya engelleyebilirsiniz.</p>'),
    ('iletisim', 'İletişim ve haklarınız', 'İletişim',
     f'<p>Sorularınız için {MAIL} adresine yazabilirsiniz. Kişisel verilerinize ilişkin haklarınızı kullanmak için <a href="/kvkk-basvuru/">KVKK Başvuru</a> sayfasını inceleyebilirsiniz.</p>'),
]
CEREZ_SOURCES = ('<details class="legal-sources"><summary>Mevzuat ve kaynaklar</summary>'
                 f'<a class="text-link" href="https://www.kvkk.gov.tr/Icerik/7353/Cerez-Uygulamalari-Hakkinda-Rehber" target="_blank" rel="noopener noreferrer">KVKK — Çerez Uygulamaları Hakkında Rehber {A}</a>'
                 f'<a class="text-link" href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener noreferrer">GitHub — Gizlilik açıklaması {A}</a></details>')


def rewrite(path, sections, sources, lead, title_note=None):
    fp = os.path.join(ROOT, path)
    h = open(fp, encoding='utf-8').read()
    body = ''.join(sec(i, t, b) for i, t, _, b in sections) + sources
    h = re.sub(r'<article class="legal-prose">.*?</article>', f'<article class="legal-prose">{body}</article>', h, count=1, flags=re.S)
    nav = ''.join(f'<a href="#{i}">{s}</a>' for i, _, s, _ in sections)
    h = re.sub(r'(<aside class="legal-sidebar"><p class="eyebrow">BU SAYFADA</p><nav aria-label="Sayfa içeriği">).*?(</nav>)', lambda m: m.group(1) + nav + m.group(2), h, count=1, flags=re.S)
    h = re.sub(r'(<section class="page-heading container">.*?<p class="page-lead">).*?(</p>)', lambda m: m.group(1) + lead + m.group(2), h, count=1, flags=re.S)
    h = re.sub(r'<span>Son güncelleme: [^<]*</span>', f'<span>Son güncelleme: {TARIH}</span>', h)
    open(fp, 'w', encoding='utf-8').write(h)


def update_basvuru():
    fp = os.path.join(ROOT, 'kvkk-basvuru/index.html')
    h = open(fp, encoding='utf-8').read()
    h = re.sub(r'<span>Son güncelleme: [^<]*</span>', f'<span>Son güncelleme: {TARIH}</span>', h)
    if 'id="haklar"' not in h:
        haklar = sec('haklar', 'Hangi hakları kullanabilirsiniz?', '<p>KVKK’nın 11. maddesi uyarınca:</p>' + HAKLAR)
        h = h.replace('<article class="legal-prose">', '<article class="legal-prose">' + haklar, 1)
        h = h.replace('<nav aria-label="Sayfa içeriği">', '<nav aria-label="Sayfa içeriği"><a href="#haklar">Haklarınız</a>', 1)
    if 'id="kurula-sikayet"' not in h:
        sik = sec('kurula-sikayet', 'Kişisel Verileri Koruma Kurulu’na şikâyet', SIKAYET)
        h = h.replace('<details class="legal-sources">', sik + '<details class="legal-sources">', 1)
        h = re.sub(r'(<nav aria-label="Sayfa içeriği">.*?)(</nav>)', r'\1<a href="#kurula-sikayet">Kurula şikâyet</a>\2', h, count=1, flags=re.S)
    h = h.replace('Yazılı başvuru için güncel yazışma adresini endlesscotr@gmail.com üzerinden öğrenebilirsiniz.', 'Yazılı başvurunuzu Kızılırmak Mahallesi, 1450. Sokak No: 16, Çankaya/Ankara adresine gönderebilirsiniz.', 1)
    h = h.replace('Elektronik başvuru ve iletişim adresi: endlesscotr@gmail.com.', 'Yazışma adresi: Kızılırmak Mahallesi, 1450. Sokak No: 16, Çankaya/Ankara. Elektronik başvuru ve iletişim adresi: endlesscotr@gmail.com.', 1)
    open(fp, 'w', encoding='utf-8').write(h)


# ---------------------------------------------------------------- kullanım koşulları
KK_SECTIONS = [
    ('kapsam', 'Kapsam', 'Kapsam',
     '<p>Bu koşullar, Aleyna ERKADAM’a ait şahıs işletmesi tarafından ENDLESS.CO markasıyla işletilen internet sitesinin kullanımına ilişkindir. Siteyi kullanarak bu koşulları kabul etmiş sayılırsınız.</p>'),
    ('icerik', 'Sitedeki bilgilerin niteliği', 'Bilgilerin niteliği',
     '<p>Sitedeki hizmet açıklamaları ve Bilgi Merkezi yazıları genel bilgilendirme amaçlıdır; kurumunuza özel profesyonel danışmanlığın yerine geçmez.</p>'
     '<p>Destek programlarının koşulları, takvimleri ve bütçeleri ilgili kurumlar tarafından değiştirilebilir. Başvuru öncesinde her zaman programın resmî sayfası ve güncel rehberi esas alınmalıdır.</p>'),
    ('paketler', 'Hizmet paketleri, fiyatlar ve teklifler', 'Paketler ve fiyatlar',
     '<p>Hizmet paketlerinin kapsam, süre ve teslim açıklamaları tanıtım amaçlıdır. Bir hizmetin kapsamı, süresi ve ücreti, taraflar arasında yazılı olarak onaylanan teklif veya sözleşmeyle kesinleşir.</p>'
     '<p>İlk Adım paketinin sitede belirtilen ücreti KDV dahildir. Fiyatlar önceden duyurularak değiştirilebilir; değişiklik, daha önce yazılı olarak onaylanmış teklifleri etkilemez.</p>'
     '<p>Destek programlarına yapılan başvuruların sonucu ilgili kurumların değerlendirmesine bağlıdır. ENDLESS.CO, bir başvurunun kabul edileceğini veya belirli bir destek tutarının alınacağını garanti etmez.</p>'),
    ('fikri-mulkiyet', 'Fikrî mülkiyet', 'Fikrî mülkiyet',
     '<p>Sitedeki metinler, görseller, logo ve tasarım ENDLESS.CO’ya aittir veya izinle kullanılmaktadır. Kaynak gösterilerek ve bağlantı verilerek kısa alıntı yapılabilir. İçeriğin tamamının veya önemli bir bölümünün çoğaltılması, ticari amaçla kullanılması veya değiştirilerek yayımlanması için yazılı izin gerekir.</p>'),
    ('dis-baglantilar', 'Dış bağlantılar', 'Dış bağlantılar',
     '<p>Site, kamu kurumları ve diğer kuruluşların sayfalarına bağlantılar içerir. Bu sayfaların içeriği, güncelliği ve gizlilik uygulamaları ilgili kuruluşların sorumluluğundadır.</p>'),
    ('sorumluluk', 'Sorumluluğun sınırı', 'Sorumluluğun sınırı',
     '<p>Sitedeki bilgiler özenle hazırlanır ve düzenli olarak gözden geçirilir; ancak her bilginin her an eksiksiz ve güncel olduğu garanti edilemez. Sitenin kesintisiz veya hatasız çalışacağı taahhüt edilmez. Sitedeki bilgilere dayanılarak verilen kararlardan doğabilecek zararlardan, kanunen sınırlandırılamayan haller saklı kalmak üzere, sorumluluk kabul edilmez.</p>'),
    ('kisisel-veriler', 'Kişisel veriler', 'Kişisel veriler',
     '<p>İletişim formu veya e-posta yoluyla paylaştığınız kişisel verilerin nasıl işlendiği <a href="/kvkk-aydinlatma-metni/">KVKK Aydınlatma Metni</a>’nde açıklanmıştır. Site çerez kullanmaz; ayrıntılar <a href="/cerez-politikasi/">Çerez Politikası</a>’ndadır.</p>'),
    ('degisiklik', 'Değişiklikler ve uygulanacak hukuk', 'Değişiklikler ve hukuk',
     '<p>Bu koşullar güncellenebilir; güncel metin bu sayfada yayımlandığı tarihte yürürlüğe girer.</p>'
     '<p>Bu koşullara Türk hukuku uygulanır. Uyuşmazlıklarda Ankara mahkemeleri ve icra daireleri yetkilidir; tüketici işlemlerinde tüketici mevzuatındaki görev ve yetki kuralları saklıdır.</p>'),
    ('iletisim', 'İletişim', 'İletişim',
     f'<p>Bu koşullarla ilgili sorularınız için {MAIL} adresine yazabilirsiniz. Yazışma adresi: Kızılırmak Mahallesi, 1450. Sokak No: 16, Çankaya/Ankara.</p>'),
]
KK_DESC = 'ENDLESS.CO sitesinin kullanım koşulları: bilgilerin niteliği, paketler ve fiyatlar, fikrî mülkiyet, dış bağlantılar ve uygulanacak hukuk.'


def build_kullanim():
    src = open(os.path.join(ROOT, 'cerez-politikasi/index.html'), encoding='utf-8').read()
    h = src.replace('/cerez-politikasi/', '/kullanim-kosullari/')
    h = h.replace('Çerez Politikası | ENDLESS.CO', 'Kullanım Koşulları | ENDLESS.CO')
    h = h.replace('"name": "Çerez Politikası", "item"', '"name": "Kullanım Koşulları", "item"')
    h = h.replace('<span aria-current="page">Çerez Politikası</span>', '<span aria-current="page">Kullanım Koşulları</span>')
    h = h.replace('<h1>Çerez Politikası</h1>', '<h1>Kullanım Koşulları</h1>')
    h = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*', lambda m: m.group(1) + KK_DESC, h)
    h = re.sub(r'("description": ")[^"]*', lambda m: m.group(1) + KK_DESC, h)
    h = h.replace('<span>Veri sorumlusu: Aleyna ERKADAM</span>', '<span>İşletme sahibi: Aleyna ERKADAM</span>')
    # yasal menüde aktif bağlantı ve dış kaynak bloğu
    h = re.sub(r'<details class="legal-sources">.*?</details>', '', h, flags=re.S)
    os.makedirs(os.path.join(ROOT, 'kullanim-kosullari'), exist_ok=True)
    open(os.path.join(ROOT, 'kullanim-kosullari/index.html'), 'w', encoding='utf-8').write(h)
    rewrite('kullanim-kosullari/index.html', KK_SECTIONS, '',
            'Sitemizi kullanırken geçerli olan koşulları sade bir dille açıklıyoruz.')
    fp = os.path.join(ROOT, 'kullanim-kosullari/index.html')
    h = open(fp, encoding='utf-8').read()
    h = re.sub(r'<span>Son güncelleme: [^<]*</span>', '<span>Son güncelleme: 12 Kasım 2026</span>', h)
    open(fp, 'w', encoding='utf-8').write(h)


CEREZ_DESC = 'ENDLESS.CO sitesi çerez ve takip aracı kullanmaz. Siteyi ziyaret ettiğinizde oluşan teknik kayıtları ve dış bağlantıları açıklıyoruz.'


def fix_cerez_meta():
    fp = os.path.join(ROOT, 'cerez-politikasi/index.html')
    h = open(fp, encoding='utf-8').read()
    h = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*', lambda m: m.group(1) + CEREZ_DESC, h)
    h = re.sub(r'("description": ")[^"]*', lambda m: m.group(1) + CEREZ_DESC, h)
    open(fp, 'w', encoding='utf-8').write(h)


if __name__ == '__main__':
    rewrite('kvkk-aydinlatma-metni/index.html', AYD_SECTIONS, AYD_SOURCES,
            'İnternet sitemizi ziyaret ettiğinizde, iletişim formunu kullandığınızda veya bize e-posta gönderdiğinizde kişisel verilerinizin nasıl işlendiğini açıklıyoruz.')
    rewrite('cerez-politikasi/index.html', CEREZ_SECTIONS, CEREZ_SOURCES,
            'Sitemiz çerez kullanmaz. Bu sayfada, siteyi ziyaret ettiğinizde hangi teknik kayıtların oluştuğunu ve dış bağlantıların nasıl çalıştığını açıklıyoruz.')
    update_basvuru()
    fix_cerez_meta()
    build_kullanim()
    print('legal pages updated')
