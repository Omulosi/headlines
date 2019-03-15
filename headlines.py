from flask import Flask, render_template, request
import feedparser

app = Flask(__name__)


RSS_FEEDS = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox':'http://feeds.foxnews.com/foxnews/latest',
             'iol':'http://www.iol.co.za/cmlink/1.640',
             'nyt':'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
             'spiegel':'http://www.spiegel.de/international/index.rss',
             'time':'http://feeds2.feedburner.com/time/topstories',
             'reuters':'http://feeds.reuters.com/reuters/topNews',
             'wsj':'https://feeds.a.dj.com/rss/RSSWorldNews.xml',
             'ft':'https://www.ft.com/?format=rss',
             'truthdig': 'https://www.truthdig.com/rss-2/',
             'mtr': 'https://www.technologyreview.com/rss/'
            }

@app.route('/')
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    articles = feed['entries']
    publication = publication.upper()
    return render_template('home.html', articles=articles,
            publication=publication)


if __name__ == '__main__':
    app.run(debug=True)
