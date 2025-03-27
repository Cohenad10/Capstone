import requests
from bs4 import BeautifulSoup
from models import db, NewsArticle

def fetch_car_news():
    print("🔍 Starting car news scraper...")
    url = "https://www.motortrend.com/news/"
    
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        headlines = soup.select("article h3 a")[:5]

        if not headlines:
            print("❌ No headlines found. Check selector.")
        
        for h in headlines:
            title = h.get_text(strip=True)
            link = h['href']
            print(f"Found: {title}")
            if not NewsArticle.query.filter_by(title=title).first():
                db.session.add(NewsArticle(title=title, url=link))
                print(f"✅ Saved: {title}")
        
        db.session.commit()
        print("✅ News scraping complete.")

    except Exception as e:
        print("❌ Scraper error:", e)
