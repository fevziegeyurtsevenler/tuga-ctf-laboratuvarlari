"""saha_kaydi_1994.wav spektrogram bayrağı."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "game" / "assets" / "saha_kaydi_1994.wav"
PREVIEW = ROOT / "game" / "assets" / "roar_spec_preview.png"
VERIFY = ROOT / "game" / "assets" / "roar_spec_verify.png"
FLAG = "TUGA{r04r_k4s3tt3_g1zl1}"
SR = 44100


def roar(n: int) -> np.ndarray:
    t = np.arange(n) / SR
    rng = np.random.default_rng(1994)
    noise = rng.standard_normal(n)
    rumble = np.sin(2 * np.pi * 40 * t) * 0.3
    env = np.exp(-((t - 0.7) ** 2) / 0.3)
    low = np.convolve(noise, np.ones(400) / 400, mode="same")
    return np.clip(np.tanh((low * 0.3 + rumble) * (0.08 + env)) * 0.35, -1, 1)


def flag_image() -> Image.Image:
    w, h = 1000, 280
    img = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(img)
    font = None
    for path, size in (
        (Path(r"C:\Windows\Fonts\consolab.ttf"), 92),
        (Path(r"C:\Windows\Fonts\courbd.ttf"), 92),
        (Path(r"C:\Windows\Fonts\arialbd.ttf"), 84),
    ):
        if path.exists():
            font = ImageFont.truetype(str(path), size)
            break
    lines = ["TUGA{r04r_k4s3tt3", "_g1zl1}"]
    y = 20
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = max(8, (w - tw) // 2)
        for ox in range(-3, 4):
            for oy in range(-3, 4):
                draw.text((x + ox, y + oy), line, fill=255, font=font)
        y += 130
    img = img.filter(ImageFilter.MaxFilter(9))
    # Çok bloklu piksel — spektrogramda Minecraft gibi
    return img.resize((320, 80), Image.Resampling.NEAREST)


def img_to_audio(img: Image.Image, samples_per_col: int = 900) -> np.ndarray:
    px = np.array(img, dtype=np.float64)
    h, w = px.shape
    # Az satır + geniş frekans aralığı = net bantlar
    freqs = np.linspace(12000.0, 3500.0, h)
    out = np.zeros(w * samples_per_col)
    mask = px >= 100

    for x in range(w):
        rows = np.where(mask[:, x])[0]
        if rows.size == 0:
            continue
        a0 = x * samples_per_col
        tt = (np.arange(samples_per_col) + a0) / SR
        chunk = np.zeros(samples_per_col)
        for y in rows:
            chunk += np.sin(2 * np.pi * freqs[y] * tt)
        peak = np.max(np.abs(chunk)) or 1.0
        out[a0 : a0 + samples_per_col] = chunk / peak * 0.95
    return out


def verify_simple(audio: np.ndarray, path: Path, start_s: float = 2.0) -> None:
    n_fft, hop = 4096, 512
    win = np.hanning(n_fft)
    freqs = np.fft.rfftfreq(n_fft, 1 / SR)
    i0 = int(np.searchsorted(freqs, 3000))
    i1 = int(np.searchsorted(freqs, 12500))
    start = int(start_s * SR)
    cols = []
    a = start
    while a + n_fft < len(audio):
        mag = np.abs(np.fft.rfft(audio[a : a + n_fft] * win))[i0:i1]
        cols.append(mag)
        a += hop
    if not cols:
        return
    spec = np.stack(cols, axis=1)
    thr = np.percentile(spec, 55)
    vis = np.clip(spec - thr, 0, None)
    vis /= vis.max() or 1.0
    vis = (np.power(vis, 0.35) * 255).astype(np.uint8)
    Image.fromarray(vis[::-1], "L").resize((1400, 220), Image.Resampling.NEAREST).save(path)


def main() -> None:
    img = flag_image()
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    img.resize((960, 240), Image.Resampling.NEAREST).save(PREVIEW)

    roar_n = int(SR * 1.4)
    gap = int(SR * 0.35)
    flag_audio = img_to_audio(img, samples_per_col=950)
    total = roar_n + gap + len(flag_audio) + int(SR * 0.25)
    audio = np.zeros(total)
    audio[:roar_n] = roar(roar_n)
    audio[roar_n + gap : roar_n + gap + len(flag_audio)] = flag_audio
    audio = np.clip(audio, -1, 1)
    verify_simple(audio, VERIFY, start_s=(roar_n + gap) / SR - 0.1)

    import wave

    with wave.open(str(OUT), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes((audio * 32767).astype(np.int16).tobytes())
    print(f"wrote {OUT} ({total/SR:.1f}s) pixels={img.size}")


if __name__ == "__main__":
    main()
