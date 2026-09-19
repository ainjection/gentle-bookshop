"""Add The Big Book of Why for Little Ones (B0HKBW1Q8G) to the Curious Kids shelf, built
from the same template as the other Curious Kids pages, and fix the What If buy link
(it pointed at the Kindle series page B0HHXTWDJP, not the paperback B0HJND6SVK)."""
import re, html as H
esc = lambda s: H.escape(s, quote=True)
T = open('books/gross-book-of-why.html', encoding='utf-8').read()
b = dict(slug='big-book-of-why-little-ones', title="The Big Book of Why for Little Ones",
         sub="1,000 Questions and Answers for Curious Toddlers, A Fully Illustrated First Encyclopedia of Why, Ages 2 to 5",
         tag="Why do fingers go wrinkly in the bath? Why can't we see the wind? Why does toast smell so good? 1,000 questions, a picture for every one.",
         facts=["184 pages, full colour", "8.5 x 11 in", "Ages 2 to 5", "1,000 questions, ten chapters", "Paperback and Kindle"],
         asin="B0HKBW1Q8G",
         meta="1,000 questions and answers for two to five year olds, a colourful picture for every one and short explanations to read aloud.",
         about=["If you live with a two to five year old, you know how quickly one question turns into another. The Big Book of Why for Little Ones brings together 1,000 of them, with a colourful illustration for every question and short explanations written for grown-ups to read aloud.",
                "Ten chapters of 100 questions each: My Amazing Body, Pets and Farm, Wild Animals, Bugs and Little Creatures, Sky and Weather, Space, Plants and the Garden, Food and Kitchen, Things That Go, and Home, Bedtime and Me. Most pages carry six illustrated answers.",
                "There is no right order and no need to finish a page. Open anywhere, follow their curiosity, and turn the hundredth why of the day into time spent reading and pointing together."],
         who="Toddlers and pre-schoolers aged 2 to 5 who ask why about everything, and the parents and grandparents reading with them. Book 3 of the Curious Kids series, for the youngest askers.")
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
others = [('big-book-of-why-curious-kids', "The Big Book of Why for Curious Kids"), ('big-book-of-what-if', "The Big Book of What If? for Curious Kids"), ('big-book-of-why', "The Curious Kid's Big Book of Why")]
shelf = ''.join(f'    <a class="mini" href="{sl}.html"><img src="../assets/{sl}.jpg" alt="{esc(t)} cover" loading="lazy" /><h3>{esc(t)}</h3></a>\n' for sl, t in others)
s = re.sub(r'(<div class="shelf sans">\n).*?(  </div>\n</section>)', lambda m: m.group(1) + shelf + m.group(2), s, flags=re.S)
open(f'books/{b["slug"]}.html', 'w', encoding='utf-8').write(s)
print('wrote', b['slug'], '| asin count', s.count(b['asin']), '| gross leftovers', s.count('Gross'))

idx = open('index.html', encoding='utf-8').read()
card = f'''    <div class="book">
      <span class="badge sans">New release</span>
      <a class="cardlink" href="books/{b['slug']}.html"><img src="assets/{b['slug']}.jpg" alt="{esc(b['title'])} cover" loading="lazy" /><h3>{esc(b['title'])}</h3></a>
      <p class="sans">1,000 questions and answers for two to five year olds, a picture for every one. Book 3 of the series.</p>
      <a class="peek sans" href="books/{b['slug']}.html">Look inside</a>
      <a class="buy sans" href="https://www.amazon.com/dp/{b['asin']}">Get it on Amazon</a>
    </div>
'''
assert idx.count('id="curious"') == 1 and b['asin'] not in idx
i = idx.index('<section id="curious">'); j = idx.index('<div class="shelf">', i) + len('<div class="shelf">\n')
idx = idx[:j] + card + idx[j:]
n = idx.count('https://www.amazon.com/dp/B0HHXTWDJP'); idx = idx.replace('https://www.amazon.com/dp/B0HHXTWDJP', 'https://www.amazon.com/dp/B0HJND6SVK')
open('index.html', 'w', encoding='utf-8').write(idx)
w = open('books/big-book-of-what-if.html', encoding='utf-8').read(); m = w.count('B0HHXTWDJP')
open('books/big-book-of-what-if.html', 'w', encoding='utf-8').write(w.replace('B0HHXTWDJP', 'B0HJND6SVK'))
print('index: little ones card added; What If link fixed on index x', n, 'and on its page x', m)
