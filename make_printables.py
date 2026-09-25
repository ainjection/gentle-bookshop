"""Build the two search-friendly printable pages (Halloween + Christmas) on the shelf sites.
Each lists real sample-page PDFs people can print tonight, then points to the full book on Amazon.
Run: python make_printables.py"""
import html

HAL = dict(
    out='D:/halloween-books/halloween-coloring-pages-printable.html',
    url='https://ainjection.github.io/halloween-books/halloween-coloring-pages-printable.html',
    shelf='https://ainjection.github.io/halloween-books/',
    title='Printable Halloween Coloring Pages for Kids and Adults',
    desc='Print Halloween coloring pages at home tonight: bold and easy monsters, seek and find scenes, mystery mosaics, big-print word searches and grayscale pages for grown-ups.',
    h1='Halloween coloring pages', h1em='to print at home tonight',
    intro=('Every set below is a real PDF of five pages from one of our Halloween books. Pick the one that suits your little monster '
           '(or yourself), print it on ordinary Letter or A4 paper, and start colouring. If you love it, the whole book is on Amazon.'),
    font='Griffy', fonturl='family=Griffy&family=Nunito:wght@400;700;800',
    bg='radial-gradient(120% 80% at 80% 0%,#3b1f55 0%,#22133a 45%,#0b0816 100%)', ink='#f3ecff', muted='#b9a9d6',
    card='#22133a', accent='#ff7a1a', accent_ink='#1b1030', title_col='#ffb347', og='https://ainjection.github.io/halloween-books/covers/halloween-bold-easy.jpg',
    items=[
        ('halloween-bold-easy', 'samples/be-1.jpg', 'Bold and Easy, with a fun fact on every design', 'Ages 4 and up, teens and adults',
         'Thick friendly lines and big spaces: Dracula, Frankenstein, witches and mummies, each with a "Did you know?" box.', None),
        ('halloween-seek-and-find', 'samples/sf-street.jpg', 'Halloween Seek and Find', 'Ages 4 to 8',
         'Busy scenes with twelve little things to spot on every page. Find them, then colour the whole scene.', 'B0H7JDLNMW'),
        ('halloween-mosaics-vol1', 'covers/halloween-mosaics-vol1.jpg', 'Halloween Mystery Mosaics', 'Ages 6 to 12',
         'Colour each numbered circle and a hidden Halloween picture slowly appears.', 'B0HKDV7FFW'),
        ('halloween-word-search-easy', 'covers/halloween-word-search-easy.jpg', 'Halloween Word Search, Large Print', 'Adults and seniors',
         'Big, easy-to-read letters with the words running forwards. A calm October puzzle.', 'B0HG5NLN8R'),
        ('halloween-grayscale-vol1', 'samples/gs-cat.jpg', 'Halloween Grayscale for Grown-ups', 'Adult colourists',
         'Detailed shaded scenes made for coloured pencils: black cats, haunted manors, witches over rooftops.', 'B0HGVBNKZS'),
    ],
    tips=[('Which paper?', 'Plain printer paper is fine for crayons and pencils. For markers, use thicker paper or put a spare sheet underneath.'),
          ('Letter or A4?', 'The PDFs fit either size. Choose "Fit to page" in the print box.'),
          ('Which set for which age?', 'Ages 4 to 8: Bold and Easy or Seek and Find. Ages 6 to 12: Mystery Mosaics. Grown-ups: Grayscale or the large-print Word Search.'),
          ('A Halloween party idea', 'Print one page per guest and put out a pot of crayons. It fills a quiet twenty minutes between games.')],
)
XMAS = dict(
    out='D:/christmas-books/christmas-coloring-pages-printable.html',
    url='https://ainjection.github.io/christmas-books/christmas-coloring-pages-printable.html',
    shelf='https://ainjection.github.io/christmas-books/',
    title='Printable Christmas Coloring Pages for Kids and Adults',
    desc='Print Christmas coloring pages at home: festive seek and find scenes for kids and detailed grayscale Christmas pages for grown-ups.',
    h1='Christmas coloring pages', h1em='to print at home',
    intro=('Every set below is a real PDF of five pages from one of our Christmas books. Print it on ordinary Letter or A4 paper and '
           'you have a cosy afternoon sorted. If you love it, the whole book is on Amazon, ready for a stocking.'),
    font='Mountains of Christmas', fonturl='family=Mountains+of+Christmas:wght@700&family=Nunito:wght@400;700;800',
    bg='radial-gradient(120% 80% at 20% 0%,#13264d 0%,#0a1630 60%,#060d1f 100%)', ink='#eef3ff', muted='#b6c4e0',
    card='#13264d', accent='#d7263d', accent_ink='#ffffff', title_col='#ffd23f', og='https://ainjection.github.io/christmas-books/covers/christmas-seek-and-find.jpg',
    items=[
        ('christmas-seek-and-find', 'samples/sf-workshop.jpg', 'Christmas Seek and Find', 'Ages 4 to 8',
         "Santa's workshop, snowy streets and reindeer stables, each hiding little things to find and colour.", 'B0H7MK2MWQ'),
        ('christmas-grayscale-vol1', 'samples/gs-santa.jpg', 'Christmas Grayscale, Volume One', 'Adult colourists',
         'Shaded festive scenes for coloured pencils: Santa, robins, snowy cottages.', 'B0HHSG215H'),
        ('christmas-grayscale-vol2', 'samples/gs-robin.jpg', 'Christmas Grayscale, Volume Two', 'Adult colourists',
         'More detailed Christmas pages where the grey shading does the hard work.', 'B0HHSG2M4Q'),
        ('christmas-grayscale-complete', 'samples/gs-cottage.jpg', 'Christmas Grayscale: Complete Collection', '100 pages, adult colourists',
         'Both volumes in one book, the best value for a keen colourist.', 'B0HHBZK7S1'),
    ],
    tips=[('Which paper?', 'Plain printer paper suits crayons and pencils. For felt tips, use thicker paper or a spare sheet underneath.'),
          ('Letter or A4?', 'The PDFs fit either. Choose "Fit to page" when you print.'),
          ('Which set for which age?', 'Ages 4 to 8: Seek and Find. Teens and grown-ups: the Grayscale sets.'),
          ('A Christmas Eve idea', 'Print a page for everyone at the table. It keeps little hands busy while the dinner finishes.')],
)

e = lambda s: html.escape(s, quote=True)

def build(c):
    cards = ''
    for slug, img, name, who, blurb, asin in c['items']:
        buy = (f'<a class="btn ghost" href="https://www.amazon.com/dp/{asin}" target="_blank" rel="noopener">See the whole book</a>' if asin
               else f'<a class="btn ghost" href="free-halloween-coloring-book.html">Get the whole book free</a>')
        cards += f'''
    <article class="card">
      <img src="{img}" alt="{e(name)} sample page" loading="lazy" width="600" height="600">
      <div class="body"><span class="who">{e(who)}</span><h2>{e(name)}</h2><p>{e(blurb)}</p>
        <div class="acts"><a class="btn" href="pages/{slug}-sample-pages.pdf" download>Print 5 pages (PDF)</a>{buy}</div></div>
    </article>'''
    tips = ''.join(f'<div class="tip"><h3>{e(q)}</h3><p>{e(a)}</p></div>' for q, a in c['tips'])
    ld = ('{"@context":"https://schema.org","@type":"CollectionPage","name":"%s","description":"%s","url":"%s",'
          '"publisher":{"@type":"Organization","name":"The Gentle Bookshop"}}') % (e(c['title']), e(c['desc']), c['url'])
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(c['title'])} | The Gentle Bookshop</title>
<meta name="description" content="{e(c['desc'])}">
<link rel="canonical" href="{c['url']}">
<meta property="og:title" content="{e(c['title'])}"><meta property="og:description" content="{e(c['desc'])}"><meta property="og:image" content="{c['og']}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{c['fonturl']}&display=swap" rel="stylesheet">
<script type="application/ld+json">{ld}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Nunito,system-ui,sans-serif;background:{c['bg']};background-color:{c['card']};min-height:100vh;color:{c['ink']};line-height:1.6}}
.wrap{{max-width:1060px;margin:0 auto;padding:0 16px}}
nav{{padding:18px 0;font-weight:800}} nav a{{color:{c['muted']};text-decoration:none}} nav a:hover{{color:{c['ink']}}}
header{{padding:28px 0 20px;text-align:center}}
h1{{font-family:"{c['font']}",serif;font-size:clamp(2.1rem,6vw,3.6rem);line-height:1.1;color:{c['ink']}}}
h1 em{{display:block;font-style:normal;color:{c['title_col']}}}
.intro{{max-width:42rem;margin:16px auto 0;color:{c['muted']};font-size:1.08rem}}
.grid{{display:grid;gap:22px;margin:36px 0 56px}}
@media(min-width:760px){{.grid{{grid-template-columns:1fr 1fr}}}}
.card{{background:{c['card']};border:1px solid rgba(255,255,255,.1);border-radius:18px;overflow:hidden;display:flex;flex-direction:column}}
.card img{{width:100%;aspect-ratio:1/1;object-fit:contain;background:#fff}}
.body{{padding:18px 20px 22px;display:flex;flex-direction:column;gap:8px;flex:1}}
.who{{font-size:.78rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:{c['title_col']}}}
.card h2{{font-size:1.3rem;line-height:1.25}} .card p{{color:{c['muted']}}}
.acts{{display:flex;flex-wrap:wrap;gap:10px;margin-top:auto;padding-top:8px}}
.btn{{display:inline-block;font-weight:800;padding:10px 18px;border-radius:999px;background:{c['accent']};color:{c['accent_ink']};text-decoration:none}}
.btn.ghost{{background:transparent;color:{c['ink']};border:2px solid rgba(255,255,255,.35)}}
.btn:hover{{filter:brightness(1.1)}}
.tips h2{{font-family:"{c['font']}",serif;font-size:2rem;text-align:center;margin-bottom:18px;color:{c['title_col']}}}
.tipgrid{{display:grid;gap:16px}} @media(min-width:760px){{.tipgrid{{grid-template-columns:1fr 1fr}}}}
.tip{{background:rgba(255,255,255,.05);border-radius:14px;padding:16px 18px}} .tip h3{{font-size:1.05rem;margin-bottom:4px}} .tip p{{color:{c['muted']}}}
.more{{text-align:center;margin:44px 0 30px}}
footer{{text-align:center;color:{c['muted']};font-size:.9rem;padding:24px 0 40px}} footer a{{color:{c['muted']}}}
</style>
</head>
<body>
<div class="wrap">
  <nav><a href="{c['shelf']}">&larr; Back to the shelf</a></nav>
  <header>
    <h1>{e(c['h1'])} <em>{e(c['h1em'])}</em></h1>
    <p class="intro">{e(c['intro'])}</p>
  </header>
  <main>
    <section class="grid" aria-label="Printable sets">{cards}
    </section>
    <section class="tips"><h2>Printing tips</h2><div class="tipgrid">{tips}</div></section>
    <p class="more"><a class="btn" href="{c['shelf']}">See the whole shelf</a></p>
  </main>
  <footer>Made by <a href="https://ainjection.github.io/gentle-bookshop/">The Gentle Bookshop</a>. All books are printed and shipped by Amazon.</footer>
</div>
<script src="track.js" defer></script>
</body>
</html>
'''
    open(c['out'], 'w', encoding='utf-8').write(page)
    print('built', c['out'])

for c in (HAL, XMAS): build(c)
