-- Son Vardiya - Lab Veritabanı Şeması ve Örnek Veriler
-- Şirket: NovaSis Teknoloji A.Ş. - Dahili Personel Portalı

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS employee_profiles;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS announcements;
DROP TABLE IF EXISTS archive_records;
DROP TABLE IF EXISTS support_tickets;

-- Giriş yapılabilen kullanıcı hesapları (parametrize sorgularla kullanılır, bilerek zafiyetsiz)
-- password_hash: werkzeug generate_password_hash(..., method="pbkdf2:sha256") çıktısıdır.
-- Düz metin şifre HİÇBİR yerde saklanmaz; login sırasında check_password_hash ile doğrulanır.
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    display_name TEXT NOT NULL
);

-- Personel dizininin sorguladığı tablo (SQL Injection burada)
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    note TEXT
);

-- Personel profil sayfası için ek, normal şirket bilgileri (departman, dahili,
-- e-posta, hesap durumu). 'note' alanı BURADA YOKTUR - gizli not yalnızca
-- employees.note alanında tutulur ve profil sayfalarında hiç render edilmez.
CREATE TABLE employee_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    username TEXT,              -- yalnızca giriş hesabı olan personelde dolu (elif.demir, mehmet.kaya)
    department TEXT NOT NULL,
    internal_ext TEXT NOT NULL,
    email TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Aktif'
);

-- Doküman/arşiv (IDOR burada). category/status/updated_at yalnızca
-- görünüm zenginliği için eklenmiştir; sahiplik/erişim mantığını etkilemez.
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    owner_username TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    image_filename TEXT,
    category TEXT NOT NULL DEFAULT 'Genel',
    status TEXT NOT NULL DEFAULT 'Onaylandı',
    updated_at TEXT NOT NULL DEFAULT '2026-08-01'
);

-- İkinci aşamanın anahtarı: zarf üzerindeki koddan ulaşılan gizli kayıt.
-- 'code' bilinmeden bu tabloya normal gezinmeyle ulaşılamaz.
CREATE TABLE archive_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

-- Portal ana sayfasındaki duyuru panosu (salt-okunur, parametrize; zafiyet içermez)
CREATE TABLE announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'Genel',
    posted_by TEXT NOT NULL,
    posted_at TEXT NOT NULL
);

-- IT Destek biletleri (salt-okunur, parametrize; zafiyet içermez)
CREATE TABLE support_tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_no TEXT UNIQUE NOT NULL,
    requester_name TEXT NOT NULL,
    subject TEXT NOT NULL,
    description TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    opened_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- ---- Kullanıcılar ----
-- Oyuncu hesabı: elif.demir / elif123 (README'de belirtilir, çözüm için gereken tek hesap).
-- mehmet.kaya yalnızca gerçekçilik amaçlı bir "gerçek personel" hesabıdır (10-14 numaralı
-- dokümanların sahibidir); çözüm zincirinin bir parçası değildir.
-- Şifreler hash'lenmiş olarak saklanır: elif123 / mehmet123 (bkz. README - Oyuncu Başlangıç Bilgisi).
INSERT INTO users (username, password_hash, display_name) VALUES
    ('mehmet.kaya', 'pbkdf2:sha256:1000000$4IMlz53h9vJwyUai$4f97b09cc701a289b0f5d111e6eae1e8c0b1253cd47e90605282ce1ad77264ba', 'Mehmet Kaya'),
    ('elif.demir', 'pbkdf2:sha256:1000000$yx6mJwxLXHR7XGxa$10e937925fb0b792479d8eef05bf8265129aa8ef7932c72af4429fefd62dc52c', 'Elif Demir');

-- ---- Çalışanlar (SQLi hedefi) ----
-- name ve role arama sonuçlarında normalde görünür; "note" alanı arayüzde hiç
-- gösterilmez, sadece UNION-based injection ile sorguya eklenerek çekilebilir.
-- İlk 9 kayıt (id 1-9) mevcut/orijinal laba aittir ve İÇERİKLERİ DEĞİŞTİRİLMEMİŞTİR.
INSERT INTO employees (name, role, note) VALUES
    ('Ahmet Yılmaz', 'Genel Müdür', 'Kamera kayıtlarını yedekledim. Güvenlik kamera arşiv referansı: 4471. İlgili kayıt Sistem Yönetimi arşivinde tutuluyor. TUGA{sqli_personel_arsivi}'),
    ('Mehmet Kaya', 'Yazılım Geliştirici', 'Yıllık izin formunu İK''ya iletti.'),
    ('Elif Demir', 'Muhasebe Uzmanı', 'Q3 bütçe raporunu tamamladı, onay bekleniyor.'),
    ('Burak Şahin', 'Sistem Yöneticisi', 'Gece yapılan bakım sonrası sunucu loglarını kontrol etti, anormallik bulunamadı.'),
    ('Zeynep Aydın', 'İnsan Kaynakları', 'Yeni personel oryantasyon programını planladı.'),
    ('Cem Öztürk', 'Satış Temsilcisi', 'Müşteri görüşmesi notları CRM''e işlendi.'),
    ('Selin Kara', 'Pazarlama Uzmanı', 'Sosyal medya içerik takvimi güncellendi.'),
    ('Emre Yıldız', 'Destek Uzmanı', 'Destek bileti #582 çözümlendi.'),
    ('Deniz Aksoy', 'Güvenlik Görevlisi', 'Gece vardiyası devir teslim notunu bıraktı, olağan bir gece geçtiğini belirtti.');

-- Ek personel (id 10-14) - yalnızca portalı doldurmak için, çözüm zincirine dahil değil.
INSERT INTO employees (name, role, note) VALUES
    ('Ayşe Çelik', 'İK Uzmanı', 'Yeni işe alım süreci için mülakat takvimini güncelledi.'),
    ('Kerem Doğan', 'Finans Analisti', 'Q3 bütçe dosyasını muhasebe ile paylaştı.'),
    ('Mert Kaan Sezer', 'BT Destek Uzmanı', 'Yazıcı sürücü güncellemesini 3. katta tamamladı.'),
    ('Gizem Arslan', 'Hukuk Danışmanı', 'Tedarikçi sözleşmesi taslağını inceledi.'),
    ('Onur Tekin', 'Satın Alma Uzmanı', 'Donanım tedarik sürecini takip ediyor.');

-- ---- Personel profil bilgileri (departman, dahili, e-posta, durum) ----
-- 'note' alanı burada YOKTUR; gizli not sadece employees.note içindedir ve
-- hiçbir profil şablonunda render edilmez.
INSERT INTO employee_profiles (employee_id, username, department, internal_ext, email, status) VALUES
    (1,  NULL,           'Genel Müdürlük',        '1001', 'ahmet.yilmaz@novasis.com.tr',   'Aktif'),
    (2,  'mehmet.kaya',  'Yazılım Geliştirme',    '2114', 'mehmet.kaya@novasis.com.tr',    'Aktif'),
    (3,  'elif.demir',   'Muhasebe',              '2231', 'elif.demir@novasis.com.tr',     'Aktif'),
    (4,  NULL,           'Bilgi Teknolojileri',   '2010', 'burak.sahin@novasis.com.tr',    'Aktif'),
    (5,  NULL,           'İnsan Kaynakları',      '2305', 'zeynep.aydin@novasis.com.tr',   'Aktif'),
    (6,  NULL,           'Satış',                 '2412', 'cem.ozturk@novasis.com.tr',     'Aktif'),
    (7,  NULL,           'Pazarlama',             '2450', 'selin.kara@novasis.com.tr',     'Aktif'),
    (8,  NULL,           'BT Destek',             '2020', 'emre.yildiz@novasis.com.tr',    'Aktif'),
    (9,  NULL,           'Güvenlik',              '2500', 'deniz.aksoy@novasis.com.tr',    'Aktif'),
    (10, NULL,           'İnsan Kaynakları',      '2308', 'ayse.celik@novasis.com.tr',     'Aktif'),
    (11, NULL,           'Muhasebe',              '2235', 'kerem.dogan@novasis.com.tr',    'Aktif'),
    (12, NULL,           'BT Destek',             '2022', 'mertkaan.sezer@novasis.com.tr', 'Aktif'),
    (13, NULL,           'Hukuk',                 '2601', 'gizem.arslan@novasis.com.tr',   'Aktif'),
    (14, NULL,           'Satın Alma',            '2701', 'onur.tekin@novasis.com.tr',     'İzinli');

-- ---- Dokümanlar (IDOR hedefi) ----
-- mehmet.kaya, "Arşiv" sayfasında yalnızca kendi dokümanlarını (10-14) görür.
-- 4471 numaralı kayıt "sistem" hesabına ait olup listede hiç görünmez, ancak
-- /documents/view?id=4471 endpoint'i sahiplik kontrolü yapmadığı için doğrudan
-- ID ile erişilebilir. Bu 6 kayıt (10-15, 4471) ORİJİNAL laba aittir ve
-- İÇERİKLERİ DEĞİŞTİRİLMEMİŞTİR.
INSERT INTO documents (id, owner_username, title, content, image_filename, category, status, updated_at) VALUES
    (10, 'mehmet.kaya', 'Sprint Planlama Notları',
     'Bu hafta backlog önceliklendirmesi yapıldı. Yeni özellik: bildirim modülü. Sonraki sprint için tahmini kapasite 34 story point.',
     NULL, 'Yazılım', 'Onaylandı', '2026-08-27'),
    (11, 'mehmet.kaya', 'IT Ekipman Talep Formu',
     'Talep edilen: 1x monitör, 1x mekanik klavye. Talep no: #2291. Durum: Onay bekleniyor.',
     NULL, 'BT', 'İncelemede', '2026-08-22'),
    (12, 'mehmet.kaya', 'Personel Toplantı Notları',
     'Haftalık ekip toplantısında görüşülenler: sprint retrospektifi, yeni işe alım süreci, ofis düzeni ile ilgili geri bildirimler.',
     NULL, 'Genel', 'Onaylandı', '2026-08-20'),
    (13, 'mehmet.kaya', 'Sistem Bakım Raporu',
     'Gece 02:00-04:00 arasında yapılan planlı ağ bakımı tamamlandı. Bakım sırasında bazı segmentlerde kısa süreli bağlantı kesintileri kaydedildi. Detaylı log Sistem Yönetimi''nde saklanmaktadır.',
     NULL, 'BT', 'Onaylandı', '2026-08-31'),
    (14, 'mehmet.kaya', 'Arşiv Erişim Politikası',
     'Şirket içi arşiv sistemi, departmanlara göre erişim seviyelerine ayrılmıştır. Güvenlik kamerası kayıtları ve güvenlik olay raporları yalnızca Sistem Yönetimi ekibine açıktır ve normal personel listesinde görüntülenmez. Bu tür kayıtlara erişim gerektiğinde resmi talep süreci izlenmelidir.',
     NULL, 'Güvenlik', 'Onaylandı', '2026-07-14'),
    (15, 'elif.demir', 'Q3 Bütçe Özeti',
     'Departman harcamaları bütçenin %94''ünde. Detaylar ek dosyada. Q4 planlaması önümüzdeki hafta başlayacak.',
     NULL, 'Finans', 'Onaylandı', '2026-08-30'),
    (4471, 'sistem', 'Güvenlik Kamera Kaydı - Koridor B, Yönetim Katı',
     'ERİŞİM SEVİYESİ: Sistem Yönetimi
KAYIT NO: 4471
KAMERA: Koridor-B / Yönetim Katı
TARİH: 31.08.2026

Aşağıda ilgili zaman aralığına ait kamera kareleri listelenmiştir:
14:31:08 · 14:33:12 · 14:33:19 · 14:33:47 · 14:34:02 · 14:41:55

Bu kayıt normal şartlarda yalnızca Sistem Yönetimi ekibine açıktır.',
     'img/cctv_4471.jpg', 'Güvenlik', 'Kısıtlı', '2026-08-31');

-- Ek dokümanlar (ana hikâyeyle ilgisiz, portalı doldurmak için). Farklı kayıt
-- numaraları kullanır; 4471 ile karışmaz.
INSERT INTO documents (id, owner_username, title, content, image_filename, category, status, updated_at) VALUES
    (1042, 'elif.demir', 'Q3 Bütçe Raporu',
     'Departman bazlı Q3 harcama kalemleri ve bütçe sapma analizi ekte özetlenmiştir. Genel toplamda bütçenin %94''ü kullanılmıştır. En yüksek sapma BT donanım kaleminde görülmüştür (+%6). Q4 için revize bütçe teklifi finans komitesine sunulacaktır.',
     NULL, 'Finans', 'Onaylandı', '2026-08-29'),
    (1187, 'kerem.dogan', 'Fatura Onay Listesi',
     'Ağustos ayına ait tedarikçi faturaları onay sürecine alınmıştır. Toplam 18 fatura incelenmiş, 16''sı onaylanmış, 2''si eksik evrak nedeniyle tedarikçiye iade edilmiştir. Onaylanan faturalar muhasebe sistemine işlenmiştir.',
     NULL, 'Finans', 'Onaylandı', '2026-08-28'),
    (1305, 'cem.ozturk', 'Masraf Beyanı',
     'Saha ziyareti kapsamında yapılan ulaşım ve konaklama masrafları beyan edilmiştir. Toplam tutar: 4.250 TL. Fiş ve fatura görselleri ekte yer almaktadır. Onay için bölge müdürüne iletilmiştir.',
     NULL, 'Finans', 'İncelemede', '2026-08-25'),
    (1876, 'ayse.celik', 'Personel İzin Çizelgesi',
     'Eylül-Ekim dönemi için departman bazlı yıllık izin planlaması hazırlanmıştır. Kritik proje dönemlerinde eş zamanlı izin çakışmaması için ekip liderleriyle ön görüşme yapılmıştır.',
     NULL, 'İK', 'Onaylandı', '2026-08-24'),
    (2041, 'burak.sahin', 'Varlık Sayım Formu',
     'Yıllık BT donanım sayımı tamamlanmıştır. Toplam 214 masaüstü, 96 dizüstü, 38 yazıcı ve 12 sunucu envanterde kayıtlıdır. 3 adet kullanılmayan monitör hurdaya ayrılmak üzere işaretlenmiştir.',
     NULL, 'BT', 'Onaylandı', '2026-08-19'),
    (2291, 'burak.sahin', 'Yıllık Sistem Bakım Raporu',
     'Sunucu odası yıllık bakım ve soğutma sistemi kontrolü tamamlanmıştır. UPS bataryaları test edilmiş, biri değiştirilmek üzere işaretlenmiştir. Bir sonraki planlı bakım Kasım ayında yapılacaktır.',
     NULL, 'BT', 'Onaylandı', '2026-08-12'),
    (2560, 'mertkaan.sezer', 'VPN Kullanım Kılavuzu',
     'Uzaktan çalışan personel için VPN istemcisi kurulum ve bağlantı adımlarını içerir. Bağlantı sorunlarında önce istemcinin güncel sürümde olduğu kontrol edilmelidir. Devam eden sorunlar için IT Destek''e bilet açılması istenir.',
     NULL, 'BT', 'Onaylandı', '2026-07-30'),
    (2934, 'gizem.arslan', 'Bilgi Güvenliği Politikası',
     'Şirket içi bilgi güvenliği politikası; şifre yönetimi, cihaz kullanımı, uzaktan erişim ve veri sınıflandırma kurallarını kapsar. Tüm personelin yıllık farkındalık eğitimini tamamlaması zorunludur.',
     NULL, 'Güvenlik', 'Onaylandı', '2026-06-15'),
    (3184, 'gizem.arslan', 'Tedarikçi Değerlendirme Formu',
     'Donanım tedarikçilerinin teslim süresi, kalite ve fiyat performansı çeyreklik olarak değerlendirilmiştir. İki tedarikçi performans iyileştirme planına alınmıştır.',
     NULL, 'Satın Alma', 'İncelemede', '2026-08-21'),
    (3401, 'zeynep.aydin', 'Toplantı Tutanağı',
     'Departman yöneticileri haftalık koordinasyon toplantısı tutanağı. Gündem: yeni işe alım süreçleri, ofis yerleşim planı, Q4 hedefleri ön değerlendirmesi.',
     NULL, 'Genel', 'Onaylandı', '2026-08-26'),
    (4102, 'deniz.aksoy', 'Kamera Sistemleri Bakım Raporu',
     'Bina genelindeki güvenlik kamerası sisteminin periyodik bakımı tamamlanmıştır. Tüm kayıt cihazları çalışır durumdadır. Depolama kapasitesi %61 doluluk seviyesindedir.',
     NULL, 'Güvenlik', 'Onaylandı', '2026-08-10'),
    (4210, 'burak.sahin', 'Sunucu Bakım Planı',
     'Ekim ayı için planlanan sunucu bakım takvimi ve etkilenecek servislerin listesi. Bakım pencereleri gece saatlerinde, düşük kullanım aralığında planlanmıştır.',
     NULL, 'BT', 'Onaylandı', '2026-08-09'),
    (4398, 'gizem.arslan', 'İş Sürekliliği Planı',
     'Olağandışı durumlarda (elektrik kesintisi, sistem arızası, doğal afet) kritik iş süreçlerinin sürdürülmesine yönelik plan. Sorumlu ekipler ve iletişim zinciri ekte belirtilmiştir.',
     NULL, 'Yönetim', 'Onaylandı', '2026-05-20'),
    (4890, 'onur.tekin', 'Donanım Teslim Formu',
     'Yeni işe başlayan personele teslim edilen dizüstü bilgisayar, adaptör ve erişim kartı kayıtlarını içerir. Teslimatlar İK oryantasyon süreciyle koordineli yürütülmüştür.',
     NULL, 'Satın Alma', 'Onaylandı', '2026-08-05'),
    (5021, 'onur.tekin', 'Envanter Listesi',
     'Depo ve ofis genelindeki sabit kıymetlerin güncel envanter listesi. Yıl sonu sayımı öncesi ön kontrol amacıyla hazırlanmıştır.',
     NULL, 'Satın Alma', 'Onaylandı', '2026-07-22');

-- ---- İkinci aşama: zarf üzerindeki koddan ulaşılan kayıt ----
-- Bu tabloya normal gezinmeyle (menü/liste) ulaşılamaz; yalnızca 4471 numaralı
-- kamera kaydındaki zarf üzerinde görünen "4471-B" kodu bilinerek erişilebilir.
INSERT INTO archive_records (code, title, content) VALUES
    ('4471-B', 'Ek Kayıt - Zarf İçeriği',
     'KAYIT NO: 4471-B
İLİŞKİLİ KAYIT: 4471
KATEGORİ: Ek Belge

Koridorda teslim edilen zarfın içeriği, güvenlik biriminin ilk incelemesi sonucunda bu
kayda eklenmiştir. Zarfın üzerindeki referans numarası (4471-B), 4471 numaralı kamera
kaydıyla ilişkilendirilmiştir.

İncelemeye göre teslimat önceden planlanmış görünüyor; zarfın içeriği ve teslim edilen
kişilerin kimliği hâlâ araştırılıyor. Bina giriş kayıtlarında bu şahıslara dair önceki bir
kayıt bulunamadı.

Vaka, ilgili birimlere iletilmiştir.

TUGA{son_vardiyanin_sirri}');

-- ---- Duyuru Panosu ----
-- Portal ana sayfasında görüntülenen, rutin şirket içi duyurular. Olay ile
-- ilgili asıl bildirim, dashboard'da ayrı bir "Olağan Dışı Durum Bildirimi"
-- bileşeninde gösterilir (bkz. portal.html) - burada yalnızca sıradan
-- duyurular yer alır.
INSERT INTO announcements (title, body, category, posted_by, posted_at) VALUES
    (
        'Planlı Ağ Bakımı Tamamlandı',
        'Dün gece 02:00-04:00 saatleri arasında bina ağ altyapısında planlı bakım çalışması yapılmıştır. ' ||
        'Çalışma sırasında bazı sistemlerde kısa süreli bağlantı kesintileri yaşanmış olabilir. ' ||
        'Herhangi bir sorunla karşılaşan çalışanlarımız Sistem Yönetimi ile iletişime geçebilir.',
        'BT', 'Sistem Yönetimi', '2026-08-31 07:50'
    ),
    (
        'Yıllık İzin Takvimi Güncellendi',
        'Yıl sonu izin planlaması için güncel takvim İK portalına yüklenmiştir. ' ||
        'İzin taleplerinizi 15 Eylül''e kadar sisteme girmeniz rica olunur.',
        'İK', 'İnsan Kaynakları', '2026-08-25 09:00'
    ),
    (
        'Ofis Kafeterya Menüsü Yenilendi',
        'Bu ay itibarıyla kafeterya menümüze yeni seçenekler eklendi. Görüş ve önerileriniz için ' ||
        'idari işler birimiyle iletişime geçebilirsiniz.',
        'Genel', 'İdari İşler', '2026-08-18 10:30'
    ),
    (
        'VPN İstemci Güncellemesi Zorunlu',
        'Güvenlik güncellemesi içeren yeni VPN istemci sürümü yayınlanmıştır. Mevcut sürümler 20 Eylül''den ' ||
        'itibaren desteklenmeyecektir. Güncelleme adımları için VPN Kullanım Kılavuzu''na bakınız.',
        'BT', 'Sistem Yönetimi', '2026-08-29 11:15'
    ),
    (
        'Yemekhane Çalışma Saatleri Değişti',
        'Yemekhane, 1 Eylül itibarıyla hafta içi 11:30-14:30 saatleri arasında hizmet verecektir. ' ||
        'Değişiklik yoğunluk analizine göre yapılmıştır.',
        'Genel', 'İdari İşler', '2026-08-27 08:40'
    ),
    (
        'Otopark Kart Sistemi Düzenlemesi',
        'Otopark girişlerinde kullanılan personel kartı sistemi güncellenmiştir. Kartını çalıştırmayan ' ||
        'personelin resepsiyon ile iletişime geçmesi rica olunur.',
        'Genel', 'İdari İşler', '2026-08-23 09:10'
    ),
    (
        'Bilgi Güvenliği Farkındalık Eğitimi',
        'Tüm personel için zorunlu yıllık bilgi güvenliği farkındalık eğitimi 10-20 Eylül tarihleri arasında ' ||
        'online platform üzerinden verilecektir. Katılım departman yöneticileri tarafından takip edilecektir.',
        'Güvenlik', 'Bilgi Güvenliği', '2026-08-21 13:00'
    ),
    (
        'Yeni Personel Kartı Uygulaması Başlıyor',
        'Fiziksel kartların yanında mobil personel kartı uygulaması pilot olarak devreye alınmıştır. ' ||
        'Gönüllü katılımcılar İK ile iletişime geçebilir.',
        'İK', 'İnsan Kaynakları', '2026-08-19 10:00'
    ),
    (
        'Q3 Kapanış İşlemleri Takvimi',
        'Q3 mali kapanış işlemleri için son masraf beyanı ve fatura giriş tarihi 5 Eylül olarak belirlenmiştir. ' ||
        'Gecikmeli girişler Q4''e aktarılacaktır.',
        'Finans', 'Muhasebe', '2026-08-28 14:20'
    ),
    (
        'Yazıcı Bakım Çalışması - 3. Kat',
        '3. kat ortak alan yazıcısında planlı bakım çalışması yapılacaktır. Çalışma süresince 2. kat ' ||
        'yazıcısının kullanılması rica olunur.',
        'BT', 'BT Destek', '2026-08-17 15:30'
    ),
    (
        'E-posta Sistemi Güncellemesi',
        'Kurumsal e-posta sisteminde performans iyileştirmesi amacıyla bakım çalışması yapılacaktır. ' ||
        'Çalışma sırasında gelen kutusuna kısa süreli erişim gecikmeleri yaşanabilir.',
        'BT', 'Sistem Yönetimi', '2026-08-14 07:00'
    ),
    (
        'Ofis Giriş Prosedürü Hatırlatması',
        'Ziyaretçi girişlerinde resepsiyonda kayıt zorunludur. Personel kartını unutan çalışanların ' ||
        'güvenlik biriminden geçici kart talep etmesi gerekmektedir.',
        'Güvenlik', 'Güvenlik', '2026-08-11 09:45'
    );

-- ---- IT Destek Biletleri ----
-- Rutin BT destek talepleri. Ana çözüm zincirine dahil değildir; portalın
-- gerçekçi hissini güçlendirmek için eklenmiştir.
INSERT INTO support_tickets (ticket_no, requester_name, subject, description, priority, status, opened_at, updated_at) VALUES
    ('541', 'Cem Öztürk', 'VPN bağlantı problemi',
     'Uzaktan çalışma sırasında VPN bağlantısı sürekli düşüyor. İstemci en güncel sürüme güncellendi, sorun devam ediyor.',
     'Orta', 'İşlemde', '2026-08-24 09:12', '2026-08-26 11:00'),
    ('557', 'Selin Kara', 'Yazıcı bağlantısı',
     '3. kat ortak yazıcısına ağ üzerinden bağlanılamıyor. Diğer katlardaki yazıcılar sorunsuz çalışıyor.',
     'Düşük', 'Kapalı', '2026-08-20 10:05', '2026-08-21 09:30'),
    ('563', 'Ayşe Çelik', 'Kartvizit şablonu talebi',
     'Yeni işe başlayan personel için güncel kurumsal kartvizit şablonu talep edilmektedir.',
     'Düşük', 'Kapalı', '2026-08-19 13:40', '2026-08-20 10:15'),
    ('582', 'Emre Yıldız', 'E-posta senkronizasyon problemi',
     'Mobil cihazda kurumsal e-posta hesabı yeni gelen iletileri senkronize etmiyor. Masaüstü istemcisinde sorun yok.',
     'Orta', 'Kapalı', '2026-08-15 08:50', '2026-08-15 16:20'),
    ('601', 'Kerem Doğan', 'Kablosuz ağ bağlantısı',
     'Toplantı odası 2''de kablosuz ağ sinyali zayıf, sık sık bağlantı kopuyor.',
     'Düşük', 'İşlemde', '2026-08-25 11:20', '2026-08-27 09:00'),
    ('614', 'Gizem Arslan', 'Hesap kilitlenmesi',
     'Art arda yanlış şifre denemesi sonrası hesap geçici olarak kilitlendi. Kilit açma talebi.',
     'Yüksek', 'Kapalı', '2026-08-22 14:05', '2026-08-22 14:40'),
    ('631', 'Zeynep Aydın', 'Outlook yapılandırması',
     'Yeni dizüstü bilgisayarda Outlook profili yeniden yapılandırılamıyor, eski e-postalar görünmüyor.',
     'Orta', 'İşlemde', '2026-08-26 10:30', '2026-08-27 08:15'),
    ('644', 'Mert Kaan Sezer', 'VPN istemcisi güncellemesi',
     'Departman genelinde VPN istemcisinin yeni sürüme toplu güncellenmesi talep edilmektedir.',
     'Orta', 'Açık', '2026-08-28 09:00', '2026-08-28 09:00'),
    ('672', 'Onur Tekin', 'Depo ağ erişimi',
     'Depo bölümündeki barkod okuyucu terminali ağa bağlanamıyor, IP ataması kontrol edilmeli.',
     'Orta', 'Açık', '2026-08-29 13:10', '2026-08-29 13:10'),
    ('695', 'Burak Şahin', 'Yedekleme uyarı bildirimi',
     'Gece yedekleme görevinden e-posta uyarısı gelmedi, bildirim listesi kontrol edilmeli.',
     'Düşük', 'İşlemde', '2026-08-30 07:40', '2026-08-30 12:00'),
    ('712', 'Deniz Aksoy', 'Turnike kart okuyucu arızası',
     'Zemin kat yan giriş turnikesindeki kart okuyucu bazı kartları geç okuyor.',
     'Orta', 'Açık', '2026-08-31 08:15', '2026-08-31 08:15'),
    ('728', 'Ahmet Yılmaz', 'Ofis sabit hat arızası',
     'Yönetim katı ofis telefonunda zaman zaman arama sonrası bağlantı kopuyor. Santral tarafında kontrol istenmiştir.',
     'Düşük', 'Açık', '2026-08-29 16:45', '2026-08-29 16:45');
