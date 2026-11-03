# youtube/ — wtf.life YouTube channel launch package

Produced 2026-09-03 on Chief Protein's order („Chce miec kanal na youtube. Wtf.life — zaloz za mnie. Uzyj calego pbs”). Everything a channel needs except the three clicks only the account owner can make. Spend so far: **$0**. Nothing is published.

| Read this if you are… | File |
|---|---|
| Chief Protein, 25 minutes, doing the human steps | `CHANNEL_SETUP.md` |
| …and want the paste-ready Polish strings | `channel-copy.md` |
| the org, ratifying or debating the decision | `PBS_DECISION_RECORD.md` (Rule 53: OPTIONS / DECISION / KNOWN IMPERFECTIONS) |
| the session wiring the mini | `pipeline/INTEGRATION.md` |
| the ledger keeper | `ledger.jsonl` → append to `WTF_PRODUCTION_LEDGER.jsonl` |

## What is in here

```
branding/    avatar-800x800.png · banner-2560x1440.png · watermark-150x150.png · _proof-banner-safe-areas.png
shorts/      make_shorts.py (deterministic builder) · backlog.csv (62 rows: title, description, priority, imperfections) · proof/ (2 built Shorts + 3 hash sidecars)
pipeline/    youtube_api.py · youtube_publisher.py · youtube_connect.py · test_youtube_publisher.py · INTEGRATION.md
```

## Status board

| Step | State |
|---|---|
| Handle `@wtf.life` | free on 2026-09-03 (`@wtflife` taken) |
| Branding | rendered, safe-area verified |
| Channel copy (PL) | ready, 677-char description, keywords, defaults, playlists |
| Shorts backlog | 58 videos classified, 26 priority-1; 3 proof files built and hash-checked |
| Publisher code | written, 9/9 offline tests pass, **not registered** (channel dark by default) |
| PBS decision | Rule 53 package presented; quorum 1/1 single-surface — needs L4 run on the mini or ratification |
| Channel creation | **waiting on Chief Protein** (Google login, phone, OAuth consent) |

## Re-verify locally ($0)

```bash
python3 youtube/shorts/make_shorts.py --list
python3 youtube/shorts/make_shorts.py --check youtube/shorts/proof/2026-09-03-igs-0745-short.mp4
cd youtube/pipeline && python3 -m unittest -v test_youtube_publisher
```
