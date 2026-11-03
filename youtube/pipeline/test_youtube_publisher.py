"""Offline tests for youtube_publisher (no network, no keys — Rule 30 zero-paid-test).
Runs anywhere: `python3 -m unittest test_youtube_publisher`.
config/common/publishers/youtube_api are stubbed because the real ones bind to
/Users/norbertredkie/_pbs paths."""
from __future__ import annotations

import os
import sys
import types
import unittest
from pathlib import Path


def _install_stubs(tmp: Path):
    cfg = types.ModuleType("config")
    cfg.STATE = tmp
    cfg.YOUTUBE_SCHEDULING_ENABLED = True
    cfg.YOUTUBE_PUBLISHING_IDENTITY = "wtf.life"
    pub = types.ModuleType("publishers")

    class NotConfigured(Exception):
        pass

    class AdapterFailure(Exception):
        def __init__(self, code):
            super().__init__(code); self.code = code
    pub.NotConfigured = NotConfigured
    pub.AdapterFailure = AdapterFailure
    pub._reel_caption = lambda body: body + "\n\nTreść i głos wygenerowane przez #NAIS.WTF AI.\n#wtf #geopolityka #bitcoin #finanse #autopromocja"
    pub._require_public_video = lambda entry: Path(entry["path"]).with_suffix(".mp4")
    yt = types.ModuleType("youtube_api")
    yt.TOKEN_FILE = tmp / "youtube_token.json"

    class YouTubeError(RuntimeError):
        def __init__(self, code):
            super().__init__(code); self.code = code
    yt.YouTubeError = YouTubeError
    yt.calls = []
    yt.identity = {"id": "UC1", "handle": "wtf.life", "title": "WTF.LIFE"}
    yt.readback = {"id": "VID1", "uploadStatus": "uploaded", "privacyStatus": "private", "title": "t"}
    yt.channel_identity = lambda: yt.identity
    def upload(video, title, description, tags, *, privacy, synthetic, **kw):
        yt.calls.append(("upload", video.name, title, description, privacy, synthetic)); return "VID1"
    yt.upload = upload
    yt.read_back = lambda vid: yt.readback
    for name, mod in (("config", cfg), ("publishers", pub), ("youtube_api", yt)):
        sys.modules[name] = mod
    sys.modules.pop("youtube_publisher", None)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import youtube_publisher as YP
    return cfg, pub, yt, YP


class T(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = Path(tempfile.mkdtemp())
        self.cfg, self.pub, self.yt, self.YP = _install_stubs(self.tmp)
        (self.tmp / "youtube_token.json").write_text("{}")
        os.environ.pop("YOUTUBE_PRIVACY", None)
        self.entry = {"slot": "yt-0800", "platform": "youtube", "kind": "video_script", "date": "2026-09-03",
                      "topic": "Atak ransomware z pomocą agentów AI trwał mniej niż 10 godzin",
                      "body": "OPIS POD WIDEO:\nKrócej niż dzień pracy.\n\nHASHTAGI: #ai #ransomware",
                      "path": str(self.tmp / "yt-0800.md")}

    def test_dark_channel_blocks_before_any_api_call(self):
        self.cfg.YOUTUBE_SCHEDULING_ENABLED = False
        with self.assertRaises(self.pub.NotConfigured):
            self.YP.live(self.entry)
        self.assertEqual(self.yt.calls, [])

    def test_missing_token_blocks(self):
        (self.tmp / "youtube_token.json").unlink()
        with self.assertRaises(self.pub.NotConfigured) as cm:
            self.YP.live(self.entry)
        self.assertIn("no token", str(cm.exception))
        self.assertEqual(self.yt.calls, [])

    def test_identity_mismatch_is_fail_closed(self):
        self.yt.identity = {"id": "UC9", "handle": "somebodyelse", "title": "x"}
        with self.assertRaises(self.pub.NotConfigured) as cm:
            self.YP.live(self.entry)
        self.assertIn("identity mismatch", str(cm.exception))
        self.assertEqual(self.yt.calls, [])          # never uploads to the wrong channel

    def test_happy_path_private_by_default_with_synthetic_flag_and_readback(self):
        res = self.YP.live(self.entry)
        self.assertEqual(res["status"], "published")
        self.assertTrue(res["detail"].startswith("VID1 privacy=private"))
        kind, name, title, desc, privacy, synthetic = self.yt.calls[0]
        self.assertEqual(privacy, "private")          # S-5: private until ratified
        self.assertTrue(synthetic)                    # synthetic-media disclosure always on
        self.assertEqual(title, self.entry["topic"])
        self.assertTrue(desc.endswith("#Shorts"))
        self.assertIn("#autopromocja", desc)

    def test_public_only_via_env_switch_and_forced_private_is_reported_honestly(self):
        os.environ["YOUTUBE_PRIVACY"] = "public"
        self.yt.readback = {"id": "VID1", "uploadStatus": "uploaded", "privacyStatus": "private", "title": "t"}
        res = self.YP.live(self.entry)
        self.assertIn("privacy=private (requested public)", res["detail"])   # API-audit lock, S-16 truth

    def test_readback_failure_is_adapter_failure_not_published(self):
        self.yt.readback = {"id": "VID1", "uploadStatus": "rejected", "privacyStatus": "private", "title": "t"}
        with self.assertRaises(self.pub.AdapterFailure):
            self.YP.live(self.entry)

    def test_provider_error_codes_are_bounded(self):
        def boom(*a, **k):
            raise self.yt.YouTubeError("upload_put_http_403")
        self.yt.upload = boom
        with self.assertRaises(self.pub.AdapterFailure) as cm:
            self.YP.live(self.entry)
        self.assertEqual(cm.exception.code, "youtube_upload_put_http_403")

    def test_title_is_truncated_to_100_chars(self):
        self.entry["topic"] = "słowo " * 40
        self.YP.live(self.entry)
        self.assertLessEqual(len(self.yt.calls[0][2]), 100)

    def test_missing_topic_blocks(self):
        self.entry["topic"] = ""
        with self.assertRaises(self.pub.NotConfigured):
            self.YP.live(self.entry)


if __name__ == "__main__":
    unittest.main()
