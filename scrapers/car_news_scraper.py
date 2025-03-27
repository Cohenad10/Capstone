import requests
from bs4 import BeautifulSoup
from models import db, NewsArticle

def fetch_car_news():
    url = "https://www.motortrend.com/news/"
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        headlines = soup.select("article h3 a")[:5]

        for h in headlines:
            title = h.get_text(strip=True)
            link = h['href']
            if not NewsArticle.query.filter_by(title=title).first():
                db.session.add(NewsArticle(title=title, url=link))
        db.session.commit()

    except Exception as e:
        print("Failed to fetch news:", e)
