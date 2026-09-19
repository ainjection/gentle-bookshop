"""Add the three Halloween Mystery Mosaics books to the site now, with the buy buttons
pointing at an Amazon search until the ASINs exist (swap with fix_asin() later)."""
import re, html as H, os, sys, json
import fitz
from PIL import Image
esc = lambda s: H.escape(s, quote=True)
T = open('books/gross-book-of-why.html', encoding='utf-8').read()
SRC = r"D:\kdp-halloween-mosaic"
SEARCH = "https://www.amazon.com/s?k=Halloween+Mystery+Mosaics+The+Gentle+Bookshop"

BOOKS = [
    dict(slug='halloween-mosaics-vol1', title="Halloween Mystery Mosaics, Volume One",
         sub="Color by Number for Kids Ages 6-12, 50 Hidden Pictures to Reveal",
         tag="Fifty walls of numbered circles. Color them in and a pumpkin, a ghost or a haunted house pushes its way out of the dark.",
         facts=["112 pages", "8.5 x 11 in", "Ages 6 to 12", "50 mystery pictures, 15 colors", "Single-sided pages", "Paperback, $9.99"],
         about=["Every page hides a picture. All you can see at the start is a grid of numbered and lettered circles on a black page. No outline, no clue. Fill the circles with their colors and a shape starts to appear, and your child will not know what it is until it is looking back at them.",
                "Fifteen colors, keyed 1 to 9 and A to F, with the full key printed on every page and a color test page at the front to match your own pens. Pages are single sided so markers cannot spoil the next picture, every reveal is printed small at the back, and there is a tracker to tick off all fifty.",
                "Five extra pictures to print at home are waiting behind a code inside the back cover."],
         who="Boys and girls aged 6 to 12 who like a puzzle with a payoff. Kitchen table, car, rainy October afternoon, and a good trick-or-treat alternative.",
         cover=os.path.join(SRC, "cover-rob", "front-rob-4k.png"),
         pdf=os.path.join(SRC, "UPLOAD-V1", "1-INTERIOR-112pp-8.625x11.25-BLEED.pdf"), pages=[1, 2, 3, 5, 9, 103, 109]),
    dict(slug='halloween-mosaics-vol2', title="Halloween Mystery Mosaics, Volume Two",
         sub="Color by Number for Kids Ages 6-12, 50 More Hidden Pictures to Reveal",
         tag="Fifty brand new mysteries: a vampire boy, a fox in the pumpkin patch, a skeleton tipping his hat. None of them in Volume One.",
         facts=["112 pages", "8.5 x 11 in", "Ages 6 to 12", "50 new mystery pictures, 15 colors", "Single-sided pages", "Paperback, $9.99"],
         about=["The second book in the series, and it stands on its own. Fifty new pictures hidden inside walls of numbered circles: sixteen characters, twelve animals and twenty-two spooky places and things, drawn in the same cute spooky style.",
                "Same fifteen colors, keyed 1 to 9 and A to F, key on every page, color test page at the front, single-sided pages, every reveal printed small at the back, and a tracker for all fifty.",
                "Five extra pictures to print at home behind the code inside the back cover."],
         who="Kids aged 6 to 12 who finished Volume One and want more, or anyone starting here. The two books make a pair.",
         cover=os.path.join(SRC, "cover-v2", "front-v2-4k.png"),
         pdf=os.path.join(SRC, "UPLOAD-V2", "1-INTERIOR-112pp-8.625x11.25-BLEED.pdf"), pages=[1, 2, 3, 5, 9, 103, 109]),
    dict(slug='halloween-mosaics-complete', title="Halloween Mystery Mosaics: The Complete Collection",
         sub="Color by Number for Kids Ages 6-12, 100 Hidden Pictures, Volumes One and Two in One Book",
         tag="Every picture from Volume One and every picture from Volume Two, one hundred mysteries in a single big book.",
         facts=["218 pages", "8.5 x 11 in", "Ages 6 to 12", "100 mystery pictures, 15 colors", "Single-sided pages", "Paperback, $15.99"],
         about=["The whole of October in one book. One hundred Halloween pictures hidden inside walls of numbered circles, the full contents of Volume One and Volume Two together, numbered 1 to 100.",
                "Fifteen colors keyed 1 to 9 and A to F, key on every page, color test page at the front, single-sided pages, all one hundred reveals printed small at the back, and a tracker to tick them off.",
                "If you already own Volume One or Volume Two, you have half of these pictures. If you own neither, this is the better buy."],
         who="Kids aged 6 to 12 who will get through fifty in a fortnight, classrooms, and grandparents who want one present that lasts the whole month.",
         cover=os.path.join(SRC, "cover-v3", "front-v3-4k.png"),
         pdf=os.path.join(SRC, "UPLOAD-V3", "1-INTERIOR-218pp-8.625x11.25-BLEED.pdf"), pages=[1, 2, 3, 103, 105, 203, 209]),
]

def page_from(pdf, book, n):
    s = T
    s = s.replace("The Curious Kid's Gross Book of Why: 150 Revolting Questions With Real Answers", f"{book['title']}: {book['sub']}")
    s = s.replace("The Curious Kid's Gross Book of Why", book['title'])
    s = s.replace('content="Why do we fart? Why is snot green? Why do dogs sniff each other\'s bottoms? Real answers, checked twice. Look inside 7 sample pages, then get it on Amazon."', f'content="{esc(book["tag"])} Look inside 7 sample pages, then get it on Amazon."')
    s = s.replace('content="Why do we fart? Why is snot green? Why do dogs sniff each other\'s bottoms? Real answers, checked twice."', f'content="{esc(book["tag"])}"')
    s = s.replace("Why do we fart? Why is snot green? Why do dogs sniff each other's bottoms? Real answers, checked twice.", book['tag'])
    s = s.replace("gross-book-of-why", book['slug'])
    s = s.replace("https://www.amazon.com/dp/B0HHZTLVH3", SEARCH)
    s = re.sub(r'<ul class="facts sans">.*?</ul>', '<ul class="facts sans">' + ''.join(f'<li>{f}</li>' for f in book['facts']) + '</ul>', s, flags=re.S)
    s = re.sub(r'(<section class="desc">\s*<h2>About this book</h2>\s*).*?(</section>)', lambda m: m.group(1) + ''.join(f'    <p>{p}</p>\n' for p in book['about']) + m.group(2), s, flags=re.S)
    s = re.sub(r'<div class="who sans">.*?</div>', f'<div class="who sans">{book["who"]}</div>', s, flags=re.S)
    s = s.replace('<a href="../index.html#gifts">Birthday &amp; Gift Books</a>', '<a href="../index.html#mosaics">Halloween Mystery Mosaics</a>')
    s = s.replace('<div class="kicker sans">Birthday &amp; Gift Books</div>', '<div class="kicker sans">Halloween Mystery Mosaics</div>')
    others = [b for b in BOOKS if b['slug'] != book['slug']]
    shelf = ''.join(f'    <a class="mini" href="{o["slug"]}.html"><img src="../assets/{o["slug"]}.jpg" alt="{esc(o["title"])} cover" loading="lazy" /><h3>{esc(o["title"])}</h3></a>\n' for o in others)
    s = re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + shelf + m.group(2), s, flags=re.S)
    return s

cards = ''
data = json.load(open('books.json', encoding='utf-8'))
for b in BOOKS:
    im = Image.open(b['cover']).convert('RGB'); im.thumbnail((900, 1200)); im.save(f"assets/{b['slug']}.jpg", quality=88)
    d = fitz.open(b['pdf']); os.makedirs(f"assets/samples/{b['slug']}", exist_ok=True)
    for k, p in enumerate(b['pages'], 1):
        pix = d[p - 1].get_pixmap(dpi=72); pg = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        full = pg.copy(); full.thumbnail((1200, 1600)); full.save(f"assets/samples/{b['slug']}/{k}.jpg", quality=85)
        th = pg.copy(); th.thumbnail((400, 520)); th.save(f"assets/samples/{b['slug']}/{k}-thumb.jpg", quality=80)
    open(f"books/{b['slug']}.html", 'w', encoding='utf-8').write(page_from(b['pdf'], b, 7))
    cards += f'''    <div class="book">
      <span class="badge sans">New release</span>
      <a class="cardlink" href="books/{b['slug']}.html"><img src="assets/{b['slug']}.jpg" alt="{esc(b['title'])} cover" loading="lazy" /><h3>{esc(b['title'])}</h3></a>
      <p class="sans">{esc(b['facts'][3])}. {esc(b['facts'][2])}.</p>
      <a class="peek sans" href="books/{b['slug']}.html">Look inside</a>
      <a class="buy sans" href="{SEARCH}">Get it on Amazon</a>
    </div>
'''
    data = [x for x in data if x['slug'] != b['slug']]
    data.append({"slug": b['slug'], "asin": "", "title": f"{b['title']}: {b['sub']}", "short": b['title'], "cover": f"{b['slug']}.jpg",
                 "shelf": "mosaics", "shelf_name": "Halloween Mystery Mosaics", "tagline": b['tag'], "who": b['who'], "facts": b['facts'],
                 "samples": 7, "description": b['about'], "related": ["mosaics"]})
    print('built', b['slug'])
json.dump(data, open('books.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

idx = open('index.html', encoding='utf-8').read()
idx = re.sub(r'<section id="mosaics">.*?</section>\n\n', '', idx, flags=re.S)
section = '''<section id="mosaics">
  <div class="kicker sans">Color by number, picture hidden</div>
  <h2>Halloween Mystery Mosaics</h2>
  <p class="sect-sub sans">A wall of numbered circles on a black page. Color them in and a pumpkin, a ghost or a
     haunted house appears. No outline, no clue. Ages 6 to 12.</p>
  <div class="shelf">
''' + cards + '''  </div>
</section>

'''
idx = idx.replace('<section id="curious">', section + '<section id="curious">', 1)
open('index.html', 'w', encoding='utf-8').write(idx)
print('index sections mosaics:', idx.count('id="mosaics"'))
