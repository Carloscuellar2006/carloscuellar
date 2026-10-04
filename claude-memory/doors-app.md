---
name: doors-app
description: Doors is a five-area life dashboard in doors/, inside the google map scrapper folder.
metadata:
  type: project
---

Doors (built 2026-08-23) lives at `doors/` inside the "google map scrapper"
directory — that folder is a Google Maps scraper otherwise. Don't assume files
there relate to scraping.

It started as a single-metric door-knocking tracker and Carlos redirected it into
a general life dashboard across five areas: Business, Relationships, Gym,
Content, Spirit. Design intent, rules, and the excluded list are in
`doors/README.md`.

**Why:** He changed the scope twice (added bank-balance levels, then the full
dashboard) after writing a spec that explicitly excluded gamification, gym, and
content. Those were deliberate, reaffirmed reversals — not drift to correct.

**How to apply:** Don't re-litigate the scope reversals. The one invariant he has
never dropped is the floor rule: every area has a floor, meeting it is a win, and
only zero breaks a streak. Protect that when adding anything. He does react to
scope-creep warnings, so flag additions that introduce a second number per area.
See [[decide-dont-survey]].
