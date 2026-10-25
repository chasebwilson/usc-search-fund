# USC Search Fund — website

Static site. No build step, no dependencies. Six pages plus one stylesheet.

```
index.html       Home (incl. featured searcher video)
program.html     The Program (BAEP-560, semester arc, leadership, vision)
students.html    For Students (why search, straight talk, how to join, resources,
                 searcher videos, FAQ)
searchers.html   For Searchers (network, the three search structures, SoCal market)
investors.html   For Investors (ways to engage, the fund ambition, ecosystem, owners, contact)
press.html       Press & Events (ETA conference calendar, press coverage)
assets/site.css  All styling
```

Navigation is three audience tracks — students, searchers, investors — plus a program
overview and Press & Events. Business owners live in a section on the investors page
rather than owning a page of their own.

The nav label for `press.html` is just **"Press"**, deliberately. Six items plus the
brand and its "Greif Center · Marshall" subtitle overflow `.masthead__inner`, which is
capped at `--maxw` (1120px) and so does not gain room on wider screens. "Press & Events"
made "Home" overlap the subtitle on every desktop width. If a seventh nav item is ever
added, the masthead needs rethinking, not another shortened label.

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

## Still open

1. **Semester arc** — `program.html` week groupings are indicative, drawn from the
   Fall 2026 syllabus and the Class 6 Sourcing Sprint. Confirm against the real schedule.
2. **Naming and approval** — "USC Search Fund," the Greif Center affiliation, and the
   USC cardinal palette all imply institutional endorsement. Marshall has a brand/trademark
   review process for anything using the USC name publicly. In flight with Dustin and the
   Greif Center.
3. **Two claims on `press.html` that Dustin should sanity-check** — the Booth–Kellogg
   entry says "north of 900 attendees," and the Wharton entry is characterised as
   "denser on institutional investors than most." Both came from research, not from
   anyone who has attended. Easy to soften if wrong.
4. **NYT headline** — the 2009 New York Times piece on `press.html` uses the title
   Dustin supplied, "Paying Entrepreneurs to Find the Right Business." The URL resolves
   (403, i.e. paywalled, not 404) but the headline itself was never independently
   verified — nytimes.com blocks automated access.
5. **Speaker permission for the videos** — the six clips were recorded for a class and
   are now on a public page. Confirm each speaker is fine with that. Dustin's call.
6. **Footer disclaimer** — "Not an offer to sell or a solicitation to buy any security"
   is there deliberately, because the site references a future fund. Keep it.

## Done (do not redo)

- **Contact email** — `info@uscsearchfund.org` is live, a Hostinger Starter Business
  Email mailbox. No `REPLACE` placeholders remain anywhere.
- **Instructor bios and headshots** — both real, both `<img>`. Dustin's bio was supplied
  verbatim by him on 2026-08-30 and his firm is **NCL Partners** (formerly Next Coast
  Legacy — the Search Party podcast materials still say the old name). Chris's bio is
  shorter than Dustin's on purpose; Dustin asked for his own wording kept as-is.
- **Greif Center link** — verified resolving 2026-08-30.

## Editorial rules established 2026-08-30

These were deliberate. Undoing them without knowing why will make the site worse.

- **Books link to publishers, never Amazon.** `store.hbr.org` for the HBR Guide,
  `lioncrest.com` for Buy Then Build. Amazon reads as commerce on a university page and
  ASINs rot. Note that `buythenbuild.com` was rejected specifically because its landing
  page is an email-capture funnel into paid courses and its own "Book" link is an Amazon
  affiliate URL.
- **Conferences link to host sites, never a single year's event page.** Dates move
  annually; `socaletaconference.com` will surface the current edition on its own. This
  is what keeps `press.html` from rotting after handoff. Month and city are on the page;
  specific dates deliberately are not.
- **The Stanford study links to the evergreen CES landing page**, while the homepage
  stats band cites the specific 2026 study its figures came from. Both are correct for
  their purpose — do not "fix" one to match the other.
- **Videos are never committed to this repo.** They live on the `@USCETA` YouTube
  channel, unlisted, embedded via `youtube-nocookie` with `loading="lazy"`. The source
  files are ~260MB each at 17Mbps — over GitHub's 100MB hard file limit, and six of them
  would be ~1.6GB against a repo that is otherwise ~2MB.
- **`.deflist dt a` has separate light and dark underline colours.** The dark variant
  exists for the resources band on `students.html`. Setting one without the other makes
  links invisible on one background or the other — this shipped broken once.

## Provenance

- LinkedIn URLs for Dustin and Chris came directly from Chase, 2026-08-30.
- The WSJ, FT, and NYT article URLs came directly from Chase — those three domains block
  automated access, so they cannot be re-derived by searching.
- The other nine press URLs were found and verified by request. Four of them
  (Bloomberg, both Fast Company pieces, Forbes 2014) return 403 to automated checks;
  that is bot-blocking, not a dead link.

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
- The video grid deliberately breaks the site pattern: every other grid collapses to one
  column below 900px, but `.video-grid` stays 2-up until 620px. Six full-width videos on
  a tablet is an endless scroll, and 16:9 thumbnails stay legible at ~320px where body
  text would not. Desktop layout verified 2026-08-30; **mobile rendering of the video
  grid was never visually confirmed** — the browser tooling would not resize the viewport.

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
- JS hash routing, six switchable pages.

Both forms strip the YouTube iframes via `links_for_video()` and replace each with a
plain "Watch on YouTube" link. iOS Mail's preview blocks iframes outright, so an embed
renders as an empty box with no hint a video was ever there.

All three bugs above shipped at least once. The standalone form is verified by loading it
in an iframe with `sandbox="allow-same-origin"` (scripts disabled) and asserting: zero
scripts, standards mode, all five sections visible, and no horizontal page overflow.
