"""Add the Dysgraphia Print Workbook for Older Kids 8-12 (live 28 Oct 2026) to the site.
Buy links use an Amazon search until the ASIN exists: set ASIN below and re-run (idempotent), then python seo.py."""
import re, html as H, os, json
import fitz
from PIL import Image
esc = lambda s: H.escape(s, quote=True)
ASIN = 'B0HPMLLRM7'
SLUG = 'dysgraphia-print-8-12'
TITLE = "Dysgraphia Print Workbook for Older Kids Ages 8-12"
SUB = "Daily Handwriting Practice with Shaded Bands, Dotted Midlines, Spacing Guides and Lefty Tips"
TAG = "For 8 to 12 year olds who know every letter but still write print nobody can read. 81 ten minute lessons with shaded bands, dotted midlines and spacing guides."
FACTS = ["174 pages", "8.5 x 11 in", "Ages 8 to 12", "81 daily lessons", "Extra b, d, p and q practice", "Paperback, $12.99"]
ABOUT = ["For older kids who know every letter and still write print nobody can read, with or without a diagnosis of dysgraphia. The book rebuilds neat handwriting in 81 short daily lessons of about ten minutes.",
         "Shaded writing bands and dotted midlines show exactly where each letter sits, so letters stop floating, shrinking and drifting. Every letter model shows numbered stroke order, and the book opens with pencil warm ups of lines, curves and loops.",
         "Four line sizes step down from big letters to normal notebook size, with spacing guides between words. Extra pages for b, d, p and q, real words and fun fact sentences made for older kids, tips for left handed writers and an 81 day progress tracker."]
WHO = "Kids aged 8 to 12 whose print is messy, slow or hard to read, and the parents, tutors, teachers and therapists helping them. Pages may be photocopied for your own home or one classroom."
COVER = r"D:\kdp-dysgraphia\UPLOAD\4-front-cover-preview.png"
PDF = r"D:\kdp-dysgraphia\UPLOAD\1-interior-174pages.pdf"
PAGES = [1, 9, 25, 75, 95, 129, 155]
SEARCH = "https://www.amazon.com/s?k=Dysgraphia+Print+Workbook+for+Older+Kids+Ages+8-12&i=stripbooks"
BUY = f"https://www.amazon.com/dp/{ASIN}" if ASIN else SEARCH
RELATED = [('dysgraphia-teens', 'Dysgraphia Workbook: Teens'), ('dysgraphia-quill-kids', 'Dysgraphia Workbook with Quill'), ('dysgraphia-cursive', 'Dysgraphia Workbook: Cursive')]

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
s = re.sub(r'\n\s*<a class="gplay sans"[^\n]*</a>', '', s)   # template's Google Play link is the Gross Book's ebook
assert 'gross' not in s.lower(), 'template leftovers'

im = Image.open(COVER).convert('RGB'); im.thumbnail((900, 1200)); im.save(f"assets/{SLUG}.jpg", quality=88)
d = fitz.open(PDF); os.makedirs(f"assets/samples/{SLUG}", exist_ok=True)
for k, p in enumerate(PAGES, 1):
    pix = d[p - 1].get_pixmap(dpi=110); pg = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    full = pg.copy(); full.thumbnail((1200, 1600)); full.save(f"assets/samples/{SLUG}/{k}.jpg", quality=85)
    th = pg.copy(); th.thumbnail((400, 520)); th.save(f"assets/samples/{SLUG}/{k}-thumb.jpg", quality=80)
open(f"books/{SLUG}.html", 'w', encoding='utf-8').write(s)

data = [x for x in json.load(open('books.json', encoding='utf-8')) if x['slug'] != SLUG]
data.append({"slug": SLUG, "asin": ASIN, "title": f"{TITLE}: {SUB}", "short": "Dysgraphia Print Workbook: Ages 8-12", "cover": f"{SLUG}.jpg",
             "shelf": "dysgraphia", "shelf_name": "Dysgraphia Workbooks", "tagline": TAG, "who": WHO, "facts": FACTS,
             "samples": 7, "description": ABOUT, "related": ["dysgraphia"]})
json.dump(data, open('books.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# homepage (window.GENTLE_BOOKS data model): card on the dysgraphia shelf; renderer honours an optional url
idx = open('index.html', encoding='utf-8').read()
entry = json.dumps({SLUG: {"asin": ASIN, "url": BUY, "short": "Dysgraphia Print Workbook: Ages 8-12" + ("" if ASIN else " (coming soon)"), "cover": f"{SLUG}.jpg"}})[1:-1]
idx = re.sub(r', "' + SLUG + r'": \{[^}]*\}', '', idx)
idx = idx.replace('}};</script>', '}, ' + entry + '};</script>', 1)
if f'data-books="{SLUG},' not in idx:
    idx = idx.replace('data-books="dysgraphia-quill-kids,', f'data-books="{SLUG},dysgraphia-quill-kids,', 1)
old = 'href="https://www.amazon.com/dp/${b.asin}" target="_blank" rel="noopener">Amazon</a>'
if old in idx:
    idx = idx.replace(old, 'href="${b.url || \'https://www.amazon.com/dp/\' + b.asin}" target="_blank" rel="noopener">Amazon</a>')
open('index.html', 'w', encoding='utf-8').write(idx)
print('added', SLUG, '| homepage mentions:', idx.count(SLUG), '| buy:', BUY[:60])
