import datetime
import requests
import feedparser
from functools import lru_cache
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

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

    articles = []

    for name, info in sources.items():
        try:
            print(f"\n🔍 Fetching {name} feed...")
            response = requests.get(info['url'], headers=HEADERS)
            feed = feedparser.parse(response.content)

            if not feed.entries:
                print(f"❌ {name} returned no entries!")
                continue

            print(f"✅ {name}: {len(feed.entries)} entries found.")

            for entry in feed.entries[:10]:
                published = entry.get("published", "Unknown date")
                try:
                    published_dt = datetime.datetime(*entry.published_parsed[:6])
                except:
                    published_dt = datetime.datetime.utcnow()

                # Get thumbnail
                image_url = None
                if 'media_content' in entry:
                    image_url = entry.media_content[0].get('url')
                elif 'summary' in entry:
                    soup = BeautifulSoup(entry.summary, 'html.parser')
                    img_tag = soup.find('img')
                    if img_tag:
                        image_url = img_tag.get('src')

                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': published,
                    'published_dt': published_dt,
                    'source_name': name,
                    'source_logo': info['logo'],
                    'image': image_url
                }

                articles.append(article)
                print(f"  - Added: {name} | {entry.title}")

        except Exception as e:
            print(f"🔥 Failed to fetch {name}: {e}")

    articles.sort(key=lambda x: x['published_dt'], reverse=True)
    print(f"\n✅ Total articles loaded: {len(articles)}\n")
    return articles
