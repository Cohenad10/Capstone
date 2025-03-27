import requests
from bs4 import BeautifulSoup
from views import db, NewsArticle

def fetch_car_news():
    url = "https://www.motortrend.com/news/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    headlines = soup.select("article h3 a")[:5]

    for h in headlines:
        title = h.get_text(strip=True)
        link = h['href']
        if not NewsArticle.query.filter_by(title=title).first():
            db.session.add(NewsArticle(title=title, url=link))
    db.session.commit()
