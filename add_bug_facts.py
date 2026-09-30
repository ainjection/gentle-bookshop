"""Add 500 Gross and Amazing Bug Facts (paperback B0HJP8829L, checked on amazon.com 30 Sep 2026) to the site:
cover + 7 sample pages rendered from the print PDFs, a look-inside page built from the Little Ones page,
books.json entry, homepage GENTLE_BOOKS entry and a card on the Curious Kids shelf. Rob asked for it 30 Sep 2026."""
import json, re, html as H
from pathlib import Path
import fitz
from PIL import Image

esc = lambda s: H.escape(s, quote=True)
SLUG, ASIN = 'bug-facts', 'B0HJP8829L'
TITLE = '500 Gross and Amazing Bug Facts'
SUB = 'An Illustrated Insect and Spider Book for Curious Kids Ages 5-10'
TAG = 'A housefly tastes with its feet. A velvet worm fires sticky slime. Tiny animals, enormous surprises.'
META = '500 illustrated bug facts for curious kids aged 5 to 10: insects, spiders and creepy-crawly neighbours, four discoveries on every page.'
FACTS = ['144 pages, full colour', '8.5 x 11 in', 'Ages 5 to 10', '500 discoveries, four to a page', 'Paperback and Kindle']
ABOUT = ['A velvet worm fires sticky glue. A housefly tastes with its feet. An army ant colony builds a bridge out of its own bodies. The closer you look at small animals, the stranger the world gets.',
         '500 Gross and Amazing Bug Facts takes curious children on a tour of insects, spiders, centipedes, snails, slugs and their tiny neighbours. Every page holds four illustrated discoveries, written in clear language a five year old can follow and a ten year old will still enjoy.',
         'Chapters on slime, stings, disguises, builders, hunters and night life, plus a glossary that explains the tricky words, a discovery quiz with answers and an animal index so a favourite creature is easy to find again.',
         'This is a book for dipping into. Read four facts at bedtime, or let a child browse and land wherever a creature catches the eye.']
WHO = 'Curious kids aged 5 to 10 who turn over every log and stone, reluctant readers who want short, surprising facts, and the parents and teachers reading along. Part of the Curious Kids shelf.'

# ---- images: cover from the wrap PDF, 7 sample pages from the interior PDF ----
wrap = fitz.open('D:/kdp-bugs/OUTPUT/bug-facts-cover-wrap.pdf')[0]
z = 3.0; pix = wrap.get_pixmap(matrix=fitz.Matrix(z, z)); W = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
bx = int(0.125 * 72 * z); tw = int(8.5 * 72 * z)
front = W.crop((W.width - bx - tw, bx, W.width - bx, W.height - bx)); front.thumbnail((900, 1200)); front.save(f'assets/{SLUG}.jpg', quality=88)
doc = fitz.open('D:/kdp-bugs/OUTPUT/bug-facts-interior.pdf')
sd = Path(f'assets/samples/{SLUG}'); sd.mkdir(parents=True, exist_ok=True)
for n, p in enumerate([1, 9, 10, 12, 15, 17, 24], 1):
    px = doc[p - 1].get_pixmap(matrix=fitz.Matrix(1.2, 1.2)); im = Image.frombytes('RGB', (px.width, px.height), px.samples)
    im.thumbnail((621, 810)); im.save(sd / f'{n}.jpg', quality=85)
    t = im.copy(); t.thumbnail((399, 520)); t.save(sd / f'{n}-thumb.jpg', quality=82)

# ---- look-inside page from the Little Ones template ----
s = open('books/big-book-of-why-little-ones.html', encoding='utf-8').read()
s = s.replace('The Big Book of Why for Little Ones: 1,000 Questions and Answers for Curious Toddlers, A Fully Illustrated First Encyclopedia of Why, Ages 2 to 5', f'{TITLE}: {SUB}')
s = s.replace('1,000 questions and answers for two to five year olds, a colourful picture for every one and short explanations to read aloud.', META)
s = s.replace("Why do fingers go wrinkly in the bath? Why can't we see the wind? Why does toast smell so good? 1,000 questions, a picture for every one.", TAG)
s = s.replace('The Big Book of Why for Little Ones', TITLE)
s = s.replace('big-book-of-why-little-ones', SLUG).replace('B0HKBW1Q8G', ASIN)
s = s.replace('"numberOfPages": 184, "typicalAgeRange": "2-"', '"numberOfPages": 144, "typicalAgeRange": "5-10"')
s = s.replace('<a href="../index.html#gifts">Birthday &amp; Gift Books</a>', '<a href="../index.html#curious">Curious Kids</a>')
s = re.sub(r'<ul class="facts sans">.*?</ul>', '<ul class="facts sans">' + ''.join(f'<li>{f}</li>' for f in FACTS) + '</ul>', s, flags=re.S)
s = re.sub(r'(<section class="desc">\s*<h2>About this book</h2>\s*).*?(</section>)', lambda m: m.group(1) + ''.join(f'    <p>{esc(p)}</p>\n' for p in ABOUT) + m.group(2), s, flags=re.S)
s = re.sub(r'<div class="who sans">.*?</div>', f'<div class="who sans">{esc(WHO)}</div>', s, flags=re.S)
others = [('big-book-of-why-curious-kids', 'The Big Book of Why for Curious Kids'), ('gross-book-of-why', "The Curious Kid's Gross Book of Why"), ('big-book-of-what-if', 'The Big Book of What If? for Curious Kids')]
shelf = ''.join(f'    <a class="mini" href="{sl}.html"><img src="../assets/{sl}.jpg" alt="{esc(t)} cover" loading="lazy" /><h3>{esc(t)}</h3></a>\n' for sl, t in others)
s = re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + shelf + m.group(2), s, flags=re.S)
assert 'Little Ones' not in s and '1,000' not in s, 'template leftovers'
open(f'books/{SLUG}.html', 'w', encoding='utf-8').write(s)

# ---- books.json ----
books = json.load(open('books.json', encoding='utf-8'))
if not any(b['asin'] == ASIN for b in books):
    books.append(dict(slug=SLUG, asin=ASIN, title=f'{TITLE}: {SUB}', short=TITLE, cover=f'{SLUG}.jpg', shelf='curious', shelf_name='Curious Kids',
                      tagline=TAG, who=WHO, facts=FACTS[:4] + ['Paperback, $19.99. Also on Kindle'], samples=7, description=ABOUT, related=['curious']))
    json.dump(books, open('books.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ---- homepage: GENTLE_BOOKS entry + Curious Kids shelf card ----
idx = open('index.html', encoding='utf-8').read()
if f'"{SLUG}":' not in idx:
    idx = idx.replace('window.GENTLE_BOOKS = {', f'window.GENTLE_BOOKS = {{"{SLUG}": {{"asin": "{ASIN}", "short": "{TITLE} (new)", "cover": "{SLUG}.jpg"}}, ', 1)
idx = idx.replace('data-books="big-book-of-why-little-ones,gross-book-of-why"', f'data-books="{SLUG},big-book-of-why-little-ones,gross-book-of-why"', 1)
assert idx.count(f'"{SLUG}":') == 1 and f'data-books="{SLUG},' in idx
open('index.html', 'w', encoding='utf-8').write(idx)
print('done: page, cover, 7 samples, books.json, homepage card')
