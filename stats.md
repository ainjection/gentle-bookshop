# Gentle Bookshop click counter

Live on every page of https://ainjection.github.io/gentle-bookshop/ since 8 Sep 2026.

## What it records
One row per event, no cookies, no personal data, no IP stored:

| column | meaning |
|---|---|
| ts | when |
| book | slug of the book page, or `home` for the shop front |
| kind | `view` (page opened), `amazon` (Amazon button clicked), `lookinside` (card or Look inside link clicked from the shop front) |
| ref | the site they came from (host only, e.g. `youtube.com`, `pinterest.com`) |
| target | ASIN for an Amazon click, book slug for a Look inside click |
| ua_mobile | phone or not |

## Where it lives
Supabase project `meme-ai` (ref `kvjientfaaewancbmzrr`, eu-west-2), table `public.events`.
It was Rob's own paused, unused project. Move it to its own project any time; only `track.js` needs the new URL and key.

Security: the key in `track.js` is the public publishable key and can only INSERT.
Reads, updates and deletes are denied (verified 8 Sep: select 401, delete 401, bad `kind` 400).

## How to read the numbers
Use the Supabase MCP `execute_sql` against project `kvjientfaaewancbmzrr`.

Last 7 days per book, views vs Amazon clicks vs click rate:

```sql
select book,
       count(*) filter (where kind='view')   as views,
       count(*) filter (where kind='amazon') as amazon_clicks,
       round(100.0 * count(*) filter (where kind='amazon')
             / nullif(count(*) filter (where kind='view'),0), 1) as pct
from public.events
where ts > now() - interval '7 days'
group by book
order by amazon_clicks desc, views desc;
```

Where the traffic came from:

```sql
select coalesce(nullif(ref,''),'(direct)') as source, count(*) as hits
from public.events
where ts > now() - interval '7 days'
group by 1 order by hits desc;
```

Compare with the KDP sales report for the same week: views tell you what the posts are doing,
Amazon clicks tell you what the page is doing, sales tell you what the listing is doing.
