"""Add the Amazon Associates tag to every amazon.com link across the live sites, and the required disclosure line.
  python add_associates_tag.py            dry run: counts per file
  python add_associates_tag.py --write    rewrite files
Idempotent: a link that already carries tag= is left alone.
"""
import os, re, sys

TAG = "gentlebooksho-20"
SITES = [r"D:\ainjection-root", r"D:\gentle-bookshop-live", r"D:\halloween-books", r"D:\janice-kingsley", r"D:\christmas-books", r"D:\curious-kids"]
EXT = (".html", ".js")
# an amazon.com URL up to the first quote, whitespace, backtick or closing bracket; ${asin} template pieces are allowed through
URL = re.compile(r"https?://(?:www\.)?amazon\.com/[^\s\"'<>`)]*")
DISCLOSURE = '<p class="amzn-disclosure" style="font-size:12px;opacity:.7;margin:18px 0 0">As an Amazon Associate I earn from qualifying purchases.</p>'


def tag(url):
    if re.search(r"[?&]tag=", url):
        return url
    if url.rstrip("/").endswith("amazon.com/dp") or url.endswith("amazon.com/"):
        return url   # a JS string that is concatenated with an ASIN later: the tag is added after the ASIN in code, not here
    base, hash_ = (url.split("#", 1) + [""])[:2]
    base = base.rstrip(".,;")
    trail = url[len(base):] if not hash_ else ""
    joined = base + ("&" if "?" in base else "?") + "tag=" + TAG
    return joined + ("#" + hash_ if hash_ else "") + trail


def process(path, write):
    s = open(path, encoding="utf-8").read()
    n = 0
    def rep(m):
        nonlocal n
        new = tag(m.group(0)); n += new != m.group(0); return new
    out = URL.sub(rep, s)
    added_disc = False
    if path.endswith(".html") and "qualifying purchases" not in out and "amazon.com" in out and "</footer>" in out:
        out = out.replace("</footer>", DISCLOSURE + "</footer>", 1); added_disc = True
    if write and out != s:
        open(path, "w", encoding="utf-8").write(out)
    return n, added_disc


def main():
    write = "--write" in sys.argv
    total = files = disc = 0
    for site in SITES:
        for root, dirs, names in os.walk(site):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "raw", "_rec")]
            for name in names:
                if name.endswith(EXT):
                    n, d = process(os.path.join(root, name), write)
                    if n or d:
                        files += 1; total += n; disc += d
                        print(f"{'WROTE' if write else 'would'} {n:3d} links{' +disclosure' if d else ''}  {os.path.relpath(os.path.join(root, name), site)}  [{os.path.basename(site)}]")
    print(f"{total} links in {files} files, disclosure added to {disc} pages")


if __name__ == "__main__":
    main()
