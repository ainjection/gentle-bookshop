"""Build books/<slug>.html from books.json and link the index cards to them.
Run from the site folder:  python build-books.py
"""
import json, re, html, os

books = json.load(open('books.json', encoding='utf-8'))
index = open('index.html', encoding='utf-8').read()

# title + cover for every ASIN on the index, used for "more on this shelf"
cards = {}
for m in re.finditer(r'<div class="book">(.*?)</div>', index, re.S):
    c = m.group(1)
    asin = re.search(r'/dp/([A-Z0-9]+)', c)
    img = re.search(r'src="assets/([^"]+)"', c)
    h3 = re.search(r'<h3>(.*?)</h3>', c, re.S)
    if asin and img and h3:
        cards[asin.group(1)] = (img.group(1), re.sub(r'\s+', ' ', h3.group(1)).strip())
slug_of = {b['asin']: b['slug'] for b in books}

CSS = """
  :root { --teal:#105c64; --teal-d:#0b454c; --teal-l:#1a7a84; --cream:#fcf7ec; --paper:#fffdf8; --ink:#21302e; --orange:#f08c34; --yellow:#fac846; --muted:#5f7472; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family: Georgia,'Times New Roman',serif; background:var(--paper); color:var(--ink); }
  .sans { font-family:'Segoe UI',system-ui,-apple-system,sans-serif; }
  .top { background:var(--teal); color:var(--cream); padding:14px 22px; }
  .top-inner { max-width:1080px; margin:0 auto; display:flex; align-items:center; gap:14px; }
  .top img { width:44px; height:44px; border-radius:50%; border:2px solid var(--cream); object-fit:cover; }
  .top a { color:var(--cream); text-decoration:none; font-weight:700; }
  .top .crumb { margin-left:auto; font-size:14px; color:#dcebe9; }
  .top .crumb a { font-weight:400; }
  .hero { max-width:1080px; margin:0 auto; padding:44px 22px 10px; display:grid; grid-template-columns:minmax(220px,340px) 1fr; gap:40px; align-items:start; }
  .hero img { width:100%; border-radius:10px; box-shadow:0 18px 40px rgba(0,0,0,.25); }
  .kicker { letter-spacing:.24em; text-transform:uppercase; font-size:12.5px; color:var(--orange); font-weight:700; }
  h1 { font-size:clamp(26px,3.6vw,40px); line-height:1.15; color:var(--teal-d); margin:8px 0 14px; }
  .tagline { font-size:18px; font-style:italic; color:var(--muted); line-height:1.5; margin-bottom:20px; }
  .facts { list-style:none; display:flex; flex-wrap:wrap; gap:8px; margin:0 0 22px; }
  .facts li { background:var(--cream); border:1px solid #eadfc7; border-radius:20px; padding:6px 14px; font-size:13.5px; }
  .buy { display:inline-block; padding:14px 32px; background:var(--orange); color:#fff; border-radius:28px; text-decoration:none; font-weight:700; font-size:16px; }
  .buy:hover { background:#d9781f; }
  .buy-note { font-size:13px; color:var(--muted); margin-top:10px; }
  section { max-width:1080px; margin:0 auto; padding:40px 22px 0; }
  h2 { font-size:clamp(22px,3vw,30px); color:var(--teal-d); margin-bottom:8px; }
  .sect-sub { color:var(--muted); margin-bottom:22px; font-size:15.5px; line-height:1.55; }
  .gallery { display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:14px; }
  .gallery a { display:block; background:#fff; border:1px solid #e6dcc6; border-radius:8px; padding:6px; box-shadow:0 6px 18px rgba(16,60,56,.10); transition:transform .15s; }
  .gallery a:hover { transform:translateY(-4px); }
  .gallery img { width:100%; display:block; border-radius:4px; }
  .desc p { font-size:16.5px; line-height:1.7; margin-bottom:16px; max-width:760px; }
  .who { background:var(--cream); border-radius:16px; padding:24px 26px; max-width:760px; font-size:16px; line-height:1.65; }
  .shelf { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:22px; max-width:760px; }
  .mini { background:var(--cream); border-radius:14px; padding:16px; text-align:center; text-decoration:none; color:var(--ink); box-shadow:0 8px 24px rgba(16,60,56,.10); }
  .mini img { width:100%; max-width:170px; border-radius:6px; box-shadow:0 8px 20px rgba(0,0,0,.2); }
  .mini h3 { font-size:15.5px; margin-top:12px; color:var(--teal-d); line-height:1.3; }
  .cta { max-width:1080px; margin:48px auto 0; padding:0 22px 56px; text-align:center; }
  footer { text-align:center; padding:40px 20px 50px; color:var(--muted); font-size:14px; line-height:1.8; background:var(--cream); margin-top:20px; }
  footer a { color:var(--teal); font-weight:700; text-decoration:none; }
  .lb { position:fixed; inset:0; background:rgba(11,69,76,.94); display:none; align-items:center; justify-content:center; z-index:50; cursor:zoom-out; }
  .lb.open { display:flex; }
  .lb img { max-width:min(96vw,900px); max-height:92vh; border-radius:6px; box-shadow:0 20px 60px rgba(0,0,0,.6); background:#fff; }
  .lb button { position:absolute; top:50%; transform:translateY(-50%); background:rgba(255,255,255,.12); color:#fff; border:0; font-size:38px; width:56px; height:80px; cursor:pointer; border-radius:8px; }
  .lb .prev { left:12px; } .lb .next { right:12px; }
  .lb .count { position:absolute; bottom:18px; left:0; right:0; text-align:center; color:#dcebe9; font-size:14px; }
  @media (max-width:640px) { .hero { grid-template-columns:1fr; gap:24px; } .hero img { max-width:260px; margin:0 auto; display:block; } }
"""

JS = """
  const links=[...document.querySelectorAll('.gallery a')], lb=document.getElementById('lb'), im=lb.querySelector('img'), cnt=lb.querySelector('.count');
  let i=0; const show=n=>{i=(n+links.length)%links.length; im.src=links[i].href; cnt.textContent=(i+1)+' / '+links.length; lb.classList.add('open');};
  links.forEach((a,n)=>a.addEventListener('click',e=>{e.preventDefault(); show(n);}));
  lb.querySelector('.prev').onclick=e=>{e.stopPropagation(); show(i-1);};
  lb.querySelector('.next').onclick=e=>{e.stopPropagation(); show(i+1);};
  lb.onclick=()=>lb.classList.remove('open');
  document.addEventListener('keydown',e=>{ if(!lb.classList.contains('open')) return; if(e.key==='Escape') lb.classList.remove('open'); if(e.key==='ArrowRight') show(i+1); if(e.key==='ArrowLeft') show(i-1); });
"""

def esc(s): return html.escape(s, quote=False)

os.makedirs('books', exist_ok=True)
for b in books:
    amz = f"https://www.amazon.com/dp/{b['asin']}"
    gallery = ''.join(
        f'    <a href="../assets/samples/{b["slug"]}/{k}.jpg"><img src="../assets/samples/{b["slug"]}/{k}-thumb.jpg" alt="{esc(b["short"])} sample page {k}" loading="lazy" /></a>\n'
        for k in range(1, b['samples'] + 1))
    related = ''
    for a in b['related']:
        if a in cards:
            img, name = cards[a]
            href = f'{slug_of[a]}.html' if a in slug_of else f'https://www.amazon.com/dp/{a}'
            related += f'    <a class="mini" href="{href}"><img src="../assets/{img}" alt="{esc(name)} cover" loading="lazy" /><h3>{name}</h3></a>\n'
    desc = ''.join(f'    <p>{esc(p)}</p>\n' for p in b['description'])
    facts = ''.join(f'<li>{esc(f)}</li>' for f in b['facts'])
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(b['short'])} | The Gentle Bookshop</title>
<meta name="description" content="{esc(b['tagline'])} Look inside {b['samples']} sample pages, then get it on Amazon." />
<meta property="og:title" content="{esc(b['short'])}" />
<meta property="og:description" content="{esc(b['tagline'])}" />
<meta property="og:image" content="https://ainjection.github.io/gentle-bookshop/assets/{b['cover']}" />
<style>{CSS}</style>
</head>
<body>
<div class="top sans"><div class="top-inner">
  <img src="../assets/logo.png" alt="The Gentle Bookshop" />
  <a href="../index.html">The Gentle Bookshop</a>
  <span class="crumb"><a href="../index.html#{b['shelf']}">{esc(b['shelf_name'])}</a> &rsaquo; {esc(b['short'])}</span>
</div></div>

<div class="hero">
  <div><img src="../assets/{b['cover']}" alt="{esc(b['title'])} cover" /></div>
  <div>
    <div class="kicker sans">{esc(b['shelf_name'])}</div>
    <h1>{esc(b['title'])}</h1>
    <p class="tagline">{esc(b['tagline'])}</p>
    <ul class="facts sans">{facts}</ul>
    <a class="buy sans" href="{amz}">Get it on Amazon</a>
    <p class="buy-note sans">Printed and shipped by Amazon. Scroll down to look inside first.</p>
  </div>
</div>

<section id="look-inside">
  <h2>Look inside</h2>
  <p class="sect-sub sans">{b['samples']} real pages from the printed book. Tap any page to see it full size.</p>
  <div class="gallery">
{gallery}  </div>
</section>

<section class="desc">
  <h2>About this book</h2>
{desc}</section>

<section>
  <h2>Who it is for</h2>
  <div class="who sans">{esc(b['who'])}</div>
</section>

<section>
  <h2>More on this shelf</h2>
  <div class="shelf sans">
{related}  </div>
</section>

<div class="cta"><a class="buy sans" href="{amz}">Get {esc(b['short'])} on Amazon</a></div>

<footer class="sans">
  <p><strong>The Gentle Bookshop</strong> &mdash; gentle books for little ones and golden years.</p>
  <p><a href="../index.html">All books</a> &middot; <a href="https://www.youtube.com/@TheGentleBookshop">YouTube</a> &middot; <a href="https://www.pinterest.com/digitalexpress77/amazon-kdp/">Pinterest</a></p>
</footer>

<div class="lb" id="lb"><button class="prev" aria-label="Previous">&lsaquo;</button><img src="" alt="Sample page" /><button class="next" aria-label="Next">&rsaquo;</button><div class="count sans"></div></div>
<script>{JS}</script>
</body>
</html>
"""
    open(f'books/{b["slug"]}.html', 'w', encoding='utf-8').write(page)
    print('built books/' + b['slug'] + '.html')

# link index cards: cover + title go to the book page, add a Look inside link above the Amazon button
for b in books:
    if f'href="books/{b["slug"]}.html"' in index:
        print(b['slug'], 'index card already linked'); continue
    pat = re.compile(r'(<div class="book">\s*(?:<span class="badge sans">[^<]*</span>\s*)?)<img src="assets/' + re.escape(b['cover']) + r'"([^>]*)/>\s*<h3>(.*?)</h3>(.*?)<a class="buy sans" href="https://www.amazon.com/dp/' + b['asin'] + '">', re.S)
    def rep(m):
        return (f'{m.group(1)}<a class="cardlink" href="books/{b["slug"]}.html"><img src="assets/{b["cover"]}"{m.group(2)}/>'
                f'<h3>{m.group(3)}</h3></a>{m.group(4)}<a class="peek sans" href="books/{b["slug"]}.html">Look inside</a>\n      '
                f'<a class="buy sans" href="https://www.amazon.com/dp/{b["asin"]}">')
    index, n = pat.subn(rep, index, count=1)
    print(b['slug'], 'index card linked' if n else 'INDEX CARD NOT FOUND')

if '.cardlink' not in index:
    index = index.replace('  .buy:hover', '  .cardlink { text-decoration:none; color:inherit; }\n  .peek { display:inline-block; margin-top:12px; color:var(--teal); font-weight:700; font-size:14px; text-decoration:none; }\n  .peek:hover { text-decoration:underline; }\n  .buy:hover', 1)
open('index.html', 'w', encoding='utf-8').write(index)
