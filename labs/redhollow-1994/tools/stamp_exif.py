from pathlib import Path

import piexif
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "game" / "assets" / "vitrin.jpg"
FAKE = "TUGA{y4nl1s_v1tr1n_1z1}"
REAL = "TUGA{v1tr1n_k4m3r4s1}"
HEX = REAL.encode("ascii").hex()
TRAIL = "decoy — last-call notlar (basliga bakma)"


def _utf16le(s: str) -> bytes:
    return s.encode("utf-16le") + b"\x00\x00"


def main() -> None:
    img = Image.open(IMG)
    if img.mode != "RGB":
        img = img.convert("RGB")
    # Windows Ayrıntılar: Başlık = XPTitle / ImageDescription (sahte)
    # Yorumlar / UserComment = hex(gerçek flag) — decode gerekir
    user_comment = b"ASCII\x00\x00\x00" + HEX.encode("ascii")
    exif = {
        "0th": {
            piexif.ImageIFD.Artist: "Rachel Mia",
            piexif.ImageIFD.Software: "Night Hatch saha kamerasi",
            piexif.ImageIFD.DateTime: "1994:08:11 22:17:00",
            piexif.ImageIFD.ImageDescription: FAKE.encode("ascii"),
            piexif.ImageIFD.XPTitle: _utf16le(FAKE),
            piexif.ImageIFD.XPComment: _utf16le(TRAIL),
            piexif.ImageIFD.XPSubject: _utf16le("frame-17-final"),
            piexif.ImageIFD.Copyright: "Night Hatch 1994",
        },
        "Exif": {
            piexif.ExifIFD.DateTimeOriginal: "1994:08:11 22:17:00",
            piexif.ExifIFD.UserComment: user_comment,
        },
        "GPS": {},
        "1st": {},
        "thumbnail": None,
    }
    img.save(IMG, "jpeg", quality=88, exif=piexif.dump(exif))
    print(f"stamped {IMG}")
    print(f"fake title={FAKE}")
    print(f"usercomment hex={HEX}")


if __name__ == "__main__":
    main()
