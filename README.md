# Imagify — visual studio site

A multi-page static portfolio site (Swiss-editorial style): giant Times New Roman
display type, Geist Mono labels, white/black/grey palette, counter-scrolling
project columns with grid/list view toggle.

## Pages

- `index.html` — hero wordmark + infinite project browser (grid ↔ list)
- `projects.html` — the browser standalone
- `projects/<slug>.html` — 20 generated project case pages
- `studio.html` — statement, team ticker, full-bleed CTA block
- `journal.html` — masonry journal grid
- `contact.html` — full-bleed contact card

## Editing content

All copy lives in `data/content.json`. After editing, regenerate every page:

```
python3 generate.py
```

Plain static output — no build tools or Node required. Serve the folder with any
static server, e.g. `python3 -m http.server 8000`.

Images are placeholders from Unsplash (see footer credit); fonts: Geist Mono
(OFL) vendored in `assets/fonts`, display serif is system Times New Roman.
