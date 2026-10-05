"""Render one sentence of Athens place names twice, plain and with IPA, for an ear check."""
import json, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
import narrate as n
from pathlib import Path
OUT = n.ROOT / "research" / "pron"
OUT.mkdir(parents=True, exist_ok=True)
plain = ("From Syntagma the bus runs past Plaka and Makrygianni, around to Monastiraki, Psyrri and Thissio, "
         "then up to Omonia, Kolonaki and the marble stadium the Athenians call Kallimarmaro.")
ipa = n.spoken(plain, "rob").split("\n", 1)[1]
VOICE = "JBFqnCBsd6RMkjVDRZzb"  # George
key = n.api_key()
vid = VOICE
for name, text in (("plain", plain), ("ipa", ipa)):
    text = f"{n.DIRECTION["rob"]}\n{text}"
    body = json.dumps({"model_id": n.MODEL, "text": text, "voice_settings": n.SETTINGS["rob"]}).encode()
    audio, h = n.req(key, f"/v1/text-to-speech/{vid}?output_format=mp3_44100_128", body, {"Content-Type": "application/json"})
    (OUT / f"{name}.mp3").write_bytes(audio)
    n.audit(f"[agent-voice audit] verb=pron-test project=athens-line voice={vid} model={n.MODEL} chars={len(text)} credits={h.get('character-cost')}")
    print(name, n.duration_seconds(OUT / f"{name}.mp3"), "s")
