---
name: door-knock-planner
description: "How Carlos wants the Huntsville door-knocking planner to work, and which data sources actually exist for it"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9aeb542e-85af-49bf-99ba-b7680b5e9be5
  modified: 2026-09-23T05:05:41.991Z
---

`~/Desktop/door-knocking/build_routes.py` plans door-to-door routes for [[big-spring-target-customer]] in Huntsville, AL.

**The rule Carlos set (Sept 22, 2026):** Redfin's $500k+ filter picks the *neighborhood*, never the doors. When he is out knocking he knocks **every house on the street**. And a street only counts if the area around it is **majority** $500k+ — a couple of expensive houses on an otherwise mid-priced street does not qualify it.

**Data reality, measured not assumed:**
- OpenStreetMap **roads** in Huntsville are complete — a Blossomwood box returned 65 ways / 49 named streets. Street centrelines are reliable.
- OSM **addresses** (31 points, 4 streets) and **buildings** (12) in that same box are far too sparse to enumerate or count doors. Door counts must stay *estimates* from street length ÷ frontage.
- Redfin exports **sold homes only**, cap at 350 rows, require his login, and their ToS forbids scraping — he downloads the CSVs himself. Two exports per ZIP are needed: one `min-price=500k`, one with **no price filter**, because the cheap sales are the denominator of the majority test. With only the filtered file the share is 100% everywhere and the tool must say so rather than pass everything.
- Overpass rate-limits and 504s often; the script retries each mirror and caches to `.roads-cache.json`.

**Why:** These findings cost real probing to establish and they constrain what the tool can honestly claim. Presenting an estimated door count as a house list, or a 2-comp street as a rich neighborhood, would send him out on wasted days.

**How to apply:** Never route only the filtered houses. Never present door counts as exact. Keep addresses only — no owner names or phone numbers. The Huntsville solicitation permit question is still unconfirmed with the City Clerk and the tool warns about it on every page.
