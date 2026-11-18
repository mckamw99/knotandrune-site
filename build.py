"""Builds the Knot & Rune site.

Each page body lives in src/<name>.html. This script wraps every body with the
shared header and footer and writes the finished page to the site root.
Run:  python3 build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
SITE = "https://www.knotandrune.com/"

# Email sign-up. Create a Google Form with one "Email" question, then paste its
# formResponse URL and the email field's entry id here and rebuild.
# Until both are filled in, the sign-up box says sign-ups open soon.
SIGNUP_FORM_ACTION = ""      # e.g. https://docs.google.com/forms/d/e/XXXX/formResponse
SIGNUP_EMAIL_ENTRY = ""      # e.g. entry.123456789

PAGES = [
    # file, nav label, <title>, meta description
    ("index.html", "Home", "Knot & Rune | Where the knots meet the runes",
     "Coloring books and keepsakes from the places where Celtic, Norse and Highland worlds meet. Every page carries a short, sourced note of real history or lore."),
    ("books.html", "Books", "Books | Knot & Rune",
     "The Celtic Tree Zodiac and the Knot & Rune line-up of adult and Wee Knot coloring books."),
    ("free-pages.html", "Free Pages", "Free Coloring Pages | Knot & Rune",
     "Free printable coloring pages from Knot & Rune books, sent by email."),
    ("lore.html", "Lore", "Lore | Knot & Rune",
     "Short, sourced pieces on Ogham, the tree calendar and the Norse-Gael north."),
    ("about.html", "About", "About | Knot & Rune",
     "Knot & Rune is a small publishing imprint of Aequitas Network LLC. Books by W. Kroboth."),
]
NAV = [p for p in PAGES if p[0] != "index.html"]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">')


def header(current):
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{f}"{cur if f == current else ""}>{label}</a>' for f, label, *_ in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/logo-horizontal.svg" alt="Knot &amp; Rune" width="230" height="44"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav">{links}</nav>
  </div>
</header>"""


FOOTER = """<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <img src="assets/logo-horizontal-reversed.svg" alt="Knot &amp; Rune" width="240" height="46">
        <p class="caption" style="color:inherit;margin-top:14px;font-style:italic;font-family:var(--display);font-size:1.1rem">Where the knots meet the runes.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul><li><a href="books.html">Books</a></li><li><a href="free-pages.html">Free coloring pages</a></li><li><a href="lore.html">Lore</a></li><li><a href="about.html">About</a></li></ul>
      </div>
      <div>
        <h4>Shops &amp; societies</h4>
        <p style="font-size:.95rem">Clan societies, Highland games vendors and shops: wholesale details will be posted here before launch.</p>
      </div>
    </div>
    <div class="legal">
      <p>Knot &amp; Rune is an imprint of Aequitas Network LLC. Books by W. Kroboth.</p>
      <p>&copy; 2026 Aequitas Network LLC. Book text and art &copy; W. Kroboth.</p>
    </div>
  </div>
</footer>
<script>
(function () {
  var t = document.querySelector('.nav-toggle'), n = document.getElementById('nav');
  if (t) t.addEventListener('click', function () { var o = n.classList.toggle('open'); t.setAttribute('aria-expanded', o); });
  document.querySelectorAll('form.signup-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      var msg = f.querySelector('.form-msg'), email = f.querySelector('input[type="email"]');
      if (!email.value || !email.checkValidity()) { e.preventDefault(); msg.hidden = false; msg.textContent = 'Please enter a valid email address.'; email.focus(); return; }
      if (!f.getAttribute('action')) { e.preventDefault(); msg.hidden = false; msg.textContent = 'Sign-ups open soon. Please check back at launch.'; return; }
      setTimeout(function () { f.querySelector('.fields').hidden = true; msg.hidden = false; msg.textContent = 'Thank you. Your free pages are on their way.'; }, 400);
    });
  });
})();
</script>"""


def signup(form_id):
    action = f' action="{SIGNUP_FORM_ACTION}" method="POST" target="sink-{form_id}"' if SIGNUP_FORM_ACTION and SIGNUP_EMAIL_ENTRY else ""
    name = SIGNUP_EMAIL_ENTRY or "email"
    sink = f'<iframe name="sink-{form_id}" title="Sign-up submission" hidden></iframe>' if action else ""
    return f"""<form class="signup-form" id="{form_id}"{action} novalidate>
  <div class="fields" style="display:contents">
    <label for="{form_id}-email">Your email</label>
    <input type="email" id="{form_id}-email" name="{name}" autocomplete="email" required placeholder="you@example.com">
    <button class="btn" type="submit">Send me the free pages</button>
  </div>
  <p class="form-msg" role="status" hidden></p>
</form>{sink}
<p class="caption" style="color:inherit;opacity:.8;margin-top:.6rem">One email when there's something new. Unsubscribe any time.</p>"""


def page(file, title, desc):
    body = (SRC / file).read_text()
    body = body.replace("{{SIGNUP}}", signup("signup-" + file.split(".")[0]))
    canon = SITE + ("" if file == "index.html" else file)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Knot &amp; Rune: Where the knots meet the runes">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{canon}">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="assets/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta name="theme-color" content="#1D3B2A">
{FONTS}
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
{header(file)}
<main id="main">
{body}
</main>
{FOOTER}
</body>
</html>
"""


if __name__ == "__main__":
    for file, _label, title, desc in PAGES:
        (ROOT / file).write_text(page(file, title, desc))
        print("built", file)
