import os
import smtplib
from email.message import EmailMessage
from datetime import datetime, timezone

import feedparser
from dotenv import load_dotenv
from openai import OpenAI

from feeds import FEEDS

load_dotenv()
client = OpenAI()


def fetch_news(max_items_per_feed=8):
    items = []

    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:max_items_per_feed]:
            items.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "")[:800],
                "source": feed.feed.get("title", feed_url),
                "published": entry.get("published", ""),
            })

    return items


def summarize_news(items):
    news_text = "\n\n".join(
        f"Source: {item['source']}\n"
        f"Title: {item['title']}\n"
        f"Published: {item['published']}\n"
        f"Summary: {item['summary']}\n"
        f"Link: {item['link']}"
        for item in items
    )

    prompt = f"""
You are a business analyst helping an independent Amplitude Analytics consultant based in the Netherlands under a ZZP business entity.

Review the news items below and create a weekly briefing for the consultant.

Focus on:
- Netherlands business and regulatory news
- EU business and regulatory news
- AI, SaaS, startups, analytics, privacy, data, martech
- macroeconomic developments relevant to consulting, tech, or B2B sales

Return:
1. Executive summary
2. Top 7 developments
3. Why each matters to my consulting business
4. Suggested actions or angles
5. Source links

News items:
{news_text}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text


def send_email(subject, body):
    msg = EmailMessage()
    msg["From"] = os.environ["SMTP_USER"]
    msg["To"] = os.environ["EMAIL_TO"]
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL(
        os.environ["SMTP_HOST"],
        int(os.environ["SMTP_PORT"])
    ) as server:
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        server.send_message(msg)

def main():
    items = fetch_news()
    briefing = summarize_news(items)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    subject = f"NL/EU Business News Briefing — {today}"

    send_email(subject, briefing)
    print(f"Found {len(items)} articles")
    print(briefing[:500])

if __name__ == "__main__":
    main()
