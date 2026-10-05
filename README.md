# Athens, from the top deck

An audio companion for the red **Athens Line** of the CitySightseeing hop-on hop-off bus: 15 stops looping
from Syntagma (A1) past Plaka, the Acropolis, the Temple of Olympian Zeus, Kolonaki's museum mile, the marble
stadium, the neoclassical Trilogy, the National Archaeological Museum, Omonia, Karaiskaki, Monastiraki and the
Central Market. A sixteenth "stop" covers food and where to eat. It's the sibling of
[Santorini, along the rim](https://github.com/RobGruhl/santorini-rim) and
[Rhodes Landfall](https://github.com/RobGruhl/rhodes-landfall).

Two tracks share the same 16 stops. Each stop has a short version (about forty seconds, for when the bus rolls
straight past) and a long one (two to three minutes, for hopping off or sitting in traffic):

- **Rob** (`narration/rob.json`): the classical city and how democracy worked, the Parthenon's engineering,
  Hadrian, the War of Independence and the new state's neoclassical capital, the 1896 Games, the Antikythera
  mechanism, 1973, food and wine.
- **Jamie** (`narration/jamie.json`): how Athenians lived and live: women's lives, the islanders of Anafiotika,
  the 1922 refugees, markets, kiosks, gardens, the cats and the light. Rendered steadier and softer.

Stop order follows the arrows on the operator's route map. Their site doesn't publish it; see `research/route.md`.

## Build

```
python3 scripts/narrate.py --set rob          # plan: clips, characters, credits left
python3 scripts/narrate.py --set rob --yes    # render missing clips into docs/audio/rob/
python3 scripts/narrate.py --set jamie --yes
python3 scripts/build.py                      # docs/index.html (?as=jamie opens Jamie's track)
python3 scripts/album.py                      # album/<set>/ tagged for Apple Music (gitignored)
```

Narration uses ElevenLabs **Eleven v4** (`eleven_v4`), voice George, on the standard text-to-speech endpoint,
exactly as in the Santorini build:
- Only Stability and Similarity apply.
- Pauses come from paragraph breaks or `[pause]`.
- Each set gets a bracketed direction tag at render time.
- Greek names get IPA between slashes (`SAY` in `narrate.py`). `scripts/pron_test.py` renders an ear check
  into `research/pron/`.

Stop 16 (Eat) is written once in `rob.json` and copied into `narration/jamie-eat.json`, so both tracks have it.

The page is static (`docs/`, served by GitHub Pages) and can save a track for offline listening.
