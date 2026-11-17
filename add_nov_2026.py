"""Add the four books published since 4 Nov 2026: Women Born in 1946, The Advent Doors, No Word List, Records Don't Lie. Same method as add_women_1951.py / add_whodunit_xmas.py
(book page cloned from books/born-1951.html). Idempotent; then python seo.py."""
import re, html as H, os, json
import fitz
from PIL import Image
esc = lambda s: H.escape(s, quote=True)
SHELVES = {'gifts': 'Birthday & Gift Books', 'mystery': 'Mystery Puzzles', 'puzzles-games': 'Puzzles & Brain Games', 'stories': 'Illustrated Story Books'}
TEMPLATE = open('books/born-1951.html', encoding='utf-8').read()


def paras(text):                       # description paragraphs, minus the opening hook line (it is the tagline)
    return [p.strip() for p in text.split('\n\n') if p.strip()][1:]


def section(path, start, stop):        # the text between two headings in a listing file
    t = open(path, encoding='utf-8').read()
    return t.split(start, 1)[1].split(stop, 1)[0].strip().strip('`').strip()


def add(slug, asin, short, title, sub, tag, facts, about, who, cover, pdf, pages, shelf, related, first_in):
    books = json.load(open('books.json', encoding='utf-8'))
    short_of = {b['slug']: b['short'] for b in books}
    s = TEMPLATE
    s = s.replace("101 Things People Born in 1951 Will Never Forget: The 75th Birthday Gift for Men and Women", esc(f"{title}: {sub}"))
    s = s.replace("Somebody you love was born in 1951. Give them the year back.", esc(tag))
    s = re.sub(r'<ul class="facts sans">.*?</ul>', '<ul class="facts sans">' + ''.join(f'<li>{esc(f)}</li>' for f in facts) + '</ul>', s, flags=re.S)
    s = re.sub(r'(<section class="desc">\s*<h2>About this book</h2>\s*).*?(</section>)', lambda m: m.group(1) + ''.join(f'    <p>{esc(p)}</p>\n' for p in about) + m.group(2), s, flags=re.S)
    s = re.sub(r'<div class="who sans">.*?</div>', lambda m: f'<div class="who sans">{esc(who)}</div>', s, flags=re.S)
    mini = ''.join(f'    <a class="mini" href="{r}.html"><img src="../assets/{r}.jpg" alt="{esc(short_of[r])} cover" loading="lazy" /><h3>{esc(short_of[r])}</h3></a>\n' for r in related)
    s = re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + mini + m.group(2), s, flags=re.S)
    s = s.replace("Born in 1951: 101 Things You Will Never Forget", esc(short))
    s = s.replace("Birthday &amp; Gift Books", esc(SHELVES[shelf])).replace("index.html#gifts", f"index.html#{shelf}")
    s = s.replace("born-1951", slug)
    s = s.replace("https://www.amazon.com/dp/B0HJ2PXK3N?tag=gentlebooksho-20", f"https://www.amazon.com/dp/{asin}?tag=gentlebooksho-20")
    s = re.sub(r'<!--seo-->.*?<!--/seo-->', '', s, flags=re.S)   # seo.py rebuilds it
    assert all(x not in s for x in ('B0HJ2PXK3N', 'Men and Women', '14.99', '143 pages', 'Give them the year back', '75th birthday, 1951')), f'{slug}: template leftovers'
    assert len(pages) == 8, 'the template shows 8 sample pages'

    im = Image.open(cover).convert('RGB'); im.thumbnail((900, 1200)); im.save(f"assets/{slug}.jpg", quality=88)
    d = fitz.open(pdf); os.makedirs(f"assets/samples/{slug}", exist_ok=True)
    for k, p in enumerate(pages, 1):
        pix = d[p - 1].get_pixmap(dpi=110); pg = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        full = pg.copy(); full.thumbnail((1200, 1600)); full.save(f"assets/samples/{slug}/{k}.jpg", quality=85)
        th = pg.copy(); th.thumbnail((400, 520)); th.save(f"assets/samples/{slug}/{k}-thumb.jpg", quality=80)
    open(f"books/{slug}.html", 'w', encoding='utf-8').write(s)

    books = [x for x in books if x['slug'] != slug]
    books.append({"slug": slug, "asin": asin, "title": f"{title}: {sub}", "short": short, "cover": f"{slug}.jpg", "shelf": shelf,
                  "shelf_name": SHELVES[shelf], "tagline": tag, "who": who, "facts": facts, "samples": len(pages), "description": about})
    json.dump(books, open('books.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

    idx = open('index.html', encoding='utf-8').read()
    entry = json.dumps({slug: {"asin": asin, "short": short + " (new)", "cover": f"{slug}.jpg"}})[1:-1]
    idx = re.sub(r', "' + slug + r'": \{[^}]*\}', '', idx)
    idx = idx.replace('}};</script>', '}, ' + entry + '};</script>', 1)
    for anchor in first_in:            # put the book first on each home page shelf whose list starts with `anchor`
        if re.search('data-books="[^"]*' + re.escape(slug) + ',[^"]*' + re.escape(anchor), idx): continue
        assert idx.count(f'data-books="{anchor}') == 1, f'shelf starting {anchor} not found'
        idx = idx.replace(f'data-books="{anchor}', f'data-books="{slug},{anchor}', 1)
    open('index.html', 'w', encoding='utf-8').write(idx)
    print('added', slug, '| homepage mentions:', idx.count(slug))


W = "D:/kdp-{y}-women/"
GIFT = "The {n} birthday gift for a mom, a grandma, a wife, a sister, an aunt or an old friend born in {y}. Also lovely for Mother's Day, a retirement, or a reminiscence group."
add('women-1946', 'B0HR7MP2PB', "Women Born in 1946: 101 Things Only She Remembers", "101 Things Only Women Born in 1946 Remember",
    "The 80th Birthday Gift for Her: Dolls, Charm Bracelets, Music and Memories of a 1950s Girlhood, with Trivia Quizzes and Word Search Puzzles - Large Print",
    "She was born in 1946. Give her back the girl she was.",
    ["221 pages", "6 x 9 in", "Large 16 point print", "101 memories, 11 word searches, 50 question party quiz", "Paperback, $12.99"],
    paras(open(W.format(y=1946) + 'desc.txt', encoding='utf-8').read()),
    GIFT.format(n='80th', y=1946), W.format(y=1946) + 'print/_front-panel.jpg',
    W.format(y=1946) + 'KDP-UPLOAD/1-INTERIOR-6x9-221pp-NO-BLEED-16pt.pdf', [4, 5, 19, 20, 40, 80, 120, 170],
    'gifts', ['women-1951', 'women-1957', 'women-1967'], ['women-1967,'])
N = 'D:/kdp-24-nights/KDP-UPLOAD/'
add('advent-doors', 'B0HR1LLB23', "The Advent Doors: 24 Christmas Stories", "The Advent Doors",
    "24 Christmas Stories for Kids: One Cozy Bedtime Tale for Each Night Until Santa Comes",
    "Twenty four doors. Twenty four nights. One story for every night before Christmas.",
    ["298 pages", "8.5 x 8.5 in", "Ages 3 to 8", "24 read aloud stories, full colour pictures in every one", "Paperback, $24.99"],
    paras(open(N + '5-DESCRIPTION-paste-into-KDP.txt', encoding='utf-8').read()),
    "Children aged 3 to 8 and the grown ups who read to them. Start it on December 1 as a family tradition, or give it as a gift that lasts all through December.",
    'D:/kdp-aplus-v3/advent-doors/cover.png', N + '1-INTERIOR-8.5x8.5-298pp-BLEED.pdf', [1, 9, 10, 11, 22, 34, 58, 100],
    'stories', ['little-star', 'goodnight-capybara', 'christmas-seek-and-find'], ['goodnight-capybara,', 'christmas-seek-and-find,christmas-grayscale-vol1'])
T = 'D:/kdp-teen-quizsearch/UPLOAD/'
add('no-word-list', 'B0HRSWKV76', "No Word List: 100 Trivia Puzzles for Clever Teens", "No Word List",
    "100 Trivia Puzzles for Clever Teens: Quiz Word Searches, Code Breakers, Word Sudoku and Crosswords That Teach You Something",
    "Most word searches hand you the answers. This one makes you earn them.",
    ["120 pages", "8.5 x 11 in", "Ages 12 and up", "100 puzzles in five styles, three levels, answers at the back", "Paperback, $9.99"],
    paras(section(T + '3-LISTING.txt', 'DESCRIPTION (plain text)', 'KEYWORDS')),
    "Teens aged 12 and up who like quizzes, facts and brain games, and anyone who thinks ordinary word searches are too easy. Good for car rides, rainy weekends and time away from a screen.",
    T + '4-front-cover-for-reference.png', T + '1-INTERIOR-no-word-list-120pp-8.5x11-NO-BLEED.pdf', [5, 6, 9, 12, 30, 55, 80, 100],
    'puzzles-games', ['dogs-mystery-mosaics', 'halloween-word-search-hard', 'whodunit-cozy-village'], ['halloween-pocket-sudoku,'])
R = 'D:/kdp-dead-air/UPLOAD/'
add('records-dont-lie', 'B0HRT1178V', "Records Don't Lie: A Murder Mystery Puzzle Book", "Records Don't Lie",
    "A Murder Mystery Puzzle Book for Teens and Adults: One Connected Case, Six Suspects, 73 Evidence Puzzles to Solve",
    "Six people were on site. All six have a reason. All six have an alibi.",
    ["140 pages", "8.5 x 11 in", "Ages 13 and up", "One connected case, 73 evidence puzzles, hints and full solution", "Paperback, $10.99"],
    paras(section(R + '3-LISTING-title-description-keywords.txt', 'DESCRIPTION (plain text)', 'KEYWORDS')),
    "Teens and adults, ages 13 and up, who love mysteries, escape rooms and logic puzzles. No gore and nothing a parent would mind. Six bonus cases to solve face to face with a friend.",
    R + '4-front-cover-for-reference.png', R + '1-INTERIOR-records-dont-lie-140pp.pdf', [1, 5, 6, 7, 20, 50, 90, 120],
    'mystery', ['whodunit-naughty-list', 'whodunit-cozy-village', 'no-word-list'], ['whodunit-naughty-list,'])
