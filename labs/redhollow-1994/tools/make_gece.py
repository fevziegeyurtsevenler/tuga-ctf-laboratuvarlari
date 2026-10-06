from pathlib import Path

import numpy as np
import wave

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "game" / "assets" / "gece.wav"
SR = 44100
SEC = 28.0


def note(freq, n, vol, fade=0.4):
    t = np.arange(n) / SR
    wave_ = np.sin(2 * np.pi * freq * t)
    wave_ += 0.35 * np.sin(2 * np.pi * freq * 2 * t)
    wave_ += 0.12 * np.sin(2 * np.pi * freq * 3 * t)
    env = np.ones(n)
    fade_n = int(SR * fade)
    env[:fade_n] *= np.linspace(0, 1, fade_n)
    env[-fade_n:] *= np.linspace(1, 0, fade_n)
    return wave_ * env * vol


def main() -> None:
    n = int(SR * SEC)
    t = np.arange(n) / SR
    rng = np.random.default_rng(94)
    rain = rng.standard_normal(n)
    rain = np.convolve(rain, np.ones(12) / 12, mode="same") * 0.045
    drone = (
        0.11 * np.sin(2 * np.pi * 73.4 * t)
        + 0.08 * np.sin(2 * np.pi * 110 * t)
        + 0.05 * np.sin(2 * np.pi * 146.8 * t)
    )
    melody = np.zeros(n)
    seq = [146.8, 174.6, 196.0, 174.6, 130.8, 146.8, 110.0, 146.8]
    step = int(SR * 3.4)
    for i, f in enumerate(seq):
        start = i * step
        leng = int(SR * 3.1)
        if start + leng > n:
            break
        melody[start : start + leng] += note(f, leng, 0.07, fade=0.8)
    mix = np.tanh(rain + drone + melody)
    pcm = (mix * 32767).astype(np.int16)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
