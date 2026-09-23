"""Add Chair Tai Chi (live, B0HKJ1QF7S) and Sciatica Relief (in KDP review: buy button -> Amazon search
until the ASIN exists) as book pages with 7 look-inside pages each, and to books.json. The shop front
itself is rebuilt by revamp_index.py. Same page method as add_halloween_mosaics.py."""
import re, html as H, os, json
import fitz
from PIL import Image
esc = lambda s: H.escape(s, quote=True)
T = open('books/gross-book-of-why.html', encoding='utf-8').read()

BOOKS = [
    dict(slug='chair-tai-chi', asin='B0HKJ1QF7S', buy='https://www.amazon.com/dp/B0HKJ1QF7S',
         title="Chair Tai Chi for Seniors Over 60",
         sub="The 28-Day Do-It-Together Program for Couples: 40 Seated Moves Fully Illustrated Step by Step, 10 Minutes a Day",
         tag="Two chairs. Ten minutes. Together. Forty seated moves, every one shown with both partners in every picture.",
         facts=["138 pages", "8.5 x 11 in", "Large, clear type", "40 seated moves, 130 pictures", "28-day plan with a tracker", "Paperback"],
         about=["Most chair tai chi books are written for one person on one chair. This one is for two of you. Every one of the 40 seated moves is shown in three full-colour pictures with both partners in every frame, arrows showing the path, and a plain caption that tells you what to do, how far to go and when to breathe.",
                "Inside: 8 warm-ups and 2 gentle seated leg moves, 10 tai chi forms adapted for two chairs (Cloud Hands, Brush Knee, Ward Off, Parting the Horse's Mane and more), 12 together drills you can only do as a pair, all no-contact, then 6 cool-downs and 4 breathing practices.",
                "The 28-Day Together Plan runs one week per spread, with a partner tip for every day and a tick box for each of you. There is also a chapter for the days it is not going to plan: different mobility levels, a missed week, bad days."],
         who="Couples over 60, and anyone who would rather move with a partner, a friend, a parent or a carer than alone. Everything is done sitting down.",
         cover='assets/_src-chair-tai-chi.jpg',
         pdf=r"D:\kdp-senior-fitness\UPLOAD\01-INTERIOR-8.5x11-colour-138pp-NO-BLEED.pdf", pages=[1, 3, 12, 14, 22, 23, 120]),
    dict(slug='sciatica-relief', asin='B0HKS8XR7X',
         buy='https://www.amazon.com/dp/B0HKS8XR7X',
         title="Sciatica Relief for Seniors",
         sub="50 Gentle Illustrated Exercises to Ease Lower Back and Leg Pain and Keep It From Coming Back, 10 Minutes a Day",
         tag="Pain that travels down your leg is not a leg problem. Fifty gentle exercises that go where the trouble actually is, in large print.",
         facts=["101 pages", "8.5 x 11 in", "Large print (16 point)", "50 exercises, a picture for each", "50 follow-along videos", "Paperback, $16.99"],
         about=["The sciatic nerve leaves your lower back, passes through the deep muscles of the buttock and runs all the way down the back of your leg. That is why rubbing the sore spot never helps. This book is in two halves, because settling sciatica down and keeping it away are two different jobs.",
                "Part One settles the pain down: movements that take the load off, nerve glides, and releases for the piriformis, hip and hamstring muscles that trap the nerve. Part Two keeps it from coming back: knees, balance, core strength, neck, shoulders and posture.",
                "No floor? No problem. Every exercise is listed by position, and the sitting and standing ones make a complete programme on their own. A QR code inside opens a follow-along video for every exercise, plus a 28-day plan, a progress tracker and two tear-out cards."],
         who="Anyone over 60 living with sciatica or lower back and leg pain, including people who cannot get down to the floor. General wellbeing guidance, not medical advice.",
         cover=r"D:\sciatica-book\COVER-V4\front-4k.png",
         pdf=r"D:\sciatica-book\UPLOAD-MERGED\01-INTERIOR-8.5x11-101pp-LARGEPRINT.pdf", pages=[1, 9, 11, 21, 33, 89, 90]),
]


def page_from(book):
    s = T
    s = s.replace("The Curious Kid's Gross Book of Why: 150 Revolting Questions With Real Answers", f"{book['title']}: {book['sub']}")
    s = s.replace("The Curious Kid's Gross Book of Why", book['title'])
    s = s.replace('content="Why do we fart? Why is snot green? Why do dogs sniff each other\'s bottoms? Real answers, checked twice. Look inside 7 sample pages, then get it on Amazon."', f'content="{esc(book["tag"])} Look inside 7 sample pages, then get it on Amazon."')
    s = s.replace('content="Why do we fart? Why is snot green? Why do dogs sniff each other\'s bottoms? Real answers, checked twice."', f'content="{esc(book["tag"])}"')
    s = s.replace("Why do we fart? Why is snot green? Why do dogs sniff each other's bottoms? Real answers, checked twice.", book['tag'])
    s = s.replace("gross-book-of-why", book['slug'])
    s = s.replace("https://www.amazon.com/dp/B0HHZTLVH3", book['buy'])
    s = re.sub(r'<ul class="facts sans">.*?</ul>', '<ul class="facts sans">' + ''.join(f'<li>{esc(f)}</li>' for f in book['facts']) + '</ul>', s, flags=re.S)
    s = re.sub(r'(<section class="desc">\s*<h2>About this book</h2>\s*).*?(</section>)', lambda m: m.group(1) + ''.join(f'    <p>{esc(p)}</p>\n' for p in book['about']) + m.group(2), s, flags=re.S)
    s = re.sub(r'<div class="who sans">.*?</div>', f'<div class="who sans">{esc(book["who"])}</div>', s, flags=re.S)
    s = s.replace('<a href="../index.html#gifts">Birthday &amp; Gift Books</a>', '<a href="../index.html#seniors">Care &amp; Comfort for Seniors</a>')
    s = s.replace('<div class="kicker sans">Birthday &amp; Gift Books</div>', '<div class="kicker sans">Care &amp; Comfort for Seniors</div>')
    other = [b for b in BOOKS if b['slug'] != book['slug']][0]
    shelf = f'    <a class="mini" href="{other["slug"]}.html"><img src="../assets/{other["slug"]}.jpg" alt="{esc(other["title"])} cover" loading="lazy" /><h3>{esc(other["title"])}</h3></a>\n'
    for slug, name in [('memory-activity', 'Memory Lane Activity Book'), ('puzzles', 'Gentle Puzzles for Seniors')]:
        shelf += f'    <a class="mini" href="{slug}.html"><img src="../assets/{slug}.jpg" alt="{esc(name)} cover" loading="lazy" /><h3>{esc(name)}</h3></a>\n'
    s = re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + shelf + m.group(2), s, flags=re.S)
    return s


data = json.load(open('books.json', encoding='utf-8'))
for b in BOOKS:
    im = Image.open(b['cover']).convert('RGB'); im.thumbnail((900, 1200)); im.save(f"assets/{b['slug']}.jpg", quality=88)
    d = fitz.open(b['pdf']); os.makedirs(f"assets/samples/{b['slug']}", exist_ok=True)
    for k, p in enumerate(b['pages'], 1):
        pix = d[p - 1].get_pixmap(dpi=110); pg = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        full = pg.copy(); full.thumbnail((1200, 1600)); full.save(f"assets/samples/{b['slug']}/{k}.jpg", quality=85)
        th = pg.copy(); th.thumbnail((400, 520)); th.save(f"assets/samples/{b['slug']}/{k}-thumb.jpg", quality=80)
    open(f"books/{b['slug']}.html", 'w', encoding='utf-8').write(page_from(b))
    data = [x for x in data if x['slug'] != b['slug']]
    data.append({"slug": b['slug'], "asin": b['asin'], "title": f"{b['title']}: {b['sub']}", "short": b['title'], "cover": f"{b['slug']}.jpg",
                 "shelf": "seniors", "shelf_name": "Care & Comfort for Seniors", "tagline": b['tag'], "who": b['who'], "facts": b['facts'],
                 "samples": 7, "description": b['about'], "related": ["seniors"], "buy": b['buy']})
    print('built', b['slug'])
json.dump(data, open('books.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
