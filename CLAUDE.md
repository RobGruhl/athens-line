# Athens Line: agent notes

Public repo `RobGruhl/athens-line`, served by GitHub Pages from `docs/`. It's an audio companion for the
CitySightseeing red Athens Line hop-on hop-off bus, built the same way as `~/Projects/santorini` (santorini-rim).
Read `README.md` and `research/route.md`, which has the official stop names, the timetable and the sights list
from Rob's photos of the operator's map.

- **Narration** lives in `narration/{rob,jamie}.json`. Stop 16 (Eat) is written once in `rob.json` and copied to
  `jamie-eat.json`. Jamie's track is gentler: people and daily life, and nothing graphic.
- **Rendering** uses ElevenLabs Eleven v4 through `scripts/narrate.py`. Rob gave a standing `--yes` for
  narration renders on this project (2026-10-05). The plan, without `--yes`, shows characters and credits left.
  v4 bills about 0.1 credit per character until 12 Oct 2026, then 1 credit per character. Every clip is
  audited in `~/.local/state/agent-voice/audit.log`.
- **Always audit after rendering:** `python3 scripts/audit_audio.py` transcribes every clip locally
  (mlx_whisper, free) and flags v4 loops, which need both a repeated phrase AND a slow pace, since Whisper
  invents loops too. Re-render flagged clips with the printed command. If one loops twice, add `--stability 0.7`
  (Jamie's setting, which hasn't looped). First pass, 2026-10-05: four of Rob's clips looped (3s, 6L, 10L, 12L).
  All are fixed; 3s and 10L needed 0.7.
- **Pronunciation:** add Greek names to `SAY` (IPA). Never put IPA in the scripts themselves.
  `scripts/pron_test.py` is the ear check.
- **After any narration or audio change**, run `python3 scripts/build.py` (it re-stamps the service worker so
  phones pick up the change), then commit and push.
- **The operator's brochure photos** (`research/*.jpg`) are copyrighted and gitignored. Never commit them.
- **Facts are public.** Both writers flagged claims they couldn't fully verify; their reports are summarized
  in `research/fact-notes.md`. Check those first if anyone questions a line.
