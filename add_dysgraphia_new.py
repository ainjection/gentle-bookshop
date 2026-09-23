"""Add Dysgraphia High School (B0HJDKRRDH) and Dysgraphia Cursive (B0HJRP8S6F) as book pages, put them on the
Learning shelf, and rebuild the Best Sellers shelf from REAL KDP sales (Rob's KDP report, 23 Sep 2026):
Teens 35, Kids 6, Halloween Grayscale Vol 1 4, Complete 3, High School 3, Cursive / Big Book of Why / 100 Dogs 1.
Same page method as add_seniors_new.py, templated from the Teens page.  python add_dysgraphia_new.py"""
import re, json, os, html as H
import fitz
from PIL import Image
esc = lambda s: H.escape(s, quote=True)
T = open('books/dysgraphia-teens.html', encoding='utf-8').read()
T_TITLE = "Dysgraphia Handwriting Workbook for Teens: Trace-and-Fade Practice to Build Legible, Confident Writing for Ages 10-14"
T_TAG = "A handwriting workbook that finally treats an older writer their age."

BOOKS = [
    dict(slug='dysgraphia-highschool', asin='B0HJDKRRDH', short='Dysgraphia Workbook: High School',
         title="Dysgraphia Handwriting Workbook for High School: Speed, Legibility and Note-Taking Practice for Ages 14-18",
         tag="By fifteen, nobody needs another workbook that starts with the letter A. This one fixes the writing that has to happen at speed.",
         blurb='Speed, legibility, note-taking and exam writing for ages 14 to 18.',
         facts=["120 pages", "8.5 x 11 in", "Ages 14 to 18", "Note-taking and exam writing drills", "Paperback, $9.99"],
         about=["If your teenager has dysgraphia, the problem at this age is rarely forming letters. It is that writing costs so much effort they cannot keep up: notes go half finished, exam answers run out of time before they run out of ideas, and the handwriting falls apart in the last paragraph, exactly where the marks are.",
                "It starts with a timed writing sample and a six-point legibility check that decides what to work on first. Then the eleven letter pairs that collapse under speed (a and o, r and n, b and d and more), each shown with its stroke order, the usual mistake and a model, then used inside real words.",
                "After that: letter height, slant, spacing and the baseline, moving down to ordinary ruled paper; numbers, dates and maths in columns; forms, messages and homework records; note-taking with shorthand and Cornell layout; and exam answers planned and written with the support removed step by step. It closes with the same timed sample, so there is something real to compare."],
         who="Students aged 14 to 18 with dysgraphia or handwriting that breaks down at speed, and the parents, tutors and occupational therapists supporting them. Left-handed friendly.",
         cover=r"D:\dysgraphia-highschool\UPLOAD\02-COVER-WRAP-DYSGRAPHIA-HIGHSCHOOL.pdf",
         pdf=r"D:\dysgraphia-highschool\UPLOAD\01-INTERIOR-DYSGRAPHIA-HIGHSCHOOL.pdf", pages=[1, 8, 15, 21, 41, 44, 81, 94]),
    dict(slug='dysgraphia-cursive', asin='B0HJRP8S6F', short='Dysgraphia Workbook: Cursive',
         title="Dysgraphia Cursive Handwriting Workbook: Trace-and-Fade Joined-Up Practice for Ages 8-13",
         tag="Joined-up writing, one stroke at a time. Cursive taught the way struggling writers actually learn it.",
         blurb='Joined-up writing one stroke at a time, for ages 8 to 13.',
         facts=["114 pages", "8.5 x 11 in", "Ages 8 to 13", "Letter joins and speed drills", "Paperback, $9.99"],
         about=["Cursive is where a lot of struggling writers quietly give up. The letters arrive all at once, the joins are never actually taught, and a child who was managing print is suddenly told to speed up and join up in the same week. This book slows that down.",
                "Letters are grouped by the stroke that starts them, not by the alphabet. Learn the undercurve once and it gives you i, u, t, w and r; learn the overcurve and it gives you n, m, v, y and x. Then the joins, then whole words, then sentences, then pages with no models at all.",
                "Every page uses trace-and-fade: a dark model, lighter ones, start dots, then an empty line to write it cold. Every row has a model letter at both ends, so a left hand never hides the example, and there is a page on paper angle and grip written for left-handers."],
         who="Children aged 8 to 13 with dysgraphia or messy handwriting who are starting or struggling with cursive. Home practice, homeschool, classroom and occupational therapy support. Left-handed friendly.",
         cover=r"D:\dysgraphia-cursive\UPLOAD\2-COVER-WRAP-17.5067x11.25-spine-0.2567.pdf",
         pdf=r"D:\dysgraphia-cursive\UPLOAD\1-INTERIOR-114pp-8.5x11-NO-BLEED.pdf", pages=[1, 5, 11, 37, 43, 49, 61, 87]),
]
SIBLINGS = [('dysgraphia-teens', 'Dysgraphia Workbook: Teens'), ('dysgraphia-kids', 'Dysgraphia Workbook: Kids'),
            ('dysgraphia-highschool', 'Dysgraphia Workbook: High School'), ('dysgraphia-cursive', 'Dysgraphia Workbook: Cursive')]


def front_cover(wrap_pdf):
    page = fitz.open(wrap_pdf)[0]; r = page.rect; b = 0.125 * 72  # front = right 8.5in inside the bleed
    clip = fitz.Rect(r.x1 - b - 8.5 * 72, r.y0 + b, r.x1 - b, r.y1 - b)
    pix = page.get_pixmap(dpi=150, clip=clip)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def page_from(b):
    s = T.replace(T_TITLE, b['title']).replace(T_TAG, b['tag']).replace('Dysgraphia Workbook: Teens', b['short'])
    s = s.replace('dysgraphia-teens', b['slug']).replace('B0H7D6LNHF', b['asin'])
    s = s.replace('Look inside 8 sample pages', f"Look inside {len(b['pages'])} sample pages")
    s = re.sub(r'<ul class="facts sans">.*?</ul>', '<ul class="facts sans">' + ''.join(f'<li>{esc(f)}</li>' for f in b['facts']) + '</ul>', s, flags=re.S)
    s = re.sub(r'(<section class="desc">\s*<h2>About this book</h2>\s*).*?(</section>)', lambda m: m.group(1) + ''.join(f'    <p>{esc(p)}</p>\n' for p in b['about']) + m.group(2), s, flags=re.S)
    s = re.sub(r'<div class="who sans">.*?</div>', f'<div class="who sans">{esc(b["who"])}</div>', s, flags=re.S)
    shelf = ''.join(f'    <a class="mini" href="{sl}.html"><img src="../assets/{sl}.jpg" alt="{esc(n)} cover" loading="lazy" /><h3>{esc(n)}</h3></a>\n'
                    for sl, n in SIBLINGS if sl != b['slug'])
    return re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + shelf + m.group(2), s, flags=re.S)


data = json.load(open('books.json', encoding='utf-8'))
teens = next(x for x in data if x['slug'] == 'dysgraphia-teens')
for b in BOOKS:
    im = front_cover(b['cover']); im.thumbnail((900, 1200)); im.save(f"assets/{b['slug']}.jpg", quality=88)
    d = fitz.open(b['pdf']); os.makedirs(f"assets/samples/{b['slug']}", exist_ok=True)
    for k, p in enumerate(b['pages'], 1):
        pix = d[p - 1].get_pixmap(dpi=110); pg = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        full = pg.copy(); full.thumbnail((1200, 1600)); full.save(f"assets/samples/{b['slug']}/{k}.jpg", quality=85)
        th = pg.copy(); th.thumbnail((400, 520)); th.save(f"assets/samples/{b['slug']}/{k}-thumb.jpg", quality=80)
    open(f"books/{b['slug']}.html", 'w', encoding='utf-8').write(page_from(b))
    data = [x for x in data if x['slug'] != b['slug']]
    data.append({**{k: teens[k] for k in ('shelf', 'shelf_name')}, "slug": b['slug'], "asin": b['asin'], "title": b['title'],
                 "short": b['short'], "cover": f"{b['slug']}.jpg", "tagline": b['tag'], "who": b['who'], "facts": b['facts'],
                 "samples": len(b['pages']), "description": b['about'], "related": ["B0H7D6LNHF", "B0H7B8ZMBN"],
                 "buy": f"https://www.amazon.com/dp/{b['asin']}"})
    print('built', b['slug'])
json.dump(data, open('books.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ---- index: new cards on the Learning shelf (after Teens), Best Sellers rebuilt from real sales
idx = open('index.html', encoding='utf-8').read()
card = lambda sl: re.search(r'    <div class="book">\n(?:(?!    </div>\n).)*?href="books/' + sl + r'\.html".*?\n    </div>\n', idx, re.S).group(0)
strip = lambda c: re.sub(r'\s*<span class="badge sans[^"]*">[^<]*</span>', '', c)
for b in BOOKS:
    if f'books/{b["slug"]}.html' in idx: continue
    new = (f'    <div class="book">\n      <a class="cardlink" href="books/{b["slug"]}.html"><img src="assets/{b["slug"]}.jpg" alt="{esc(b["short"])} cover" loading="lazy" /><h3>{esc(b["short"])}</h3></a>\n'
           f'      <p class="sans">{b["blurb"]}</p>\n      <a class="peek sans" href="books/{b["slug"]}.html">Look inside</a>\n'
           f'      <a class="buy sans" href="https://www.amazon.com/dp/{b["asin"]}">Get it on Amazon</a>\n    </div>\n')
    ls = idx.index('<section id="learning">'); le = idx.index('</section>', ls)
    learn = idx[ls:le]; t = strip(card('dysgraphia-teens'))
    at = learn.find('href="books/dysgraphia-teens.html"'); at = learn.index('    </div>\n', at) + len('    </div>\n') if at >= 0 else learn.rindex('  </div>')
    idx = idx[:ls] + learn[:at] + new + learn[at:] + idx[le:]
BEST = ['dysgraphia-teens', 'dysgraphia-kids', 'halloween-grayscale-vol1', 'halloween-grayscale-complete', 'dysgraphia-highschool', 'dysgraphia-cursive', 'big-book-of-why-little-ones']
cards = ''.join(strip(card(sl)).replace('    <div class="book">\n', '    <div class="book">\n      <span class="badge sans badge-best">Best seller</span>\n', 1) for sl in BEST)
idx = re.sub(r'(<section id="bestsellers"[^>]*>.*?<div class="shelf">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + cards + m.group(2), idx, count=1, flags=re.S)
idx = re.sub(r'(<section id="bestsellers".*?<p class="sect-sub sans">).*?(</p>)', r'\1The books readers actually buy: our Dysgraphia handwriting workbooks for kids, teens and high school, the Halloween grayscale colouring books for grown-ups, and our Big Book of Why.\2', idx, count=1, flags=re.S)
open('index.html', 'w', encoding='utf-8').write(idx)
print('index updated; best sellers:', BEST)
