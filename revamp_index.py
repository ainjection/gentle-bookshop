"""Rebuild the shop front around what sells (Rob, 23 Sep 2026).

- compact two-column hero so books show on the first screen, with a "Shop our best sellers" button
- shelf order: Best Sellers -> Halloween (seasonal) -> New This Month -> category shelves by sales
- ONE badge rule: "Best seller" on the best sellers, "New" on this month's books, nothing else
  (the old "New release" was on 36 of 49 cards, which meant nothing)
- every existing card is reused verbatim (blurbs unchanged); only its badge changes
Run after add_seniors_new.py.  python revamp_index.py
"""
import re, json, html as H
esc = lambda s: H.escape(s, quote=True)

idx = open('index.html', encoding='utf-8').read()
first = idx.index('<section id=')
last = idx.rindex('</section>') + len('</section>')
head, tail = idx[:first], idx[last:]
sections = idx[first:last]

# every card, keyed by slug, badge stripped
cards = {}
for m in re.finditer(r'    <div class="book">.*?\n    </div>\n', sections, re.S):
    c = re.sub(r'\s*<span class="badge sans">[^<]*</span>', '', m.group(0))
    slug = re.search(r'href="books/([^"]+)\.html"', c).group(1)
    cards.setdefault(slug, c)
# old section intros, reused for the category shelves
intro = {}
for m in re.finditer(r'<section id="([^"]+)">\s*(<div class="kicker sans">.*?</p>)\s*<div class="shelf">', sections, re.S):
    intro[m.group(1)] = m.group(2)
old_order = {m.group(1): re.findall(r'href="books/([^"]+)\.html" ?>?<img', m.group(2)) or
             re.findall(r'class="cardlink" href="books/([^"]+)\.html"', m.group(2))
             for m in re.finditer(r'<section id="([^"]+)">(.*?)</section>', sections, re.S)}

books = {b['slug']: b for b in json.load(open('books.json', encoding='utf-8'))}
BLURB = {'chair-tai-chi': 'Forty seated moves for two, ten minutes a day, both of you in every picture.',
         'sciatica-relief': 'Fifty gentle exercises in large print, with a follow-along video for each.'}
for slug in ('chair-tai-chi', 'sciatica-relief'):
    b = books[slug]
    cards[slug] = (f'    <div class="book">\n'
                   f'      <a class="cardlink" href="books/{slug}.html"><img src="assets/{b["cover"]}" alt="{esc(b["short"])} cover" loading="lazy" /><h3>{esc(b["short"])}</h3></a>\n'
                   f'      <p class="sans">{BLURB[slug]}</p>\n'
                   f'      <a class="peek sans" href="books/{slug}.html">Look inside</a>\n'
                   f'      <a class="buy sans" href="{b["buy"]}">Get it on Amazon</a>\n'
                   f'    </div>\n')

BEST = ['dysgraphia-teens', 'dysgraphia-kids', 'left-handed-handwriting', 'pre-writing-skills', 'left-handed-tracing', 'big-book-of-why-little-ones']
NEW = ['chair-tai-chi', 'sciatica-relief']
HALLOWEEN = ['halloween-grayscale-complete', 'halloween-grayscale-vol1', 'halloween-grayscale-vol2',
             'halloween-mosaics-complete', 'halloween-mosaics-vol1', 'halloween-mosaics-vol2',
             'halloween-seek-and-find', 'halloween-word-search-easy', 'halloween-word-search-hard']
BADGE = {**{s: 'Best seller' for s in BEST}, **{s: 'New' for s in NEW}}


def card(slug):
    c = cards[slug]
    if slug in BADGE:
        c = c.replace('    <div class="book">\n', f'    <div class="book">\n      <span class="badge sans{" badge-best" if BADGE[slug] == "Best seller" else ""}">{BADGE[slug]}</span>\n', 1)
    return c


def section(sid, intro_html, slugs, extra_cls=''):
    return (f'<section id="{sid}"{extra_cls}>\n  {intro_html}\n  <div class="shelf">\n'
            + ''.join(card(s) for s in slugs) + '  </div>\n</section>\n\n')


out = section('bestsellers', '<div class="kicker sans">Readers&rsquo; favourites</div>\n  <h2>Our Best Sellers</h2>\n'
              '  <p class="sect-sub sans">The books people come back for: calm, step-by-step handwriting help for children who find '
              'writing hard, left-handers included, and our Big Book of Why.</p>', BEST, ' class="featured"')
out += section('halloween', '<div class="kicker sans">Halloween is on 31 October</div>\n  <h2>Halloween Books</h2>\n'
               '  <p class="sect-sub sans">Everything spooky in one place: grayscale colouring for grown-ups, hidden-picture '
               'mosaics and seek and find for kids, and large-print word searches for all ages.</p>', HALLOWEEN, ' class="seasonal"')
out += section('new', '<div class="kicker sans">Just published</div>\n  <h2>New This Month</h2>\n'
               '  <p class="sect-sub sans">Two new books for staying mobile after 60, both large print, both illustrated step by step, '
               'both ten minutes a day.</p>', NEW)
# category shelves, ordered by what sells, without the Halloween books (they have their own shelf now)
ORDER = ['learning', 'curious', 'seniors', 'grayscale', 'seekfind', 'puzzles-games', 'gifts', 'stories', 'coloring']
shown = set(HALLOWEEN)
for sid in ORDER:
    slugs = [s for s in old_order[sid] if s in cards and s not in HALLOWEEN]
    if sid == 'seniors':
        slugs = NEW + slugs
    if slugs:
        out += section(sid, intro[sid], slugs)
        shown |= set(slugs)
missing = [s for s in cards if s not in shown and s not in BEST]
assert not missing, f'cards dropped: {missing}'

# ---- compact hero: text left, video right; nav in the new order
head = head.replace('''  <nav class="shelfnav sans">
    <a href="#coloring">Colouring</a>
    <a href="#grayscale">Grayscale</a>
    <a href="#stories">Story Books</a>
    <a href="#curious">Curious Kids</a>
    <a href="#learning">Learning</a>
    <a href="#seekfind">Seek &amp; Find</a>
    <a href="#puzzles-games">Puzzles</a>
    <a href="#seniors">Seniors</a>
    <a href="#gifts">Gifts</a>
  </nav>''', '''  <nav class="shelfnav sans">
    <a class="nav-hot" href="#bestsellers">Best Sellers</a>
    <a class="nav-hot" href="#halloween">Halloween</a>
    <a class="nav-hot" href="#new">New</a>
    <a href="#learning">Learning</a>
    <a href="#curious">Curious Kids</a>
    <a href="#seniors">Seniors</a>
    <a href="#grayscale">Grayscale</a>
    <a href="#seekfind">Seek &amp; Find</a>
    <a href="#puzzles-games">Puzzles</a>
    <a href="#gifts">Gifts</a>
    <a href="#stories">Story Books</a>
    <a href="#coloring">Colouring</a>
  </nav>''')
head = re.sub(r'<p class="hero-sub sans">.*?</p>', '<p class="hero-sub sans">Handwriting workbooks for children who find writing hard, '
              'large-print books for seniors, colouring, puzzles and stories. Every book made with care: big friendly pages and zero stress.</p>', head, flags=re.S)
head = head.replace('<div class="social sans">', '<div class="social sans">\n    <a class="shopbest" href="#bestsellers">Shop our best sellers</a>', 1)
head = head.replace('<header>', '<header>\n <div class="hero-grid">\n  <div class="hero-text">', 1)
head = head.replace('  <div class="hero-video">', '  </div>\n  <div class="hero-video">', 1)
head = head.replace('</header>', ' </div>\n</header>', 1)
CSS = '''
  /* 23 Sep 2026 revamp: compact hero, best sellers first */
  header { padding-top: 34px !important; padding-bottom: 34px !important; }
  .hero-grid > * { min-width: 0; }
  .hero-grid { max-width: 1120px; margin: 0 auto; display: grid; grid-template-columns: 1.05fr 1fr; gap: 36px; align-items: center; text-align: left; }
  .hero-text .logo { width: 84px; height: 84px; border-width: 4px; float: left; margin: 4px 18px 0 0; }
  .hero-text h1 { margin: 0 0 4px; font-size: clamp(32px, 3.9vw, 46px); line-height: 1.05; }
  .hero-text .shelfnav { clear: both; padding-top: 10px; }
  .hero-text .hero-sub { margin: 14px 0 0; max-width: none; }
  .hero-text .social { justify-content: flex-start; margin-top: 20px; }
  .hero-text .shelfnav { justify-content: flex-start; }
  .hero-grid .hero-video { margin: 0; max-width: none; }
  .social a.shopbest { background: var(--orange) !important; color: #fff !important; border-color: var(--orange) !important; }
  .shelfnav a.nav-hot { background: var(--yellow); color: var(--ink); }
  section.featured { background: #fff7e8; }
  section.seasonal { background: #f7efe6; }
  .badge.badge-best { background: var(--orange); color: #fff; }
  @media (max-width: 900px) {
    .hero-grid { grid-template-columns: 1fr; text-align: center; gap: 22px; }
    .hero-text .social, .hero-text .shelfnav { justify-content: center; }
    .hero-grid .hero-video { display: none; }
    .hero-text .logo { float: none; margin: 0 auto 10px; display: block; }
  }
'''
head = head.replace('</style>', CSS + '</style>', 1)
open('index.html', 'w', encoding='utf-8').write(head + out.rstrip() + '\n' + tail.lstrip('\n'))
print('cards', len(cards), '| best', len(BEST), '| halloween', len(HALLOWEEN), '| new', len(NEW))
