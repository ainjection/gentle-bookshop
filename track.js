/* Gentle Bookshop click counter. Counts page views and Amazon button clicks per book.
   No cookies, no personal data: book slug, event kind, referrer host, and the time. */
(function () {
  var URL = 'https://kvjientfaaewancbmzrr.supabase.co/rest/v1/events';
  var KEY = 'sb_publishable_AISP1QyNwBJJFrKDZNjIAA_zYdxWnFQ';
  var page = location.pathname.replace(/\/index\.html$/, '/');
  var m = page.match(/\/books\/([a-z0-9-]+)\.html$/);
  var book = m ? m[1] : 'home';
  var ref = '';
  try { ref = document.referrer ? new URL(document.referrer).host : ''; } catch (e) {}
  function send(kind, extra) {
    if (KEY.indexOf('__') === 0) return;
    var body = JSON.stringify({ book: book, kind: kind, ref: ref, target: extra || null, ua_mobile: /Mobi|Android/i.test(navigator.userAgent) });
    try {
      if (navigator.sendBeacon) {
        var blob = new Blob([body], { type: 'application/json' });
        // sendBeacon cannot set headers, so fall through to fetch with keepalive
      }
      fetch(URL, { method: 'POST', keepalive: true, mode: 'cors',
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
