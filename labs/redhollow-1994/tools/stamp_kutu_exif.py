"""kaset_kutu.jpg EXIF: GitHub adresi UserComment'te."""
from pathlib import Path

import piexif
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "game" / "assets" / "kaset.jpg"
OUT = ROOT / "game" / "assets" / "kaset_kutu.jpg"
GH = "https://github.com/rplny/night-hatch-field-kit"


def _utf16le(s: str) -> bytes:
    return s.encode("utf-16le") + b"\x00\x00"


def make_cover(base: Image.Image) -> Image.Image:
    img = base.convert("RGB")
    img = img.resize((960, 720), Image.Resampling.LANCZOS)
    img = ImageEnhance.Brightness(img).enhance(0.55)
    img = ImageEnhance.Contrast(img).enhance(1.15)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
    draw = ImageDraw.Draw(img)
    font = None
    for path, size in (
        (Path(r"C:\Windows\Fonts\arial.ttf"), 22),
        (Path(r"C:\Windows\Fonts\calibri.ttf"), 22),
    ):
        if path.exists():
            font = ImageFont.truetype(str(path), size)
            break
    draw.rectangle((40, 40, 920, 120), fill=(18, 14, 10))
    draw.text((60, 58), "NIGHT HATCH · SAHA KITI · IC KAPAK", fill=(180, 150, 110), font=font)
    draw.text((60, 88), "kopya — arsiv 1994", fill=(120, 100, 80), font=font)
    return img


def main() -> None:
    if SRC.exists():
        base = Image.open(SRC)
    else:
        base = Image.new("RGB", (960, 720), (20, 16, 12))
    img = make_cover(base)

    # Başlık sahte; asıl adres UserComment + XPComment (GitHub)
    user_comment = b"ASCII\x00\x00\x00" + GH.encode("ascii")
    exif = {
        "0th": {
            piexif.ImageIFD.Artist: "Lara Lock",
            piexif.ImageIFD.Software: "NH field camera",
            piexif.ImageIFD.DateTime: "1994:08:11 23:04:00",
            piexif.ImageIFD.ImageDescription: "ic kapak — etiket yalan".encode("utf-8"),
            piexif.ImageIFD.XPTitle: _utf16le("ic kapak (arsiv)"),
            piexif.ImageIFD.XPComment: _utf16le(GH),
            piexif.ImageIFD.XPSubject: _utf16le("open source leave-behind"),
            piexif.ImageIFD.Copyright: "Lara Lock 1994",
        },
        "Exif": {
            piexif.ExifIFD.DateTimeOriginal: "1994:08:11 23:04:00",
            piexif.ExifIFD.UserComment: user_comment,
        },
        "GPS": {},
        "1st": {},
        "thumbnail": None,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "jpeg", quality=90, exif=piexif.dump(exif))
    print(f"wrote {OUT}")
    print(f"github in EXIF: {GH}")


if __name__ == "__main__":
    main()
