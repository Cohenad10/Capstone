import feedparser
import datetime
from functools import lru_cache

@lru_cache(maxsize=1)
def fetch_car_news():
    feed_urls = [
        'https://www.motortrend.com/rss/all.xml',
        'https://www.caranddriver.com/rss/all.xml',
        'https://www.autoblog.com/rss.xml'
    ]
    articles = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:  # Grab more articles per site
            published = entry.get("published", "Unknown date")
            try:
                published_dt = datetime.datetime(*entry.published_parsed[:6])
            except:
                published_dt = datetime.datetime.utcnow()

            articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': published,
                'published_dt': published_dt,
                'source': feed.feed.title if 'title' in feed.feed else 'Unknown Source'
            })

    # Sort all articles by newest date
    articles.sort(key=lambda x: x['published_dt'], reverse=True)
    return articles
