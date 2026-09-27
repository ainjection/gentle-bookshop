"""Add the Write with Quill dysgraphia workbook (listed 27 Sep 2026, ASIN pending) to the site.
Buy links use an Amazon search until the ASIN exists: set ASIN below and re-run (idempotent), then python seo.py."""
import re, html as H, os, json
import fitz
from PIL import Image
esc = lambda s: H.escape(s, quote=True)
ASIN = ''
SLUG = 'dysgraphia-quill-kids'
TITLE = "Dysgraphia Handwriting Workbook for Kids Ages 7-11"
SUB = "Print Practice and a Cursive Starter with Numbered Starting Points, Arrows, and Big-to-Small Lines"
TAG = "Every print letter taught by how it moves, with numbered starting points, arrows and big-to-small lines. Plus a gentle cursive starter."
FACTS = ["138 pages", "8.5 x 11 in", "Ages 7 to 11, grades 2 to 5", "All 26 letters in movement families", "Cursive starter", "Paperback, $11.99"]
ABOUT = ["Handwriting help for kids who find writing hard, with or without a diagnosis of dysgraphia. Every print letter is taught by how it moves, in five movement families, with numbered starting points, arrows and a short letter talk to say out loud.",
         "Practice starts on big lines and steps down to real wide-ruled notebook paper. The letters kids mix up most, b and d, and p and q, are learned in different families and get extra Letter Detective pages. Then capitals, numbers, spacing, words, sentences and dictation.",
         "Part 3 is a gentle cursive starter: the basic strokes and all 26 lowercase letters, each with its own movement cue, then joins, words and phrases. A grown-up guide, progress pages, a certificate and an answer key are included, and Quill the hedgehog keeps them company all the way."]
WHO = "Kids aged 7 to 11 (grades 2 to 5) whose handwriting is slow, tiring or hard to read, and the parents, teachers and tutors helping them. Suggested sessions of about 10 minutes."
COVER = r"D:\kdp-dysgraphia-us\art\rob\front-rob.jpg"
PDF = r"D:\kdp-dysgraphia-us\UPLOAD-KDP\1-INTERIOR-Dysgraphia-Workbook-US-138pp.pdf"
PAGES = [1, 8, 14, 22, 41, 109, 127]
SEARCH = "https://www.amazon.com/s?k=Dysgraphia+Handwriting+Workbook+for+Kids+Ages+7-11+Print+Practice+Cursive+Starter&i=stripbooks"
BUY = f"https://www.amazon.com/dp/{ASIN}" if ASIN else SEARCH
RELATED = [('dysgraphia-kids', 'Dysgraphia Workbook: Kids'), ('dysgraphia-cursive', 'Dysgraphia Workbook: Cursive'), ('left-handed-handwriting', 'Left-Handed Handwriting Workbook')]

s = open('books/gross-book-of-why.html', encoding='utf-8').read()
s = s.replace("The Curious Kid's Gross Book of Why: 150 Revolting Questions With Real Answers", f"{TITLE}: {SUB}")
s = s.replace("The Curious Kid's Gross Book of Why", TITLE)
s = s.replace('content="Why do we fart? Why is snot green? Why do dogs sniff each other\'s bottoms? Real answers, checked twice. Look inside 7 sample pages, then get it on Amazon."', f'content="{esc(TAG)} Look inside 7 sample pages, then get it on Amazon."')
s = s.replace('content="Why do we fart? Why is snot green? Why do dogs sniff each other\'s bottoms? Real answers, checked twice."', f'content="{esc(TAG)}"')
s = s.replace("Why do we fart? Why is snot green? Why do dogs sniff each other's bottoms? Real answers, checked twice.", TAG)
s = s.replace("gross-book-of-why", SLUG)
s = s.replace("https://www.amazon.com/dp/B0HHZTLVH3", esc(BUY))
s = re.sub(r'<ul class="facts sans">.*?</ul>', '<ul class="facts sans">' + ''.join(f'<li>{f}</li>' for f in FACTS) + '</ul>', s, flags=re.S)
s = re.sub(r'(<section class="desc">\s*<h2>About this book</h2>\s*).*?(</section>)', lambda m: m.group(1) + ''.join(f'    <p>{p}</p>\n' for p in ABOUT) + m.group(2), s, flags=re.S)
s = re.sub(r'<div class="who sans">.*?</div>', f'<div class="who sans">{WHO}</div>', s, flags=re.S)
s = s.replace('<a href="../index.html#gifts">Birthday &amp; Gift Books</a>', '<a href="../index.html">Dysgraphia Workbooks</a>')
s = s.replace('<div class="kicker sans">Birthday &amp; Gift Books</div>', '<div class="kicker sans">Dysgraphia Workbooks</div>')
shelf = ''.join(f'    <a class="mini" href="{slug}.html"><img src="../assets/{slug}.jpg" alt="{esc(t)} cover" loading="lazy" /><h3>{esc(t)}</h3></a>\n' for slug, t in RELATED)
s = re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + shelf + m.group(2), s, flags=re.S)
if not ASIN:
    s = s.replace('Get it on Amazon</a>', 'Coming soon to Amazon</a>')
assert 'gross' not in s.lower(), 'template leftovers'

im = Image.open(COVER).convert('RGB'); im.thumbnail((900, 1200)); im.save(f"assets/{SLUG}.jpg", quality=88)
d = fitz.open(PDF); os.makedirs(f"assets/samples/{SLUG}", exist_ok=True)
for k, p in enumerate(PAGES, 1):
    pix = d[p - 1].get_pixmap(dpi=110); pg = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    full = pg.copy(); full.thumbnail((1200, 1600)); full.save(f"assets/samples/{SLUG}/{k}.jpg", quality=85)
    th = pg.copy(); th.thumbnail((400, 520)); th.save(f"assets/samples/{SLUG}/{k}-thumb.jpg", quality=80)
open(f"books/{SLUG}.html", 'w', encoding='utf-8').write(s)

data = [x for x in json.load(open('books.json', encoding='utf-8')) if x['slug'] != SLUG]
data.append({"slug": SLUG, "asin": ASIN, "title": f"{TITLE}: {SUB}", "short": "Dysgraphia Workbook with Quill", "cover": f"{SLUG}.jpg",
             "shelf": "dysgraphia", "shelf_name": "Dysgraphia Workbooks", "tagline": TAG, "who": WHO, "facts": FACTS,
             "samples": 7, "description": ABOUT, "related": ["dysgraphia"]})
json.dump(data, open('books.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# homepage (window.GENTLE_BOOKS data model): card on the dysgraphia shelf; renderer honours an optional url
idx = open('index.html', encoding='utf-8').read()
entry = json.dumps({SLUG: {"asin": ASIN, "url": BUY, "short": "Dysgraphia Workbook with Quill" + ("" if ASIN else " (coming soon)"), "cover": f"{SLUG}.jpg"}})[1:-1]
idx = re.sub(r', "' + SLUG + r'": \{[^}]*\}', '', idx)
idx = idx.replace('}};</script>', '}, ' + entry + '};</script>', 1)
if f'data-books="{SLUG},' not in idx:
    idx = idx.replace('data-books="dysgraphia-kids,dysgraphia-teens,', f'data-books="{SLUG},dysgraphia-kids,dysgraphia-teens,', 1)
old = 'href="https://www.amazon.com/dp/${b.asin}" target="_blank" rel="noopener">Amazon</a>'
if old in idx:
    idx = idx.replace(old, 'href="${b.url || \'https://www.amazon.com/dp/\' + b.asin}" target="_blank" rel="noopener">Amazon</a>')
open('index.html', 'w', encoding='utf-8').write(idx)
print('added', SLUG, '| homepage mentions:', idx.count(SLUG), '| buy:', BUY[:60])
