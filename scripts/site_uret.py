#!/usr/bin/env python3
"""labs/*/lab.yml dosyalarından katalog sitesini (docs/) ve README katalog
bloğunu üretir.

Kaynak gerçeği (source of truth) = her labın lab.yml'si. Katkıcılar sadece
labs/<slug>/ ekler; bu script her merge'de siteyi, README katalog tablosunu,
llms.txt'yi, sitemap'i ve sayaçları yeniden üretir.
    python3 scripts/site_uret.py
"""
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("HATA: PyYAML gerekli →  pip install pyyaml")

KOK = Path(__file__).resolve().parent.parent
LABS = KOK / "labs"
DOCS = KOK / "docs"
README = KOK / "README.md"
KULLANICI = "fevziegeyurtsevenler"
REPO = "tuga-ctf-laboratuvarlari"
SITE_URL = f"https://{KULLANICI}.github.io/{REPO}"
REPO_URL = f"https://github.com/{KULLANICI}/{REPO}"

ALAN_EMOJI = {
    "Web": "🕸️", "Ağ": "🌐", "OSINT": "🔎", "Binary/Pwn": "💥",
    "Tersine Mühendislik": "🔩", "Kripto": "🔐", "Adli Bilişim": "🔬",
    "AI Güvenliği": "🤖", "Diğer": "🗂️",
}
ZORLUK_SIRA = {"Kolay": 0, "Orta": 1, "Zor": 2}


def lablari_yukle():
    lablar = []
    for k in sorted(p for p in LABS.iterdir() if p.is_dir()):
        yml = k / "lab.yml"
        if not yml.exists():
            continue
        d = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
        d["_slug"] = d.get("slug", k.name)
        d["_port"] = d.get("port", 8080)
        d["_flag_sayi"] = len(d.get("flaglar", []) or [])
        d["_zaf_sayi"] = len(d.get("zafiyetler", []) or [])
        lablar.append(d)
    # şablon en başa, sonra zorluk, sonra başlık
    lablar.sort(key=lambda d: (not d.get("sablon"), ZORLUK_SIRA.get(d.get("zorluk"), 9),
                               str(d.get("baslik", ""))))
    return lablar


def kur_komutu(slug):
    return (f"git clone --depth 1 --filter=blob:none --sparse {REPO_URL}.git && "
            f"cd {REPO} && git sparse-checkout set labs/{slug} && "
            f"cd labs/{slug} && docker compose up -d --build")


def kart_html(d):
    slug = d["_slug"]
    alan = d.get("alan", "Diğer")
    emoji = ALAN_EMOJI.get(alan, "🗂️")
    zor = d.get("zorluk", "Orta")
    e = html.escape
    etiketler = "".join(f'<span class="etiket">{e(str(t))}</span>'
                        for t in (d.get("etiketler") or []))
    sablon_rozet = '<span class="rozet-sablon">📘 ŞABLON — kopyala</span>' if d.get("sablon") else ""
    ara = " ".join([str(d.get("baslik", "")), str(d.get("senaryo", "")), alan, zor,
                    " ".join(str(x) for x in (d.get("etiketler") or [])),
                    " ".join(str(x) for x in (d.get("zafiyetler") or []))]).lower()
    zaf_list = "".join(f"<li>{e(str(z))}</li>" for z in (d.get("zafiyetler") or []))
    return f'''<article class="kart" data-alan="{e(alan)}" data-zorluk="{e(zor)}" data-slug="{e(slug)}" data-ara="{e(ara)}">
  <div class="kart-ust">
    <span class="rozet-alan">{emoji} {e(alan)}</span>
    <span class="rozet-zor zor-{ {'Kolay':'kolay','Orta':'orta','Zor':'zor'}.get(zor,'orta') }">{e(zor)}</span>
    {sablon_rozet}
  </div>
  <h3>{e(str(d.get("baslik","")))}</h3>
  <p class="senaryo">{e(str(d.get("senaryo","")).strip())}</p>
  <details class="zaf"><summary>{d["_zaf_sayi"]} zafiyet · {d["_flag_sayi"]} flag</summary><ul>{zaf_list}</ul></details>
  <div class="etiketler">{etiketler}</div>
  <div class="yazar">👤 <a href="https://github.com/{e(str(d.get("yazar","")))}" target="_blank" rel="noopener">{e(str(d.get("yazar","")))}</a></div>
  <div class="kart-alt">
    <button class="btn kur-btn" data-kur="{e(kur_komutu(slug))}" data-port="{d["_port"]}">▶ Kurulum komutu</button>
    <button class="btn bayrak-btn" data-slug="{e(slug)}">🚩 Flag gir</button>
  </div>
  <div class="bayrak-panel" data-slug="{e(slug)}" hidden></div>
</article>'''


def uret():
    if not LABS.exists():
        sys.exit("HATA: labs/ yok")
    lablar = lablari_yukle()
    toplam = len(lablar)
    flag_toplam = sum(d["_flag_sayi"] for d in lablar)
    alanlar = []
    for d in lablar:
        a = d.get("alan", "Diğer")
        if a not in alanlar:
            alanlar.append(a)

    # ---- README katalog bloğu + rozet ----
    if README.exists():
        rm = README.read_text(encoding="utf-8")
        rm = re.sub(r"lab-\d+-1C2957", f"lab-{toplam}-1C2957", rm)
        rm = re.sub(r"flag-\d+-2E4FD0", f"flag-{flag_toplam}-2E4FD0", rm)
        satirlar = ["| Lab | Alan | Zorluk | Zafiyet | Flag | Yazar |",
                    "|-----|------|--------|---------|------|-------|"]
        for d in lablar:
            ad = str(d.get("baslik", ""))
            slug = d["_slug"]
            satirlar.append(
                f"| [{ad}](labs/{slug}/) | {ALAN_EMOJI.get(d.get('alan','Diğer'),'🗂️')} {d.get('alan','Diğer')} "
                f"| {d.get('zorluk','')} | {d['_zaf_sayi']} | {d['_flag_sayi']} | "
                f"[@{d.get('yazar','')}](https://github.com/{d.get('yazar','')}) |")
        blok = "\n".join(satirlar)
        rm = re.sub(r"(<!-- LAB-KATALOG:BASLA -->).*?(<!-- LAB-KATALOG:BITIS -->)",
                    r"\1\n" + blok + r"\n\2", rm, flags=re.DOTALL)
        README.write_text(rm, encoding="utf-8")

    # ---- site ----
    alan_cipler = "".join(
        f'<button class="cip" data-tur="alan" data-deger="{html.escape(a)}">'
        f'{ALAN_EMOJI.get(a,"🗂️")} {html.escape(a)} '
        f'<b>{sum(1 for d in lablar if d.get("alan")==a)}</b></button>'
        for a in alanlar)
    zorluk_cipler = "".join(
        f'<button class="cip" data-tur="zorluk" data-deger="{z}">{z} '
        f'<b>{sum(1 for d in lablar if d.get("zorluk")==z)}</b></button>'
        for z in ("Kolay", "Orta", "Zor") if any(d.get("zorluk") == z for d in lablar))
    kartlar = "\n".join(kart_html(d) for d in lablar)

    flag_veri = {d["_slug"]: [{"ipucu": f.get("ipucu", ""), "h": str(f.get("sha256", "")).lower()}
                              for f in (d.get("flaglar") or [])] for d in lablar}

    jsonld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "TÜGA CTF Laboratuvarları",
        "description": "Senaryolu, Docker ile lokalde çalışan Türkçe siber güvenlik CTF laboratuvarları dizini.",
        "url": SITE_URL, "inLanguage": "tr",
        "dateModified": date.today().isoformat(),
        "publisher": {"@type": "Organization", "name": "TÜGA Siber Güvenlik Komitesi"},
        "mainEntity": {"@type": "ItemList", "numberOfItems": toplam,
                       "itemListElement": [
                           {"@type": "ListItem", "position": i + 1, "name": d.get("baslik", ""),
                            "url": f"{REPO_URL}/tree/main/labs/{d['_slug']}",
                            "description": str(d.get("senaryo", "")).strip()}
                           for i, d in enumerate(lablar)]},
    }

    sablon = (DOCS / "sablon.html").read_text(encoding="utf-8")
    sayfa = (sablon
             .replace("@@TOPLAM@@", str(toplam))
             .replace("@@ALAN_SAYI@@", str(len(alanlar)))
             .replace("@@FLAG_TOPLAM@@", str(flag_toplam))
             .replace("@@ALAN_CIPLER@@", alan_cipler)
             .replace("@@ZORLUK_CIPLER@@", zorluk_cipler)
             .replace("@@KARTLAR@@", kartlar)
             .replace("@@FLAG_VERI@@", json.dumps(flag_veri, ensure_ascii=False))
             .replace("@@JSONLD@@", json.dumps(jsonld, ensure_ascii=False))
             .replace("@@TARIH@@", date.today().strftime("%d.%m.%Y")))
    (DOCS / "index.html").write_text(sayfa, encoding="utf-8")

    # ---- llms.txt / llms-full.txt ----
    llms = ["# TÜGA CTF Laboratuvarları", "",
            "> Senaryolu, Docker ile lokalde çalışan Türkçe siber güvenlik CTF "
            "laboratuvarları dizini. TÜGA Siber Güvenlik Komitesi yürütür; her lab "
            "en az 2 farklı zafiyet ve 2 flag içerir, PR ile katkıya açıktır.", "",
            f"- Site: {SITE_URL}", f"- Repo: {REPO_URL}",
            f"- Lab sayısı: {toplam} | Alan: {len(alanlar)} | Toplam flag: {flag_toplam}", "",
            "## Laboratuvarlar"]
    for d in lablar:
        llms.append(f"- {d.get('baslik','')} ({d.get('alan','')}, {d.get('zorluk','')}) "
                    f"— {str(d.get('senaryo','')).strip()[:160]}")
    (DOCS / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")

    tam = ["# TÜGA CTF Laboratuvarları — tam liste", ""]
    for d in lablar:
        tam += [f"## {d.get('baslik','')}",
                f"- Alan: {d.get('alan','')} | Zorluk: {d.get('zorluk','')} | Yazar: {d.get('yazar','')}",
                f"- Senaryo: {str(d.get('senaryo','')).strip()}",
                f"- Zafiyetler: {'; '.join(str(z) for z in (d.get('zafiyetler') or []))}",
                f"- Kurulum: labs/{d['_slug']} → docker compose up -d --build (port {d['_port']})", ""]
    (DOCS / "llms-full.txt").write_text("\n".join(tam), encoding="utf-8")

    (DOCS / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{SITE_URL}/</loc><lastmod>{date.today().isoformat()}</lastmod></url>\n"
        "</urlset>\n", encoding="utf-8")
    (DOCS / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")

    print(f"OK: {toplam} lab, {len(alanlar)} alan, {flag_toplam} flag → docs/ + README güncellendi")


if __name__ == "__main__":
    uret()
