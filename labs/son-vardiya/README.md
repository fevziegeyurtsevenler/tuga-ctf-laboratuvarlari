# 🕵️ Son Vardiya

Senaryo tabanlı Web Güvenliği / Web Pentest laboratuvarı. Flask + SQLite + Docker ile izole/local ortamda çalışır.

## Senaryo

Bu sabah **NovaSis Teknoloji A.Ş.** ofisine gelen çalışanlar Genel Müdür **Ahmet Yılmaz**'ı bulamadı. Masasında açık bırakılmış telefonunda 112'yi aramaya çalıştığına dair tamamlanamamış bir çağrı kaydı var.

Elindeki tek araç şirketin dahili **Personel Portalı**. Portalı incele, çalışan kayıtlarını araştır ve Ahmet Yılmaz'ın son vardiyada başına ne geldiğini ortaya çıkar.

## Oyuncu Başlangıç Bilgisi

Labı çözmeye başlamak için aşağıdaki senaryo hesabı kullanılabilir:

| Kullanıcı adı | Şifre |
|---|---|
| `elif.demir` | `elif123` |

Bu hesap, oyuncunun ilk erişim hesabıdır. Diğer personel hesapları (ör. `mehmet.kaya`) çözüm için
gerekli değildir; yalnızca personel dizininde gerçekçilik katmak amacıyla bulunur ve 10-14 numaralı
dokümanların sahibidir.

## Kurulum

```bash
docker compose up --build
```

Tarayıcı: **http://127.0.0.1:5001**

Temiz bir veritabanıyla başlamak için:

```bash
docker compose down -v
docker compose up --build
```

Durdurmak için:

```bash
docker compose down
```

## Çözüm Mantığı (spoiler vermeyen)

Portalda Ahmet Yılmaz'ın kayıp olduğu bilgisiyle başlarsın. Personel dizinindeki arama işlevini incelemek, gizli bir çalışan notunun ortaya çıkarılmasına; notta bulunan kayıt numarası ise normal listede görünmeyen bir dokümana ulaşılmasına götürür.

Kamera kaydındaki görsel kanıt ayrıca dikkatli incelenmelidir. Görsel üzerinde çözümü tarif eden ok, daire veya açıklama bulunmaz.

## Lab Hakkında

Labda iki zincirlenmiş web zafiyeti bulunur:

1. **Union-based SQL Injection** — Personel araması
2. **IDOR / Broken Object Level Authorization** — Doküman görüntüleme

Son aşamada teknik bir exploit yerine kamera görüntüsündeki fiziksel bir referansın keşfedilmesi gerekir.

## Flag Formatı

Labda 2 flag bulunur ve `TUGA{...}` formatındadır.

## Güvenlik Notu

Uygulama bilerek zafiyetli hazırlanmıştır. Yalnızca izole/local eğitim ortamında çalıştırın; internete açık şekilde deploy etmeyin.

Bilinçli olarak zafiyetli bırakılan iki alan (arama ve doküman görüntüleme) dışındaki her şey normal
üretim pratiğine uygun tutulmuştur: kullanıcı şifreleri düz metin değil, `pbkdf2:sha256` ile hash'lenmiş
olarak saklanır (`werkzeug.security`); login sorgusu tamamen parametrizedir; şablonlar Jinja auto-escape
sayesinde XSS'e kapalıdır; container root olmayan bir kullanıcıyla çalışır; servis yalnızca `127.0.0.1`'e
bağlanır. Amaç, oyuncunun "her şey zafiyetli" değil, gerçekçi bir uygulamada belirli, bulunması gereken
zafiyetlerle karşılaştığını hissetmesidir.

## Test

Uygulama ayağa kalktıktan sonra tüm çözüm zincirini (giriş → SQLi → Flag 1 → IDOR → CCTV → Flag 2)
uçtan uca doğrulayan bir smoke test betiği bulunur:

```bash
docker compose up --build -d
bash tests/smoke_test.sh
```

Betik `curl` ile ilerler, her adımda beklenen içeriğin (flag'ler dahil) döndüğünü kontrol eder,
`4471-A`..`4471-Z` gibi yanlış kodların flag sızdırmadığını doğrular ve rate limiting'in
devreye girdiğini teyit eder. Herhangi bir adım başarısız olursa hata koduyla çıkar.

## Kötüye Kullanım Koruması

`/login` ve `/archive/<code>` endpoint'lerinde hafif, bellek-içi bir rate limiter bulunur
(sırasıyla 60 sn'de 8, 15 sn'de 6 istek). Pencere dolunca istekler kendiliğinden serbest kalır —
**kalıcı kilit yoktur**; normal bir oyuncunun birkaç manuel denemesi hiçbir zaman engellenmez.
Amaç yalnızca otomatik/ardışık kaba kuvvet denemelerini yavaşlatmaktır, imkansız kılmak değil.

## Klasör Yapısı

```text
son-vardiya/
├── docker-compose.yml
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   ├── templates/
│   └── static/
│       └── img/
│           └── cctv_4471.jpg
├── database/
│   └── init.sql
├── tests/
│   └── smoke_test.sh
├── README.md
└── WRITEUP.md
```
