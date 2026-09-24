"""lab.yml alanlarını TÜGA sözleşmesine göre yerelde kontrol eder."""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML gerekli: pip install pyyaml")

KOK = Path(__file__).resolve().parents[1]
d = yaml.safe_load((KOK / "lab.yml").read_text(encoding="utf-8"))
ALANLAR = {
    "Web",
    "Ağ",
    "OSINT",
    "Binary/Pwn",
    "Tersine Mühendislik",
    "Kripto",
    "Adli Bilişim",
    "AI Güvenliği",
    "Diğer",
}
ZORLUKLAR = {"Kolay", "Orta", "Zor"}
ZORUNLU = [
    "slug",
    "baslik",
    "alan",
    "zorluk",
    "yazar",
    "senaryo",
    "zafiyetler",
    "flaglar",
    "port",
]
h = []
ad = KOK.name
for k in ZORUNLU:
    if k not in d or d[k] in (None, "", [], {}):
        h.append(f"eksik {k}")
if d.get("slug") != ad:
    h.append(f"slug klasör adıyla aynı olmalı ({d.get('slug')} / {ad})")
if d.get("alan") not in ALANLAR:
    h.append("alan geçersiz")
if d.get("zorluk") not in ZORLUKLAR:
    h.append("zorluk geçersiz")
if not isinstance(d.get("zafiyetler"), list) or len(d["zafiyetler"]) < 2:
    h.append("en az 2 zafiyet")
if not isinstance(d.get("flaglar"), list) or len(d["flaglar"]) < 2:
    h.append("en az 2 flag")
sha = re.compile(r"^[0-9a-f]{64}$")
for i, f in enumerate(d.get("flaglar") or [], 1):
    if not isinstance(f, dict):
        h.append(f"flag {i} sözlük değil")
        continue
    if not sha.match(str(f.get("sha256", "")).lower()):
        h.append(f"flag {i} sha256")
    if "flag" in f or "bayrak" in f:
        h.append(f"flag {i} düz metin")
    if not f.get("ipucu"):
        h.append(f"flag {i} ipucu yok")
if not isinstance(d.get("port"), int):
    h.append("port sayı olmalı")
if not (KOK / "docker-compose.yml").exists():
    h.append("docker-compose.yml yok")
if not (KOK / "Dockerfile").exists():
    h.append("Dockerfile yok")
if not (KOK / "README.md").exists():
    h.append("README.md yok")
if h:
    for x in h:
        print(" •", x)
    sys.exit(1)
print("lab.yml sözleşmeye uygun")
