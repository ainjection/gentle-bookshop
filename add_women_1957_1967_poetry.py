"""Add Women 1957 (B0HPY6ZY13), Women 1967 (B0HQBQ4S4W) and Where You Are Now (B0HQ8KK2CW), Rob 4 Nov 2026.
Template = books/women-1951.html. Idempotent; then python seo.py."""
import re, html as H, os, json
import fitz
from PIL import Image
esc = lambda s: H.escape(s, quote=True)
TPL = open('books/women-1951.html', encoding='utf-8').read()
T_SHORT = "Women Born in 1951: 101 Things Only She Remembers"
T_TITLE = "101 Things Only Women Born in 1951 Remember: The 75th Birthday Gift for Her: Dolls, Fashion, Music and Memories of a 1950s Girlhood"
T_TAG = "She was born in 1951. Give her back the girl she was."

def desc(path):  # KDP description file, first paragraph is the tagline
    return [p.strip() for p in open(path, encoding='utf-8').read().split('\n\n') if p.strip()][1:]

BOOKS = [
 dict(slug='women-1957', asin='B0HPY6ZY13', short="Women Born in 1957: 101 Things Only She Remembers",
      title="101 Things Only Women Born in 1957 Remember: The 70th Birthday Gift for Her: Dolls, Platform Shoes, Music and Memories of a 1960s Girlhood, with Trivia Quizzes and Word Search Puzzles",
      tag="She was born in 1957. Give her back the girl she was.",
      facts=["118 pages", "6 x 9 in", "101 memories, 11 word searches, 50 question party quiz", "Pencil drawings throughout", "Paperback, $12.99"],
      about=desc(r"D:\kdp-1957-women\KDP-UPLOAD\5-DESCRIPTION-paste-into-KDP.txt"),
      who="The 70th birthday gift for a mom, a grandma, a wife, a sister, an aunt or an old friend born in 1957. Also lovely for Mother's Day, a retirement, or a reminiscence group.",
      cover=r"D:\kdp-1957-women\print\_front-panel.jpg", pdf=r"D:\kdp-1957-women\KDP-UPLOAD\1-INTERIOR-6x9-118pp-NO-BLEED.pdf",
      pages=[4, 5, 26, 41, 47, 72, 98, 99], shelf='gifts', shelf_name='Birthday &amp; Gift Books',
      related=[('women-1951', T_SHORT), ('women-1967', "Women Born in 1967: 101 Things Only She Remembers"), ('born-1956', 'Born in 1956: 101 Things You Will Never Forget')]),
 dict(slug='women-1967', asin='B0HQBQ4S4W', short="Women Born in 1967: 101 Things Only She Remembers",
      title="101 Things Only Women Born in 1967 Remember: The 60th Birthday Gift for Her: Roller Skates, Mixtapes and Memories of a 1970s Girlhood, with Trivia, Party Games, Recipes and Word Search Puzzles",
      tag="She was born in 1967. Give her back the girl she was.",
      facts=["138 pages", "6 x 9 in", "101 memories, 12 word searches, hidden pictures", "Party pack: Birthday Bingo, quiz, 8 retro recipes", "Paperback, $12.99"],
      about=desc(r"D:\kdp-1967-women\KDP-UPLOAD\5-DESCRIPTION-paste-into-KDP.txt"),
      who="The 60th birthday gift for a mom, a wife, a sister, an aunt or an old friend born in 1967. The party pack makes it the centre of the birthday table.",
      cover=r"D:\kdp-1967-women\print\_front-panel.jpg", pdf=r"D:\kdp-1967-women\KDP-UPLOAD\1-INTERIOR-6x9-138pp-NO-BLEED.pdf",
      pages=[5, 6, 7, 62, 64, 75, 99, 112], shelf='gifts', shelf_name='Birthday &amp; Gift Books',
      related=[('women-1951', T_SHORT), ('women-1957', "Women Born in 1957: 101 Things Only She Remembers"), ('born-1966', 'Born in 1966: 101 Things You Will Never Forget')]),
 dict(slug='where-you-are-now', asin='B0HQ8KK2CW', short="Where You Are Now: Gentle Poems for Grief",
      title="Where You Are Now: Gentle Poems for Grief, Loss and the Love That Stays",
      tag="For anyone who still makes two cups.",
      facts=["By Janice Kingsley", "120 pages", "6 x 9 in", "95 short poems in five chapters", "Watercolour illustrations throughout"],
      about=None,  # read from the listing file below
      who="A gentle sympathy gift for someone who has lost a mother, father, husband, wife, grandparent or friend, and cannot find the words. A page of bereavement helplines for the UK, Ireland and the USA is at the back.",
      cover=r"D:\poetry-test\book\UPLOAD-WHERE-YOU-ARE-NOW\4-EBOOK-COVER-1600x2560.jpg", pdf=r"D:\poetry-test\book\UPLOAD-WHERE-YOU-ARE-NOW\1-PAPERBACK-INTERIOR-6x9-120pp.pdf",
      pages=[13, 27, 55, 76, 97, 115], shelf='poetry', shelf_name='Poetry', related=[]),
]
lst = open(r"D:\poetry-test\book\UPLOAD-WHERE-YOU-ARE-NOW\5-LISTING-ALL-FIELDS.txt", encoding='utf-8').read()
body = lst.split('----------------------------------------------------------------')[1]
BOOKS[2]['about'] = [p.strip().replace('\n', ', ') if p.count('\n') > 2 else p.strip().replace('\n', ' ') for p in body.split('\n\n') if p.strip()][1:]

for b in BOOKS:
    slug, asin = b['slug'], b['asin']
    buy = f"https://www.amazon.com/dp/{asin}?tag=gentlebooksho-20"
    s = TPL.replace(T_TITLE, b['title']).replace(T_TAG, b['tag'])
    s = re.sub(r'<ul class="facts sans">.*?</ul>', '<ul class="facts sans">' + ''.join(f'<li>{esc(f)}</li>' for f in b['facts']) + '</ul>', s, flags=re.S)
    s = re.sub(r'(<section class="desc">\s*<h2>About this book</h2>\s*).*?(</section>)', lambda m: m.group(1) + ''.join(f'    <p>{esc(p)}</p>\n' for p in b['about']) + m.group(2), s, flags=re.S)
    s = re.sub(r'<div class="who sans">.*?</div>', f'<div class="who sans">{esc(b["who"])}</div>', s, flags=re.S)
    if not b['related']:
        s = re.sub(r'<section>\s*<h2>More on this shelf</h2>.*?</section>\n\n', '', s, flags=re.S)
    s = s.replace('href="../index.html#gifts">Birthday &amp; Gift Books<', f'href="../index.html#{b["shelf"]}">{b["shelf_name"]}<')
    s = s.replace("https://www.amazon.com/dp/B0HMP5XJ88?tag=gentlebooksho-20", buy)
    s = s.replace(T_SHORT, b['short']).replace("women-1951", slug)
    s = s.replace('<div class="kicker sans">Birthday &amp; Gift Books</div>', f'<div class="kicker sans">{b["shelf_name"]}</div>')
    if b['related']:
        shelf = ''.join(f'    <a class="mini" href="{sl}.html"><img src="../assets/{sl}.jpg" alt="{esc(t)} cover" loading="lazy" /><h3>{esc(t)}</h3></a>\n' for sl, t in b['related'])
        s = re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + shelf + m.group(2), s, flags=re.S)
    s = re.sub(r'<!--seo-->.*?<!--/seo-->', '', s, flags=re.S)
    assert 'B0HMP5XJ88' not in s and '75th' not in s and '1950s' not in s, (slug, 'template leftovers')

    im = Image.open(b['cover']).convert('RGB'); im.thumbnail((900, 1200)); im.save(f"assets/{slug}.jpg", quality=88)
    d = fitz.open(b['pdf']); os.makedirs(f"assets/samples/{slug}", exist_ok=True)
    for k, p in enumerate(b['pages'], 1):
        pix = d[p - 1].get_pixmap(dpi=110); pg = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        if b['shelf'] == 'poetry':
            from PIL import ImageOps
            bb = ImageOps.invert(pg.convert('L').crop((0, 0, pg.width, int(pg.height * 0.9)))).point(lambda v: 255 if v > 30 else 0).getbbox(); m = 40
            x0, y0, x1, y1 = bb; w = max(x1 - x0, (y1 - y0) * 3 // 4) + 2 * m; cx = (x0 + x1) // 2; h = w * 4 // 3; cy = (y0 + y1) // 2
            pg = pg.crop((max(0, cx - w // 2), max(0, cy - h // 2), min(pg.width, cx + w // 2), min(pg.height, cy + h // 2)))
        full = pg.copy(); full.thumbnail((1200, 1600)); full.save(f"assets/samples/{slug}/{k}.jpg", quality=85)
        th = pg.copy(); th.thumbnail((400, 520)); th.save(f"assets/samples/{slug}/{k}-thumb.jpg", quality=80)
    n = len(b['pages'])  # template has 8 sample links; drop the extras
    s = re.sub(r'    <a href="\.\./assets/samples/%s/(\d+)\.jpg">.*?</a>\n' % slug, lambda m: m.group(0) if int(m.group(1)) <= n else '', s)
    s = s.replace('Look inside 8 sample pages', f'Look inside {n} sample pages').replace('8 real pages from', f'{n} real pages from')
    open(f"books/{slug}.html", 'w', encoding='utf-8').write(s)

    data = [x for x in json.load(open('books.json', encoding='utf-8')) if x['slug'] != slug]
    data.append({"slug": slug, "asin": asin, "title": b['title'], "short": b['short'], "cover": f"{slug}.jpg",
                 "shelf": b['shelf'], "shelf_name": H.unescape(b['shelf_name']), "tagline": b['tag'], "who": b['who'], "facts": b['facts'],
                 "samples": n, "description": b['about'], "related": []})
    json.dump(data, open('books.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

idx = open('index.html', encoding='utf-8').read()
for b in BOOKS:
    slug = b['slug']
    entry = json.dumps({slug: {"asin": b['asin'], "short": b['short'] + " (new)", "cover": f"{slug}.jpg"}})[1:-1]
    idx = re.sub(r', "' + slug + r'": \{[^}]*\}', '', idx)
    idx = idx.replace('}};</script>', '}, ' + entry + '};</script>', 1)
if 'data-books="women-1967,women-1957,' not in idx:
    idx = idx.replace('data-books="women-1951,', 'data-books="women-1967,women-1957,women-1951,', 1)
CTA = '<a class="cta" href="books/where-you-are-now.html" style="margin-top:12px;background:#a06a5e;color:#fff">Where You Are Now, new on Amazon</a>'
if 'books/where-you-are-now.html' not in idx:
    old = """Visit Janice's poetry page</a>"""
    assert idx.count(old) == 1
    idx = idx.replace(old, old + CTA)
idx = idx.replace('.poetry .cta{background:#3b3540;', '.poetry .cta{background:#3b3540;color:#fff;')
idx = idx.replace('style="margin-left:10px;background:#a06a5e"', 'style="margin-top:12px;background:#a06a5e;color:#fff"')
open('index.html', 'w', encoding='utf-8').write(idx)
print('ok', [idx.count(b['slug']) for b in BOOKS])
