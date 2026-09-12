"""Build the three Curious Kids book pages from the Gross page template and add a Curious Kids shelf to index.html."""
import re, html as H
T = open('books/gross-book-of-why.html', encoding='utf-8').read()

BOOKS = [
    dict(slug='big-book-of-why', title="The Curious Kid's Big Book of Why", sub="300 Mind-Blowing Answers to the Why Questions Kids Really Ask, Ages 6-12",
         tag="Why is the sky blue? Why does popcorn pop? Why do we dream? 300 real answers, every one checked twice.",
         facts=["224 pages", "7 x 10 in", "Ages 6 to 12", "300 questions, 310 drawings", "Paperback, $14.99. Also on Kindle"],
         asin="B0HJDYLGG1", meta="Why is the sky blue? Why does popcorn pop? Why do we dream? 300 real answers for kids aged 6 to 12, checked twice.",
         about=["The Curious Kid's Big Book of Why answers 300 questions across ten journeys: space, animals, the human body, everyday science, the oceans, dinosaurs, weather and the restless Earth, food and cooking, the mind and the senses, and machines. Every question has its own drawing.",
                "Each answer is about a hundred words: long enough to explain properly, short enough to read aloud in under a minute. Open it anywhere. No order, no homework, no tests.",
                "What makes this one different is that the answers are checked. Each one was written against published sources from museums, universities, national science agencies and peer-reviewed journals, then checked a second time against those same sources. Where scientists genuinely do not agree yet, the book says so."],
         who="Children aged 6 to 12 who ask a hundred questions a day, and the grown-ups who would rather not say \"I don't know\" again. Bedtime, the car, the dinner table."),
    dict(slug='big-book-of-why-curious-kids', title="The Big Book of Why for Curious Kids", sub="Over 1,000 Facts, 100 Big Questions, Every Answer Explained and Illustrated",
         tag="Why do cats purr? Why is the sea salty? Why can't you tickle yourself? 100 big questions, one full-colour illustrated page each.",
         facts=["108 pages, full colour", "8.5 x 11 in", "Ages 6 to 12", "100 questions, over 1,000 facts", "Paperback and Kindle"],
         asin="B0HJMB7HJ5", meta="100 big questions, one full-colour illustrated page each, with a wow fact and a true-or-false quiz. Ages 6 to 12.",
         about=["The Big Book of Why for Curious Kids answers 100 of the best questions properly, in one full-colour page each, without talking down and without going on too long.",
                "Every page works the same way, so children always know where to look: one big illustration with labels, a clear answer in one short paragraph, three points that sum it up, a Wow Fact worth repeating at the dinner table, and a True or False quiz to test what they have just learned.",
                "Ten subjects: Animals. Space. Planet Earth. Weather and Nature. The Human Body. Science and How Things Work. Food and Everyday Life. History and Long Ago. Senses and Mind. Inventions and Machines."],
         who="Curious kids aged 6 to 12 who want to understand how the world works, not just memorise facts. Confident readers on their own, or reading together at bedtime."),
    dict(slug='big-book-of-what-if', title="The Big Book of What If? for Curious Kids", sub="100 Explorer Adventures, Over 1,000 Facts, Every Answer Explained and Illustrated",
         tag="What if your spacesuit sprang a leak on the Moon? What if a polar bear approached your camp? 100 explorer adventures, one illustrated page each.",
         facts=["108 pages, full colour", "8.5 x 11 in", "Ages 6 to 12", "100 adventures, over 1,000 facts", "Paperback and Kindle"],
         asin="B0HHXTWDJP", meta="100 explorer adventures answered properly, one full-colour page each, with a wow fact and a true-or-false quiz. Ages 6 to 12.",
         about=["Every child has wondered what it would be like to walk on the Moon, dive to the bottom of the sea or stand near a volcano. The Big Book of What If? takes 100 of those daydreams seriously and answers every one properly, in one full-colour page each.",
                "Every page has one big illustration with labels, a clear answer, three points that sum it up, a Wow Fact and a True or False quiz. It is a book about thinking like an explorer: noticing, planning, and knowing when to turn back.",
                "Ten expeditions: Space. Deep Ocean. Underground. Polar. Jungle. Desert. Mountain. Volcano. Wildlife. Science and Machines. Book 2 in the series, alongside The Big Book of Why for Curious Kids."],
         who="Curious kids aged 6 to 12 who love adventure and want to know how real explorers stay safe, find things out and get home."),
]
def esc(s): return H.escape(s, quote=True)
for b in BOOKS:
    s = T
    s = s.replace("The Curious Kid's Gross Book of Why: 150 Revolting Questions With Real Answers", f"{b['title']}: {b['sub']}")
    s = s.replace("The Curious Kid's Gross Book of Why", b['title'])
    s = s.replace('content="Why do we fart? Why is snot green? Why do dogs sniff each other\'s bottoms? Real answers, checked twice. Look inside 7 sample pages, then get it on Amazon."', f'content="{esc(b["meta"])} Look inside 7 sample pages, then get it on Amazon."')
    s = s.replace('content="Why do we fart? Why is snot green? Why do dogs sniff each other\'s bottoms? Real answers, checked twice."', f'content="{esc(b["meta"])}"')
    s = s.replace("Why do we fart? Why is snot green? Why do dogs sniff each other's bottoms? Real answers, checked twice.", b['tag'])
    s = s.replace("gross-book-of-why", b['slug'])
    s = s.replace("B0HHZTLVH3", b['asin'])
    s = re.sub(r'<ul class="facts sans">.*?</ul>', '<ul class="facts sans">' + ''.join(f'<li>{f}</li>' for f in b['facts']) + '</ul>', s, flags=re.S)
    s = re.sub(r'(<section class="desc">\s*<h2>About this book</h2>\s*).*?(</section>)', lambda m: m.group(1) + ''.join(f'    <p>{p}</p>\n' for p in b['about']) + m.group(2), s, flags=re.S)
    s = re.sub(r'<div class="who sans">.*?</div>', f'<div class="who sans">{b["who"]}</div>', s, flags=re.S)
    s = s.replace('<a href="../index.html#gifts">Birthday &amp; Gift Books</a>', '<a href="../index.html#curious">Curious Kids</a>')
    s = s.replace('<div class="kicker sans">Birthday &amp; Gift Books</div>', '<div class="kicker sans">Curious Kids</div>')
    # "More on this shelf": the other three curious books
    others = [o for o in BOOKS + [dict(slug='gross-book-of-why', title="The Curious Kid's Gross Book of Why")] if o['slug'] != b['slug']][:3]
    shelf = ''.join(f'    <a class="mini" href="{o["slug"]}.html"><img src="../assets/{o["slug"]}.jpg" alt="{esc(o["title"])} cover" loading="lazy" /><h3>{esc(o["title"])}</h3></a>\n' for o in others)
    s = re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + shelf + m.group(2), s, flags=re.S)
    open(f'books/{b["slug"]}.html', 'w', encoding='utf-8').write(s)
    print('wrote', b['slug'])
# Gross page: point its crumb/kicker/shelf at the Curious Kids shelf too
g = T.replace('<a href="../index.html#gifts">Birthday &amp; Gift Books</a>', '<a href="../index.html#curious">Curious Kids</a>').replace('<div class="kicker sans">Birthday &amp; Gift Books</div>', '<div class="kicker sans">Curious Kids</div>')
shelf = ''.join(f'    <a class="mini" href="{o["slug"]}.html"><img src="../assets/{o["slug"]}.jpg" alt="{esc(o["title"])} cover" loading="lazy" /><h3>{esc(o["title"])}</h3></a>\n' for o in BOOKS)
g = re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + shelf + m.group(2), g, flags=re.S)
open('books/gross-book-of-why.html', 'w', encoding='utf-8').write(g)

# index: new Curious Kids section before #gifts, and drop the Gross card from gifts
idx = open('index.html', encoding='utf-8').read()
card = lambda slug, title, blurb, asin, badge: f'''    <div class="book">
      {'<span class="badge sans">New release</span>' if badge else ''}
      <a class="cardlink" href="books/{slug}.html"><img src="assets/{slug}.jpg" alt="{esc(title)} cover" loading="lazy" /><h3>{esc(title)}</h3></a>
      <p class="sans">{blurb}</p>
      <a class="peek sans" href="books/{slug}.html">Look inside</a>
      <a class="buy sans" href="https://www.amazon.com/dp/{asin}">Get it on Amazon</a>
    </div>
'''
section = '''<section id="curious">
  <div class="kicker sans">Big questions, real answers</div>
  <h2>Curious Kids</h2>
  <p class="sect-sub sans">For the child who asks why a hundred times a day. Every answer checked, every page
     illustrated, and a quiz to see what stuck.</p>
  <div class="shelf">
''' + card('big-book-of-why-curious-kids', "The Big Book of Why for Curious Kids", "100 big questions, one full-colour illustrated page each, over 1,000 facts. Ages 6 to 12.", "B0HJMB7HJ5", True) \
    + card('big-book-of-what-if', "The Big Book of What If? for Curious Kids", "100 explorer adventures answered properly, in full colour. Book 2 of the series.", "B0HHXTWDJP", True) \
    + card('big-book-of-why', "The Curious Kid&rsquo;s Big Book of Why", "300 questions, 310 drawings, every answer checked twice. Ages 6 to 12. Also on Kindle.", "B0HJDYLGG1", False) \
    + card('gross-book-of-why', "The Curious Kid&rsquo;s Gross Book of Why", "150 revolting questions with real answers. For kids who ask why. Also on Kindle.", "B0HHZTLVH3", False) + '''  </div>
</section>

'''
gross_card = re.search(r'    <div class="book">\n      <span class="badge sans">New release</span>\n      <a class="cardlink" href="books/gross-book-of-why.html">.*?    </div>\n', idx, re.S).group(0)
idx = idx.replace(gross_card, '')
idx = idx.replace('<section id="gifts">', section + '<section id="gifts">')
open('index.html', 'w', encoding='utf-8').write(idx)
print('index updated', idx.count('id="curious"'))
