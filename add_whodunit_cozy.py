"""Add Whodunit Puzzles for Adults: Cozy Village Murders (B0HNGPTYRK, live 18 Oct 2026) + the Mystery Room homepage
section with the how-to-solve video. Idempotent; then python seo.py."""
import re, html as H, os, json, urllib.request
import fitz
from PIL import Image
esc = lambda s: H.escape(s, quote=True)
ASIN = 'B0HNGPTYRK'
SLUG = 'whodunit-cozy-village'
SHORT = "Whodunit Puzzles for Adults: Cozy Village Murders"
TITLE = "Whodunit Puzzles for Adults: Cozy Village Murders"
SUB = "60 Murder Mystery Logic Puzzles, Easy to Hard, Find the Killer from the Floor Plan"
TAG = "Sixty murder mysteries you solve with a pencil, plus one grand finale."
FACTS = ["108 pages", "8.5 x 11 in", "Full colour inside", "60 cases plus a grand finale, hints and full solutions", "Paperback, $12.99"]
LISTING = open(r"D:\kdp-whodunit-research\book-cosy\KDP-UPLOAD\3-LISTING.md", encoding='utf-8').read()
DESC = LISTING.split("COPY FROM HERE")[1].split("\n", 1)[1].split("-----")[0]
ABOUT = [p.strip() for p in DESC.split('\n\n') if p.strip()][1:]
WHO = "For anyone who loves cozy mysteries, logic grid puzzles or a quiet screen break that makes them think. A lovely gift for a mum, a dad, a grandparent or a puzzle-mad friend."
COVER = "https://m.media-amazon.com/images/I/71R+Fu8L-PL._SL1293_.jpg"
PDF = r"D:\kdp-whodunit-research\book-cosy\KDP-UPLOAD\1-INTERIOR-8.5x11-108pp-NO-BLEED.pdf"
PAGES = [1, 7, 8, 9, 30, 50, 70, 76]
BUY = f"https://www.amazon.com/dp/{ASIN}?tag=gentlebooksho-20"
RELATED = [('dogs-mystery-mosaics', None), ('halloween-pocket-sudoku', None), ('halloween-mosaics-complete', None)]
VIDEO = '''<section id="how-to-solve">
  <h2>Watch how to solve a case</h2>
  <p class="sect-sub sans">Two minutes, step by step: read the floor plan, use each card, find the killer.</p>
  <video controls playsinline preload="none" poster="../assets/video/whodunit-how-to-solve.jpg" style="display:block;width:100%;max-width:360px;margin:0 auto;border-radius:14px;box-shadow:0 14px 34px rgba(0,0,0,.25)"><source src="../assets/video/whodunit-how-to-solve.mp4" type="video/mp4" /></video>
</section>
'''

books = json.load(open('books.json', encoding='utf-8'))
short_of = {b['slug']: b['short'] for b in books}
s = open('books/born-1951.html', encoding='utf-8').read()
s = s.replace("101 Things People Born in 1951 Will Never Forget: The 75th Birthday Gift for Men and Women", f"{TITLE}: {SUB}")
s = s.replace("Somebody you love was born in 1951. Give them the year back.", TAG)
s = re.sub(r'<ul class="facts sans">.*?</ul>', '<ul class="facts sans">' + ''.join(f'<li>{f}</li>' for f in FACTS) + '</ul>', s, flags=re.S)
s = re.sub(r'(<section class="desc">\s*<h2>About this book</h2>\s*).*?(</section>)', lambda m: m.group(1) + ''.join(f'    <p>{esc(p)}</p>\n' for p in ABOUT) + m.group(2), s, flags=re.S)
s = re.sub(r'<div class="who sans">.*?</div>', f'<div class="who sans">{esc(WHO)}</div>', s, flags=re.S)
shelf = ''.join(f'    <a class="mini" href="{slug}.html"><img src="../assets/{slug}.jpg" alt="{esc(short_of[slug])} cover" loading="lazy" /><h3>{esc(short_of[slug])}</h3></a>\n' for slug, _ in RELATED)
s = re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + shelf + m.group(2), s, flags=re.S)
s = s.replace("Born in 1951: 101 Things You Will Never Forget", SHORT)
s = s.replace("Birthday &amp; Gift Books", "Mystery Puzzles").replace("index.html#gifts", "index.html#mystery")
s = s.replace("born-1951", SLUG)
s = s.replace("https://www.amazon.com/dp/B0HJ2PXK3N?tag=gentlebooksho-20", BUY)
s = s.replace('<section id="look-inside">', VIDEO + '<section id="look-inside">', 1)
s = re.sub(r'<!--seo-->.*?<!--/seo-->', '', s, flags=re.S)  # seo.py rebuilds it
assert all(x not in s for x in ('B0HJ2PXK3N', 'Men and Women', '14.99', '1951', 'Gift Books')), 'template leftovers'

req = urllib.request.Request(COVER, headers={"User-Agent": "Mozilla/5.0"})
open(f"assets/{SLUG}-src.jpg", 'wb').write(urllib.request.urlopen(req).read())
im = Image.open(f"assets/{SLUG}-src.jpg").convert('RGB'); im.thumbnail((900, 1200)); im.save(f"assets/{SLUG}.jpg", quality=88)
os.remove(f"assets/{SLUG}-src.jpg")
d = fitz.open(PDF); os.makedirs(f"assets/samples/{SLUG}", exist_ok=True)
for k, p in enumerate(PAGES, 1):
    pix = d[p - 1].get_pixmap(dpi=110); pg = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    full = pg.copy(); full.thumbnail((1200, 1600)); full.save(f"assets/samples/{SLUG}/{k}.jpg", quality=85)
    th = pg.copy(); th.thumbnail((400, 520)); th.save(f"assets/samples/{SLUG}/{k}-thumb.jpg", quality=80)
open(f"books/{SLUG}.html", 'w', encoding='utf-8').write(s)

books = [x for x in books if x['slug'] != SLUG]
books.append({"slug": SLUG, "asin": ASIN, "title": f"{TITLE}: {SUB}", "short": SHORT, "cover": f"{SLUG}.jpg",
              "shelf": "mystery", "shelf_name": "Mystery Puzzles", "tagline": TAG, "who": WHO, "facts": FACTS,
              "samples": len(PAGES), "description": ABOUT})
json.dump(books, open('books.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ---- homepage: book map entry, Mystery Room section, nav link -------------------------------------------------
idx = open('index.html', encoding='utf-8').read()
entry = json.dumps({SLUG: {"asin": ASIN, "short": SHORT, "cover": f"{SLUG}.jpg"}})[1:-1]
idx = re.sub(r', "' + SLUG + r'": \{[^}]*\}', '', idx)
idx = idx.replace('}};</script>', '}, ' + entry + '};</script>', 1)
CSS = '''.mystery{position:relative;padding:clamp(60px,8vw,100px) 0 clamp(50px,6vw,80px);background:radial-gradient(70% 90% at 70% 40%,#3a1a20 0%,#1d1418 55%,#120d10 100%);color:#fcf7ec}
.mystery .pin{max-width:1180px;margin:0 auto;padding:0 clamp(16px,5vw,56px);display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}
.mystery h2{font-family:var(--display);font-weight:800;font-size:clamp(2.2rem,4.4vw,3.4rem);line-height:1.05;margin:.2em 0 .35em;color:#fcf7ec}
.mystery h2 em{font-style:italic;color:#fac846}
.mystery p{font-size:1.15rem;line-height:1.6;color:#e9dccf;max-width:540px;margin:0 0 22px}
.mystery .kicker{color:#fac846}
.mystery video{display:block;width:100%;max-width:340px;margin:0 auto;border-radius:16px;border:4px solid #fac846;box-shadow:0 24px 60px rgba(0,0,0,.55);background:#000}
.mystery .vcap{text-align:center;font-weight:800;color:#fac846;margin-top:12px;font-size:.95rem}
@media (max-width:760px){.mystery .pin{grid-template-columns:1fr;gap:30px}}
'''
SECTION = f'''<!-- ================= MYSTERY ROOM (whodunit logic puzzles) ================= -->
<section class="mystery" id="mystery" aria-label="Mystery puzzles for grown-ups">
  <div class="pin">
    <div>
      <div class="kicker">For grown-ups</div>
      <h2>The <em>Mystery Room</em></h2>
      <p>Whodunit logic puzzles you solve with a pencil. Each case is a painted floor plan and one true statement from every suspect. Place everyone in the right square, and whoever shares a room with the body is the killer.</p>
      <p>No guessing and nothing gory. Every case has exactly one answer, with hints and full solutions at the back.</p>
      <a class="cta" href="books/{SLUG}.html">Look inside the first book</a>
    </div>
    <div>
      <video controls playsinline preload="none" poster="assets/video/whodunit-how-to-solve.jpg"><source src="assets/video/whodunit-how-to-solve.mp4" type="video/mp4" /></video>
      <div class="vcap">Watch how to solve a case, step by step</div>
    </div>
  </div>
  <div class="shelf-title light">Whodunit logic puzzles</div>
  <div class="shelf dark" data-books="{SLUG}"></div>
</section>

'''
if '.mystery{' not in idx:
    idx = idx.replace('.poetry{position:relative', CSS + '.poetry{position:relative', 1)
if 'id="mystery"' not in idx:
    idx = idx.replace('<!-- ================= POETRY (Janice Kingsley) ================= -->', SECTION + '<!-- ================= POETRY (Janice Kingsley) ================= -->', 1)
if 'href="#mystery"' not in idx:
    idx = idx.replace('<a href="#golden">Golden years</a>', '<a href="#golden">Golden years</a><a href="#mystery">Mysteries</a>', 1)
open('index.html', 'w', encoding='utf-8').write(idx)
print('added', SLUG, '| homepage mentions:', idx.count(SLUG), '| section:', 'id="mystery"' in idx, '| nav:', 'href="#mystery"' in idx)
