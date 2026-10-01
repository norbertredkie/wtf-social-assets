# CHANNEL_SETUP — the human steps, click by click (Chief Protein only)

Why you and not the org: Google account login, phone verification, the OAuth
consent screen and the Cloud project owner role are credentials only you hold
(IRON CLAD 22 lawful blocker: "credentials he alone holds"). Everything else
in this folder is done. Budget: ~25 minutes, $0.

## A. Create the channel (10 min)

1. Log into Google with the account that should OWN the channel. Recommendation:
   a `hello@wtf.life` Google Workspace/Gmail identity, not your private one, so
   the org can hold the OAuth without your personal mailbox (IRON CLAD 56).
2. youtube.com → avatar → **Utwórz kanał** → choose **Użyj nazwy niestandardowej**.
   Name: `WTF.LIFE`. Do NOT use your personal name.
3. Studio (studio.youtube.com) → **Dostosowanie** → **Marka**:
   - Zdjęcie: `youtube/branding/avatar-800x800.png`
   - Baner: `youtube/branding/banner-2560x1440.png` (safe-area verified: every pixel of text sits inside 1546×423 — see `_proof-banner-safe-areas.png`)
   - Znak wodny: `youtube/branding/watermark-150x150.png`, "cały film"
4. **Podstawowe informacje**: name `WTF.LIFE`; handle `@wtf.life`
   (free as of 2026-09-03; fallbacks in `channel-copy.md`); description, links,
   contact e-mail, keywords — all paste-ready in `channel-copy.md`.
5. **Ustawienia → Kanał → Podstawowe informacje**: kraj Polska; słowa kluczowe.
   **Ustawienia → Kanał → Ustawienia zaawansowane**: „Nie, ten kanał nie jest przeznaczony dla dzieci”.
6. **Weryfikacja telefonu** (youtube.com/verify) — unlocks custom thumbnails,
   >15 min uploads and, with time, the Community tab. Uses your phone; org cannot.
7. **Domyślne ustawienia przesyłania** — paste from `channel-copy.md` §Upload defaults.
   Tick **„Zmieniona lub syntetyczna treść”** in the defaults; it must be on for every upload.

## B. First content, manual, PRIVATE (5 min)

Upload the three proof files so the format can be ratified on YouTube itself
(S-5: exact bytes, with audio):

| File | Format | Title (from `shorts/backlog.csv`) |
|---|---|---|
| `2026-09-03-igr-0740/igr-0740.mp4` (byte-identical passthrough) | reel → Short | Atak ransomware z pomocą agentów AI trwał mniej niż 10 godzin |
| `youtube/shorts/proof/2026-09-03-igs-0745-short.mp4` | stories concat → Short | Ransomware z agentami AI w mniej niż 10 godzin. WTF: firma nie zauważyła części śladów |
| `youtube/shorts/proof/2026-09-02-ig-2000-short.mp4` | carousel letterboxed → Short | Czemu ropa kosztuje dziś 95 dolarów? Iran odpowiedział rakietami |

Visibility **Prywatny**. Watch them on YouTube, then answer the ratification in
`PBS_DECISION_RECORD.md` §Ratification (one word per line: which of the three
formats go public). Note: the reel and the stories file are the SAME message
of 2026-09-03 — S-9 says only one of them goes public.

## C. Google Cloud project for the automat (10 min, once)

1. console.cloud.google.com → new project `wtf-life-social` → **APIs & Services → Library → YouTube Data API v3 → Enable**.
2. **OAuth consent screen**: External, app name `NAIS.WTF Social`, support e-mail `hello@wtf.life`,
   scopes `youtube.upload` + `youtube.readonly`. Add the channel's Google account as a test user.
   In **Testing** mode refresh tokens expire after 7 days → click **Publish app** (no audit needed for publishing the consent screen itself).
3. **Credentials → Create → OAuth client ID → Desktop app** → download; put the two values into Keychain (commands in `pipeline/INTEGRATION.md` §5). Never into `.env` or the repo.
4. Later (org handles the form, you sign): **YouTube API Services compliance audit** — until it passes, API uploads are forced PRIVATE by YouTube. Manual "make public" in Studio is the bridge.
5. On the mini, GUI session: `python3 products/threadwizard/social/youtube_connect.py` → consent → expect `channel = @wtf.life`.

## D. What you will get back

- `logs/published.jsonl` row `platform=youtube status=published detail=<videoId> privacy=…` after every dispatch (S-16).
- A Telegram line per upload from the existing dispatcher reporting (no new channel of communication).
- Rule 46 nag when the refresh token dies.

## Rollback (Rule 32)

- One upload: Studio → film → Usuń (or keep private). Reversible, tested by YouTube's own flow.
- Whole channel: Ustawienia → Ustawienia zaawansowane → **Usuń zawartość kanału** (Google keeps the handle reserved briefly; the Google account survives). DECLARED-ONLY — not rehearsed here.
