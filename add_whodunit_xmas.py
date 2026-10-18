"""Add Whodunit Puzzles for Adults: The Naughty List Murders (B0HNH15RH4, live 18 Oct 2026) to the Mystery Room shelf.
Run after add_whodunit_cozy.py (it owns the section). Idempotent; then python seo.py."""
import re, html as H, os, json, urllib.request
import fitz
from PIL import Image
esc = lambda s: H.escape(s, quote=True)
ASIN = 'B0HNH15RH4'
SLUG = 'whodunit-naughty-list'
SHORT = "Whodunit Puzzles for Adults: The Naughty List Murders"
TITLE = "Whodunit Puzzles for Adults: The Naughty List Murders"
SUB = "61 Funny Christmas Mysteries to Solve, Easy to Hard, with Hints and Full Solutions"
TAG = "Somebody at the North Pole has been very naughty indeed. Yes, it might be Santa."
FACTS = ["108 pages", "8.5 x 11 in", "Full colour inside", "61 Christmas cases, hints and full solutions", "Paperback, $12.99"]
DESC = json.load(open(r"D:\kdp-whodunit-research\book-xmas\listing.json", encoding='utf-8'))["description"]
ABOUT = [p.strip() for p in DESC.split('\n\n') if p.strip()][1:]
WHO = "For anyone who loves murder mysteries, logic puzzles and a bit of Christmas mischief. A perfect stocking stuffer or Secret Santa gift for a puzzle-mad friend, a parent or a grandparent."
COVER = "https://m.media-amazon.com/images/I/71O3XCKaGgL._SL1293_.jpg"
PDF = r"D:\kdp-whodunit-research\book-xmas\KDP-UPLOAD\1-INTERIOR-8.5x11-108pp-NO-BLEED.pdf"
PAGES = [1, 7, 8, 9, 30, 50, 70, 76]
BUY = f"https://www.amazon.com/dp/{ASIN}?tag=gentlebooksho-20"
RELATED = [('whodunit-cozy-village', None), ('christmas-grayscale-vol1', None), ('christmas-grayscale-vol2', None)]
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

# ---- homepage: book map entry + first on the Mystery Room shelf ----------------------------------------------
idx = open('index.html', encoding='utf-8').read()
entry = json.dumps({SLUG: {"asin": ASIN, "short": SHORT, "cover": f"{SLUG}.jpg"}})[1:-1]
idx = re.sub(r', "' + SLUG + r'": \{[^}]*\}', '', idx)
idx = idx.replace('}};</script>', '}, ' + entry + '};</script>', 1)
idx = idx.replace('data-books="whodunit-cozy-village"', f'data-books="{SLUG},whodunit-cozy-village"', 1)
assert f'data-books="{SLUG},whodunit-cozy-village"' in idx, 'mystery shelf not found'
open('index.html', 'w', encoding='utf-8').write(idx)
print('added', SLUG, '| homepage mentions:', idx.count(SLUG))
