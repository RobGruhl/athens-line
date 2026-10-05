#!/usr/bin/env python3
"""Catch Eleven v4 glitches: transcribe every clip locally (mlx_whisper, free) and compare it with its script.

v4 sometimes loops a phrase. Whisper can also invent loops of its own, so a clip is flagged only
when BOTH signals agree: the transcript repeats six-word phrases the script doesn't, AND the clip runs
long for its text (fewer characters per second than 90% of the set's median). Transcription runs with
--condition-on-previous-text False, which keeps Whisper from looping on itself.

  python3 scripts/audit_audio.py                 # transcribe what's missing, report every set
  python3 scripts/audit_audio.py --set rob --retranscribe 06-national-gardens-long
Exit 1 if anything is flagged; prints the --stops/--only arguments to re-render it.
"""
import argparse, glob, json, re, statistics, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TX = ROOT / "research" / "transcripts" / "v2"   # gitignored; v2 = no-conditioning transcripts
MODEL = "mlx-community/whisper-large-v3-turbo"
norm = lambda t: re.sub(r"[^a-z ]", " ", t.lower()).split()


def grams(words, n=6):
    c = {}
    for i in range(len(words) - n + 1):
        g = " ".join(words[i:i + n]); c[g] = c.get(g, 0) + 1
    return c


def transcribe(mp3: Path, out: Path, force=False):
    txt = out / (mp3.stem + ".txt")
    if force or not txt.exists():
        out.mkdir(parents=True, exist_ok=True)
        subprocess.run(["mlx_whisper", str(mp3), "--model", MODEL, "--output-dir", str(out),
                        "--output-format", "txt", "--verbose", "False", "--condition-on-previous-text", "False"],
                       check=True, capture_output=True)
    return txt.read_text()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", action="append")
    ap.add_argument("--retranscribe", action="append", default=[], help="clip stem(s) to transcribe again")
    a = ap.parse_args()
    bad = []
    for w in a.set or ["rob", "jamie"]:
        stops = {}
        for f in sorted(glob.glob(str(ROOT / "narration" / f"{w}*.json"))):
            for s in json.load(open(f)): stops[s["slug"]] = s
        clips = json.load(open(ROOT / "docs" / "audio" / w / "manifest.json"))["clips"]
        rate = {}
        for slug, c in clips.items():
            for L in ("short", "long"):
                if L in c and c[L].get("sec"):
                    rate[c[L]["file"].split("/")[-1][:-4]] = len(stops[slug][L]) / c[L]["sec"]
        med = statistics.median(rate.values())
        for mp3 in sorted((ROOT / "docs" / "audio" / w).glob("*.mp3")):
            n, rest = mp3.stem.split("-", 1)
            slug, length = rest.rsplit("-", 1)
            heard = norm(transcribe(mp3, TX / w, mp3.stem in a.retranscribe))
            script = norm(re.sub(r"\[[^\]]+\]", " ", stops[slug][length]))
            gh, gs = grams(heard), grams(script)
            loops = [g for g, k in gh.items() if k > 1 and k > gs.get(g, 0)]
            slow = rate.get(mp3.stem, med) / med
            if len(loops) >= 2 and slow < 0.9:
                bad.append((w, int(n), length, mp3.stem, len(loops), slow, loops[:2]))
    for w, n, length, stem, nl, slow, ex in bad:
        print(f"✗ {w}/{stem}: {nl} looped phrases, runs at {slow:.0%} of median pace  {ex}")
        print(f"    python3 scripts/narrate.py --set {w} --stops {n} --only {length} --force --yes")
    print("✓ all clips match their scripts" if not bad else f"{len(bad)} clip(s) flagged")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
