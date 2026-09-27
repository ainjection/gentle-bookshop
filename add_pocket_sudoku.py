"""Add Pocket Sudoku & Grayscale Coloring: Halloween Edition (live 27 Sep 2026, B0HL6G178R) to the site:
book page with 7 sample pages, a New release card at the front of the Halloween section, and books.json."""
import re, html as H, os, json
import fitz
from PIL import Image
esc = lambda s: H.escape(s, quote=True)
T = open('books/gross-book-of-why.html', encoding='utf-8').read()
SRC = r"D:\kdp-sudoku-grayscale"
B = dict(slug='halloween-pocket-sudoku', asin='B0HL6G178R', title="Pocket Sudoku & Grayscale Coloring: Halloween Edition",
         sub="100 Sudoku Puzzles + 100 Grayscale Pictures to Color, Easy to Hard, Travel Size 5 x 8 Inches",
         tag="100 Sudoku puzzles. 100 Halloween pictures. Each puzzle faces a grayscale picture you can color.",
         facts=["230 pages", "5 x 8 in", "100 puzzles: 34 easy, 33 medium, 33 hard", "100 grayscale pictures", "All solutions included", "Paperback, $9.99"],
         about=["Solve a puzzle, then turn to the picture beside it and bring it to life. Every one of the hundred Sudoku puzzles faces a grayscale Halloween picture: black cats in moonlit windows, haunted manors, witches at their cauldrons, pumpkins, owls and gothic lanes.",
                "The puzzles build from 34 easy to 33 medium and 33 hard, with a clear banner where each level begins. Every puzzle has exactly one solution, each page tells you where its answer is, and all the solutions are at the back.",
                "A pencil test page at the front shows how your colors look over the gray before you start. Colored pencils work best: each picture backs onto a puzzle page, so markers can bleed through."],
         who="Adults and teens who love Sudoku and want something prettier than a plain puzzle book, and colorists who want a smaller project. Travel size, for commutes, waiting rooms and Halloween gift bags.",
         cover=os.path.join(SRC, "rob", "front-fixed.png"), pdf=os.path.join(SRC, "UPLOAD-halloween", "01-INTERIOR.pdf"), pages=[1, 3, 4, 5, 72, 73, 204])
BUY = f"https://www.amazon.com/dp/{B['asin']}"
RELATED = [('halloween-grayscale-complete', 'Halloween Grayscale: Complete Collection'), ('halloween-grayscale-vol1', 'Halloween Grayscale: Vol. 1'),
           ('halloween-mosaics-complete', 'Halloween Mystery Mosaics: The Complete Collection')]

s = T
s = s.replace("The Curious Kid's Gross Book of Why: 150 Revolting Questions With Real Answers", f"{B['title']}: {B['sub']}")
s = s.replace("The Curious Kid's Gross Book of Why", B['title'])
s = s.replace('content="Why do we fart? Why is snot green? Why do dogs sniff each other\'s bottoms? Real answers, checked twice. Look inside 7 sample pages, then get it on Amazon."', f'content="{esc(B["tag"])} Look inside 7 sample pages, then get it on Amazon."')
s = s.replace('content="Why do we fart? Why is snot green? Why do dogs sniff each other\'s bottoms? Real answers, checked twice."', f'content="{esc(B["tag"])}"')
s = s.replace("Why do we fart? Why is snot green? Why do dogs sniff each other's bottoms? Real answers, checked twice.", B['tag'])
s = s.replace("gross-book-of-why", B['slug'])
s = s.replace("https://www.amazon.com/dp/B0HHZTLVH3", BUY)
s = re.sub(r'<ul class="facts sans">.*?</ul>', '<ul class="facts sans">' + ''.join(f'<li>{f}</li>' for f in B['facts']) + '</ul>', s, flags=re.S)
s = re.sub(r'(<section class="desc">\s*<h2>About this book</h2>\s*).*?(</section>)', lambda m: m.group(1) + ''.join(f'    <p>{p}</p>\n' for p in B['about']) + m.group(2), s, flags=re.S)
s = re.sub(r'<div class="who sans">.*?</div>', f'<div class="who sans">{B["who"]}</div>', s, flags=re.S)
s = s.replace('<a href="../index.html#gifts">Birthday &amp; Gift Books</a>', '<a href="../index.html#halloween">Halloween Books</a>')
s = s.replace('<div class="kicker sans">Birthday &amp; Gift Books</div>', '<div class="kicker sans">Halloween Books</div>')
shelf = ''.join(f'    <a class="mini" href="{slug}.html"><img src="../assets/{slug}.jpg" alt="{esc(t)} cover" loading="lazy" /><h3>{esc(t)}</h3></a>\n' for slug, t in RELATED)
s = re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + shelf + m.group(2), s, flags=re.S)
assert 'gross' not in s.lower() and B['asin'] in s, 'template leftovers'

im = Image.open(B['cover']).convert('RGB'); im.thumbnail((900, 1200)); im.save(f"assets/{B['slug']}.jpg", quality=88)
d = fitz.open(B['pdf']); os.makedirs(f"assets/samples/{B['slug']}", exist_ok=True)
for k, p in enumerate(B['pages'], 1):
    pix = d[p - 1].get_pixmap(dpi=110); pg = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    full = pg.copy(); full.thumbnail((1200, 1600)); full.save(f"assets/samples/{B['slug']}/{k}.jpg", quality=85)
    th = pg.copy(); th.thumbnail((400, 520)); th.save(f"assets/samples/{B['slug']}/{k}-thumb.jpg", quality=80)
open(f"books/{B['slug']}.html", 'w', encoding='utf-8').write(s)

data = [x for x in json.load(open('books.json', encoding='utf-8')) if x['slug'] != B['slug']]
data.append({"slug": B['slug'], "asin": B['asin'], "title": f"{B['title']}: {B['sub']}", "short": "Pocket Sudoku: Halloween Edition", "cover": f"{B['slug']}.jpg",
             "shelf": "halloween", "shelf_name": "Halloween Books", "tagline": B['tag'], "who": B['who'], "facts": B['facts'],
             "samples": 7, "description": B['about'], "related": ["grayscale"]})
json.dump(data, open('books.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

card = f'''    <div class="book">
      <span class="badge sans">New release</span>
      <a class="cardlink" href="books/{B['slug']}.html"><img src="assets/{B['slug']}.jpg" alt="{esc(B['title'])} cover" loading="lazy" /><h3>Pocket Sudoku: Halloween Edition</h3></a>
      <p class="sans">100 Sudoku puzzles, each facing a grayscale Halloween picture to color. Easy to hard.</p>
      <a class="peek sans" href="books/{B['slug']}.html">Look inside</a>
      <a class="buy sans" href="{BUY}">Get it on Amazon</a>
    </div>
'''
idx = open('index.html', encoding='utf-8').read()
if B['slug'] not in idx:
    i = idx.index('<section id="halloween"'); j = idx.index('<div class="shelf">', i) + len('<div class="shelf">\n')
    idx = idx[:j] + card + idx[j:]
    open('index.html', 'w', encoding='utf-8').write(idx)
print('added', B['slug'], 'cards:', idx.count(f'books/{B["slug"]}.html'))
