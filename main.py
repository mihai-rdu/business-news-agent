import feedparser
from feeds import FEEDS


def fetch_news():
    items = []

    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:5]:
            items.append({
                "source": feed.feed.get("title", feed_url),
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", ""),
                "published": entry.get("published", ""),
            })

    return items


if __name__ == "__main__":
    for item in fetch_news():
        print(item["source"])
        print(item["title"])
        print(item["link"])
        print()
