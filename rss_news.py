import datetime
import requests
import feedparser
from functools import lru_cache
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119 Safari/537.36"
}

@lru_cache(maxsize=1)
def fetch_car_news():
    sources = {
        'Top Gear': {
            'url': 'https://www.topgear.com/rss/car-news',
            'logo': 'top_gear.png'
        },
        'Car and Driver': {
            'url': 'https://www.caranddriver.com/rss/all.xml',
            'logo': 'car_and_driver.png'
        },
        'Carscoops': {
            'url': 'https://www.carscoops.com/feed/',
            'logo': 'carscoops.png'
        }
    }

    articles = []

    for name, info in sources.items():
        try:
            print(f"\n🔍 Fetching {name}...")
            response = requests.get(info['url'], headers=HEADERS, timeout=10)
            feed = feedparser.parse(response.content)

            if not feed.entries:
                print(f"❌ No articles found for {name}.")
                continue

            print(f"✅ {name}: {len(feed.entries)} articles loaded.")

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
                    img = soup.find('img')
                    if img and img.get('src'):
                        image_url = img['src']

                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': published,
                    'published_dt': published_dt,
                    'source_name': name,
                    'source_logo': info['logo'],
                    'image': image_url
                })

                print(f"  ➕ {name}: {entry.title}")

        except Exception as e:
            print(f"🔥 Error fetching {name}: {e}")

    articles.sort(key=lambda x: x['published_dt'], reverse=True)
    print(f"\n📦 Total articles: {len(articles)}\n")
    return articles
