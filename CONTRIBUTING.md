# Lab Ekleme Rehberi 🚩

Bu repoya katkı = **kendi mini CTF laboratuvarını** eklemek. Aşağıdaki akış
komite duyurusundaki sözleşmenin aynısı.

## 0. Önce senaryonu onaylat (özelden)

Kod yazmadan önce şunları komite grubunda / özelden Fevzi'ye ilet:

- **Alan:** Web · Ağ · OSINT · Binary/Pwn · Tersine Mühendislik · Kripto · Adli Bilişim · AI Güvenliği · Diğer
- **Senaryo:** hayal gücüne dayalı kısa kurgu (görsel/hikâye ekleyebilirsin)
- **Kabaca teknik plan:** hangi 2 zafiyet, 2 flag nereden çıkacak, hangi servisler

Onaylaşınca geliştirmeye başla. Takıldığın her yerde yaz, beraber çözeriz.

## 1. Kabul kriterleri (sözleşme)

| # | Kural |
|---|-------|
| 1 | Lab **Docker ile lokalde** ayağa kalkmalı: `docker compose up -d --build` yeter |
| 2 | **En az 2 FARKLI zafiyet** içermeli (ör. IDOR + SSTI; iki ayrı sınıf) |
| 3 | Çözüme giden **en az 2 flag** olmalı, format `TUGA{...}` |
| 4 | `lab.yml`'ye flag'in **düz metnini ASLA** yazma — yalnızca `sha256` hash'i |
| 5 | Senaryo ve arayüz **Türkçe**; içerik yasal ve özgün olmalı |
| 6 | Lab lokalde / izinli ortamda çalışacak; internete açık servis varsaymamalı |

## 2. Lab klasörünü oluştur

En kolayı **`labs/sablon-lab/`'ı kopyalayıp** içini değiştirmek — çalışan bir örnek:
Flask + tek container, 1 IDOR + 1 SSTI zafiyeti, 2 flag.

```bash
cp -r labs/sablon-lab labs/benim-labim
cd labs/benim-labim
# app.py / Dockerfile / docker-compose.yml → kendi senaryonla değiştir
# lab.yml → doldur (aşağıda), 'sablon: true' satırını SİL
```

Zorunlu dosyalar: `lab.yml`, `docker-compose.yml`, `Dockerfile` (+ kaynak), `README.md`.
`COZUM.md` opsiyonel (eklersen tepesine SPOILER uyarısı koy).

### lab.yml şeması

```yaml
slug: benim-labim            # klasör adıyla AYNI
baslik: "Lab başlığın"
alan: Web                    # yukarıdaki 9 alandan biri (birebir yaz)
zorluk: Kolay                # Kolay | Orta | Zor
yazar: github-kullanici-adin
senaryo: >
  2-3 cümlelik kurgu.
zafiyetler:                  # en az 2, farklı sınıflar
  - "IDOR — yetkisiz nesne erişimi"
  - "SSTI — şablon enjeksiyonu"
flaglar:                     # en az 2; SADECE sha256 hash
  - ipucu: "Çözene doğru yön gösteren kısa ipucu"
    sha256: "..."            # python3 scripts/flag_hash.py 'TUGA{...}'
  - ipucu: "İkinci flag ipucu"
    sha256: "..."
port: 8080                   # docker compose ile açtığın ana port
etiketler: [idor, ssti]      # opsiyonel
```

**Flag hash'ini üret** (flag'i terminal geçmişine yazmadan):
```bash
python3 scripts/flag_hash.py            # gizli sorar
# veya
python3 scripts/flag_hash.py 'TUGA{ornek}'
```

## 3. Lokalde doğrula

```bash
cd labs/benim-labim && docker compose up -d --build   # kalkıyor mu?
# → zafiyetleri sömür, 2 flag'i de bulabildiğini teyit et
pip install pyyaml
python3 scripts/lab_dogrula.py          # sözleşme denetimi geçmeli
```

## 4. PR aç

```bash
git checkout -b lab/benim-labim
git add labs/benim-labim
git commit -m "lab: benim-labim eklendi"
git push origin lab/benim-labim
# GitHub'da PR aç, şablondaki kutucukları işaretle
```

- CI, PR'da `lab.yml` şemasını ve `docker compose` yapısını denetler.
- Maintainer (İçerik Takımı) 72 saatte bakar; labı lokalde ayağa kaldırıp iki flag'i de doğrular.
- `docs/` ve README katalogu **otomatik** üretilir — onlara dokunma, sadece `labs/` ekle.

## Davranış
Saygılı ol, emeğe saygı duy, tartışmayı lab kalitesi üzerinden yap. Bu repo hepimizin vitrini.
