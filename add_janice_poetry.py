"""Link the Janice Kingsley author site from the main shop (Rob 1 Oct 2026): nav link, a Poetry band before the seasonal shelf, footer link."""
p = 'index.html'; s = open(p, encoding='utf-8').read()
JK = 'https://ainjection.github.io/janice-kingsley/'
def rep(old, new):
    global s
    assert s.count(old) == 1, old[:60]; s = s.replace(old, new)
assert 'id="poetry"' not in s
rep('<a href="#golden">Golden years</a><a href="#season">Halloween</a>', '<a href="#golden">Golden years</a><a href="#poetry">Poetry</a><a href="#season">Halloween</a>')
css = '''.poetry{position:relative;padding:clamp(60px,8vw,100px) clamp(16px,4vw,48px);background:radial-gradient(60% 80% at 75% 45%,#f6dfe3 0%,#e3ebf5 45%,var(--cream) 80%)}
.poetry .pin{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}
.poetry h2{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;font-size:clamp(2.4rem,4.6vw,3.6rem);line-height:1.05;margin:.2em 0 .35em;color:#3b3540}
.poetry h2 em{font-style:italic;color:#a06a5e}
.poetry p{font-family:"Cormorant Garamond",Georgia,serif;font-size:1.35rem;line-height:1.45;color:#5a5258;max-width:520px;margin:0 0 26px}
.poetry .kicker{color:#a06a5e}
.poetry .cta{background:#3b3540}
.pfan{position:relative;height:380px}
.pfan img{position:absolute;width:40%;max-width:210px;border-radius:3px;box-shadow:0 18px 40px rgba(60,40,30,.25)}
@media (max-width:820px){.poetry .pin{grid-template-columns:1fr;text-align:center}.poetry p{margin-left:auto;margin-right:auto}.pfan{height:300px;max-width:420px;width:100%;margin:0 auto}}
'''
rep('</style>', css + '</style>') if s.count('</style>') == 1 else None
band = f'''<!-- ================= POETRY (Janice Kingsley) ================= -->
<section class="poetry" id="poetry" aria-label="Poetry by Janice Kingsley">
  <div class="pin">
    <div>
      <div class="kicker">For grown-ups</div>
      <h2>Gentle poems by <em>Janice Kingsley</em></h2>
      <p>Short, honest poems for grief, heartbreak and love, with soft watercolour paintings throughout. Read one at the kettle, or a chapter on a long night.</p>
      <a class="cta" href="{JK}?src=gentle-poetry">Visit Janice's poetry page</a>
    </div>
    <a class="pfan" href="{JK}?src=gentle-poetry-books" aria-label="Janice Kingsley's poetry books">
      <img src="{JK}assets/cover-where-you-are-now.jpg" alt="Where You Are Now cover" loading="lazy" style="left:6%;top:10%;transform:rotate(-8deg)">
      <img src="{JK}assets/cover-still-learning-to-leave.jpg" alt="Still Learning to Leave cover" loading="lazy" style="left:31%;top:4%;transform:rotate(3deg);z-index:2">
      <img src="{JK}assets/art-butterflies.jpg" alt="You Still Give Me Butterflies painting" loading="lazy" style="left:56%;top:26%;width:34%;transform:rotate(9deg)">
    </a>
  </div>
</section>

<!-- ================= SEASONAL: HALLOWEEN ================= -->'''
rep('<!-- ================= SEASONAL: HALLOWEEN ================= -->', band)
rep('<a href="https://ainjection.github.io/halloween-books/?src=gentle-footer">The Halloween Shelf</a>',
    f'<a href="https://ainjection.github.io/halloween-books/?src=gentle-footer">The Halloween Shelf</a><a href="{JK}?src=gentle-footer">Poetry by Janice Kingsley</a>')
if 'Cormorant+Garamond' not in s:
    rep('</head>', '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&display=swap" rel="stylesheet">\n</head>')
open(p, 'w', encoding='utf-8').write(s); print('ok')
