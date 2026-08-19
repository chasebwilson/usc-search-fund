# USC Search Fund — website

Static site. No build step, no dependencies. Four pages plus one stylesheet.

```
index.html       Home
program.html     The Program (BAEP-560, semester arc, leadership, vision)
students.html    For Students (why search, straight talk, how to join, resources, FAQ)
searchers.html   For Searchers (network, the three search structures, SoCal market)
investors.html   For Investors (ways to engage, the fund ambition, ecosystem, owners, contact)
assets/site.css  All styling
```

Navigation is three audience tracks — students, searchers, investors — plus a program
overview. Business owners live in a section on the investors page rather than owning a
page of their own.

## Picking this back up later

Everything needed lives in this folder and it's under git — `git log` shows the history.

```
python3 -m http.server 8899          # then open http://localhost:8899
python3 build-preview.py ~/Desktop/USC-Search-Fund-draft.html --standalone
```

The second command regenerates the single-file copy for emailing. Run it after any edit
to the pages or the stylesheet, or the shared copy goes stale.

## Preview

Double-click `index.html`, or:

```
cd ~/Desktop/Marshall/usc-search-fund && python3 -m http.server 8899
# then open http://localhost:8899
```

## Deploying

Any static host works. GitHub Pages, Netlify, Vercel, or Cloudflare Pages — drop the
folder in, no configuration needed.

## TO FILL IN before this goes public

1. **Contact email** — `investors.html` has `REPLACE@usc.edu` in two places (the mailto
   link and the button label). Search for `REPLACE`.
2. **Instructor bios** — `program.html#leadership` has one-paragraph placeholders for
   Dustin Sellers and Chris Lueck written from limited information. Get their real bios
   and headshots. The portrait slots are `<div class="person__portrait">Portrait</div>` —
   swap for `<img>`.
3. **Semester arc** — `program.html` week groupings are indicative, drawn from the
   Fall 2026 syllabus and the Class 6 Sourcing Sprint. Confirm against the real schedule.
4. **Greif Center link** — verify the URL in `program.html` still resolves.
5. **Naming and approval** — "USC Search Fund," the Greif Center affiliation, and the
   USC cardinal palette all imply institutional endorsement. Marshall has a brand/trademark
   review process for anything using the USC name publicly. Worth clearing with Dustin
   and the Greif Center before this is indexed.
6. **Footer disclaimer** — "Not an offer to sell or a solicitation to buy any security"
   is there deliberately, because the site references a future fund. Keep it.

## Data sources

The four figures in the homepage stats band (862 funds, 33.9% IRR, 4.75x ROI, 2.88 PME)
come from the 2026 Stanford GSB Search Fund Study, measured as of 12/31/2025, and are
cited inline. Refresh when the next study publishes.

## Design notes

- Type: Source Serif 4 (headlines) + Inter (body), both via Google Fonts.
- Palette: USC cardinal `#990000`, gold `#ffc72c` used only on dark sections,
  near-black `#0f0f0f` ink, warm off-white `#f7f6f3` for alternating bands.
- Light theme only, by intent — institutional sites should look the same for everyone.
- No photography yet. A hero image was tried and reverted; the design stands on type and
  whitespace alone. If a licensed USC photo is added later, the hero is the place for it.
- All layout is CSS grid with breakpoints at 900px, 760px, and 420px.
- Below 900px the desktop nav is replaced by a `<details>` disclosure menu (no JS).
  Verified at 390 / 430 / 768px: standards mode, zero horizontally overflowing elements.

## Sharing a single-file copy

`build-preview.py` folds the five pages into one file. Two output forms, deliberately
different — do not confuse them:

**`--standalone`** — for emailing or opening from disk.
- Full document wrapper. Without `<!doctype html>` browsers drop into quirks mode.
- `<meta name="viewport">`. Without it phones render at 980px and no media query fires.
- **Zero JavaScript.** All five sections are stacked in one continuous document and the
  nav links are plain in-page anchors. iOS Mail previews attachments in a viewer that
  does not run page scripts, so anything JS-dependent is dead on arrival there.
- On mobile the hamburger is replaced by an always-visible scrolling nav strip, because
  with no JS a disclosure menu stays open on top of the content after a tap.
- Anchor jumps are instant (`scroll-behavior:auto`) — sections sit ~6000px apart and
  smooth-scrolling that distance is a slow crawl.

**default** — for the hosted artifact/embed.
- No document wrapper; the host supplies doctype/head/body.
- JS hash routing, five switchable pages.

All three bugs above shipped at least once. The standalone form is verified by loading it
in an iframe with `sandbox="allow-same-origin"` (scripts disabled) and asserting: zero
scripts, standards mode, all five sections visible, and no horizontal page overflow.
