"""Add Dysgraphia Teens Volume 2 and Dysgraphia Cursive for Teens (both live 22 Nov 2026). Idempotent. Then python seo.py."""
import re, html as H, os, json
from PIL import Image
esc = lambda s: H.escape(s, quote=True)
T = re.sub(r'<!--seo-->.*?<!--/seo-->', '', open('books/dysgraphia-print-8-12.html', encoding='utf-8').read(), flags=re.S)   # seo.py rebuilds this block
OLD = json.load(open('books.json', encoding='utf-8'))
O = next(x for x in OLD if x['slug'] == 'dysgraphia-print-8-12')
WHO_TAIL = "Parents who want a clear plan to follow at home, and tutors, special education teachers and occupational therapists who need structured practice between sessions."
BOOKS = [dict(
    slug='dysgraphia-teens-vol2', asin='B0HSLMSYYF', src='D:/kdp-dysgraphia-teens-v2', short='Dysgraphia Workbook: Teens Volume 2',
    title='Dysgraphia Handwriting Workbook for Teens Volume 2',
    sub='Sentences to Paragraphs: An 8-Week Plan of 10-Minute Sessions for Ages 10-14, with Example Answers, Real-Life Writing Practice and a Parent Guide',
    tag='From one clear sentence to a full paragraph in eight weeks, ten minutes a day. For teens who already know their letters.',
    facts=['140 pages', '8.5 x 11 in', 'Ages 10 to 14', '8-week plan, 40 sessions', 'Example answers and a parent guide', 'Paperback, $11.99'],
    about=["Your teen can form the letters. The trouble starts when the letters have to become sentences, and the sentences have to fill a page that a teacher can read. Volume 2 picks up where a first handwriting workbook stops.",
           "Every day is two facing pages. On the first, the student traces a short fact, copies it, then adds one sentence of their own, with an example answer beside the lines. The second page changes each day: fix broken sentences, join short ones, plan a paragraph, do a piece of real-life writing, then write freely.",
           "The lines get smaller as control improves, from large guide lines in week 1 to college ruled in week 8. Inside: a tracker, before and after pages, a two-minute speed check every week, an answer key, a four-page guide for parents and tutors, twenty spare practice pages and a certificate."],
    who="Tweens and teens aged 10 to 14 with dysgraphia or messy handwriting who already know their letters. " + WHO_TAIL,
    pages=[10, 12, 13, 24, 29, 31, 43],
    related=[('dysgraphia-teens', 'Dysgraphia Workbook: Teens'), ('dysgraphia-cursive-teens', 'Dysgraphia Cursive: Teens'), ('dysgraphia-highschool', 'Dysgraphia Workbook: High School')]),
  dict(
    slug='dysgraphia-cursive-teens', asin='B0HSLVS38H', src='D:/kdp-dysgraphia-cursive-teens', short='Dysgraphia Cursive: Teens',
    title='Dysgraphia Cursive Handwriting Workbook for Teens',
    sub='First Letter to Full Page: An 8-Week Plan of 10-Minute Sessions for Ages 10-14, with Signature Practice, Reading Cursive and a Parent Guide',
    tag='From a first joined letter to a full page of cursive in eight weeks, ten minutes a day. No cursive needed to start.',
    facts=['126 pages', '8.5 x 11 in', 'Ages 10 to 14', '8-week plan, 40 sessions', 'All 26 letters, small and capital', 'Paperback, $11.99'],
    about=["Most cursive workbooks for teens open with fifty pages of single letters on lines made for a seven-year-old. This one takes a student aged 10 to 14 from a first joined letter to a full college ruled page in eight weeks.",
           "Letters are taught in groups that share a movement, not in alphabet order: a black model to follow, gray letters to trace and empty rows to write on. Every word in the first three weeks uses only letters already taught, and real words arrive on day two.",
           "Inside: all 26 small letters, the four high joins that cause the most trouble, all 26 capitals, practice at reading cursive, a signature page, cards, an envelope, class notes, a weekly two-minute speed check, a three-page guide for parents and tutors and a certificate."],
    who="Tweens and teens aged 10 to 14 with dysgraphia or messy handwriting who were never taught cursive, or were taught it too fast. " + WHO_TAIL,
    pages=[8, 10, 12, 13, 28, 29, 42],
    related=[('dysgraphia-teens-vol2', 'Dysgraphia Workbook: Teens Volume 2'), ('dysgraphia-teens', 'Dysgraphia Workbook: Teens'), ('dysgraphia-cursive', 'Dysgraphia Workbook: Cursive')])]

idx = open('index.html', encoding='utf-8').read()
data = OLD
for b in BOOKS:
    s = T.replace(O['title'], f"{b['title']}: {b['sub']}").replace(O['title'].split(':')[0], b['title'])
    s = s.replace(esc(O['tagline']), esc(b['tag'])).replace(O['tagline'], b['tag'])
    s = s.replace('dysgraphia-print-8-12', b['slug']).replace('B0HPMLLRM7', b['asin'])
    s = re.sub(r'<ul class="facts sans">.*?</ul>', '<ul class="facts sans">' + ''.join(f'<li>{f}</li>' for f in b['facts']) + '</ul>', s, flags=re.S)
    s = re.sub(r'(<section class="desc">\s*<h2>About this book</h2>\s*).*?(</section>)', lambda m: m.group(1) + ''.join(f'    <p>{p}</p>\n' for p in b['about']) + m.group(2), s, flags=re.S)
    s = re.sub(r'<div class="who sans">.*?</div>', f'<div class="who sans">{b["who"]}</div>', s, flags=re.S)
    shelf = ''.join(f'    <a class="mini" href="{sl}.html"><img src="../assets/{sl}.jpg" alt="{esc(t)} cover" loading="lazy" /><h3>{esc(t)}</h3></a>\n' for sl, t in b['related'])
    s = re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + shelf + m.group(2), s, flags=re.S)
    for bad in ('Older Kids', '8-12', '8 to 12', '174', '81 ', '12.99', 'Shaded'):
        assert bad not in s, ('template leftover', bad, b['slug'], s[max(0, s.find(bad) - 80):s.find(bad) + 80])
    im = Image.open(b['src'] + '/front-cover.jpg').convert('RGB'); im.thumbnail((900, 1200)); im.save(f"assets/{b['slug']}.jpg", quality=88)
    os.makedirs(f"assets/samples/{b['slug']}", exist_ok=True)
    for k, p in enumerate(b['pages'], 1):
        pg = Image.open(f"{b['src']}/pages/p{p:03d}.png").convert('RGB')
        full = pg.copy(); full.thumbnail((1200, 1600)); full.save(f"assets/samples/{b['slug']}/{k}.jpg", quality=85)
        th = pg.copy(); th.thumbnail((400, 520)); th.save(f"assets/samples/{b['slug']}/{k}-thumb.jpg", quality=80)
    open(f"books/{b['slug']}.html", 'w', encoding='utf-8').write(s)
    data = [x for x in data if x['slug'] != b['slug']]
    data.append({"slug": b['slug'], "asin": b['asin'], "title": f"{b['title']}: {b['sub']}", "short": b['short'], "cover": b['slug'] + '.jpg',
                 "shelf": "dysgraphia", "shelf_name": "Dysgraphia Workbooks", "tagline": b['tag'], "who": b['who'], "facts": b['facts'],
                 "samples": 7, "description": b['about'], "related": ["dysgraphia"]})
    entry = json.dumps({b['slug']: {"asin": b['asin'], "url": f"https://www.amazon.com/dp/{b['asin']}", "short": b['short'] + " (new)", "cover": b['slug'] + '.jpg'}})[1:-1]
    idx = re.sub(r', "' + b['slug'] + r'": \{[^}]*\}', '', idx)
    idx = idx.replace('}};</script>', '}, ' + entry + '};</script>', 1)
    if f'"{b["slug"]},' not in idx and f',{b["slug"]},' not in idx:
        idx = idx.replace('dysgraphia-print-8-12,dysgraphia-quill-kids,', f'{b["slug"]},dysgraphia-print-8-12,dysgraphia-quill-kids,', 1)
    print('added', b['slug'], '| homepage mentions:', idx.count(b['slug']))
json.dump(data, open('books.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
open('index.html', 'w', encoding='utf-8').write(idx)
