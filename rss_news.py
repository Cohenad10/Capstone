import feedparser

def fetch_car_news():
    feed_urls = [
        'https://www.motortrend.com/rss/all.xml',
        'https://www.caranddriver.com/rss/all.xml',
        'https://www.autoblog.com/rss.xml'
    ]
    articles = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:  # 3 headlines per source
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.published
            })
    return articles
