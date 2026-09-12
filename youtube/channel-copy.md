# WTF.LIFE on YouTube — channel copy (Polish, paste-ready)

All strings below are channel-facing and therefore Polish. Branding strings
are the code invariants from `publishers.py` / `carousel_cta.py` (S-13):
address written `WWW.WTF.LIFE`, discount line `KOD: WTF = −10%`, required tags
`#wtf #geopolityka #bitcoin #finanse #autopromocja`, AI disclosure line as on
the live assets since 2026-08-31 (`NAIS.WTF AI · autopromocja`).

## Identity

| Field | Value | Notes |
|---|---|---|
| Channel name | `WTF.LIFE` | wordmark casing, as on every asset footer |
| Handle | `@wtf.life` | **free on 2026-09-03** (youtube.com/@wtf.life → 404). `@wtflife` is TAKEN ("WTF LIFE CLIPS"). Fallbacks in order: `@wtf.life.pl`, `@wtf_life`, `@wtflifepl` |
| Country | Polska | |
| Default language | Polski | |
| Category (uploads) | Wiadomości i polityka (25) | |
| Links (order) | 1. `https://wtf.life/krypto` "Książka + audiobook" · 2. `https://wtf.life` "WWW.WTF.LIFE" · 3. Instagram · 4. TikTok | first link is shown on the channel header |
| Contact e-mail | `hello@wtf.life` | never a personal mailbox (IRON CLAD 56) |
| Watermark | `branding/watermark-150x150.png`, "cały film" | |

## Description (max 1000 chars, currently 677)

```
Codziennie jedno „what the fuck?!” ze świata pieniędzy, technologii i władzy — po polsku, bez żargonu i bez straszenia.

Twarde dane, miękka podawka. Co się wydarzyło, co to realnie zmienia i czego jeszcze nie wiemy. Krótko, bo masz życie.

Autor marki: Norbert Redkie — książka i audiobook „WTF?! KRYPTO” (29 rozdziałów, 7,5 h audio). Zamawiasz na WWW.WTF.LIFE, KOD: WTF = −10%.

Treść, obraz i głos w filmach są generowane przez NAIS.WTF AI (sklonowany głos autora) na podstawie codziennego, sprawdzonego raportu. Każdy film jest oznaczony jako treść syntetyczna. To nie jest doradztwo inwestycyjne. Porad inwestycyjnych: 0.

#wtf #geopolityka #bitcoin #finanse #autopromocja
```

## Keywords (channel settings → Podstawowe informacje → Słowa kluczowe)

```
"wtf.life" "what the fuck" "finanse osobiste" geopolityka bitcoin krypto kryptowaluty ropa inflacja giełda "Norbert Redkie" "WTF Krypto" audiobook shorts polska
```

## Upload defaults (Studio → Ustawienia → Domyślne ustawienia przesyłania)

- Tytuł: `<hook z raportu dnia>` (≤100 znaków — patrz `shorts/backlog.csv`)
- Opis (szablon):
  ```
  <hook>

  Wydanie WTF.LIFE z <dzień miesiąc rok>.

  Książka i audiobook „WTF?! KRYPTO” — WWW.WTF.LIFE · KOD: WTF = −10%

  Treść i głos wygenerowane przez NAIS.WTF AI · autopromocja

  #wtf #geopolityka #bitcoin #finanse #autopromocja #Shorts
  ```
- Widoczność: **Prywatny** (do ratyfikacji formatu — S-5), potem Publiczny
- Zmieniona lub syntetyczna treść: **TAK** (głos sklonowany + obrazy generowane) — obowiązkowe
- Dla dzieci: NIE · Płatna promocja: NIE (autopromocja własnej książki nie jest płatną promocją strony trzeciej; `#autopromocja` zostaje w opisie per UOKiK)
- Język filmu: polski · Kategoria: Wiadomości i polityka · Komentarze: wstrzymaj do sprawdzenia (kanał nowy, spam)
- Licencja: standardowa YouTube

## Playlists (sekcje strony głównej w tej kolejności)

1. `Shorts` (auto) — „Codzienne WTF”
2. `Główny raport dnia` — karuzele (3 rzeczy dnia) jako Shorts
3. `NAGŁE` — wydania nadzwyczajne (np. WTI 10.08)
4. `WTF?! KRYPTO — fragmenty` — puste do czasu decyzji org o fragmentach audiobooka (kanoniczny hash w `wtf-krypto-pr/canon/book_manifest.json`)

## Channel trailer (unsubscribed visitors) — recommendation

Use `2026-09-03-igr-0740` (ransomware w mniej niż 10 godzin, 2:11) as the
trailer until a dedicated 30-second trailer is produced through the film
pipeline. A trailer is a new format → S-5 proof-before-posting.

## Pinned comment (each Short)

```
Cała historia i wszystkie przypisy: WWW.WTF.LIFE · KOD: WTF = −10%. Treść i głos: NAIS.WTF AI (sklonowany głos autora) · autopromocja.
```

## Replies to comments (IRON CLAD 56)

Replies are written by NAIS, in NAIS's first person, never as Norbert. Template
opening for anything that could be read as the author speaking: „Tu NAIS —
asystent AI kanału, nie Norbert.” Comment replies are outward speech and go
through the grounded-speech rule (Rule 39): facts only from the day's report.
