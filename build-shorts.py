"""Flip-through Shorts for every book, from the same data the website uses.
  python build-shorts.py <slug> [<slug> ...]    or    python build-shorts.py all
Output: D:/gentle-shorts-media/<slug>/<slug>.mp4 (1080x1920, ~20-25s) + verify frames.
Pipeline per book: cover + sample pages (assets/samples/<slug>) -> Kokoro VO (bf_emma) -> whisper word captions
-> generated music bed (D:/music-generated, safe) -> HyperFrames comp -> render -> ffprobe + frame check.
"""
import os, sys, json, subprocess, shutil, html as H, wave, contextlib, time
from PIL import Image

SITE = 'D:/recordings/gentle-bookshop-site'
OUT = 'D:/gentle-shorts-media'
MUSIC = {'soft': 'D:/music-generated/vidiq-lullaby-musicbox-117s.mp3', 'calm': 'D:/music-generated/vidiq-ambient-piano-strings-118s.mp3'}
SOFT_SHELVES = {'coloring', 'stories', 'seekfind'}
SITE_URL = 'ainjection.github.io/gentle-bookshop'

books = {b['slug']: b for b in json.load(open(f'{SITE}/books.json', encoding='utf-8'))}
scripts = json.load(open(f'{SITE}/shorts-scripts.json', encoding='utf-8'))

def dominant(im):
    """Most common hue among saturated mid-tone pixels, returned as the average RGB of that hue bucket."""
    small = im.convert('RGB').resize((80, 120)); hsv = small.convert('HSV')
    buckets = {}
    for (r, g, b), (h, s, v) in zip(small.getdata(), hsv.getdata()):
        if s < 90 or v < 60 or v > 235: continue
        k = h // 21
        acc = buckets.setdefault(k, [0, 0, 0, 0]); acc[0] += r; acc[1] += g; acc[2] += b; acc[3] += 1
    if not buckets: return (60, 90, 100)
    acc = max(buckets.values(), key=lambda a: a[3])
    return (acc[0] // acc[3], acc[1] // acc[3], acc[2] // acc[3])
def hexmix(c, t, w=(0, 0, 0)): return '#%02x%02x%02x' % tuple(int(a * (1 - t) + b * t) for a, b in zip(c, w))
def log(*a): print(time.strftime('[%H:%M:%S]'), *a, flush=True)

def build(slug):
    b = books[slug]; sc = scripts[slug]
    proj = f'{OUT}/{slug}'; os.makedirs(proj, exist_ok=True); os.chdir(proj)
    cover = Image.open(f'{SITE}/assets/{b["cover"]}').convert('RGB'); cover.save('cover.jpg', quality=90)
    col = dominant(cover); bg = hexmix(col, 0.58); glow = hexmix(col, 0.28)
    pages = []
    for k in range(1, b['samples'] + 1):
        src = f'{SITE}/assets/samples/{slug}/{k}.jpg'; dst = f'pg{k:02d}.jpg'
        im = Image.open(src); im.thumbnail((1000, 1300)); im.save(dst, quality=88); pages.append(dst)
    # VO
    open('script.txt', 'w', encoding='utf-8').write(sc['vo'])
    if not os.path.exists('vo.wav'):
        r = subprocess.run('hyperframes tts script.txt --voice bf_emma --speed 1.04 -o vo.wav', shell=True, capture_output=True, text=True)
        if not os.path.exists('vo.wav'): raise RuntimeError('tts failed: ' + r.stderr[-300:])
    with contextlib.closing(wave.open('vo.wav')) as wf: vo_dur = wf.getnframes() / wf.getframerate()
    # captions
    if os.path.exists('words.json'): groups = json.load(open('words.json'))
    else:
        from faster_whisper import WhisperModel
        segs, _ = WhisperModel('small.en', compute_type='int8').transcribe('vo.wav', word_timestamps=True)
        words = [{'w': w.word.strip(), 's': round(w.start, 3), 'e': round(w.end, 3)} for s in segs for w in s.words]
        groups, cur = [], []
        for x in words:
            cur.append(x)
            if len(cur) == 3 or x['w'].endswith(('.', ',', '?')):
                groups.append({'text': ' '.join(t['w'] for t in cur), 'start': cur[0]['s'], 'end': cur[-1]['e']}); cur = []
        if cur: groups.append({'text': ' '.join(t['w'] for t in cur), 'start': cur[0]['s'], 'end': cur[-1]['e']})
        for i in range(len(groups) - 1): groups[i]['end'] = min(groups[i + 1]['start'], groups[i]['end'] + 0.6)
        json.dump(groups, open('words.json', 'w'))
    total = round(vo_dur + 0.5 + 3.5, 2)
    # music (generated, safe): trim + fade
    mus = MUSIC['soft' if b['shelf'] in SOFT_SHELVES else 'calm']
    subprocess.run(f'ffmpeg -y -v error -i "{mus}" -t {total} -af "afade=t=in:d=1,afade=t=out:st={total - 2.5}:d=2.5" -c:a libmp3lame -q:a 3 music.mp3', shell=True, check=True)
    # timeline
    cover_end = 3.0; end_hold = 3.5; n = len(pages)
    win = total - cover_end - end_hold; dur = round(win / n, 3)
    clips, tweens = [], []
    for i, p in enumerate(pages):
        t = round(cover_end + i * dur, 3); d = round(dur + 0.05, 3)
        drift = 26 if i % 2 == 0 else -26
        clips.append(f'<div class="pagewrap clip" id="pw{i}" data-start="{t}" data-duration="{d}" data-track-index="0"><img class="pageimg" src="{p}"/></div>')
        tweens.append(f'tl.fromTo("#pw{i} .pageimg",{{x:1100,rotation:7}},{{x:0,rotation:0,duration:0.42,ease:"power3.out"}},{t});')
        tweens.append(f'tl.fromTo("#pw{i} .pageimg",{{y:{drift}}},{{y:{-drift},duration:{d},ease:"none"}},{t});')
    end_start = round(cover_end + n * dur, 3); end_dur = round(total - end_start, 3)
    caps, ctw = [], []
    for i, g in enumerate(groups):
        s = round(g['start'] + 0.5, 3); e = round(g['end'] + 0.5, 3)
        caps.append(f'<div class="capline" id="cg{i}">{H.escape(g["text"])}</div>')
        ctw.append(f'tl.fromTo("#cg{i}",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.14}},{s});tl.set("#cg{i}",{{opacity:0}},{e});')
    hook = H.escape(sc['hook']); short = H.escape(b['short'])
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
 body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:{bg};font-family:"Segoe UI",system-ui,sans-serif}}
 .scenebg{{position:absolute;inset:0;background:radial-gradient(ellipse 1000px 1400px at 50% 38%,{glow} 0%,rgba(0,0,0,0) 72%)}}
 .grain{{position:absolute;inset:0;opacity:.07;background-image:repeating-linear-gradient(0deg,#fff 0 1px,transparent 1px 3px)}}
 .pagewrap{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding-bottom:120px}}
 .pageimg{{max-width:940px;max-height:1240px;border:14px solid #fff;border-radius:8px;box-shadow:0 34px 90px rgba(0,0,0,.55)}}
 #coverwrap,#endwrap{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:44px}}
 #coverwrap img,#endwrap img{{max-width:820px;max-height:1060px;border-radius:14px;box-shadow:0 34px 100px rgba(0,0,0,.6)}}
 .toptag{{font-weight:800;font-size:66px;line-height:1.15;color:#fff;text-align:center;text-shadow:0 4px 18px rgba(0,0,0,.6);padding:0 60px}}
 .capline{{position:absolute;bottom:250px;left:50px;right:50px;text-align:center;font-weight:800;font-size:64px;line-height:1.2;color:#fff;
   text-shadow:0 4px 18px rgba(0,0,0,.85);-webkit-text-stroke:2px rgba(20,16,10,.9);paint-order:stroke fill;opacity:0;z-index:30}}
 .brand{{position:absolute;top:70px;left:0;right:0;text-align:center;font-weight:700;font-size:34px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.82)}}
 #endtag{{font-weight:800;font-size:60px;color:#ffd98a;text-align:center;text-shadow:0 4px 16px rgba(0,0,0,.6)}}
 #endurl{{font-size:38px;color:#fff;opacity:.9;margin-top:-20px}}
</style></head><body>
<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-start="0" data-duration="{total}">
 <div class="scenebg"></div><div class="grain"></div>
 <div class="brand">The Gentle Bookshop</div>
 <audio id="vo" data-start="0.5" data-duration="{round(vo_dur, 2)}" data-track-index="6" src="vo.wav" data-volume="1"></audio>
 <audio id="music" data-start="0" data-duration="{total}" data-track-index="7" src="music.mp3" data-volume="0.5"></audio>
 <div id="coverwrap" class="clip" data-start="0" data-duration="{cover_end}" data-track-index="0"><div class="toptag" id="ct">{hook}</div><img src="cover.jpg"/></div>
 {''.join(clips)}
 <div id="endwrap" class="clip" data-start="{end_start}" data-duration="{end_dur}" data-track-index="0"><img src="cover.jpg"/><div id="endtag">Look inside. Link below.</div><div id="endurl">{SITE_URL}</div></div>
 {''.join(caps)}
</div>
<script>
window.__timelines=window.__timelines||{{}};var tl=gsap.timeline({{paused:true}});
tl.fromTo("#coverwrap img",{{scale:.9,opacity:0}},{{scale:1,opacity:1,duration:.6,ease:"power3.out"}},.1);
tl.fromTo("#ct",{{y:-40,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"power2.out"}},.3);
{''.join(tweens)}
tl.fromTo("#endwrap img",{{scale:.94,opacity:0}},{{scale:1,opacity:1,duration:.5,ease:"power2.out"}},{end_start});
tl.fromTo("#endtag",{{y:36,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"power3.out"}},{round(end_start + .25, 3)});
tl.fromTo("#endurl",{{opacity:0}},{{opacity:.9,duration:.4}},{round(end_start + .6, 3)});
{''.join(ctw)}
window.__timelines["main"]=tl;
</script></body></html>"""
    open('index.html', 'w', encoding='utf-8').write(page)
    out = f'{proj}/{slug}.mp4'
    if os.path.exists(out): os.remove(out)
    r = subprocess.run(f'hyperframes render "{proj}" -o "{out}" --fps 30 --quality high --quiet', shell=True, capture_output=True, text=True)
    if not os.path.exists(out): raise RuntimeError('render failed: ' + (r.stderr or r.stdout)[-400:])
    pr = subprocess.run(f'ffprobe -v error -show_entries format=duration:stream=width,height -of csv=p=0 "{out}"', shell=True, capture_output=True, text=True).stdout.replace('\n', ' ')
    for k, t in enumerate((1.0, cover_end + 0.8, total / 2, total - 1.5)):
        subprocess.run(f'ffmpeg -v error -y -ss {t} -i "{out}" -frames:v 1 -vf "scale=360:-1,format=yuvj420p" _f{k}.jpg', shell=True)
    sheet = Image.new('RGB', (4 * 360, 640), 'black')
    for k in range(4):
        if os.path.exists(f'_f{k}.jpg'): sheet.paste(Image.open(f'_f{k}.jpg'), (k * 360, 0))
    sheet.save('_verify.jpg', quality=80)
    log(slug, 'DONE', pr, f'vo={vo_dur:.1f}s total={total}s pages={n}')

if __name__ == '__main__':
    todo = list(books) if sys.argv[1] == 'all' else sys.argv[1:]
    for s in todo:
        if s not in scripts: log(s, 'NO SCRIPT'); continue
        try: build(s)
        except Exception as e: log(s, 'FAILED', e)
