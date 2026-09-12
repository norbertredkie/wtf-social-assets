"""ThreadWizard Social — YouTube (Shorts) live adapter for the wtf.life channel.

Drop next to publishers.py and register:  publishers._LIVE["youtube"] = youtube_publisher.live
(see INTEGRATION.md for the exact config.py / blast-budget.yaml / publishers.py edits).

Order of gates, all fail-closed (IRON SOCIAL S-3/S-5/S-8/S-16):
  1. S-8  channel enabled in config AND token authenticates as the approved handle
  2. S-3  exact mp4 bytes bound to their production proof (publishers._require_public_video)
  3. S-5  privacy defaults to PRIVATE until Chief Protein has ratified the YouTube
          format from the exact bytes; going public is an env switch he flips
          (YOUTUBE_PRIVACY=public), never a code default
  4. S-16 read-after-write: the id and privacy we log are what YouTube reports
"""
from __future__ import annotations

import os
import re

import config as C
import publishers as P

TITLE_MAX = 100
SHORTS_TAG = "#Shorts"
DEFAULT_TAGS = ["wtf", "wtf.life", "geopolityka", "bitcoin", "finanse", "krypto", "shorts"]


def _title(entry: dict) -> str:
    """Queue frontmatter `topic` is the hook the slicer wrote for the day (S-11:
    the caption never lies — the title is the material's own topic, not fresh copy)."""
    topic = re.sub(r"\s+", " ", str(entry.get("topic", "")).strip())
    if not topic:
        raise P.NotConfigured("YouTube: queue entry has no topic for the title (S-11)")
    if len(topic) > TITLE_MAX:
        topic = topic[:TITLE_MAX - 1].rsplit(" ", 1)[0] + "…"
    return topic


def _description(entry: dict) -> str:
    """Same OPIS/HASHTAGI + brand line + required tags as IG Reels/TikTok, plus #Shorts."""
    cap = P._reel_caption(entry["body"])
    return cap.rstrip() + " " + SHORTS_TAG


def _identity_guard() -> None:
    if not getattr(C, "YOUTUBE_SCHEDULING_ENABLED", False):
        raise P.NotConfigured("YouTube: dark — YOUTUBE_SCHEDULING_ENABLED=False (S-8)")
    approved = getattr(C, "YOUTUBE_PUBLISHING_IDENTITY", "")
    if not approved:
        raise P.NotConfigured("YouTube: no approved identity in config (S-8)")
    import youtube_api as Y
    if not Y.TOKEN_FILE.exists():
        raise P.NotConfigured("YouTube: no token — run youtube_connect.py")
    ident = Y.channel_identity()
    if ident.get("handle", "").casefold() != approved.lstrip("@").casefold():
        # Same shape as the X incident of 2026-08-09: wrong account = channel dark.
        raise P.NotConfigured(f"YouTube: identity mismatch (S-8): token is @{ident.get('handle')}")


def live(entry: dict) -> dict:
    _identity_guard()
    video = P._require_public_video(entry)          # S-3: mp4 + proof sidecar, hash-bound
    import youtube_api as Y
    privacy = os.environ.get("YOUTUBE_PRIVACY", "private")
    if privacy not in ("private", "unlisted", "public"):
        raise P.NotConfigured("YouTube: YOUTUBE_PRIVACY must be private|unlisted|public")
    try:
        vid = Y.upload(video, _title(entry), _description(entry), DEFAULT_TAGS,
                       privacy=privacy, synthetic=True)
        seen = Y.read_back(vid)                      # S-16
    except Y.YouTubeError as e:
        raise P.AdapterFailure(f"youtube_{e.code}")
    if seen.get("uploadStatus") not in ("uploaded", "processed"):
        raise P.AdapterFailure("youtube_readback_status")
    if seen.get("privacyStatus") != privacy:
        # Not an error to hide: the API-audit lock forces private. Log the truth.
        return {"status": "published",
                "detail": f"{vid} privacy={seen.get('privacyStatus')} (requested {privacy})"}
    return {"status": "published", "detail": f"{vid} privacy={privacy}"}
