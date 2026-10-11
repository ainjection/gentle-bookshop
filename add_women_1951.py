"""Add 101 Things Only Women Born in 1951 Remember (B0HMP5XJ88, live 11 Oct 2026). Idempotent; then python seo.py."""
import re, html as H, os, json
import fitz
from PIL import Image
esc = lambda s: H.escape(s, quote=True)
ASIN = 'B0HMP5XJ88'
SLUG = 'women-1951'
SHORT = "Women Born in 1951: 101 Things Only She Remembers"
TITLE = "101 Things Only Women Born in 1951 Remember"
SUB = "The 75th Birthday Gift for Her: Dolls, Fashion, Music and Memories of a 1950s Girlhood"
TAG = "She was born in 1951. Give her back the girl she was."
FACTS = ["168 pages", "6 x 9 in", "Large 14 point print", "101 chapters, 10 word searches, 50 question party quiz", "Paperback, $12.99"]
ABOUT = [p.strip() for p in open(r"D:\kdp-1951-women\desc.txt", encoding='utf-8').read().split('\n\n') if p.strip()][1:]
WHO = "The 75th birthday gift for a mom, a grandma, a wife, a sister, an aunt or an old friend born in 1951. Also lovely for Mother's Day, a retirement, or a reminiscence group."
COVER = r"D:\kdp-1951-women\print\_front-panel.jpg"
PDF = r"D:\kdp-1951-women\KDP-UPLOAD\1-INTERIOR-6x9-168pp-NO-BLEED.pdf"
PAGES = [4, 5, 22, 24, 16, 80, 100, 14]
BUY = f"https://www.amazon.com/dp/{ASIN}?tag=gentlebooksho-20"
RELATED = [('born-1951', 'Born in 1951: 101 Things You Will Never Forget'), ('born-1956', 'Born in 1956: 101 Things You Will Never Forget'), ('born-1960', 'Born in 1960: 101 Things You Will Never Forget')]

s = open('books/born-1951.html', encoding='utf-8').read()
s = s.replace("101 Things People Born in 1951 Will Never Forget: The 75th Birthday Gift for Men and Women", f"{TITLE}: {SUB}")
s = s.replace("Somebody you love was born in 1951. Give them the year back.", TAG)
s = re.sub(r'<ul class="facts sans">.*?</ul>', '<ul class="facts sans">' + ''.join(f'<li>{f}</li>' for f in FACTS) + '</ul>', s, flags=re.S)
s = re.sub(r'(<section class="desc">\s*<h2>About this book</h2>\s*).*?(</section>)', lambda m: m.group(1) + ''.join(f'    <p>{esc(p)}</p>\n' for p in ABOUT) + m.group(2), s, flags=re.S)
s = re.sub(r'<div class="who sans">.*?</div>', f'<div class="who sans">{esc(WHO)}</div>', s, flags=re.S)
shelf = ''.join(f'    <a class="mini" href="{slug}.html"><img src="../assets/{slug}.jpg" alt="{esc(t)} cover" loading="lazy" /><h3>{esc(t)}</h3></a>\n' for slug, t in RELATED)
s = re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + shelf + m.group(2), s, flags=re.S)
s = s.replace("Born in 1951: 101 Things You Will Never Forget", SHORT)
s = s.replace("born-1951", SLUG)
s = s.replace("https://www.amazon.com/dp/B0HJ2PXK3N?tag=gentlebooksho-20", BUY)
s = re.sub(r'<!--seo-->.*?<!--/seo-->', '', s, flags=re.S)  # seo.py rebuilds it
assert 'B0HJ2PXK3N' not in s and 'Men and Women' not in s and '14.99' not in s, 'template leftovers'

im = Image.open(COVER).convert('RGB'); im.thumbnail((900, 1200)); im.save(f"assets/{SLUG}.jpg", quality=88)
d = fitz.open(PDF); os.makedirs(f"assets/samples/{SLUG}", exist_ok=True)
for k, p in enumerate(PAGES, 1):
    pix = d[p - 1].get_pixmap(dpi=110); pg = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    full = pg.copy(); full.thumbnail((1200, 1600)); full.save(f"assets/samples/{SLUG}/{k}.jpg", quality=85)
    th = pg.copy(); th.thumbnail((400, 520)); th.save(f"assets/samples/{SLUG}/{k}-thumb.jpg", quality=80)
open(f"books/{SLUG}.html", 'w', encoding='utf-8').write(s)

data = [x for x in json.load(open('books.json', encoding='utf-8')) if x['slug'] != SLUG]
data.append({"slug": SLUG, "asin": ASIN, "title": f"{TITLE}: {SUB}", "short": SHORT, "cover": f"{SLUG}.jpg",
             "shelf": "gifts", "shelf_name": "Birthday & Gift Books", "tagline": TAG, "who": WHO, "facts": FACTS,
             "samples": len(PAGES), "description": ABOUT, "related": ["B0HJ2PXK3N", "B0HJC5LFYL", "B0HHY8LZFG"]})
json.dump(data, open('books.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

idx = open('index.html', encoding='utf-8').read()
entry = json.dumps({SLUG: {"asin": ASIN, "short": SHORT + " (new)", "cover": f"{SLUG}.jpg"}})[1:-1]
idx = re.sub(r', "' + SLUG + r'": \{[^}]*\}', '', idx)
idx = idx.replace('}};</script>', '}, ' + entry + '};</script>', 1)
if f'data-books="{SLUG},' not in idx:
    idx = idx.replace('data-books="born-1951,', f'data-books="{SLUG},born-1951,', 1)
open('index.html', 'w', encoding='utf-8').write(idx)
print('added', SLUG, '| homepage mentions:', idx.count(SLUG))
