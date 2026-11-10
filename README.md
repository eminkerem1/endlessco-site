# ENDLESS.CO web sitesi

endlessco.tr sitesinin 11 Kasım 2026 tarihli birebir kopyası. Bu depo **endlessco.com.tr** adresinde test ortamı olarak yayınlanır.

## Test ortamı ayarları (canlıya alırken geri alınacak)

- Tüm sayfalarda `<meta name="robots" content="noindex,nofollow">` (orijinali `index,follow,max-image-preview:large`).
- `robots.txt` tüm siteyi kapatır (orijinali `Allow: /` ve sitemap satırı).
- `CNAME` dosyası yayın alan adını belirler.
- `app.js` içindeki `aliasHosts` listesinden `endlessco.com.tr` ve `www.endlessco.com.tr` çıkarıldı (orijinal site bu adresleri endlessco.tr'ye yönlendiriyordu).

## İletişim formu

Form, FormSubmit (formsubmit.co) AJAX uç noktası üzerinden endlesscotr@gmail.com adresine gönderir. İlk gönderimde FormSubmit bu adrese bir **etkinleştirme e-postası** yollar; e-postadaki bağlantıya tıklanana kadar form gönderimleri teslim edilmez.

Canlıya geçişte bu değişiklikler geri alınır; ilk commit (`ca336b2`) sitenin orijinal hâlidir.
