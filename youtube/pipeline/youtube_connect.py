#!/usr/bin/env python3
"""One-time OAuth for the wtf.life YouTube channel (run on the mini, GUI session).

Chief Protein clicks the consent screen while logged into the Google account
that OWNS the @wtf.life channel. Everything else is automatic. The refresh
token lands in state/youtube_token.json (0600) — never in the repo.

  python3 youtube_connect.py            # opens the URL, waits on localhost:8765
"""
from __future__ import annotations

import http.server
import os
import urllib.parse
import webbrowser

import youtube_api as Y

PORT = int(os.environ.get("YOUTUBE_OAUTH_PORT", "8765"))
REDIRECT = f"http://localhost:{PORT}/"


def main() -> None:
    cid, _ = Y._creds()
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": cid, "redirect_uri": REDIRECT, "response_type": "code",
        "scope": " ".join(Y.SCOPES), "access_type": "offline", "prompt": "consent",
        "include_granted_scopes": "true"})
    code: dict = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            code["v"] = (q.get("code") or [""])[0]
            self.send_response(200); self.end_headers()
            self.wfile.write(b"OK - you can close this tab.")
        def log_message(self, *a):  # silence
            pass

    print("Open this URL in the browser logged into the wtf.life Google account:\n", url)
    webbrowser.open(url)
    with http.server.HTTPServer(("localhost", PORT), H) as s:
        s.handle_request()
    if not code.get("v"):
        raise SystemExit("no code received")
    Y.exchange_code(code["v"], REDIRECT)
    ident = Y.channel_identity()
    print(f"token saved to {Y.TOKEN_FILE}; channel = @{ident['handle']} ({ident['id']})")


if __name__ == "__main__":
    main()
