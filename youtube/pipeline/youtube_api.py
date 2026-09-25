"""ThreadWizard Social — YouTube Data API v3 adapter for the wtf.life channel.

Mirrors tiktok_api.py: stdlib only (urllib), token in state/youtube_token.json
(0600), refreshed automatically from the refresh_token; the first token is
minted once by youtube_connect.py through the Google OAuth consent screen,
which only Chief Protein can click (IRON CLAD 22: credential he alone holds).

Credentials (IRON CLAD 16 — never plaintext in the repo):
  YOUTUBE_CLIENT_ID / YOUTUBE_CLIENT_SECRET   -> Keychain, loaded by common.load_env()

Quota (default project quota 10 000 units/day):
  videos.insert = 1600 units  -> at most 6 uploads/day per project
  channels.list / videos.list = 1 unit each

Known platform lock: uploads from an API project that has NOT passed the
YouTube API compliance audit are forced PRIVATE by YouTube regardless of the
requested privacyStatus. The publisher treats the read-back privacyStatus as
truth (S-16), never the request.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import config as C

TOKEN_FILE = C.STATE / "youtube_token.json"
OAUTH_TOKEN = "https://oauth2.googleapis.com/token"
API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3/videos"
SCOPES = ("https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.readonly")
CATEGORY_NEWS = "25"           # News & Politics
TIMEOUT_S = 60
UPLOAD_TIMEOUT_S = 600         # Rule 51: hard wall-clock on the external call
CHUNK = 8 * 1024 * 1024        # multiple of 256 KiB as Google requires


class YouTubeError(RuntimeError):
    """Bounded, numeric-only error codes — provider bodies never leak upward
    (publishers.py reduces any other exception to its class name)."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _creds() -> tuple[str, str]:
    cid = os.environ.get("YOUTUBE_CLIENT_ID", "")
    sec = os.environ.get("YOUTUBE_CLIENT_SECRET", "")
    if not (cid and sec):
        raise YouTubeError("no_client_credentials")
    return cid, sec


def _request(method: str, url: str, *, data: bytes | None = None, headers: dict | None = None,
             timeout: int = TIMEOUT_S) -> tuple[int, dict, bytes]:
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def _save(tok: dict) -> None:
    tok["expires_at"] = time.time() + int(tok.get("expires_in", 3600)) - 120
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(tok, indent=1))
    TOKEN_FILE.chmod(0o600)


def exchange_code(code: str, redirect_uri: str) -> dict:
    """One-time: authorization code -> {access_token, refresh_token, ...}."""
    cid, sec = _creds()
    body = urllib.parse.urlencode({"code": code, "client_id": cid, "client_secret": sec,
                                   "redirect_uri": redirect_uri, "grant_type": "authorization_code"}).encode()
    status, _, raw = _request("POST", OAUTH_TOKEN, data=body,
                              headers={"Content-Type": "application/x-www-form-urlencoded"})
    tok = json.loads(raw or b"{}")
    if status != 200 or not tok.get("refresh_token"):
        raise YouTubeError(f"oauth_exchange_http_{status}")
    _save(tok)
    return tok


def token() -> str:
    """Valid access token; refreshes with the refresh_token near expiry."""
    if not TOKEN_FILE.exists():
        raise YouTubeError("no_token_file")
    tok = json.loads(TOKEN_FILE.read_text())
    if time.time() < tok.get("expires_at", 0) and tok.get("access_token"):
        return tok["access_token"]
    cid, sec = _creds()
    body = urllib.parse.urlencode({"client_id": cid, "client_secret": sec,
                                   "refresh_token": tok["refresh_token"],
                                   "grant_type": "refresh_token"}).encode()
    status, _, raw = _request("POST", OAUTH_TOKEN, data=body,
                              headers={"Content-Type": "application/x-www-form-urlencoded"})
    fresh = json.loads(raw or b"{}")
    if status != 200 or not fresh.get("access_token"):
        # Rule 46: an expired/revoked refresh token is a re-auth event, not a retry.
        raise YouTubeError(f"oauth_refresh_http_{status}")
    fresh.setdefault("refresh_token", tok["refresh_token"])
    _save(fresh)
    return fresh["access_token"]


def _auth() -> dict:
    return {"Authorization": f"Bearer {token()}"}


def channel_identity() -> dict:
    """{'id': 'UC…', 'handle': 'wtf.life', 'title': '…'} for the authenticated account.
    The S-8 identity guard compares `handle` with config.YOUTUBE_PUBLISHING_IDENTITY."""
    url = f"{API}/channels?" + urllib.parse.urlencode({"part": "snippet", "mine": "true"})
    status, _, raw = _request("GET", url, headers=_auth())
    if status != 200:
        raise YouTubeError(f"channels_list_http_{status}")
    items = json.loads(raw or b"{}").get("items") or []
    if not items:
        raise YouTubeError("no_channel_for_token")
    sn = items[0].get("snippet", {})
    return {"id": items[0].get("id", ""), "handle": str(sn.get("customUrl", "")).lstrip("@"),
            "title": sn.get("title", "")}


def upload(video: Path, title: str, description: str, tags: list[str], *,
           privacy: str = "private", synthetic: bool = True,
           category_id: str = CATEGORY_NEWS, language: str = "pl") -> str:
    """Resumable upload. Returns the YouTube video id. Raises YouTubeError on any non-success."""
    size = video.stat().st_size
    meta = {
        "snippet": {"title": title[:100], "description": description[:5000], "tags": tags[:30],
                    "categoryId": category_id, "defaultLanguage": language,
                    "defaultAudioLanguage": language},
        "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False,
                   # YouTube "altered or synthetic content" disclosure (mandatory:
                   # Norbert's cloned voice + generated imagery). Never omitted.
                   "containsSyntheticMedia": bool(synthetic)},
    }
    url = UPLOAD + "?" + urllib.parse.urlencode({"uploadType": "resumable", "part": "snippet,status"})
    status, headers, raw = _request(
        "POST", url, data=json.dumps(meta).encode(),
        headers={**_auth(), "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Length": str(size), "X-Upload-Content-Type": "video/mp4"})
    if status != 200:
        raise YouTubeError(f"upload_init_http_{status}")
    location = headers.get("Location") or headers.get("location")
    if not location:
        raise YouTubeError("upload_init_no_location")
    with video.open("rb") as f:
        data = f.read()
    status, _, raw = _request("PUT", location, data=data,
                              headers={**_auth(), "Content-Type": "video/mp4",
                                       "Content-Length": str(size)},
                              timeout=UPLOAD_TIMEOUT_S)
    if status not in (200, 201):
        raise YouTubeError(f"upload_put_http_{status}")
    vid = json.loads(raw or b"{}").get("id")
    if not vid:
        raise YouTubeError("upload_no_id")
    return vid


def read_back(video_id: str) -> dict:
    """S-16 read-after-write: the platform's own view of the upload.
    {'id', 'uploadStatus', 'privacyStatus', 'title'} or raises."""
    url = f"{API}/videos?" + urllib.parse.urlencode({"part": "status,snippet", "id": video_id})
    status, _, raw = _request("GET", url, headers=_auth())
    if status != 200:
        raise YouTubeError(f"videos_list_http_{status}")
    items = json.loads(raw or b"{}").get("items") or []
    if not items:
        raise YouTubeError("readback_not_found")
    it = items[0]
    return {"id": it.get("id"), "uploadStatus": it.get("status", {}).get("uploadStatus"),
            "privacyStatus": it.get("status", {}).get("privacyStatus"),
            "title": it.get("snippet", {}).get("title", "")}
