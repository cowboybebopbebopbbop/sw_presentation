"""High-accuracy Russian transcription using faster-whisper large-v3.

Outputs:
  meeting.txt  — plain text
  meeting.srt  — subtitle file with timestamps
  meeting.tsv  — start\tend\ttext per segment
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Add nvidia pip-installed CUDA libs to DLL search path (Windows).
try:
    import nvidia  # type: ignore
    # nvidia is a namespace package; iterate its search paths to find subpkgs.
    _roots = [Path(p) for p in nvidia.__path__]  # type: ignore[attr-defined]
    for _root in _roots:
        for _sub in ("cublas/bin", "cudnn/bin", "cuda_nvrtc/bin"):
            _p = _root / _sub
            if _p.is_dir():
                os.add_dll_directory(str(_p))
                os.environ["PATH"] = f"{_p};{os.environ.get('PATH', '')}"
except Exception as _e:
    print(f"[warn] could not register nvidia DLL dirs: {_e}", flush=True)

from faster_whisper import WhisperModel

AUDIO = Path("meeting.m4a")
MODEL_SIZE = "large-v3"
LANGUAGE = "ru"

# Try GPU first, fall back to CPU int8 (most accurate CPU mode).
def load_model() -> WhisperModel:
    try:
        m = WhisperModel(MODEL_SIZE, device="cuda", compute_type="float16")
        print("[info] using CUDA float16", flush=True)
        return m
    except Exception as e:  # missing cuDNN/cuBLAS etc.
        print(f"[info] CUDA unavailable ({e.__class__.__name__}); falling back to CPU int8", flush=True)
        return WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")


def fmt_ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds - h * 3600 - m * 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def main() -> None:
    if not AUDIO.exists():
        sys.exit(f"audio not found: {AUDIO}")

    t0 = time.time()
    model = load_model()
    print(f"[info] model loaded in {time.time()-t0:.1f}s", flush=True)

    segments_iter, info = model.transcribe(
        str(AUDIO),
        language=LANGUAGE,
        task="transcribe",
        beam_size=5,
        best_of=5,
        temperature=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        condition_on_previous_text=True,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        word_timestamps=False,
        # Bias the model toward the meeting context to reduce hallucinations.
        initial_prompt=(
            "Деловая встреча на русском языке. "
            "Участники: Арина, Марина, Дима. "
            "Обсуждение презентации, e-commerce, SimpleWine."
        ),
    )

    print(
        f"[info] detected language={info.language} prob={info.language_probability:.2f} "
        f"duration={info.duration:.1f}s",
        flush=True,
    )

    txt_lines: list[str] = []
    srt_lines: list[str] = []
    tsv_lines: list[str] = ["start\tend\ttext"]

    t_start = time.time()
    for i, seg in enumerate(segments_iter, start=1):
        text = seg.text.strip()
        txt_lines.append(text)
        srt_lines.append(
            f"{i}\n{fmt_ts(seg.start)} --> {fmt_ts(seg.end)}\n{text}\n"
        )
        tsv_lines.append(f"{seg.start:.3f}\t{seg.end:.3f}\t{text}")
        if i % 10 == 0:
            elapsed = time.time() - t_start
            audio_done = seg.end
            speed = audio_done / elapsed if elapsed else 0
            print(
                f"[progress] seg {i:>4}  {fmt_ts(seg.end)}  x{speed:.2f} realtime",
                flush=True,
            )

    Path("meeting.txt").write_text("\n".join(txt_lines), encoding="utf-8")
    Path("meeting.srt").write_text("\n".join(srt_lines), encoding="utf-8")
    Path("meeting.tsv").write_text("\n".join(tsv_lines), encoding="utf-8")

    total = time.time() - t_start
    print(
        f"[done] {len(txt_lines)} segments in {total/60:.1f} min "
        f"({info.duration/total:.2f}x realtime)",
        flush=True,
    )


if __name__ == "__main__":
    main()
