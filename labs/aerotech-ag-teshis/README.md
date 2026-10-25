# 🌐 AeroTech: Ağ Teşhis Portalı (Siber Güvenlik CTF Labı)

**TÜGA Siber Güvenlik Komitesi** proje çalışmaları kapsamında geliştirilmiş, konteynerize bir web güvenlik labı.

Misafir olarak girdiğin ağ teşhis konsolunda önce yönetici yetkisi al, sonra sunucuda komut çalıştır. **2 flag** var, format `TUGA{...}`.

## 🚀 Hızlı Kurulum

```bash
docker compose up -d --build
```

Erişim adresi: `http://localhost:5000`

Kapatmak için:
```bash
docker compose down
```

## ⚠️ Uyarı

Lab kasıtlı olarak zafiyetli. Yalnızca localhost'ta / izinli ortamda çalıştır, internete açma. Ayrıntı: [SECURITY.md](../../SECURITY.md).
