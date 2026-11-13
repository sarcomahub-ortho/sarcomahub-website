#!/usr/bin/env python3
"""Build the static pages from tools/pages/*.html.

Each page file starts with a small header block:
    title: ...
    description: ...
    path: /understanding-sarcoma/
    nav: learn            (which menu item is current; empty for none)
    ---
followed by the HTML that goes inside <main>.

Run from the repo root:  python3 tools/build.py
The shared header, footer and the S/H letter swap live here, so every page stays consistent.
"""
import pathlib, re, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "tools" / "pages"
V = "11"  # bump to make browsers fetch fresh CSS, JS and images

NAV = [
    ("home", "/", "Home"),
    ("learn", "/understanding-sarcoma/", "Understanding sarcoma"),
    ("families", "/for-parents/", "For families"),
    ("stories", "/stories/", "Stories"),
    ("touch", "/get-in-touch/", "Get in touch"),
]

HEAD = """<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><!-- remove when ready for Google -->
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://www.sarcomahub.com{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="SarcomaHub">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://www.sarcomahub.com{path}">
<meta property="og:image" content="https://www.sarcomahub.com/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="/assets/favicon-32.png?v={v}" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png?v={v}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&family=Jost:ital,wght@0,300;0,400;0,500;1,400&display=swap">
<link rel="stylesheet" href="/assets/style.css?v={v}">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <div class="wrap">
    <a class="brand" href="/" aria-label="SarcomaHub home">
      <img class="brand-logo" src="/assets/logo-96.png?v={v}" width="52" height="52" alt="SarcomaHub logo">
      <b class="brand-name">SarcomaHub</b>
    </a>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="mainNav">Menu</button>
    <nav class="main" id="mainNav" aria-label="Main">
{nav}
    </nav>
    <img class="brand-sig" src="/assets/logo-sh.svg?v={v}" width="751" height="654" alt="SH signature">
  </div>
</header>
<main id="main">
"""

FOOT = """</main>
<footer>
  <div class="wrap">
    <div class="stack">
      <b class="foot-brand">SarcomaHub</b>
      <p class="foot-note">Reliable information and a supportive community for people affected by bone and soft tissue tumours.</p>
      <p><a href="https://wa.me/919111609222">WhatsApp +91 9111 60 9222</a><br><a href="mailto:sarcomahub@gmail.com">sarcomahub@gmail.com</a></p>
    </div>
    <div class="links"><b>Learn</b><a href="/understanding-sarcoma/">What is sarcoma</a><a href="/understanding-sarcoma/#learn-signs">Warning signs</a><a href="/understanding-sarcoma/#learn-biopsy">Biopsy</a><a href="/understanding-sarcoma/#learn-surgery">Surgery</a></div>
    <div class="links"><b>Connect</b><a href="/for-parents/">For families</a><a href="/stories/">Share your story</a><a href="/get-in-touch/">Get in touch</a><a href="https://instagram.com/sarcomahub/" target="_blank" rel="noopener">Instagram</a></div>
    <p class="disclaimer">The information on SarcomaHub is for general education and does not replace advice from your own doctor. If you are worried about a lump, swelling or bone pain, please see a doctor. If someone is unwell, call SPARSH Hospital on 080 61 222 000 or go to the nearest hospital.</p>
  </div>
</footer>
<script src="/assets/site.js?v={v}" defer></script>
</body>
</html>
"""

JSONLD = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"MedicalOrganization","name":"SarcomaHub","url":"https://www.sarcomahub.com/","email":"sarcomahub@gmail.com","medicalSpecialty":"Oncologic","sameAs":["https://instagram.com/sarcomahub/"]}</script>\n'


def glyphs(text):
    """Swap the S and H of the two names for the monogram letters (visible text only)."""
    def rep(m):
        if m.group(0) == "SarcomaHub":
            return '<span class="wm"><span class="g g-s">S</span>arcoma<span class="g g-h">H</span>ub</span>'
        return '<span class="wm"><span class="g g-s">S</span>uraj <span class="g g-h">H</span>indiskere</span>'
    return re.sub(r"SarcomaHub|Suraj Hindiskere", rep, text)


def swap_body(doc):
    head, body = doc.split("<body>", 1)
    parts = re.split(r"(<[^>]+>)", body)
    skip = False
    for i, pt in enumerate(parts):
        if pt.startswith("<"):
            if re.match(r"<(script|style)\b", pt):
                skip = True
            elif re.match(r"</(script|style)>", pt):
                skip = False
            continue
        if not skip:
            parts[i] = glyphs(pt)
    return head + "<body>" + "".join(parts)


def build(src):
    raw = src.read_text()
    meta, content = raw.split("\n---\n", 1)
    m = {k.strip(): v.strip() for k, _, v in (line.partition(":") for line in meta.strip().splitlines())}
    nav = "\n".join(
        f'      <a href="{href}"{" aria-current=\"page\"" if key == m.get("nav", "") else ""}>{label}</a>'
        for key, href, label in NAV
    )
    extra = JSONLD if m["path"] == "/" else ""
    content = content.replace("{v}", V)
    doc = HEAD.format(title=html.escape(m["title"]), desc=html.escape(m["description"]), path=m["path"],
                      nav=nav, v=V, extra=extra) + content.strip("\n") + "\n" + FOOT.format(v=V)
    doc = swap_body(doc)
    out = ROOT / ("404.html" if m["path"] == "/404.html" else m["path"].strip("/") + "/index.html" if m["path"] != "/" else "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    print("built", out.relative_to(ROOT))


if __name__ == "__main__":
    for f in sorted(PAGES.glob("*.html")):
        build(f)
