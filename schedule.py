"""Draft a posting schedule from the video inventory. Nothing is posted; this writes a table for Rob to approve.
  python schedule.py 2026-09-09 7      -> D:/gentle-shorts-media/SCHEDULE-<start>.md + schedule-<start>.json
Rules: 5 fresh videos a day, same video to YouTube + TikTok + Pinterest (video pin), plus 1 image pin a day.
Slots 08:00 11:00 14:00 17:00 19:30 (22:00 = image pin). Halloween titles front-loaded until 31 Oct, Christmas from 12 Oct.
"""
import json, os, sys, glob, datetime as dt

SITE = 'D:/recordings/gentle-bookshop-site'
SHORTS = 'D:/gentle-shorts-media'
CAPY = 'D:/recordings/coloring-factory/out'
BASE = 'https://ainjection.github.io/gentle-bookshop/books/'
BOARD = {'coloring': 'Coloring Books', 'grayscale': 'Coloring Books', 'learning': 'Handwriting & Learning', 'stories': 'Kids Bedtime Stories',
         'seekfind': 'Seek & Find', 'seniors': 'amazon kdp', 'gifts': 'amazon kdp'}
SLOTS = ['08:00', '11:00', '14:00', '17:00', '19:30']
TAGS = {'coloring': '#coloringbook #boldandeasy #coloringasmr #kidsactivities #amazonfinds',
        'grayscale': '#grayscalecoloring #adultcoloring #coloringbook #coloredpencils #halloween',
        'learning': '#dysgraphia #handwriting #lefthanded #homeschool #occupationaltherapy',
        'stories': '#bedtimestory #kidsbooks #picturebook #readaloud #childrensbooks',
        'seekfind': '#seekandfind #hiddenpictures #kidsactivities #activitybook #screenfree',
        'seniors': '#wordsearch #largeprint #seniors #dementia #puzzlebook',
        'gifts': '#birthdaygift #bornin #nostalgia #giftideas #trivia'}

books = {b['slug']: b for b in json.load(open(f'{SITE}/books.json', encoding='utf-8'))}
scripts = json.load(open(f'{SITE}/shorts-scripts.json', encoding='utf-8'))
start = dt.date.fromisoformat(sys.argv[1]); days = int(sys.argv[2])

def priority(slug):
    b = books[slug]; s = 0
    if 'halloween' in slug: s -= 100
    if slug in ('dysgraphia-kids', 'dysgraphia-teens', 'left-handed-handwriting', 'puzzles'): s -= 50
    if 'christmas' in slug: s += 40 if start < dt.date(2026, 10, 12) else -60
    return s

flips = [s for s in books if os.path.exists(f'{SHORTS}/{s}/{s}.mp4')]
flips.sort(key=priority)
capy = sorted(glob.glob(f'{CAPY}/SHORT_page*.mp4'))
rows = []; fi = ci = 0
for d in range(days):
    day = start + dt.timedelta(days=d)
    for k, slot in enumerate(SLOTS):
        use_flip = (k % 5 != 2) and fi < len(flips)   # 4 flip-throughs + 1 capybara colouring short per day
        if use_flip:
            slug = flips[fi]; fi += 1; b = books[slug]; sc = scripts[slug]
            title = f'{b["short"]} | {sc["hook"]} | Look inside'[:100]
            desc = f'{sc["hook"]} {b["tagline"]}\nLook inside every page: {BASE}{slug}.html\n{b["who"]}\nMore gentle books: https://ainjection.github.io/gentle-bookshop/\n{TAGS[b["shelf"]]}'
            rows.append(dict(date=str(day), slot=slot, video=f'{SHORTS}/{slug}/{slug}.mp4', book=b['short'], link=BASE + slug + '.html', board=BOARD[b['shelf']], title=title, caption=desc, channels='YouTube, TikTok, Pinterest video'))
        else:
            if ci >= len(capy): continue
            v = capy[ci]; ci += 1; n = int(os.path.basename(v)[10:12]); b = books['capybara']
            title = f'Capybara Coloring ASMR | Bold & Easy page {n} | so satisfying'
            desc = f'Colouring page {n} from Capybara Bold & Easy. Thick lines, big shapes, zero stress.\nLook inside the book: {BASE}capybara.html\n{TAGS["coloring"]}'
            rows.append(dict(date=str(day), slot=slot, video=v, book='Capybara Bold & Easy (colouring page %d)' % n, link=BASE + 'capybara.html', board='Coloring Books', title=title, caption=desc, channels='YouTube, TikTok, Pinterest video'))
    # 22:00 image pin
    pin_slug = flips[(d * 3) % len(flips)] if flips else 'capybara'
    rows.append(dict(date=str(day), slot='22:00', video=f'D:/recordings/bookshop-pins/v2/pin-{pin_slug}.png', book=books[pin_slug]['short'], link=BASE + pin_slug + '.html', board=BOARD[books[pin_slug]['shelf']], title=books[pin_slug]['short'], caption=scripts[pin_slug]['hook'] + ' ' + books[pin_slug]['tagline'], channels='Pinterest image pin'))

json.dump(rows, open(f'{SHORTS}/schedule-{start}.json', 'w', encoding='utf-8'), indent=1)
with open(f'{SHORTS}/SCHEDULE-{start}.md', 'w', encoding='utf-8') as f:
    f.write(f'# Posting schedule draft, {start} for {days} days ({len(rows)} slots). NOTHING IS POSTED until Rob says yes.\n\n')
    cur = None
    for r in rows:
        if r['date'] != cur: cur = r['date']; f.write(f'\n## {cur}\n')
        f.write(f'- {r["slot"]}  {r["channels"]}  |  {r["book"]}\n    Title: {r["title"]}\n    Link: {r["link"]}  Board: {r["board"]}\n')
print(len(rows), 'slots;', fi, 'flip-throughs used of', len(flips), ';', ci, 'capybara shorts used of', len(capy))
