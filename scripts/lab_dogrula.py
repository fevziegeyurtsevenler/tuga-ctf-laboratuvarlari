#!/usr/bin/env python3
"""labs/*/lab.yml dosyalarını sözleşmeye göre doğrular.

CI'da her PR'da çalışır; lokalde de çalıştırabilirsin:
    python3 scripts/lab_dogrula.py
Hata bulursa çıkış kodu 1 olur ve neyin yanlış olduğunu Türkçe yazar.
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("HATA: PyYAML gerekli →  pip install pyyaml")

KOK = Path(__file__).resolve().parent.parent
LABS = KOK / "labs"

ALANLAR = {"Web", "Ağ", "OSINT", "Binary/Pwn", "Tersine Mühendislik",
           "Kripto", "Adli Bilişim", "AI Güvenliği", "Diğer"}
ZORLUKLAR = {"Kolay", "Orta", "Zor"}
ZORUNLU = ["slug", "baslik", "alan", "zorluk", "yazar", "senaryo", "zafiyetler", "flaglar", "port"]
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMPOSE = ("docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml")


def lab_dogrula(klasor: Path) -> list:
    h = []  # hatalar
    ad = klasor.name
    ymlp = klasor / "lab.yml"
    if not ymlp.exists():
        return [f"{ad}: lab.yml yok"]
    try:
        d = yaml.safe_load(ymlp.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return [f"{ad}/lab.yml: YAML okunamadı ({e})"]
    if not isinstance(d, dict):
        return [f"{ad}/lab.yml: kök bir sözlük (key: value) olmalı"]

    for k in ZORUNLU:
        if k not in d or d[k] in (None, "", [], {}):
            h.append(f"{ad}/lab.yml: '{k}' alanı zorunlu ve dolu olmalı")

    if d.get("slug") and d["slug"] != ad:
        h.append(f"{ad}/lab.yml: slug ('{d['slug']}') klasör adıyla ('{ad}') aynı olmalı")
    if d.get("alan") and d["alan"] not in ALANLAR:
        h.append(f"{ad}/lab.yml: alan '{d.get('alan')}' geçersiz. Seçenekler: {', '.join(sorted(ALANLAR))}")
    if d.get("zorluk") and d["zorluk"] not in ZORLUKLAR:
        h.append(f"{ad}/lab.yml: zorluk '{d.get('zorluk')}' geçersiz. Seçenekler: Kolay, Orta, Zor")

    zaf = d.get("zafiyetler")
    if isinstance(zaf, list):
        if len(zaf) < 2:
            h.append(f"{ad}/lab.yml: en az 2 zafiyet listelenmeli (şu an {len(zaf)})")
    elif "zafiyetler" in d:
        h.append(f"{ad}/lab.yml: zafiyetler bir liste olmalı")

    fl = d.get("flaglar")
    if isinstance(fl, list):
        if len(fl) < 2:
            h.append(f"{ad}/lab.yml: en az 2 flag olmalı (şu an {len(fl)})")
        for i, f in enumerate(fl, 1):
            if not isinstance(f, dict):
                h.append(f"{ad}/lab.yml: flag #{i} 'ipucu' ve 'sha256' içeren bir sözlük olmalı")
                continue
            s = str(f.get("sha256", "")).lower()
            if not SHA256_RE.match(s):
                h.append(f"{ad}/lab.yml: flag #{i} geçerli bir sha256 hash içermeli (64 hex). "
                         f"Üret: python3 scripts/flag_hash.py 'TUGA{{...}}'")
            if not f.get("ipucu"):
                h.append(f"{ad}/lab.yml: flag #{i} bir 'ipucu' içermeli")
            if "flag" in f or "bayrak" in f:
                h.append(f"{ad}/lab.yml: flag #{i} DÜZ METİN flag içeriyor — sadece sha256 hash yaz")
    elif "flaglar" in d:
        h.append(f"{ad}/lab.yml: flaglar bir liste olmalı")

    if "port" in d and not isinstance(d.get("port"), int):
        h.append(f"{ad}/lab.yml: port bir sayı olmalı (ör. 8080)")

    if not any((klasor / c).exists() for c in COMPOSE):
        h.append(f"{ad}: docker-compose.yml yok (lab lokalde `docker compose up` ile kalkmalı)")
    if not (klasor / "README.md").exists():
        h.append(f"{ad}: README.md yok (senaryo + kurulum anlatılmalı)")
    return h


def main():
    if not LABS.exists():
        sys.exit("HATA: labs/ klasörü yok")
    lab_dizinleri = sorted(p for p in LABS.iterdir() if p.is_dir() and (p / "lab.yml").exists())
    if not lab_dizinleri:
        print("Uyarı: hiç lab bulunamadı (labs/*/lab.yml).")
        return
    tum_hatalar = []
    for k in lab_dizinleri:
        tum_hatalar += lab_dogrula(k)
    if tum_hatalar:
        print("❌ Doğrulama başarısız:\n")
        for x in tum_hatalar:
            print("  •", x)
        print(f"\n{len(tum_hatalar)} sorun bulundu.")
        sys.exit(1)
    print(f"✅ {len(lab_dizinleri)} lab doğrulandı, sözleşmeye uygun.")


if __name__ == "__main__":
    main()
