import feedparser
import datetime
from functools import lru_cache
from bs4 import BeautifulSoup

@lru_cache(maxsize=1)
def fetch_car_news():
    feed_sources = {
        'motortrend': 'https://www.motortrend.com/rss/all.xml',
        'car_and_driver': 'https://www.caranddriver.com/rss/all.xml',
        'autoblog': 'https://www.autoblog.com/rss.xml'
    }

    articles = []

    for source_key, url in feed_sources.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:  # Get 10 per site
            published = entry.get("published", "Unknown date")
            try:
                published_dt = datetime.datetime(*entry.published_parsed[:6])
            except:
                published_dt = datetime.datetime.utcnow()

            # Try to get image from media or summary
            image_url = None
            if 'media_content' in entry:
                image_url = entry.media_content[0].get('url')
            elif 'summary' in entry:
                soup = BeautifulSoup(entry.summary, 'html.parser')
                img_tag = soup.find('img')
                if img_tag:
                    image_url = img_tag.get('src')

            articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': published,
                'published_dt': published_dt,
                'source': source_key,
                'image': image_url
            })

    # Sort all articles by date (newest first)
    articles.sort(key=lambda x: x['published_dt'], reverse=True)
    return articles
