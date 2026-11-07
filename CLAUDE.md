# inOne Imaging — website prototype

A clickable mockup of a new website for inOne Imaging, a radiologist-led practice in Melbourne's north and west. It combines the current site (inoneimaging.com.au) with screening, intervention and education sections, and adds I-MED-style patient and clinician portals. The aim is to take the best of jonesradiology.com.au, imagingassociates.net.au, radiusimaging.com.au and qscan.com.au.

Live: https://drgmitreski.github.io/inone-mockup/ (GitHub Pages, branch `main`, root folder).

## How it's built

- Edit the pages in `source/pages/*.dc.html`.
- Build with `python3 source/build.py`, which writes `index.html` at the repo root.
  - The output is one self-contained file: hash routing (`#page` or `#page--anchor`), images embedded as data URIs, and a noindex tag.
  - Never hand-edit `index.html`; it's regenerated on every build.
- `source/pages/Header.dc.html` is the shared header. Each page imports it with `<dc-import name="Header" mode="patient|clinician|none" active="...">`.
- Images live in `source/images/`. `build.py` maps the `/_blob/<id>` references in the pages to these files.
- Research publications come from `source/pubs.json` (PubMed, 2024–2026).
- Needs Python 3 with Pillow (`pip3 install pillow`).

## Doctor photos

The headshots come from `https://media.base44.com/images/public/69a9f3dc05d4f7f2914e64a9/` (file names are in `heads` in `build.py`). They load from there at runtime, and initials show if a photo fails. Goran doesn't like the initials.

**To do next:** download the five photos into `source/images/heads/` and embed them in the build as data URIs, so the faces show everywhere and the initials are gone.

## Brand

- Wordmark: navy #1A1F4A, with a segmented ring "O" in purple #5A4593 / #B3A6D4.
- Plum #2B2350 replaces navy on the home page.
- Colour for each service:
  - Diagnosis #4A3A84
  - Intervention #9A3623 / #6E1E16
  - Screening #355E46 / #1F4A36
  - Education #1D4A7E / #13294A
- Fonts: Inter for everything (weights 400–600), loaded by `build.py`. Montserrat is kept only for the wordmark (`.wm`). The old Montserrat/Hanken/Fraunces inline fonts are overridden by `source/design.css`.

## Design layer (Nov 2026 redesign)

- Direction: Stripe-inspired (via the `design-md` skill), in inOne plum. Light-weight Inter headings with tight tracking, gradient-mesh heroes, hairline cards, pill buttons, soft elevation.
- `source/design.css` is inlined by `build.py`. It holds the tokens, component classes (`.btn`, `.seg`, `.navlink`, `.door`, `.mesh`, `.eyebrow`) and global overrides (attribute selectors with `!important`) that restyle the inline-styled pages without editing each element.
- The header is sticky (nav row only) and collapses to one scrolling row on phones. `build.py` keeps its own Python copy of the header context, so change both it and `Header.dc.html`.
- The home page must still fit one screen (checked at 1280×640 and 1440×900).

## Decisions so far

- **Home page (`Main.dc.html`)**
  - Must fit one screen with no scrolling. It's been checked at 1280×640 to 2391×1350.
  - Two symmetrical boxes: For patients and For referring doctors.
  - Under the headline: a row of five overlapping faces, then "Meet our radiologists →". No names in that row.
  - The Medicare "we bulk bill" emblem goes in the bottom band.
  - Goran prefers the current home over the warm option, but wants it more inviting: less corporate, less "surgical/AI".
- **"View site as: Patient | Clinician"** toggle on every page. Each audience gets its own menu.
  - Top menu with no audience chosen: Our radiologists, Our clinics, About us.
- **Three portals:** patient (one-time code), referral, and clinical (Synapse).
- **Intervention in clinic:** complex pain, varicose veins, MSK ablation and sclerotherapy only. UAE, PAE, OVE and varicocele are hospital referral pathways.
- **Content copied from the live site:** Our radiologists, Our clinics (Roxburgh Park, Deer Park, Bacchus Marsh, Taylors Lakes) and About us.
- **Working style:** Goran wants honest critique, not agreement. Keep buttons symmetrical and neat.

## Still to confirm with Goran

- MRI offering
- Founder wording vs "radiologist-led"
- CPD points
- Results-release policy
- Photo licences (the CT stock photo, symposium photos)
- Whether the angio suite photo is inOne's
- Real clinic photos

## Ideas offered, not started

- Roll the softer home style out to the other pages: sentence-case labels, pill buttons, plum, lighter headlines.
- Hover drop-down menus like Imaging Associates.

## Publishing

Commit and push to `main`; GitHub Pages redeploys in about a minute.
