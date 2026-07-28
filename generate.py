#!/usr/bin/env python3
"""Imagify site generator.

Reads data/content.json and writes every HTML page. Re-run after editing
content: python3 generate.py
"""
import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, "data", "content.json"), encoding="utf8"))
P = DATA["projects"]; TEAM = DATA["team"]; J = DATA["journal"]
BRAND = DATA["brand"]["wordmark"]; LEGAL = DATA["brand"]["legal"]

def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- chrome

def head(title, rel, desc="Imagify is a visual studio working across identity, image and film.", snap=False):
    return f"""<!DOCTYPE html>
<html lang="en"{' class="snap"' if snap else ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="{rel}css/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='26' font-size='26' font-family='Times New Roman'>I</text></svg>">
</head>
<body>
"""

def pill_nav(rel, current):
    pages = [("Projects", "projects.html"), ("Studio", "studio.html"),
             ("Journal", "journal.html"), ("Contact", "contact.html")]
    cur = ' aria-current="page"'
    links = "\n".join(
        f'      <li><a href="{rel}{href}"{cur if key == current else ""}>{key}</a></li>'
        for key, href in pages)
    return f"""<input type="checkbox" id="nav-open" class="nav-toggle-input">
<nav class="pill-nav appear-rise" aria-label="Main">
  <div class="bar">
    <a class="brand mono" href="{rel}index.html">{LEGAL}</a>
    <label class="burger" for="nav-open" aria-label="Menu"><i></i><i></i></label>
  </div>
  <div class="menu"><div>
    <ul>
{links}
    </ul>
  </div></div>
</nav>
"""

def footer(rel):
    items = DATA["footer"]
    cells = "\n".join(f'  <a class="mono" href="{esc(i["href"])}">{esc(i["label"])}</a>' for i in items)
    return f'<footer class="site-footer">\n{cells}\n</footer>\n'

def view_toggle():
    return """<button class="view-toggle appear-rise" data-view-toggle data-mode="grid" aria-label="Switch view">
  <span class="labels mono"><span>Grid view</span><span>List view</span></span>
  <span class="ico grid"><i></i><i></i><i></i><i></i></span>
</button>
"""

def tail(rel):
    return f'<script src="{rel}js/main.js"></script>\n</body>\n</html>\n'

# ---------------------------------------------------------------- browser component

def browser_component(rel, standalone=False):
    cols = {0: [], 1: [], 2: [], 3: []}
    for pr in P:
        cols[pr["column"]].append(pr)

    def card(pr):
        return f"""        <a class="pcard" href="{rel}projects/{pr['slug']}.html">
          <span class="ph"><img src="{rel}assets/img/{pr['slug']}-hero.jpg" alt="{esc(pr['title'])} for {esc(pr['client'])}" loading="lazy"></span>
          <h2>{esc(pr['client'])}</h2>
          <span class="svc mono">{esc(pr['service'])}</span>
        </a>"""

    col_html = ""
    for i in range(4):
        copies = ""
        for c in range(3):
            cards = "\n".join(card(pr) for pr in cols[i])
            copies += f'      <div class="copy">\n{cards}\n      </div>\n'
        col_html += f'    <div class="ticker-col"><div class="belt">\n{copies}    </div></div>\n'

    rows = ""
    for pr in P:
        rows += f"""    <a class="trow" data-slug="{pr['slug']}" href="{rel}projects/{pr['slug']}.html">
      <span class="c-client">{esc(pr['client'])}</span>
      <span class="c-title">{esc(pr['title'])}</span>
      <span class="c-svc">{esc(pr['service'])}</span>
      <span class="c-year">{pr['year']}</span>
    </a>\n"""
    row_imgs = "\n".join(
        f'    <img class="row-img" data-for="{pr["slug"]}" src="{rel}assets/img/{pr["slug"]}-hero.jpg" alt="" loading="lazy">'
        for pr in P)

    sa = " standalone" if standalone else ""
    endless = "false" if standalone else "true"
    return f"""<section class="browser{sa}" data-browser data-mode="grid" data-endless="{endless}">
  <div class="ticker-wrap">
{col_html}  </div>
  <div class="list-table" data-list-table>
    <div class="thead mono">
      <span class="h-client">Client</span><span class="h-project">Project</span><span class="h-services">Services</span><span class="h-year">Year</span>
    </div>
    <div class="stagger">
{rows}    </div>
{row_imgs}
  </div>
</section>
"""

# ---------------------------------------------------------------- pages

def build_home():
    out = head(f"{BRAND} — Visual Studio", "", snap=False)
    out += pill_nav("", None)
    out += view_toggle()
    out += f"""<header class="hero">
  <h1 class="wordmark appear-sink" data-hero-wordmark>{BRAND}</h1>
  <p class="scroll-cue mono appear-fade">Scroll down</p>
</header>
"""
    out += browser_component("", standalone=False)
    out += tail("")
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf8").write(out)

def build_projects():
    out = head(f"Projects — {BRAND}", "")
    out += pill_nav("", "Projects")
    out += view_toggle()
    out += browser_component("", standalone=False)
    out += tail("")
    open(os.path.join(ROOT, "projects.html"), "w", encoding="utf8").write(out)

def build_detail(i, pr):
    prev_pr = P[(i - 1) % len(P)]
    next_pr = P[(i + 1) % len(P)]
    rel = "../"
    out = head(f"{pr['client']} {pr['title']} — {BRAND}", rel, desc=pr["desc"][:150], snap=True)
    out += pill_nav(rel, "Projects")
    out += f"""<article>
  <section class="detail-intro">
    <div class="detail-copy">
      <h1 class="appear-fade">{esc(pr['client'])}</h1>
      <div class="detail-meta mono appear-fade">
        <div>{esc(pr['title'])}<br>{esc(pr['service'])}</div>
        <div>{pr['year']}</div>
      </div>
      <p class="detail-desc appear-fade">{esc(pr['desc'])}</p>
      <a class="next-teaser" href="{rel}projects/{next_pr['slug']}.html">
        <span class="tz"><img src="{rel}assets/img/{next_pr['slug']}-hero.jpg" alt="" loading="lazy"></span>
        <span class="nx">Next</span>
      </a>
    </div>
    <figure class="detail-hero appear-fade">
      <img src="{rel}assets/img/{pr['slug']}-hero.jpg" alt="{esc(pr['title'])} — {esc(pr['client'])}">
    </figure>
    <nav class="detail-pagenav mono">
      <a href="{rel}projects/{prev_pr['slug']}.html">Previous</a>
      <a href="{rel}projects.html">View all projects</a>
      <a class="to-right" href="{rel}projects/{next_pr['slug']}.html">Next</a>
    </nav>
  </section>
  <section class="detail-duo">
    <figure><img src="{rel}assets/img/{pr['slug']}-a.jpg" alt="" loading="lazy"></figure>
    <figure><img src="{rel}assets/img/{pr['slug']}-b.jpg" alt="" loading="lazy"></figure>
  </section>
  <section class="detail-solo">
    <figure><img src="{rel}assets/img/{pr['slug']}-c.jpg" alt="" loading="lazy"></figure>
  </section>
</article>
<div class="detail-footer">"""
    out += footer(rel)
    out += "</div>\n"
    out += tail(rel)
    open(os.path.join(ROOT, "projects", pr["slug"] + ".html"), "w", encoding="utf8").write(out)

def build_studio():
    st = DATA["studio"]
    out = head(f"Studio — {BRAND}", "")
    out += pill_nav("", "Studio")
    out += f"""<section class="studio-statement">
  <h1 class="appear-sink">{esc(st['heading'])}</h1>
  <p class="appear-fade">{esc(st['statement'])}</p>
</section>
"""
    cols = {0: [], 1: [], 2: [], 3: []}
    for idx, m in enumerate(TEAM):
        cols[idx % 4].append((idx, m))
    col_html = ""
    for i in range(4):
        copies = ""
        for c in range(3):
            cards = ""
            for idx, m in cols[i]:
                cards += f"""        <div class="tcard">
          <div class="ph"><img src="assets/img/team-{idx+1}.jpg" alt="{esc(m['first'])} {esc(m['last'])}" loading="lazy"><h2>{esc(m['first'])}</h2></div>
          <div class="who mono"><span>{esc(m['first'])} {esc(m['last'])}</span><span class="role">{esc(m['role'])}</span></div>
        </div>\n"""
            copies += f'      <div class="copy">\n{cards}      </div>\n'
        col_html += f'    <div class="ticker-col"><div class="belt">\n{copies}    </div></div>\n'
    tags = "\n".join(f'      <span>{esc(t)}</span>' for t in st["services"])
    out += f"""<section class="team-belt-section" data-team-belts>
  <div class="ticker-wrap">
{col_html}  </div>
</section>
<section class="studio-cta-block">
  <img src="assets/img/studio-wide.jpg" alt="">
  <div class="studio-cta-inner">
    <a class="btn-pill" href="contact.html">Work with us</a>
    <div class="tag-stack">
{tags}
    </div>
  </div>
</section>
"""
    out += footer("")
    out += tail("")
    open(os.path.join(ROOT, "studio.html"), "w", encoding="utf8").write(out)

def build_journal():
    heights = ["tall", "mid", "tall", "mid", "sq", "tall", "mid", "tall", "mid", "tall", "sq", "mid"]
    cards = ""
    for idx, post in enumerate(J):
        cards += f"""  <div class="jcard" data-h="{heights[idx % len(heights)]}">
    <div class="ph"><img src="assets/img/journal-{idx+1}.jpg" alt="" loading="lazy"></div>
    <p class="cat mono">{esc(post['category'])}</p>
    <h2>{esc(post['title'])}</h2>
  </div>\n"""
    out = head(f"Journal — {BRAND}", "")
    out += pill_nav("", "Journal")
    out += f'<section class="journal-grid stagger">\n{cards}</section>\n'
    out += footer("")
    out += tail("")
    open(os.path.join(ROOT, "journal.html"), "w", encoding="utf8").write(out)

def build_contact():
    c = DATA["contact"]
    socials = "\n".join(f'        <a class="mono" href="#">{esc(s)}</a>' for s in c["socials"])
    out = head(f"Contact — {BRAND}", "")
    out += pill_nav("", "Contact")
    out += f"""<section class="contact-hero">
  <div class="frame">
    <img src="assets/img/contact.jpg" alt="">
    <div class="contact-card appear-fade">
      <div class="lines">
        {esc(c['studio'])}<br>
        {esc(c['address1'])}<br>
        {esc(c['address2'])}<br>
        <a href="mailto:{esc(c['email'])}">{esc(c['email'])}</a>
      </div>
      <div class="socials">
{socials}
      </div>
    </div>
  </div>
</section>
"""
    out += tail("")
    open(os.path.join(ROOT, "contact.html"), "w", encoding="utf8").write(out)

if __name__ == "__main__":
    build_home()
    build_projects()
    for i, pr in enumerate(P):
        build_detail(i, pr)
    build_studio()
    build_journal()
    build_contact()
    print(f"generated: index, projects, studio, journal, contact, {len(P)} detail pages")
