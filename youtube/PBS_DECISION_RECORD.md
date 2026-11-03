# PBS DECISION RECORD — wtf.life YouTube channel launch

**Matter:** Chief Protein's order of 2026-09-03 (verbatim, Polish): „Chce miec kanal na youtube. Wtf.life - zaloz za mnie. Uzyj calego pbs”.
**Requirement (Rule 14):** a YouTube channel for wtf.life exists and is fed by the org. The HOW below is the org's.
**Priority (Rule 52):** P2 — content as revenue (marketing for „WTF?! KRYPTO”, not the product).
**Commander:** Fable (Claude frontier surface, remote container session). **Verifier:** none reachable — see Quorum.
**Reserved classes touched (charter):** `credential_or_physical` (Google login, phone verification, OAuth consent, Cloud project owner). `out_of_roadmap_new_direction` is satisfied by the order itself (Phase 0 YES came from Chief Protein). `subjective_founder_brand` is NOT invoked: naming and format are org decisions under Rule 14.

## Quorum attestation (Rule 28) — read this first

| Seat | Path checked | Result |
|---|---|---|
| Claude (Fable) | this session | alive |
| Codex | no Codex CLI / MCP in the remote container | unreachable |
| GPT / Gemini / Grok debate legs | `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `XAI_API_KEY`, `GOOGLE_API_KEY` absent; `run_pbs.py` would exit 2 (DEGRADED ORG) | not run |

Seats alive: **1 → 1/1**. Under Rule 28 a 1-alive org may decide but may not execute a PROCEED without a second witness and may not kill. Therefore this record is a **recommendation package (Rule 53)**, single-verified: peer down. The PROCEED witness is either (a) the L4 debate on the mini —
`pbs-core/security/llm_debate.py "Should wtf.life open a YouTube Shorts channel fed by the existing film line, private-first, under IRON SOCIAL?" --context-file youtube/PBS_DECISION_RECORD.md --level L4 --save pbs-core/debates/debate-wtf-youtube-2026-09-03.json`
— or (b) Chief Protein's ratification below. Nothing in this package publishes anything; every artefact is private, local, $0.

Cross-surface receipt (Rule 45): visibility from this container into OpenClaw runs, Codex tasks and the mini's launchd is **none**; conclusion about concurrent work on this topic = `unknown`. Rule 48 owner check could not be performed — if a session on the mini already owns "YouTube", this package is its input, not a fork.

## Seat inputs (L3 confab, chaired by the CEO seat)

- **CEO** — The film line already produces a ratified 9:16, ≤3-min, Norbert-voiced asset three times a week; YouTube Shorts accepts exactly that. Zero new production cost; the only new cost is attention. Recommend PROCEED as a distribution channel of the existing product, not a new product (no Rule 12 identity fork: the channel inherits the wtf.life social identity — white serif on faded colour photo, WTF wordmark, `NAGŁE` red bar).
- **CMO** — Sells? The CTA card („KOD: WTF = −10%", WWW.WTF.LIFE) is already inside every reel, and YouTube allows clickable links in the channel header and description — the first platform where the address is a live link next to the video. Findable? Handle `@wtf.life` is free; the channel name equals the domain. Risk: news Shorts decay in 48 h; the backlog of 26 first-priority items is context, not growth.
- **CDesigner** — Banner, avatar and watermark are drawn by code from the existing wordmark (S-13). Tagline and CTA bar sit inside the 1546×423 safe area (machine-verified). Letterboxed carousel Shorts are honest but visibly weaker than full-bleed film; recommend they go second and that the org decides later on a blurred-fill variant (design change = Chief Protein's call per S-12).
- **CVideo** — Three derivations are deterministic and re-checkable by hash: reel passthrough (identical bytes), story-serial concat (stream copy, no re-encode), carousel concat + pad (re-encode, crf 23, 2.5 Mbps cap). Story chrome (CZĘŚĆ n/4, „dalej ▶") is carried into the Short — disclosed. The 58 s story-card cap (S-21) does not apply to YouTube; the Shorts cap is 180 s and every candidate passes.
- **CLO / Compliance** — (1) YouTube requires the "altered or synthetic content" disclosure for realistic cloned voice — set on every upload in code, never optional. (2) AI Act art. 50 + UOKiK: the on-screen AI line and `#autopromocja` stay. (3) IRON CLAD 56: description and comment replies are NAIS's voice; the author appears in third person only. (4) API uploads from an un-audited Google project are forced private — a platform fact, not a defect; the adapter logs the platform's value.
- **CFO** — Spend $0 to date and $0 planned: no paid generation, no ads. Quota is the constraint, not money: 6 API uploads/day per project; cadence is 1/day.
- **CSecurity** — No plaintext secrets: client id/secret to Keychain, refresh token to gitignored `state/`. S-8 identity guard mirrors the X incident: token must resolve to `@wtf.life` or the channel stays dark; enabled flag defaults to False in config.
- **Chief Tester** — 9 offline tests pass (dark channel, missing token, identity mismatch, private-by-default, synthetic flag, read-after-write failure, bounded error codes, title cap, missing topic). Three proof Shorts built and hash-verified. Not testable here: the live OAuth flow, the resumable upload against Google, the banner rendering inside YouTube's UI.

## OPTIONS (Rule 53)

1. **Shorts-only channel fed by the film line, private-first, org-automated.** 3 Shorts/week on film days (Tue/Thu/Sun) + carousel Shorts as second item on non-film days if ratified. Manual "make public" in Studio until the API audit passes.
2. **Manual channel only.** Chief Protein uploads from the assets repo by hand; no pipeline change. Zero code risk, but violates the standing automation posture and Rule 51 (no delivery deadline, no watchdog).
3. **Wait for a dedicated long-form format.** Nothing ships until a 5–10 min video product exists. Loses the free distribution of an asset that already exists.

## DECISION — org recommends Option 1

Open `@wtf.life` on YouTube as a Shorts channel of the existing wtf.life film line; wire it as a `youtube` platform in `social/config.py` with `YOUTUBE_SCHEDULING_ENABLED=False` until the token proves the handle; first uploads private; format ratified from the exact bytes on YouTube; then public. Backlog: the 26 priority-1 items in `shorts/backlog.csv` are available as a launch batch of 7 (newest week) — older news is not re-published as fresh (S-11: dates are in every description).

Rationale in one line: the asset, the voice, the brand line and the compliance labels already exist and are ratified; YouTube is the first platform where the sales link is clickable next to the video; the marginal cost is a 25-minute human step and zero dollars.

## Kill criteria (Brutal Assessment §Kill, measurable)

1. 60 days after going public and ≥25 public Shorts: total views < 5 000 **and** subscribers < 100 → STOP the automat, keep the channel as an archive.
2. Any Community Guidelines strike or a "misleading synthetic media" takedown → channel dark same day (config flag), incident row, org root-cause before any re-enable.
3. Google API compliance audit rejected twice → the channel becomes manual-only (Option 2) and the dispatcher slot is removed; no third application without a new package.

## Rollback (Rule 32)

Before the channel is created, this record is the rollback ledger entry:
`inverse: delete uploads (Studio) → delete channel content (Ustawienia zaawansowane) — pre_state: no channel — tripwire: kill criteria 2 — rollback_tested: NO (declared-only)`.
Uploads are private-first, so every individual publication is reversible by deletion before anyone has seen it.

## KNOWN IMPERFECTIONS (S-6) — status per item

| # | Imperfection | Status |
|---|---|---|
| 1 | 4-LLM debate not run; Codex verifier unreachable; decision is single-frontier 1/1 | OPEN — needs the L4 run on the mini or Chief Protein's ratification |
| 2 | The channel is not created — Google login, phone verification and OAuth consent are Chief Protein's credentials | OPEN — runbook in `CHANNEL_SETUP.md` |
| 3 | Handle availability checked only by an unauthenticated 404 on 2026-09-03; YouTube may reserve or filter `wtf` handles | OPEN — fallbacks listed |
| 4 | Story-serial Shorts carry IG chrome (progress bar, „dalej ▶") | DISCLOSED — ratify or reject that format |
| 5 | Carousel Shorts are letterboxed 4:5 inside 9:16 (black bars) | DISCLOSED — blurred-fill variant is a design decision (S-12) |
| 6 | Banner/avatar use FreeSans Bold + DejaVu Serif Bold, not the mini's Arial Black / Georgia; wordmark itself is the original bitmap | DISCLOSED — pixel-identical fonts would need the mini's renderer |
| 7 | `products/wtf.life/BRAND_BOOK.md`, `ESTETYKA_WTF_LIFE.md` are not on disk in any repo cloned here; brand facts were taken from code invariants and the live assets | DISCLOSED |
| 8 | AI-disclosure line: live assets since 2026-08-31 say `NAIS.WTF AI`, the pbs-v5 snapshot of `publishers.py` (2026-08-27) still says `ThreadWizard.xyz` — the adapter reuses whatever `publishers._reel_caption` emits on the mini | DISCLOSED — no drift introduced here |
| 9 | Live OAuth, resumable upload and read-back are untested against Google (no credentials by design, Rule 30 zero-paid-test); code paths are covered by stubs only | OPEN — first live run is the test, private, $0 |
| 10 | API uploads forced private until Google's compliance audit passes; public publication of API uploads needs a Studio click in that window | PLATFORM FACT |
| 11 | Titles for the 58 backlog items were derived by OCR of the first frame plus editorial normalisation, not from the queue files (not in any repo here) | DISCLOSED — S-11 holds because each title is the asset's own on-screen hook |
| 12 | `ig-2000` evening slot exists in the assets but not in the pbs-v5 config snapshot on disk | DISCLOSED — INTEGRATION.md targets the live `config.py` on the mini |
| 13 | Rule 48 owner-session check and Rule 45 cross-surface inventory impossible from this container | DISCLOSED |
| 14 | PBS canonical ledger (`WTF_PRODUCTION_LEDGER.jsonl`) is not appended here (different repo, no push authority); entries are staged in `youtube/ledger.jsonl` for the mini to append | OPEN |

## Ratification (Chief Protein) — one recommendation, answer inline

The org recommends **Option 1**. To ratify, reply with the literal lines (each on its own line, so the reply can be hash-bound like the film contract):

```
RATIFY: youtube-channel-option-1
FORMAT reel: public|reject
FORMAT stories-concat: public|reject
FORMAT carousel-letterbox: public|reject
```

Until those lines exist, everything stays private and `YOUTUBE_SCHEDULING_ENABLED` stays `False`.
