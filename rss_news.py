import feedparser
import datetime
from functools import lru_cache
from bs4 import BeautifulSoup

@lru_cache(maxsize=1)
def fetch_car_news():
    sources = {
        'MotorTrend': {
            'url': 'https://www.motortrend.com/rss/all.xml',
            'logo': 'motortrend.png'
        },
        'Car and Driver': {
            'url': 'https://www.caranddriver.com/rss/all.xml',
            'logo': 'car_and_driver.png'
        },
        'Autoblog': {
            'url': 'https://www.autoblog.com/rss.xml',
            'logo': 'autoblog.png'
        }
    }

    all_articles = []

    for source_name, source_info in sources.items():
        url = source_info["url"]
        logo = source_info["logo"]

        feed = feedparser.parse(url)

        if not feed.entries:
            print(f"❌ No entries for {source_name}")
            continue

        for entry in feed.entries[:10]:
            published = entry.get("published", "Unknown date")
            try:
                published_dt = datetime.datetime(*entry.published_parsed[:6])
            except:
                published_dt = datetime.datetime.utcnow()

            # Get image if available
            image_url = None
            if 'media_content' in entry:
                image_url = entry.media_content[0].get('url')
            elif 'summary' in entry:
                soup = BeautifulSoup(entry.summary, 'html.parser')
                img = soup.find('img')
                if img and img.get('src'):
                    image_url = img['src']

            all_articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': published,
                'published_dt': published_dt,
                'source_name': source_name,
                'source_logo': logo,
                'image': image_url
            })

    all_articles.sort(key=lambda x: x['published_dt'], reverse=True)
    return all_articles
