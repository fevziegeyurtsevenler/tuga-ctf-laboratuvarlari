import base64
import hashlib
import json
import pathlib
import re
import urllib.request

root = pathlib.Path(r"C:\Users\rplny\OneDrive\Desktop\SiberGüvenlikProjeleri\redhollow-1994")
game = root / "game"
errors = []
warnings = []

expected = {
    "I-1": "TUGA{g1s3_h1c_4c1lm4d1}",
    "I-2": "TUGA{g3c3_v4rd1y4s1}",
    "I-3": "TUGA{f3n3r_t3l_0rgu}",
    "II-1": "TUGA{sf074_y4n11s_r4f}",
    "II-2": "TUGA{v1tr1n_k4m3r4s1}",
    "II-3": "TUGA{c1t_dustu_kukr3m3}",
    "III-1": "TUGA{l4r4_l0ck_1z1n1_4mb3rd3_b1r4kt1}",
    "III-2": "TUGA{r04r_k4s3tt3_g1zl1}",
    "III-3": "TUGA{s4h4_k1t1_4c1k_k4yn4k}",
    "IV-1": "TUGA{n1ght_h4tch_h1c_4c1lm4d1}",
    "IV-2": "TUGA{d0sy4_k4p4nd1_1994}",
    "IV-3": "TUGA{0v3rl4y_sf074}",
}


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def unpack(n: int):
    p = game / "js" / "bolum" / f"{n}.js"
    txt = p.read_text(encoding="utf-8")
    m = re.search(r"window\.__PACK=(.+);", txt.strip())
    if not m:
        raise ValueError("no __PACK")
    b64 = json.loads(m.group(1))
    raw = bytearray(base64.b64decode(b64))
    key = f"nh{n}".encode()
    for i in range(len(raw)):
        raw[i] ^= key[i % len(key)]
    return json.loads(raw.decode("utf-8"))


print("=== PACK / HASH ===")
for n in range(1, 5):
    try:
        data = unpack(n)
    except Exception as e:
        errors.append(f"pack {n}: {e}")
        continue
    story = data["story"]
    flags = data["flags"]
    slots = data["slots"]
    print(f"pack {n}: slots={slots} nokta={len(story['noktalar'])} foto={story['foto']}")
    for sid in slots:
        want = sha(expected[sid])
        got = flags.get(sid)
        if got != want:
            errors.append(f"hash mismatch {sid}")
        else:
            print(f"  OK {sid}")
    foto = game / story["foto"]
    if not foto.exists():
        errors.append(f"missing foto {story['foto']}")
    if story.get("altSahne"):
        ap = game / story["altSahne"]["foto"]
        if not ap.exists():
            errors.append(f"missing altSahne {story['altSahne']['foto']}")
    for nkt in story["noktalar"]:
        for key in ("dosya", "vinyet"):
            if not nkt.get(key):
                continue
            path = game / nkt[key]
            if not path.exists():
                if "bone_tagger" in nkt[key]:
                    warnings.append(f"binary missing {nkt[key]} (docker)")
                else:
                    errors.append(f"missing {nkt[key]}")
    giz = data.get("giz") or {}
    if n == 1 and "generator" not in giz:
        errors.append("ch1 missing generator giz")
    elif n == 1 and giz.get("generator") != expected["I-1"]:
        errors.append(f"ch1 generator not plaintext {giz.get('generator')!r}")
    if n == 2 and ("cerez" not in giz or "raf" not in giz):
        errors.append("ch2 missing giz fields")
    if n == 3 and "sonra" not in giz:
        errors.append("ch3 missing sonra")
    if n == 4 and "m" not in giz:
        errors.append("ch4 missing m")
    if n == 2:
        cerez = "".join(chr(c) for c in giz["cerez"])
        if cerez != expected["II-3"]:
            errors.append(f"ch2 cerez wrong {cerez}")
        else:
            print("  OK cerez ->", cerez)
        raf = bytes(int(x) for x in giz["raf"].split()).decode("ascii")
        if raf != expected["II-1"]:
            errors.append(f"ch2 raf wrong {raf}")
        else:
            print("  OK raf ->", raf)
    if n == 4:
        deep = "".join(chr(c) for c in giz["m"])
        if deep != "SF-074-DEEP":
            errors.append(f"ch4 m wrong {deep}")
        else:
            print("  OK _m ->", deep)

print("\n=== FILES ===")
need = [
    "index.html",
    "js/engine.js",
    "js/flags.js",
    "css/game.css",
    "assets/gece.wav",
    "assets/saha_kaydi_1994.wav",
    "assets/kukreme.mp3",
    "assets/lara_son.mp3",
    "files/bilet.txt",
    "files/last-call.html",
    "files/sicil.html",
    "files/spektrum.html",
    "assets/kaset.jpg",
    "robots.txt",
    "kit/index.html",
    "assets/vitrin.jpg",
    "assets/kaset_kutu.jpg",
    "assets/ch1-gise.jpg",
    "assets/ch2-sergi.jpg",
    "assets/ch3-amber.jpg",
    "assets/ch3-baraka.jpg",
    "assets/ch4-kapi.jpg",
    "assets/scare-rex.jpg",
    "assets/scare-yeme.jpg",
]
for rel in need:
    ok = (game / rel).exists()
    print(("OK " if ok else "MISS"), rel)
    if not ok:
        errors.append(f"missing {rel}")

if (game / "js" / "story.js").exists():
    errors.append("story.js should not exist")

idx = (game / "index.html").read_text(encoding="utf-8")
if "story.js" in idx:
    errors.append("index loads story.js")
if "engine.js" not in idx:
    errors.append("index missing engine")

eng = (game / "js" / "engine.js").read_text(encoding="utf-8")
for bad in ["TUGA{", "story.js", "c1t_dustu", "SF-074-DEEP", "Işık gitti"]:
    if bad in eng:
        # Turkish may vary
        if bad == "Işık gitti" and bad not in eng:
            continue
        if bad in eng:
            warnings.append(f"engine contains spoiler-ish '{bad}'")

print("\n=== DECODES ===")
bilet = (game / "files" / "bilet.txt").read_text(encoding="utf-8")
hx = re.search(r"Sira:\s*([0-9a-fA-F ]+)", bilet)
if not hx:
    errors.append("bilet hex missing")
else:
    decoded = bytes.fromhex(hx.group(1).replace(" ", "")).decode("ascii")
    print("bilet:", decoded)
    if decoded != expected["I-2"]:
        errors.append("bilet decode mismatch")

rob = (game / "robots.txt").read_text(encoding="utf-8")
if "sicil.html" not in rob:
    errors.append("robots missing sicil path")
if "spektrum.html" not in rob:
    errors.append("robots missing spektrum path")
sicil = (game / "files" / "sicil.html").read_text(encoding="utf-8")
if expected["IV-2"] not in sicil:
    errors.append("sicil missing IV-2 flag")
else:
    print("sicil:", expected["IV-2"])

lc = (game / "files" / "last-call.html").read_text(encoding="utf-8")
m = re.search(r'\{\"n\":\[([^\]]+)\]\}', lc)
if not m:
    errors.append("last-call json missing")
else:
    nums = [int(x) for x in m.group(1).split(",")]
    decoded = "".join(chr(x) for x in nums)
    print("last-call:", decoded)
    if decoded != expected["III-1"]:
        errors.append("last-call decode mismatch")

css = (game / "css" / "game.css").read_text(encoding="utf-8")
m2 = re.search(r"\.bant\.u::after\s*\{[^}]*content:\s*\"([^\"]+)\"", css, re.S)
if not m2:
    errors.append("css bant content missing")
else:
    raw = m2.group(1)
    seq = re.findall(r"\\([0-9a-fA-F]{4})", raw)
    decoded = "".join(chr(int(x, 16)) for x in seq) if seq else raw
    print("css:", decoded)
    if decoded != expected["I-3"]:
        errors.append("css decode mismatch")

# EXIF — gerçek flag UserComment içinde hex; Başlık/ImageDescription sahte
try:
    import piexif

    d = piexif.load(str(game / "assets" / "vitrin.jpg"))
    desc = d["0th"].get(piexif.ImageIFD.ImageDescription, b"")
    if isinstance(desc, bytes):
        desc = desc.decode("utf-8", "ignore")
    uc = d["Exif"].get(piexif.ExifIFD.UserComment, b"")
    if isinstance(uc, bytes) and uc.startswith(b"ASCII\x00\x00\x00"):
        uc = uc[8:]
    if isinstance(uc, bytes):
        uc = uc.decode("ascii", "ignore")
    hex_real = expected["II-2"].encode("ascii").hex()
    print("exif ImageDescription (fake):", desc)
    print("exif UserComment hex:", uc)
    if desc == expected["II-2"]:
        errors.append("exif still exposes real flag in ImageDescription")
    if uc != hex_real:
        errors.append(f"exif UserComment hex wrong {uc!r}")
    else:
        print("exif: OK (hex decode)")
except Exception as e:
    errors.append(f"exif check fail {e}")

# kit flag
kit = (game / "kit" / "index.html").read_text(encoding="utf-8")
if expected["III-3"] not in kit:
    errors.append("kit missing III-3 flag")
else:
    print("kit: OK")

# kaset kutusu EXIF → GitHub
try:
    import piexif

    kd = piexif.load(str(game / "assets" / "kaset_kutu.jpg"))
    uc = kd["Exif"].get(piexif.ExifIFD.UserComment, b"")
    if isinstance(uc, bytes) and uc.startswith(b"ASCII\x00\x00\x00"):
        uc = uc[8:].decode("ascii", "ignore")
    elif isinstance(uc, bytes):
        uc = uc.decode("ascii", "ignore")
    gh = "https://github.com/rplny/night-hatch-field-kit"
    print("kutu UserComment:", uc)
    if gh not in str(uc):
        errors.append(f"kutu EXIF missing github link ({uc!r})")
    else:
        print("kutu exif: OK")
except Exception as e:
    errors.append(f"kutu exif check fail {e}")

# bone_tagger source XOR
cpath = root / "re" / "src" / "bone_tagger.c"
if cpath.exists():
    src = cpath.read_text(encoding="utf-8")
    # extract overlay arrays roughly by running python xor known
    k = bytes([0x5A, 0x3C, 0x91, 0x07, 0xE2, 0x4B, 0x88, 0x2D])
    # parse first overlay hex list
    overs = re.findall(r"static const unsigned char (overlay|deep)\[\] = \{([^}]+)\}", src, re.S)
    for name, body in overs:
        nums = [int(x, 16) for x in re.findall(r"0x([0-9a-fA-F]+)", body)]
        out = "".join(chr(nums[i] ^ k[i % 8]) for i in range(len(nums)))
        print(f"c {name}:", out)
        if name == "overlay" and out != expected["IV-1"]:
            errors.append("bone overlay mismatch")
        if name == "deep" and out != expected["IV-3"]:
            errors.append("bone deep mismatch")
else:
    errors.append("bone_tagger.c missing")

print("\n=== HTTP ===")
for url in [
    "http://127.0.0.1:8080/",
    "http://127.0.0.1:8080/js/engine.js?v=32",
    "http://127.0.0.1:8080/js/bolum/1.js?v=9",
    "http://127.0.0.1:8080/js/bolum/2.js?v=3",
    "http://127.0.0.1:8080/assets/ch1-gise.jpg",
    "http://127.0.0.1:8080/assets/gece.wav",
]:
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            print(f"{r.status} {url}")
    except Exception as e:
        warnings.append(f"HTTP {url}: {e}")

# simulate gate logic
print("\n=== GATE ===")
bulunan = {}
for n in range(1, 5):
    # previous complete?
    prev_ok = True
    if n > 1:
        for sid in unpack(n - 1)["slots"]:
            if sid not in bulunan:
                prev_ok = False
    print(f"access ch{n} without progress: {prev_ok if n>1 else True}")
    if n > 1 and prev_ok is False:
        print(f"  gate blocks ch{n} OK")
    # mark complete
    for sid in unpack(n)["slots"]:
        bulunan[sid] = True

print("\n=== SUMMARY ===")
print("errors", len(errors))
for e in errors:
    print("ERR", e)
print("warnings", len(warnings))
for w in warnings:
    print("WARN", w)
