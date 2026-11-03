# Wiring YouTube into the ThreadWizard social pipeline (pbs-v5)

Everything in this folder is written to drop into
`products/threadwizard/social/` on the mini. Nothing here is registered yet:
the channel stays **dark** (S-8) until the edits below land AND Chief Protein
flips the two switches he alone controls (OAuth consent, `YOUTUBE_PRIVACY`).

## 1. Files to copy

| From (this repo) | To (pbs-v5) |
|---|---|
| `youtube/pipeline/youtube_api.py` | `products/threadwizard/social/youtube_api.py` |
| `youtube/pipeline/youtube_publisher.py` | `products/threadwizard/social/youtube_publisher.py` |
| `youtube/pipeline/youtube_connect.py` | `products/threadwizard/social/youtube_connect.py` |
| `youtube/pipeline/test_youtube_publisher.py` | `products/threadwizard/social/test_youtube_publisher.py` |

## 2. `social/config.py` (S-14: the only schedule file)

```python
# --- YouTube (wtf.life Shorts) ---------------------------------------------
# S-8 identity contract: the OAuth token must authenticate as this handle or
# the channel is dark. Flip YOUTUBE_SCHEDULING_ENABLED only after
# youtube_connect.py printed "channel = @wtf.life".
YOUTUBE_PUBLISHING_IDENTITY = "wtf.life"
YOUTUBE_SCHEDULING_ENABLED = False

ALL_SLOTS += [
    # Film days per the ratified weekly contract (Tue/Thu/Sun). The reel bytes
    # already carry a proof sidecar; _install_queue_copies installs a copy into
    # every video_script slot, so yt-* reuses igr-* material without re-render.
    {"slot": "yt-0800",     "days": [1, 3], "time": "08:00", "platform": "youtube", "kind": "video_script", "critical": False},
    {"slot": "yt-2010-sun", "days": [6],    "time": "20:10", "platform": "youtube", "kind": "video_script", "critical": False},
]
DAILY_CAPS["youtube"] = 1          # Rule 31 — one Short per day, cap bypass only via approved: true
```

Slot times sit 20 min after `igr-0740` / 5 min before `igr-2015-sun` so the
same proof-bound mp4 exists when the dispatcher strikes and the 40-min slot
tolerance still covers a late film.

## 3. `social/publishers.py`

```python
import youtube_publisher
_LIVE["youtube"] = youtube_publisher.live
```

`_reel_caption` / `caption_with_brand` / `with_required_tags` are reused, so
the description carries the same OPIS + HASHTAGI + AI note + required tags as
IG Reels and TikTok, plus `#Shorts`.

## 4. `pbs-core/governance/blast-budget.yaml` (Rule 31: declare the cap before the first writer)

```yaml
social-post:
  caps:
    youtube: 1
```

## 5. Secrets (IRON CLAD 16) — Keychain only

```
security add-generic-password -s pbs -a YOUTUBE_CLIENT_ID     -w '<from console.cloud.google.com>'
security add-generic-password -s pbs -a YOUTUBE_CLIENT_SECRET -w '<…>'
```

`common.load_env()` already surfaces `pbs` Keychain items into the process.
Refresh token: `social/state/youtube_token.json` (0600, gitignored with the rest of `state/`).

## 6. Rule 46 — recurring authorization registry

Register `youtube_token.json` as a credential that can expire (Google revokes
refresh tokens after 6 months of non-use and whenever the OAuth app is in
"Testing" mode — 7 days). The `oauth_refresh_http_*` code from `youtube_api.token()`
is the renewal signal; route it to the same nag that owns TikTok/X re-auth.

## 7. Rule 51 — deadline watch

Add `yt-0800` / `yt-2010-sun` to `pbs-core/monitoring/social_deadline_watch.py`
with the same wall-clock budget as `tt-*` (dispatcher 15 min; upload call has
its own 600 s timeout inside `youtube_api.upload`).

## 8. Order of first light (S-5)

1. Copy files, run `python3 -m unittest test_youtube_publisher` on the mini (offline, $0).
2. Chief Protein: `python3 youtube_connect.py` in the GUI session, logged into the
   Google account that owns @wtf.life. Expect `channel = @wtf.life`.
3. Set `YOUTUBE_SCHEDULING_ENABLED = True`; leave `YOUTUBE_PRIVACY` unset (= private).
4. Next film day the dispatcher uploads PRIVATE. Read-after-write id lands in
   `logs/published.jsonl` and the blast ledger.
5. Chief Protein watches that private Short on YouTube itself (exact bytes,
   with audio) and ratifies the format; then `YOUTUBE_PRIVACY=public` in `.env`.
6. Until the Google API project passes the YouTube API compliance audit,
   YouTube forces API uploads to private regardless — the adapter reports the
   platform's privacy value, never the requested one. Public publication in that
   window is a one-click "make public" in YouTube Studio on the already-uploaded,
   already-proofed file (no re-upload, no second publication — S-9/S-16 hold).
