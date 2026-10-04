# Image upload checklist

The HTML/JS block references images by relative path (e.g. `images/hero/hero.jpg`).
Those paths only exist on this computer — they won't resolve on your web builder.

**For each row below:** upload the file to your builder's media library, copy
the hosted URL it gives you, then find-and-replace the "Path used in code"
string with that URL inside `bsp-custom-html-js.html` before pasting it in.

| File (in /images) | Path used in code | Used for |
|---|---|---|
| hero/hero.jpg | `images/hero/hero.jpg` | Hero background photo |
| services/house-washing.jpg | `images/services/house-washing.jpg` | "House Washing" service tile |
| services/driveways.jpg | `images/services/driveways.jpg` | "Driveways & Walkways" service tile |
| services/patios-pool.jpg | `images/services/patios-pool.jpg` | "Patios & Pool Decking" service tile |
| before-after/slider-1-before.jpg | `images/before-after/slider-1-before.jpg` | Patio Cleaning slider — before |
| before-after/slider-1-after.jpg | `images/before-after/slider-1-after.jpg` | Patio Cleaning slider — after |
| before-after/slider-2-before.jpg | `images/before-after/slider-2-before.jpg` | Concrete Alcove slider — before |
| before-after/slider-2-after.jpg | `images/before-after/slider-2-after.jpg` | Concrete Alcove slider — after |
| before-after/slider-3-before.jpg | `images/before-after/slider-3-before.jpg` | Paver Patio & Fire Pit slider — before |
| before-after/slider-3-after.jpg | `images/before-after/slider-3-after.jpg` | Paver Patio & Fire Pit slider — after |
| before-after/static-1-before.jpg | `images/before-after/static-1-before.jpg` | Brick Wall — before |
| before-after/static-1-after.jpg | `images/before-after/static-1-after.jpg` | Brick Wall — after |
| before-after/static-2-before.jpg | `images/before-after/static-2-before.jpg` | Paver Patio — before |
| before-after/static-2-after.jpg | `images/before-after/static-2-after.jpg` | Paver Patio — after |
| before-after/static-3-before.jpg | `images/before-after/static-3-before.jpg` | Landscape Bed Cleanup — before |
| before-after/static-3-after.jpg | `images/before-after/static-3-after.jpg` | Landscape Bed Cleanup — after |
| before-after/static-4-before.jpg | `images/before-after/static-4-before.jpg` | Retaining Wall — before |
| before-after/static-4-after.jpg | `images/before-after/static-4-after.jpg` | Retaining Wall — after |
| before-after/static-5-before.jpg | `images/before-after/static-5-before.jpg` | Driveway — before |
| before-after/static-5-after.jpg | `images/before-after/static-5-after.jpg` | Driveway — after |
| before-after/static-6-before.jpg | `images/before-after/static-6-before.jpg` | Sidewalk (1) — before |
| before-after/static-6-after.jpg | `images/before-after/static-6-after.jpg` | Sidewalk (1) — after |
| before-after/static-7-before.jpg | `images/before-after/static-7-before.jpg` | Sidewalk (2) — before |
| before-after/static-7-after.jpg | `images/before-after/static-7-after.jpg` | Sidewalk (2) — after |

Notes:
- The service tile images (`house-washing.jpg`, `driveways.jpg`, `patios-pool.jpg`) are set as CSS
  `--img: url('...')` inline styles on 3 `<a class="bsp-service-tile">` elements — find those in the
  HTML block to replace them. Decks & Fences / Roof & Gutter / Commercial Storefronts tiles have no
  photo yet and will just show a dark tile until you add one.
- Most builders' media libraries let you bulk-upload; upload the whole `/images` folder at once and
  then match filenames back to this table.
