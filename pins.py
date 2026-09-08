"""Regenerate Pinterest pins for every book. Reads books.json + index.html (source of truth).
  python pins.py            -> D:/recordings/bookshop-pins/v2/pin-<slug>.png (1000x1500) + pins.md + pins.csv
"""
import json, re, os, html, csv
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SITE = 'D:/recordings/gentle-bookshop-site'
OUT = 'D:/recordings/bookshop-pins/v2'
BASE = 'https://ainjection.github.io/gentle-bookshop/books/'
os.makedirs(OUT, exist_ok=True)
books = json.load(open(f'{SITE}/books.json', encoding='utf-8'))
index = open(f'{SITE}/index.html', encoding='utf-8').read()
blurb = {}
for m in re.finditer(r'<div class="book">(.*?)</div>', index, re.S):
    c = m.group(1); a = re.search(r'/dp/([A-Z0-9]{10})', c); p = re.search(r'<p class="sans">(.*?)</p>', c, re.S)
    if a and p: blurb[a.group(1)] = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', p.group(1)))).strip()

F = 'C:/Windows/Fonts/'
def font(name, size):
    for f in (name, 'segoeuib.ttf'):
        try: return ImageFont.truetype(F + f, size)
        except Exception: pass
    return ImageFont.load_default()

def dominant(im):
    small = im.convert('RGB').resize((60, 90))
    best, score = (200, 150, 100), -1
    for r, g, b in small.getdata():
        mx, mn = max(r, g, b), min(r, g, b); sat = (mx - mn) / (mx + 1); lum = (r + g + b) / 3
        s = sat * (1 - abs(lum - 140) / 200)
        if s > score: score, best = s, (r, g, b)
    return best

def mix(c, w, t): return tuple(int(a * (1 - t) + b * t) for a, b in zip(c, w))

def wrap(dr, text, fnt, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if dr.textlength(t, font=fnt) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

rows = []
for b in books:
    cover = Image.open(f'{SITE}/assets/{b["cover"]}').convert('RGB')
    col = dominant(cover)
    W, H = 1000, 1500
    bg = Image.new('RGB', (W, H))
    top, bot = mix(col, (255, 255, 255), 0.82), mix(col, (255, 255, 255), 0.62)
    px = bg.load()
    for y in range(H):
        c = mix(top, bot, y / H)
        for x in range(W): px[x, y] = c
    ink = mix(col, (0, 0, 0), 0.62)
    dr = ImageDraw.Draw(bg)
    # category pill
    pf = font('segoeuib.ttf', 30); label = b['shelf_name'].upper().replace('&AMP;', '&')
    tw = dr.textlength(label, font=pf); x0 = (W - tw) / 2 - 28
    dr.rounded_rectangle((x0, 62, x0 + tw + 56, 126), radius=32, outline=ink, width=3)
    dr.text(((W - tw) / 2, 76), label, font=pf, fill=ink)
    # cover with shadow
    cw = 640; ch = int(cover.height * cw / cover.width); ch = min(ch, 760); cv = cover.resize((cw, ch))
    cx, cy = (W - cw) // 2, 190
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((cx + 10, cy + 22, cx + cw + 10, cy + ch + 22), fill=(0, 0, 0, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(22)); bg.paste(sh, (0, 0), sh); bg.paste(cv, (cx, cy))
    # hook
    hook = blurb.get(b['asin']) or b['tagline']
    hf = font('segoeprb.ttf', 64); lines = wrap(dr, hook, hf, 860)
    if len(lines) > 3: hf = font('segoeprb.ttf', 52); lines = wrap(dr, hook, hf, 880)
    y = cy + ch + 70
    for ln in lines:
        dr.text(((W - dr.textlength(ln, font=hf)) / 2, y), ln, font=hf, fill=ink); y += int(hf.size * 1.25)
    # footer
    dr.line((430, H - 150, 570, H - 150), fill=ink, width=4)
    ff = font('segoeprb.ttf', 36); t = 'The Gentle Bookshop'
    dr.text(((W - dr.textlength(t, font=ff)) / 2, H - 120), t, font=ff, fill=ink)
    bg.save(f'{OUT}/pin-{b["slug"]}.png', optimize=True)
    rows.append((b['slug'], b['short'], hook + ' ' + b['tagline'] + ' Look inside every page on our site, then get it on Amazon.', BASE + b['slug'] + '.html', b['shelf_name']))
    print('pin', b['slug'])

with open(f'{OUT}/pins.md', 'w', encoding='utf-8') as f:
    f.write('# Pinterest pins, one per book (paste title, description, link)\n\n')
    for slug, title, desc, link, board in rows:
        f.write(f'## pin-{slug}.png\nBoard: {board}\nTitle: {title}\nDescription: {desc}\nLink: {link}\n\n')
with open(f'{OUT}/pins.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f); w.writerow(['Title', 'Media URL', 'Pinterest board', 'Thumbnail', 'Description', 'Link', 'Publish date', 'Keywords'])
    for slug, title, desc, link, board in rows:
        w.writerow([title, f'https://ainjection.github.io/gentle-bookshop/pins/pin-{slug}.png', board, '', desc, link, '', ''])
print(len(rows), 'pins')
