"""Fold the five-page site into one self-contained HTML file.

Two output forms, deliberately different:

  --standalone   One continuous document, all sections stacked, nav links are
                 in-page anchors. ZERO JavaScript, so it survives iOS Mail /
                 Quick Look previews and any other JS-disabled viewer.
                 Includes <!doctype html> — without it browsers go quirks mode.

  (default)      Artifact/embed form: JS hash routing, five switchable pages.
                 No document wrapper; the host supplies doctype/head/body.
"""
import re, sys, pathlib, base64, mimetypes

SRC = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1])
STANDALONE = "--standalone" in sys.argv

PAGES = [("home", "index.html"), ("program", "program.html"),
         ("students", "students.html"), ("searchers", "searchers.html"),
         ("investors", "investors.html"), ("press", "press.html")]
NAMES = {"home": "Home", "program": "The Program", "students": "For Students",
         "searchers": "For Searchers", "investors": "For Investors",
         "press": "Press & Events"}

PAGE_RE = r'href="(index|program|students|searchers|investors|press)\.html(?:#([\w-]+))?"'

def rewrite_routed(html):
    def sub(m):
        f, frag = m.group(1), m.group(2)
        name = "home" if f == "index" else f
        return 'href="#/%s%s"' % (name, "/" + frag if frag else "")
    return re.sub(PAGE_RE, sub, html)

def rewrite_stacked(html):
    """Everything is on one page, so a link is just an in-page anchor."""
    def sub(m):
        f, frag = m.group(1), m.group(2)
        name = "home" if f == "index" else f
        return 'href="#%s"' % (frag if frag else name)
    return re.sub(PAGE_RE, sub, html)

rewrite = rewrite_stacked if STANDALONE else rewrite_routed

def inline_images(html):
    """Fold <img src="assets/..."> into data URIs.

    The standalone file travels on its own — as a mail attachment or a copy on
    someone's desktop — so a relative path to assets/images resolves to nothing
    and the portraits come through broken.
    """
    def sub(m):
        rel = m.group(1)
        f = SRC / rel
        if not f.exists():
            raise SystemExit("build-preview: missing image %s" % rel)
        mime = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
        b64 = base64.b64encode(f.read_bytes()).decode("ascii")
        return 'src="data:%s;base64,%s"' % (mime, b64)
    return re.sub(r'src="(assets/[^"]+)"', sub, html)

def links_for_video(html):
    """Replace each video iframe with a plain link to YouTube.

    The standalone file is opened as a mail attachment or from disk. iOS Mail's
    preview blocks iframes outright, so an embed renders as an empty box with no
    hint that a video was ever there. A link survives everywhere.
    """
    def sub(m):
        vid = m.group(1)
        return ('<a class="video__fallback" '
                'href="https://www.youtube.com/watch?v=%s">&#9654;&nbsp; Watch on YouTube</a>' % vid)
    return re.sub(
        r'<div class="video__frame">\s*<iframe src="https://www\.youtube-nocookie\.com/embed/([\w-]+)".*?</iframe>\s*</div>',
        sub, html, flags=re.S)


def main_of(fn):
    return re.search(r"<main>(.*?)</main>", (SRC / fn).read_text(), re.S).group(1)

css = (SRC / "assets/site.css").read_text()
src = (SRC / "index.html").read_text()
masthead = rewrite(re.search(r'<header class="masthead">.*?</header>', src, re.S).group(0))
masthead = masthead.replace(' aria-current="page"', '')
if STANDALONE:
    # The masthead carries the logo, and this file travels without its assets.
    masthead = inline_images(masthead)
footer = rewrite(re.search(r'<footer class="footer">.*?</footer>', src, re.S).group(0))

COMMON = """
:root{ color-scheme:light; }
[id]{ scroll-margin-top:5.5rem; }
a:focus-visible,summary:focus-visible,.cta-tri__item:focus-visible{
  outline:2px solid var(--cardinal); outline-offset:3px; border-radius:4px;
}
.stat__fig{ font-variant-numeric:tabular-nums; }
"""

if STANDALONE:
    body = "\n".join(
        '<section class="doc-section" id="%s">%s</section>' % (k, links_for_video(inline_images(rewrite(main_of(f)))))
        for k, f in PAGES)
    extra = COMMON + """
/* one continuous document — no JS, every section always visible */
.doc-section + .doc-section{ border-top:1px solid var(--line); }
/* sections sit ~6000px apart; smooth-scrolling that far is a slow crawl */
html{ scroll-behavior:auto; }

/* No JS here, so a disclosure menu would stay open on top of the content after
   a tap. Use an always-visible nav strip on its own row instead. */
@media (max-width:900px){
  .menu{ display:none; }
  .masthead__inner{
    height:auto; flex-direction:column; align-items:flex-start;
    gap:.3rem; padding-block:.65rem;
  }
  .nav{
    display:flex; width:100%; gap:1.15rem;
    overflow-x:auto; overscroll-behavior-x:contain;
    scrollbar-width:none; -ms-overflow-style:none;
    padding-bottom:.15rem;
  }
  .nav::-webkit-scrollbar{ display:none; }
  .nav a{ font-size:.875rem; }
  [id]{ scroll-margin-top:7rem; }
}
"""
    script = ""
else:
    body = "\n".join(
        '<div class="page" id="page-%s">%s</div>' % (k, rewrite(main_of(f)))
        for k, f in PAGES)
    extra = COMMON + """
.page{ display:none; }
.page.is-active{ display:block; animation:pageIn .34s cubic-bezier(.4,.14,.3,1) both; }
@keyframes pageIn{ from{ opacity:0; transform:translateY(6px);} to{ opacity:1; transform:none;} }
@media (prefers-reduced-motion:reduce){ .page.is-active{ animation:none; } }
"""
    script = """
<script>
(function () {
  var PAGES = ["home","program","students","searchers","investors","press"];
  var TITLES = { program:"The Program", students:"For Students", searchers:"For Searchers", investors:"For Investors", press:"Press & Events" };
  var links = document.querySelectorAll('.masthead a[href^="#/"]');

  function route() {
    var parts = location.hash.replace(/^#\\/?/, "").split("/");
    var page = PAGES.indexOf(parts[0]) > -1 ? parts[0] : "home";
    var anchor = parts[1] || "";

    PAGES.forEach(function (p) {
      document.getElementById("page-" + p).classList.toggle("is-active", p === page);
    });
    links.forEach(function (a) {
      var t = a.getAttribute("href").replace(/^#\\//, "").split("/")[0] || "home";
      if (t === page) { a.setAttribute("aria-current", "page"); } else { a.removeAttribute("aria-current"); }
    });
    document.title = page === "home" ? "USC Search Fund" : TITLES[page] + " \\u2014 USC Search Fund";
    document.querySelectorAll("details.menu").forEach(function (d) { d.open = false; });

    // the section we just revealed has not laid out yet; wait two frames
    if (anchor) {
      var el = document.getElementById(anchor);
      if (el) {
        requestAnimationFrame(function () {
          requestAnimationFrame(function () { el.scrollIntoView({ block: "start" }); });
        });
        return;
      }
    }
    window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", route);
  route();
})();
</script>"""

head_open = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n' if STANDALONE else ''
body_open = '</head>\n<body>' if STANDALONE else ''
doc_close = '\n</body>\n</html>' if STANDALONE else ''

OUT.write_text(f"""{head_open}<title>USC Search Fund</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Entrepreneurship through acquisition at the USC Marshall Lloyd Greif Center for Entrepreneurial Studies.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<style>
{css}
{extra}
</style>
{body_open}

{masthead}

<main>
{body}
</main>

{footer}
{script}{doc_close}
""")
print(("standalone (no JS)" if STANDALONE else "artifact (routed)"), "→", OUT, OUT.stat().st_size, "bytes")
