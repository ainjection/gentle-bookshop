/* Gentle Bookshop click counter. Counts page views and Amazon button clicks per book.
   No cookies, no personal data: book slug, event kind, referrer host, and the time. */
(function () {
  var ENDPOINT = 'https://kvjientfaaewancbmzrr.supabase.co/rest/v1/events';
  var KEY = 'sb_publishable_AISP1QyNwBJJFrKDZNjIAA_zYdxWnFQ';
  var page = location.pathname.replace(/\/index\.html$/, '/');
  var m = page.match(/\/books\/([a-z0-9-]+)\.html$/);
  var book = m ? m[1] : 'home';
  /* Where they came from. Social in-app browsers strip document.referrer, so a ?src=
     tag on the links we post is the only reliable signal. Remember it for the session
     so it still shows on the book page they click through to. */
  var ref = '';
  try {
    var q = new URLSearchParams(location.search);
    var src = q.get('src') || q.get('utm_source');
    if (src) { try { sessionStorage.setItem('gb_src', src); } catch (e) {} }
    else { try { src = sessionStorage.getItem('gb_src'); } catch (e) {} }
    ref = src || (document.referrer ? new URL(document.referrer).host : '');
  } catch (e) {}
  function send(kind, extra) {
    if (KEY.indexOf('__') === 0) return;
    var body = JSON.stringify({ book: book, kind: kind, ref: ref, target: extra || null, ua_mobile: /Mobi|Android/i.test(navigator.userAgent) });
    try {
      fetch(ENDPOINT, { method: 'POST', keepalive: true, mode: 'cors',
        headers: { 'Content-Type': 'application/json', 'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Prefer': 'return=minimal' },
        body: body });
    } catch (e) {}
  }
  send('view');
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a');
    if (!a || !a.href) return;
    if (a.href.indexOf('amazon.') !== -1) {
      var asin = (a.href.match(/\/dp\/([A-Z0-9]{10})/) || [])[1] || null;
      send('amazon', asin);
    } else if (a.classList.contains('peek') || a.classList.contains('cardlink')) {
      send('lookinside', (a.getAttribute('href') || '').replace(/^books\//, '').replace(/\.html$/, ''));
    }
  }, true);
})();
