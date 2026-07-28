# Swissfolio template — structural teardown (build blueprint for Imagify)

Source studied: swissfolio.framer.website (Framer template "Folio" by Swiss Themes), July 28 2026.
This document records the *structure and interaction system* we are re-implementing from
scratch with entirely different branding, copy, and imagery. No text, images, or code are
copied from the source.

## Design tokens

- Colors: `#fff` background, `#000` text, `#4f4f4f` secondary text, `#dedede` hairlines,
  overlays `rgba(0,0,0,.3)` (pill fill) + `backdrop-filter: blur(10px)`; white-on-image text.
- Serif (display + nearly everything): **Times New Roman** (deliberate anti-design choice),
  `font-size: 2.65rem (42px)`, `line-height 1.03`, `letter-spacing -0.02em`.
- Mono (labels/meta): **Geist Mono** 12px, line-height 1.3, sentence case ("Scroll down").
- Page frame margin: 17px all around. Grid: 4 columns, col width 299px @1280 (columns at
  x = 17 / 333 / 649 / 964, i.e. 316px pitch = quarter width). Radius: 5px on images/cards,
  26px (pill) on nav.
- Breakpoints: desktop ≥1200, tablet 810–1199, phone <810.

## Fixed chrome (all pages)

- **Pill nav** top-center: 365×50px, radius 26, bg rgba(0,0,0,.3) + blur(10px), white mono
  "Brand®" left + hamburger (2 bars) right. Click → panel expands downward (same width,
  ~420px tall, same frosted bg) showing vertical serif white links (Projects / Studio /
  Journal / Contact), × to close. On load the pill animates from y+200, opacity 0 → rest,
  delay .8s, dur 2.5s, ease cubic-bezier(.11,.68,.17,.99).
- **View toggle pill** top-left (home + projects only): mono label "Grid view" / "List view"
  + icon; label swaps with a small vertical slide animation.
- Footer (static pages): mono 12px row on 4-col grid: credit / template / images / privacy.

## Page: Home `/`

1. **Hero** — 100svh. Giant serif wordmark ("Folio" → for us "Imagify") nearly full-bleed
   (~87vw wide), vertically centered; tiny mono "Scroll down" bottom-center. Wordmark
   appear-animation: from y−110 + opacity 0, delay .6s, dur 2.25s, same bezier. Wordmark
   parallaxes away as you scroll past.
2. **Project browser** — pinned 100svh section, two modes (toggle top-left):
   - **Grid view (default):** 4 vertical columns of project cards (299×373: image 5px
     radius, serif client name ~42px below, mono service under it). Each column holds 5
     unique projects, content tripled for seamless wrap. Scroll-linked counter-motion:
     wheel delta moves columns 1 & 3 down and 2 & 4 up (equal magnitude ~41px/notch),
     wrapping mod one-copy-height → infinite loop, page never "ends". Columns start
     vertically staggered. Card hover → image swaps to the project's alt image (or
     scales slightly).
   - **List view:** full-width table on the 4-col grid. Mono 12px headers Client /
     Project / Services / Year; rows in 42px serif, 44px row rhythm, hairline-less.
     Hovering a row fades in (opacity, ~.3s) that project's 320×400 image, absolutely
     positioned in the center-left column area anchored near the row. Rows link to
     detail pages.
3. No footer on home (infinite browser).

## Page: Projects `/projects`

Same browser component without the hero: list table starts below chrome (~y160), or grid
mode columns. Footer only in list mode at the very bottom.

## Page: Project detail `/projects/<slug>` (×20)

- Split screen: right half = full-height hero image (17px margin, 5px radius, sticky
  while left scrolls on tall content). Left column: serif client name h1 top-left (~42px);
  mono meta block mid-left (project title + service, second sub-column: year); serif
  description paragraph (~42px, big first-line indent ~320px, ~120 words, single flowing
  sentence style).
- Below left text: mono pagination row "Previous | View all projects | Next" + a "Next"
  serif teaser with small image (296×393) that reveals on hover.
- Gallery below: two half-width full-height images side by side, then one full-width
  full-height image (all 17px margins, 5px radius).
- Footer row at bottom.

## Page: Studio `/studio`

1. Statement section: centered serif h1 "The Studio" + centered ~90-word serif paragraph
   (~42px) in middle 2 columns.
2. Team browser: same 4-column counter-scroll marquee with 8 team cards (photo 299×~350,
   serif first-name overlay at photo bottom, mono "First Last / Role" caption below).
3. Full-bleed image section (~2045px tall image): centered white "Work with us" pill CTA
   (307×~60, frosted) linking to contact; then a centered vertical stack of service tags
   (serif ~42px, outline-pill look, one per line: Branding, Art Direction, …).
4. Footer.

## Page: Journal `/journal`

Masonry grid, 4 columns × 3 rows: cards = image (299 × varying 299/339/397, radius 5),
mono category above/over, grey serif title (~28-32px, #9-ish grey → black on hover?)
below. Cards fade in staggered on load. Footer at bottom. (Cards need not link anywhere:
template links to posts; we keep href="#" or omit.)

## Page: Contact `/contact`

Full-bleed image (17px frame, radius 5, moody night city) with centered white serif block:
studio name / street / city / phone / email (~42px serif, centered, ~1.4 spacing) and
social links (Instagram / Threads / X / LinkedIn) lower. No scroll (100svh).

## Motion summary

- Appear: opacity 0→1 with y offsets (−110 hero, +200 pill nav), 2.25–2.5s, delay .6–.8s,
  ease cubic-bezier(0.11, 0.68, 0.17, 0.99). Journal/table rows stagger ~60ms.
- Scroll: native scroll everywhere except the pinned browser/team sections where wheel
  delta drives the counter-scrolling ticker columns (scroll-linked, wraps mod copy height).
- Hovers: table-row image fade; card image swap; nav links; next-teaser reveal.
- View toggle: animated crossfade/slide between grid columns and list table.
