"""Lara son saha kaydı — Türkçe kadın sesi (edge-tts)."""
from pathlib import Path
import asyncio

import edge_tts

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "game" / "assets" / "lara_son.mp3"
VOICE = "tr-TR-EmelNeural"
TEXT = (
    "Burası Lara Lock. Night Hatch arşivi mühürleniyor. "
    "On iki işareti buldun. Tebrik ederim. "
    "Ama kapıdan çıktığını sanma. "
    "Park seni de kayda aldı."
)


async def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(TEXT, VOICE, rate="-8%")
    await communicate.save(str(OUT))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
