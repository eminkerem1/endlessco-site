# ENDLESS.CO web sitesi

endlessco.tr sitesinin 11 Kasım 2026 tarihli birebir kopyası. Bu depo **endlessco.com.tr** adresinde test ortamı olarak yayınlanır.

## Test ortamı ayarları (canlıya alırken geri alınacak)

- Tüm sayfalarda `<meta name="robots" content="noindex,nofollow">` (orijinali `index,follow,max-image-preview:large`).
- `robots.txt` tüm siteyi kapatır (orijinali `Allow: /` ve sitemap satırı).
- `CNAME` dosyası yayın alan adını belirler.

Canlıya geçişte bu üç değişiklik geri alınır; ilk commit (`ca336b2`) sitenin orijinal hâlidir.
