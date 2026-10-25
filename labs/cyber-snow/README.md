# TÜGA CTF - Web Zafiyet Laboratuvarı

Bu proje, TÜGA Komitesi bünyesinde geliştirilmiş temel seviye web güvenlik zaafiyetlerini içeren bir Capture The Flag (CTF) laboratuvarıdır.

## 🎯 İçerilen Zafiyetler & Hedefler

1. **Information Disclosure (Bilgi İfşası):** Kaynak kod incelemesi ile geliştirici yorum satırlarının analizi.
2. **SQL Injection (Auth Bypass):** Giriş formunda kullanıcı girdilerinin filtrelenmemesi sonucu kimlik doğrulama mekanizmasının atlatılması.

## 🚀 Kurulum ve Çalıştırma

### 1. Docker ile (önerilen)
```bash
docker compose up -d --build
# Tarayıcıda: http://localhost:8080
# Kapatmak için: docker compose down
```

### 2. Yerel Ortamda (Python Flask)
```bash
# Sanal ortamı aktifleştirme (Windows)
.\venv\Scripts\Activate.ps1

# Bağımlılıkları yükleme
pip install -r requirements.txt

# Uygulamayı başlatma
python app.py
```

## ⚠️ Uyarı

Lab kasıtlı olarak zafiyetli. Yalnızca localhost'ta / izinli ortamda çalıştır, internete açma. Ayrıntı: [SECURITY.md](../../SECURITY.md).
