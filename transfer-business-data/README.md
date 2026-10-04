# Transfer — Big Spring business data

Everything current, nothing superseded. **8.9 MB**, well under GitHub's limits
(100 MB per file, 25 MB per file through the web uploader).

## What's here

| Folder | What |
|---|---|
| `website/` | The live home page — `index.html` + its CSS, JS, logo, privacy/terms, and the GHL embed snippets |
| `logo/` | Big Spring logo — every SVG, plus the rasters worth keeping |
| `brand/` | Brand marks and favicons, vector only |
| `business-card/` | R-V1 Renovations card — print PDF, both faces, build script |
| `referral/` | Referral card and sheet, print-ready PDFs + build script |
| `print/` | Door hanger and yard signs, printer-ready, + the scripts that made them |

## What I deliberately left out

- **7 `index.backup-*.html`** and 3 `style.backup-*.css` — superseded drafts
- **`images/` (33 MB)** — see the warning below
- **`images/opt/`** — optimized duplicates of the above
- **`social/` (4.9 MB)** and `ad-creatives/` — Facebook covers and ad images, regenerable
- **PNG twins of every print PDF** — one 13.3 MB yard-sign PNG alone; the PDF is what a printer wants
- **Preview JPGs** — proofs, not deliverables

Those still exist in `Buisness/Buisness/pressure-washing-site/`. Nothing was deleted.

## ⚠ The website's photos are NOT in here

`index.html` loads its 10 photos from GoHighLevel's CDN, not from local files:

```
https://assets.cdn.filesafe.space/v8QzAzr7K3RAa3YQ2t0A/media/...
```

That was deliberate — relative image paths don't resolve inside a GHL block. The
consequence is that **the page only shows its photos while that GHL account is
live**. If you ever lose or leave that account, the service tiles and gallery go
blank.

The originals are in `pressure-washing-site/images/` (33 MB). If you want the page
to stand alone, the image URLs need swapping back to local paths — a small change,
ask when you want it.

## Also note

- `business-card/` was recovered from **iCloud Trash** — it had been deleted and
  iCloud purges after 30 days. This copy is now the only one.
- The live site at bigspringpressurewashing.com is **older** than `website/here`.
  It still says "Big Spring Pressure Washing" and claims "Licensed & Insured",
  "Google Guaranteed" and "Background Checked Crews" — none of which you can
  currently make. Fix those in GHL regardless of whether you deploy this version.
