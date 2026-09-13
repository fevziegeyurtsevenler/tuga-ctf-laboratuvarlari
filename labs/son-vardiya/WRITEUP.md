# WRITEUP — Son Vardiya (Spoiler İçerir)

## Çözüm Zinciri

```text
Başlangıç hesabı
   ↓
Portal
   ↓
Personel → SQL Injection
   ↓
Gizli note → kayıt no 4471 + Flag 1
   ↓
Arşiv → kayıt no 4471
   ↓
IDOR → yetkisiz kamera dokümanı
   ↓
CCTV görüntüsünü dikkatli incele
   ↓
Zarf üzerindeki 4471-B
   ↓
Kısıtlı arşiv kaydı
   ↓
Flag 2
```

## Adım 1 — Giriş

Oyuncu başlangıç hesabı olarak `elif.demir / elif123` kullanır. Portalda Ahmet Yılmaz'ın bulunamadığına ve telefonunda tamamlanmamış 112 çağrısı olduğuna dair olay bildirimi görülür.

## Adım 2 — SQL Injection

Personel araması `/search?name=` parametresini doğrudan SQL sorgusuna birleştirir:

```sql
SELECT id, name, role FROM employees WHERE name LIKE '%<name>%'
```

Normal sonuçlarda yalnızca `id`, `name` ve `role` gösterilir. `note` alanı arayüzde yer almaz. UNION-based SQL Injection ile saldırgan sorgunun üçüncü sütununu kontrol ederek gizli notu sonuçlara taşıyabilir.

Örnek:

```text
/search?name=' UNION SELECT id, note, role FROM employees WHERE id=1--
```

Ahmet Yılmaz'ın notu içinde iki kritik bilgi bulunur:

- **Flag 1:** `TUGA{sqli_personel_arsivi}`
- **Kamera arşiv referansı:** `4471`

Not artık açıkça 4471'in güvenlik kamera arşiv referansı olduğunu belirttiği için oyuncunun sonraki adımı doğal olarak Arşiv bölümüne yönelir.

## Adım 3 — Arşiv ve IDOR

Arşiv sayfası normalde yalnızca oturum sahibine atanmış dokümanları listeler. Buna ek olarak kullanıcıya kayıt numarası bilinen bir dokümanı görüntüleme alanı sunar.

Buradaki kritik hata `/documents/view?id=<id>` endpoint'indedir. Endpoint yalnızca oturumun açık olup olmadığını kontrol eder; dokümanın `owner_username` değeri ile oturum kullanıcısını karşılaştırmaz.

Bu nedenle oyuncu SQL Injection'dan öğrendiği `4471` numarasını arşivdeki kayıt numarası alanına girerek şu dokümana ulaşabilir:

**Güvenlik Kamera Kaydı - Koridor B, Yönetim Katı**

Bu, labın IDOR / Broken Object Level Authorization aşamasıdır.

## Adım 4 — CCTV Görseli

Dokümanda altı karelik bir CCTV görüntüsü bulunur. Görüntüde üç kişi vardır. 14:33:47 karesinde teslim edilen zarfın üzerinde küçük ancak okunabilir bir referans bulunur:

**4471-B**

Görüntüde bu bilgiyi işaretleyen açıklama, ok veya daire yoktur. Oyuncunun görseli büyütüp incelemesi beklenir.

## Adım 5 — Kısıtlı Arşiv

Bulunan `4471-B` referansı, normal navigasyonda listelenmeyen kısıtlı arşiv kaydına götürür:

```text
/archive/4471-B
```

Kayıt, olayın son parçasını ve ikinci flag'i içerir:

**Flag 2:** `TUGA{son_vardiyanin_sirri}`

## Teknik Notlar

- Login parametrize sorgu kullanır; başlangıç hesabı lab dokümantasyonunda verilir.
- `employees.note` normal sonuçlarda görünmez; SQLi ile çekilebilir.
- `/documents` listesi oturum sahibinin dokümanlarını gösterir; 4471 listede bulunmaz.
- `/documents/view` sahiplik kontrolü yapmadığı için 4471'e IDOR ile erişilebilir.
- CCTV görseli `app/static/img/cctv_4471.jpg` dosyasındadır.
- `archive_records` kod tabanlı ayrı bir tablodur ve normal menüde listelenmez.
- Uygulama başlangıcında gerekli temel tablolar eksikse `init.sql` yeniden uygulanır; bu, eski Docker volume'larında görülebilen `no such table: announcements` benzeri lab kurulum sorunlarını önler.
