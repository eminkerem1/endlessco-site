# Hizmet alanları: genel yetkinlik anlatımı.
# Kural: hizmet alanı sayfaları "ne yaptığımızı ve nasıl düşündüğümüzü" anlatır;
# kapsam, süre, teslim ve ücret yalnızca paket sayfalarında yer alır.

AREA_ORDER = ["proje", "egitim", "deneyimsel", "kurumsal", "akademik"]

AREA_PAGES = {
    "proje": {
        "file": "hizmetler/proje-gelistirme/index.html",
        "no": "01",
        "name": "Proje Geliştirme ve Yönetimi",
        "tagline": "Fikirden desteklenen projeye, projeden kalıcı sonuca.",
        "lead": "Bir fikri desteklenebilir bir projeye, desteklenen bir projeyi de iyi yürütülmüş bir çalışmaya dönüştürmek için kurumlarla birlikte çalışıyoruz. Erasmus+, Avrupa Dayanışma Programı, kalkınma ajansları ve ulusal destek programlarında deneyimli bir ekiple ilerliyoruz.",
        "short": "Destek programlarını değerlendirme, proje kurgusu, ortaklık ve uygulama yönetimi.",
        "caps": [
            ("Fırsatları doğru okumak", "Ulusal ve uluslararası destek programlarını kurumunuzun yapısı ve hedefleriyle birlikte değerlendiriyor, gerçekten uygun olan çağrıları ayırıyoruz."),
            ("Proje mantığını kurmak", "Sorunu, hedef grubu, hedefleri ve faaliyetleri birbirine bağlayan; değerlendiricinin kolayca izleyebileceği tutarlı bir proje kurgusu oluşturuyoruz."),
            ("Ortaklığı ve kaynakları planlamak", "Ortaklık yapısını, iş bölümünü, takvimi ve kaynak ihtiyacını gerçekçi bir çerçevede planlamanıza yardımcı oluyoruz."),
            ("Uygulamayı yönetmek", "Kabul edilen projelerde eğitim, atölye, uzman koordinasyonu ve faaliyet takibi gibi işleri program kurallarına uygun biçimde yürütüyoruz."),
            ("Sonuçları görünür kılmak", "Faaliyet kayıtlarını, katılımcı geri bildirimlerini ve elde edilen sonuçları raporlamaya hazır biçimde düzenliyoruz."),
        ],
        "approach": [
            ("Önce uygunluk", "Her fikri her programa uydurmayız. Fikriniz bir çağrıya uygun değilse bunu baştan ve açıkça söyleriz."),
            ("Garanti değil, gerçekçilik", "Hibe kararını değerlendiriciler verir. Biz projenizi olabilecek en tutarlı ve güçlü hâline getirmeye odaklanırız."),
            ("Program kurallarına uyum", "Dış hizmet alımına ilişkin program kuralları neye izin veriyorsa o sınırlar içinde çalışırız; resmî yükümlülükler kurumunuzda kalır."),
        ],
        "who": ["Dernekler ve STK'lar", "Spor kulüpleri ve federasyonlar", "Üniversiteler ve öğrenci toplulukları", "Okullar ve eğitim kurumları", "Kamu kurumları ve yerel yönetimler", "İşletmeler"],
        "meta": "Destek programı seçimi, proje kurgusu, ortaklık planlaması ve uygulama yönetimi: Erasmus+, ESC, kalkınma ajansı ve ulusal programlarda danışmanlık.",
    },
    "egitim": {
        "file": "hizmetler/egitim-programlari/index.html",
        "no": "02",
        "name": "Eğitim Programları",
        "tagline": "Ertesi gün işte kullanılan eğitimler.",
        "lead": "Hazır bir eğitim kataloğundan seçim yaptırmıyoruz. Kurumunuzun gerçek ihtiyacından yola çıkıyor, katılımcıların ertesi gün işinde kullanabileceği uygulamalı eğitimler tasarlıyoruz.",
        "short": "Kuruma özel, uygulamalı eğitimler: dijital yetkinlikler, proje yönetimi ve çalışma becerileri.",
        "caps": [
            ("İhtiyacı netleştirmek", "Eğitimden ne beklendiğini, katılımcıların düzeyini ve işteki gerçek zorlukları önce birlikte tanımlıyoruz."),
            ("Dijital yetkinlikler", "Yapay zekâ araçları, ofis ve iş birliği uygulamaları ve dijital içerik üretimi gibi günlük işi doğrudan hızlandıran becerilere odaklanıyoruz."),
            ("Proje ve planlama becerileri", "Proje Döngüsü Yönetimi (PCM), planlama, izleme ve raporlama becerilerini kurumunuzun kendi örnekleri üzerinden çalışıyoruz."),
            ("İletişim ve çalışma becerileri", "Sunum, zaman yönetimi, problem çözme, girişimcilik ve kültürlerarası iletişim gibi alanlarda uygulamalı oturumlar hazırlıyoruz."),
            ("Eğitmen ve uygulama koordinasyonu", "Konuya uygun eğitmeni görevlendiriyor, materyalleri hazırlıyor ve eğitimin akışını baştan sona yönetiyoruz."),
        ],
        "approach": [
            ("Uygulama ağırlıklı", "Oturumların büyük bölümü, katılımcıların kendi işleri ve gerçek vakalar üzerinde çalıştığı uygulamalardan oluşur."),
            ("Kuruma özel içerik", "Örnekler, alıştırmalar ve vakalar sektörünüze, kurumunuza ve katılımcıların düzeyine göre hazırlanır."),
            ("Ölçülen öğrenme", "Eğitim, katılımcı geri bildirimi ve öğrenme çıktılarıyla değerlendirilir; sonuç kısa bir özetle paylaşılır."),
        ],
        "who": ["Şirketler", "Kamu kurumları", "Üniversiteler", "Okullar ve eğitim kurumları", "STK'lar", "Spor kuruluşları"],
        "meta": "Kurumlara özel, uygulamalı eğitimler: yapay zekâ ve dijital verimlilik, ofis araçları, Proje Döngüsü Yönetimi (PCM), iletişim ve çalışma becerileri.",
    },
    "deneyimsel": {
        "file": "hizmetler/deneyimsel-ogrenme/index.html",
        "no": "03",
        "name": "Deneyimsel Öğrenme",
        "tagline": "Yaşayarak öğrenen ekipler.",
        "lead": "İnsanlar en iyi, yaşadıkları ve üzerine birlikte düşündükleri deneyimlerden öğrenir. Takım, liderlik ve iletişim gelişimini bu ilkeyle; spor bilimleri, rekreasyon ve yaygın eğitim birikimimizle tasarlıyoruz.",
        "short": "Takım gelişimi, liderlik, iş simülasyonları ve açık hava programları.",
        "caps": [
            ("Takım gelişimi", "Ekiplerin iletişimini, güvenini ve birlikte çalışma biçimini ortak görevlerle görünür kılıyor ve geliştiriyoruz."),
            ("Liderlik ve karar alma", "Sorumluluk alma, yetki devri ve belirsizlik altında karar verme davranışlarını güvenli bir deneyim alanında çalışıyoruz."),
            ("İş simülasyonları", "Proje, bütçe, müşteri ve kriz senaryolarıyla gerçek iş kararlarının sonuçlarını risk almadan deneyimletiyoruz."),
            ("Açık hava ve macera temelli programlar", "Açık alanı, öğrenme hedefleriyle yapılandırılmış grup deneyimleri için kullanıyoruz. Programlar kapalı alanda da uygulanabilir."),
            ("Eğitici ve kolaylaştırıcı gelişimi", "Kendi deneyimsel etkinliklerini tasarlamak isteyen eğitimcilere, gençlik çalışanlarına ve antrenörlere yöntem kazandırıyoruz."),
        ],
        "approach": [
            ("Deneyim ve yansıtma", "Her etkinliğin ardından yaşananları birlikte değerlendirir, öğrenilenleri iş hayatına bağlarız."),
            ("Eğlence değil, öğrenme hedefi", "Program, belirlenmiş gelişim hedeflerinden geriye doğru tasarlanır; her etkinliğin bir amacı vardır."),
            ("Güvenlik ve kapsayıcılık", "Yüksek riskli faaliyetlere yer vermez, programı katılımcıların özelliklerine ve uygulama ortamına göre uyarlarız."),
        ],
        "who": ["Şirketler ve ekipleri", "Üniversiteler", "Kamu kurumları", "STK'lar ve gençlik kuruluşları", "Spor kulüpleri", "Eğitimciler ve antrenörler"],
        "meta": "Takım gelişimi, liderlik, iletişim, iş simülasyonları ve açık hava programları: öğrenme hedefli, güvenli ve kapsayıcı deneyimsel eğitim.",
    },
    "kurumsal": {
        "file": "hizmetler/kurumsal-danismanlik/index.html",
        "no": "04",
        "name": "Kurumsal Araştırma ve Danışmanlık",
        "tagline": "Doğru sorular, güvenilir veri, uygulanabilir öneriler.",
        "lead": "İyi kararlar doğru sorularla ve güvenilir veriyle başlar. Kurumların ihtiyaçlarını, paydaşlarının görüşlerini ve yürüttükleri programların sonuçlarını bilimsel yöntemlerle ortaya koyuyoruz.",
        "short": "İhtiyaç ve paydaş araştırmaları, çalıştaylar, izleme ve değerlendirme.",
        "caps": [
            ("İhtiyaç analizi", "Kurumun gelişim alanlarını ve önceliklerini varsayımlara değil, sistematik olarak toplanmış verilere dayanarak belirliyoruz."),
            ("Paydaşları dinlemek", "Çalışanların, katılımcıların ve dış paydaşların beklentilerini anket, görüşme ve odak grup çalışmalarıyla ortaya koyuyoruz."),
            ("Çalıştay ve ortak akıl", "Paydaşları bir araya getiren çalıştaylarla öncelikleri ve çözüm önerilerini birlikte belirlemeye yardımcı oluyoruz."),
            ("İzleme ve değerlendirme", "Proje ve eğitim programlarının hedeflerine ne ölçüde ulaştığını göstergeler ve ölçümlerle değerlendiriyoruz."),
            ("Bulgudan eyleme", "Araştırma sonuçlarını, kurumun uygulayabileceği somut önerilere ve eylem planlarına dönüştürüyoruz."),
        ],
        "approach": [
            ("Yöntemsel dürüstlük", "Verinin desteklemediği genellemeler ve yöntemsel dayanağı olmayan etki iddiaları yapmayız."),
            ("Etik ve gizlilik", "Katılımcıları bilgilendirir, kişisel verileri mevzuata uygun işler ve gizliliği koruruz."),
            ("Karar için yazılan raporlar", "Raporlarımızı rafta kalmak için değil, okuyanın karar verebilmesi için açık ve öz yazarız."),
        ],
        "who": ["Kamu kurumları ve yerel yönetimler", "Üniversiteler", "STK'lar", "Şirketler", "Spor kuruluşları", "Proje yürüten kuruluşlar"],
        "meta": "Kurumlar için ihtiyaç ve paydaş araştırmaları, anket, görüşme ve çalıştaylar, proje ve eğitim programlarının izleme ve değerlendirmesi.",
    },
    "akademik": {
        "file": "hizmetler/akademik-danismanlik/index.html",
        "no": "05",
        "name": "Akademik Danışmanlık",
        "tagline": "Sizin araştırmanız, sizin emeğiniz; doğru yöntemle.",
        "lead": "Lisansüstü öğrencilere, akademisyenlere ve araştırma ekiplerine; araştırmalarını kendi emekleriyle, doğru yöntemle ve güvenle yürütebilmeleri için rehberlik ediyoruz.",
        "short": "Araştırma tasarımı ve yöntem rehberliği, nitel ve nicel veri analizi.",
        "caps": [
            ("Araştırma tasarımı", "Araştırma sorusundan desen, örneklem ve veri toplama planına kadar çalışmanın yöntemsel tutarlılığını birlikte kuruyoruz."),
            ("Ölçme araçları", "Anket, ölçek ve görüşme formlarının seçimi, uyarlanması ve pilot uygulamasında yöntemsel destek veriyoruz."),
            ("Nicel analiz", "İstatistiksel analizleri uygun yöntemle yapıyor; sonuçların ne söylediğini ve neyi söylemediğini açıklıyoruz."),
            ("Nitel analiz", "Görüşme ve doküman verilerinde kodlama, tema oluşturma ve analitik tutarlılık konusunda birlikte çalışıyoruz."),
            ("Yayın ve savunma hazırlığı", "Makale, bildiri ve tez taslaklarınıza yöntemsel geri bildirim veriyor, savunmaya hazırlanmanıza yardımcı oluyoruz."),
        ],
        "approach": [
            ("Akademik dürüstlük", "Tez, makale veya bildiriyi araştırmacı adına yazmaz; veri uydurmaz, bulguları istenen sonuca göre değiştirmeyiz."),
            ("Araştırmacının sahipliği", "Çalışmanın emeği ve bilimsel sorumluluğu araştırmacıya aittir; biz yöntem ve analiz konusunda rehberlik ederiz."),
            ("Danışmanınızın yerine değil", "Resmî tez danışmanlığının yerine geçmez, o süreci tamamlayıcı biçimde destekleriz."),
        ],
        "who": ["Yüksek lisans ve doktora öğrencileri", "Akademisyenler", "Bağımsız araştırmacılar", "Araştırma ekipleri", "Üniversiteler ve araştırma merkezleri"],
        "meta": "Lisansüstü öğrenciler ve araştırmacılar için araştırma tasarımı, yöntem rehberliği, nitel ve nicel veri analizi. Akademik etik ilkelerine bağlı danışmanlık.",
    },
}
