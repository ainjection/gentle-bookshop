"""Add Google-facing data to every book page: canonical URL + schema.org Book JSON-LD.
Reads each finished page (og tags, Amazon link, price, pages, ages), so it works however the page was built.
Re-run after any rebuild:  python seo.py   (idempotent: replaces its own block)."""
import glob, html, json, re

BASE = 'https://ainjection.github.io/gentle-bookshop/'
START, END = '<!--seo-->', '<!--/seo-->'

def meta(page, prop):
    m = re.search(r'<meta (?:property|name)="%s" content="([^"]*)"' % re.escape(prop), page)
    return html.unescape(m.group(1)) if m else None

def book_ld(page, url):
    h1 = re.search(r'<h1>(.*?)</h1>', page, re.S)
    name = html.unescape(re.sub('<[^>]+>', '', h1.group(1))).strip() if h1 else meta(page, 'og:title')
    ld = {'@context': 'https://schema.org', '@type': 'Book', 'name': name, 'url': url,
          'image': meta(page, 'og:image'), 'description': meta(page, 'description'),
          'author': {'@type': 'Organization', 'name': 'The Gentle Bookshop'},
          'publisher': {'@type': 'Organization', 'name': 'The Gentle Bookshop'},
          'bookFormat': 'https://schema.org/Paperback', 'inLanguage': 'en'}
    facts = ' '.join(re.findall(r'<li>([^<]*)</li>', page))
    if (m := re.search(r'(\d+)\s*pages', facts)): ld['numberOfPages'] = int(m.group(1))
    if (m := re.search(r'[Aa]ges? (\d+)', facts)): ld['typicalAgeRange'] = m.group(1) + '-'
    amz = re.search(r'https://www\.amazon\.com/dp/[A-Z0-9]{10}', page)
    price = re.search(r'\$(\d+\.\d\d)', facts)
    if amz and price:
        ld['offers'] = {'@type': 'Offer', 'url': amz.group(0), 'price': price.group(1), 'priceCurrency': 'USD',
                        'availability': 'https://schema.org/InStock', 'seller': {'@type': 'Organization', 'name': 'Amazon'}}
    return {k: v for k, v in ld.items() if v}

def inject(path, url, ld=None):
    page = open(path, encoding='utf-8').read()
    page = re.sub(re.escape(START) + '.*?' + re.escape(END) + '\n?', '', page, flags=re.S)
    block = f'{START}<link rel="canonical" href="{url}" />'
    if ld: block += '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'
    page = page.replace('</head>', block + END + '\n</head>', 1)
    open(path, 'w', encoding='utf-8').write(page)
    return ld

n = 0
for path in sorted(glob.glob('books/*.html')):
    url = BASE + path.replace('\\', '/')
    page = open(path, encoding='utf-8').read()
    ld = inject(path, url, book_ld(page, url)); n += 1
    assert ld['name'] and ld['image'], path
inject('index.html', BASE)
print(n, 'book pages + index tagged')

if __name__ == '__main__':
    # self-check: every page has exactly one block and valid JSON
    for path in glob.glob('books/*.html'):
        p = open(path, encoding='utf-8').read()
        assert p.count(START) == 1, path
        json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', p).group(1))
    print('self-check ok')
