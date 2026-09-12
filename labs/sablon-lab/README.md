# 🏢 TÜGA İç Portalı — Şablon Lab (Web / Kolay)

> Bu klasör **kopyalanabilir şablondur**. Kendi labını yaparken bunu kopyala,
> `lab.yml`'yi ve kodu kendi senaryonla değiştir. Ayrıntılı adımlar:
> [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Senaryo
TÜGA'nın küçük bir iç personel portalı. Herkesin notları var, bir de selamlama
özelliği. Portalda **2 farklı web zafiyeti** kasıtlı olarak gizli; her biri bir
flag veriyor. Hedefin: yetkin olmayan yerlere ulaşmak.

## Kurulum
```bash
docker compose up -d --build
# Tarayıcıda:  http://localhost:8080
# Kapatmak için:  docker compose down -v
```

## Hedef
- **2 flag** var, format: `TUGA{...}`
- İki farklı zafiyet: biri **erişim kontrolü**, biri **şablon** ile ilgili.
- Çözdüğünü [katalog sitesindeki](https://fevziegeyurtsevenler.github.io/tuga-ctf-laboratuvarlari/) **flag kontrol** kutusuna yazıp doğrulayabilirsin.

## Uyarı
Bu uygulama eğitim için **kasıtlı zafiyetlidir**. Yalnızca localhost'ta / izinli
lab ortamında çalıştır, internete açma. Ayrıntı: [SECURITY.md](../../SECURITY.md).

<!-- Çözüm anahtarı bakım ekibi için COZUM.md dosyasındadır (spoiler içerir). -->
