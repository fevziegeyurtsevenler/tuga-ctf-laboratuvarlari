# ☩ Siber Mühür // SOC & DFIR Lab

Bu laboratuvar; temel ve orta seviye SOC analistlerinin tehdit avcılığı (threat hunting), web/sistem günlüğü analizi ve ağ adli bilişimi (network forensics) pratiklerini test etmek amacıyla kurgulanmış senaryo tabanlı bir CTF/DFIR platformudur.

## Senaryo Özeti
* **Vaka ID:** INC-8492-X
* **Öncelik:** P1
* **Tehdit Aktörü:** APT-Erebos
* **Hedef:** Societas Tenebris Arşivleri

Arşiv sunucusunda saptanan olağandışı kaynak kullanımı sonrası inceleme başlatılmıştır. Saldırganın web katmanından sızarak sunucuda komut koşturduğu, elde ettiği verileri ağ üzerinden dışarı sızdırdığı ve kalıcılık (persistence) sağladığı tespit edilmiştir. Katılımcının görevi sunulan kanıtlar üzerinden saldırı zincirini (Kill Chain) adım adım aydınlatmaktır.

## Kurulum
```bash
docker compose up -d
# Tarayıcıda:  http://localhost:8080
# Kapatmak için:  docker compose down -v
```

## Hedef
- **4 flag (mühür)** var, format: `TUGA{...}`
- Dört farklı zafiyet/analiz aşaması: **LFI, Anti-Forensics, DNS Tünelleme, Systemd Kalıcılığı**.
- Çözdüğünü [katalog sitesindeki](https://fevziegeyurtsevenler.github.io/tuga-ctf-laboratuvarlari/) **flag kontrol** kutusuna yazıp doğrulayabilirsin.

## Uyarı
Bu uygulama eğitim için tasarlanmıştır ve içerisinde simüle edilmiş arka kapılar/zafiyetler barındırır. Yalnızca localhost'ta / izinli lab ortamında çalıştır, internete açma. Ayrıntı: [SECURITY.md](../../SECURITY.md).

<!-- Çözüm anahtarı bakım ekibi için COZUM.md dosyasındadır (spoiler içerir). -->

