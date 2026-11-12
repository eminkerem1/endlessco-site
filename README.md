# ENDLESS.CO web sitesi

endlessco.tr sitesinin 11 Kasım 2026 tarihli birebir kopyası. Bu depo **endlessco.com.tr** adresinde test ortamı olarak yayınlanır.

## Test ortamı ayarları (canlıya alırken geri alınacak)

- Tüm sayfalarda `<meta name="robots" content="noindex,nofollow">` (orijinali `index,follow,max-image-preview:large`).
- `robots.txt` tüm siteyi kapatır (orijinali `Allow: /` ve sitemap satırı).
- `CNAME` dosyası yayın alan adını belirler.
- `app.js` içindeki `aliasHosts` listesinden `endlessco.com.tr` ve `www.endlessco.com.tr` çıkarıldı (orijinal site bu adresleri endlessco.tr'ye yönlendiriyordu).

## İletişim formu

Form, FormSubmit (formsubmit.co) AJAX uç noktası üzerinden endlesscotr@gmail.com adresine gönderir. İlk gönderimde FormSubmit bu adrese bir **etkinleştirme e-postası** yollar; e-postadaki bağlantıya tıklanana kadar form gönderimleri teslim edilmez.

Canlıya geçişte bu değişiklikler `python3 tools/go_live.py` ile tek adımda geri alınır (CNAME de endlessco.tr olur). Ardından endlessco.tr DNS'i GitHub Pages'e yönlendirilir; endlessco.com.tr için Metunic panelinden endlessco.tr'ye alan adı yönlendirmesi tanımlanır. İlk commit (`ca336b2`) sitenin orijinal hâlidir.

## Paket sayfaları

`/paketler/` ve dokuz paket sayfası `tools/build_paketler.py` ile üretilir. Paket metinleri `tools/paketler_data.py` dosyasındadır; metni orada değiştirip `python3 tools/build_paketler.py` çalıştırmak yeterlidir. Menü ve alt bilgi `kurumsal/index.html` sayfasından kopyalanır.

## Sayfaları yeniden üretme ve tema

Sıra: `python3 tools/build_paketler.py && python3 tools/build_hizmetler.py && python3 tools/build_en.py && python3 tools/build_yasal.py && python3 tools/apply_theme.py`

`apply_theme.py` her sayfanın `<body>` etiketine `kv` sınıfını ekler ve kapanış bandını slogan karolu düzene çevirir. Tema CSS'i `styles.css` sonundaki "ENDLESS.CO tema 2026-11" bölümündedir (koyu degrade başlık paneli, mono etiketler; mono yazı tipi `assets/fonts/`). Eski görünüme dönmek için bu bölümü silmek yeterlidir.

## Diğer dosyalar

- `llms.txt`: yapay zekâ asistanları için site özeti (hizmetler, paketler, rehberler).
- `kullanim-kosullari/`: `tools/build_yasal.py` ile üretilir.
- Sekme simgeleri: `assets/favicon-96.png`, `assets/apple-touch-icon.png`, kökte `favicon.ico`.
