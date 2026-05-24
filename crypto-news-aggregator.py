#!/usr/bin/env python3
"""Crypto News Aggregator - Real-time crypto news with sentiment analysis.

Aggregate news from multiple sources with basic sentiment scoring.
Built for Bitcoin and crypto market monitoring.

Usage:
    python crypto-news-aggregator.py           # Latest news
    python crypto-news-aggregator.py --source bitcoin    # Filter by topic
    python crypto-news-aggregator.py --sentiment positive # Filter by sentiment
    python crypto-news-aggregator.py --top 20            # Top 20 stories
    python crypto-news-aggregator.py --export             # JSON export

Support: https://github.com/will-work-for-bitcoin/crypto-news-aggregator
BTC Tips: 1KPUa9Njq86NJwmwqVmdjZ4oC8eHrXKqf9
"""

import sys
import json
import urllib.request
from datetime import datetime

RSS_FEEDS = {
    "coindesk": "https://feeds.feedburner.com/CoinDesk",
    "cointelegraph": "https://cointelegraph.com/rss",
    "bitcoinmagazine": "https://bitcoinmagazine.com/feeds/all",
    "theblock": "https://www.theblock.co/rss",
    "decrypt": "https://www.decrypt.co/rss",
}

def fetch_feed(feed_url):
    """Fetch RSS feed"""
    req = urllib.request.Request(feed_url, headers={"User-Agent": "crypto-news/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

def simple_sentiment(title):
    """Simple sentiment analysis"""
    positive = ["bull", "gain", "pump", "rally", "surge", "adoption", "growth", "record", "high", "break", "milestone"]
    negative = ["bear", "dump", "crash", "loss", "hack", "exploit", "ban", "regulation", "fear", "panic", "drop", "plunge"]
    
    score = 0
    words = title.lower().split()
    for word in positive:
        if word in words:
            score += 1
    for word in negative:
        if word in words:
            score -= 1
    
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    return "neutral"

def parse_rss_basic(xml_content):
    """Parse RSS XML to extract articles (simple parser)"""
    articles = []
    try:
        # Simple regex-based parsing
        import re
        items = re.findall(r'<item>(.*?)</item>', xml_content, re.DOTALL)
        for item in items:
            title = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
            link = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
            pubdate = re.search(r'<pubDate>(.*?)</pubDate>', item, re.DOTALL)
            description = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
            
            if title:
                title_text = re.sub(r'<[^>]+>', '', title.group(1)).strip()
                sentiment = simple_sentiment(title_text)
                articles.append({
                    "title": title_text,
                    "link": link.group(1).strip() if link else "",
                    "date": pubdate.group(1).strip() if pubdate else "",
                    "sentiment": sentiment,
                    "description": description.group(1)[:200].strip() if description else ""
                })
    except Exception:
        pass
    return articles

def display_news(articles, limit=20, source=None, sentiment=None):
    """Display news articles"""
    filtered = articles
    if source:
        filtered = [a for a in articles if source.lower() in a.get("title", "").lower() or 
                          source.lower() in a.get("description", "").lower()]
    if sentiment:
        filtered = [a for a in articles if a.get("sentiment") == sentiment]
    
    print(f"📰 CRYPTO NEWS AGGREGATOR")
    print("=" * 60)
    print(f"  Sources: {len(RSS_FEEDS)} | Articles: {len(filtered)}")
    print(f"  Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    for i, article in enumerate(filtered[:limit], 1):
        sent_icon = {"positive": "🟢", "negative": "🔴", "neutral": "⚪"}.get(article.get("sentiment"), "⚪")
        print(f"{i}. {sent_icon} {article['title'][:70]}")
        if article.get("link"):
            print(f"   📎 {article['link']}")
        print()
    
    print(f"  💰 BTC Tips: 1KPUa9Njq86NJwmwqVmdjZ4oC8eHrXKqf9")

def main():
    all_articles = []
    
    for name, url in RSS_FEEDS.items():
        content = fetch_feed(url)
        if content.startswith("Error"):
            print(f"  ⚠️ {name}: {content}")
            continue
        articles = parse_rss_basic(content)
        for a in articles:
            a["source"] = name
        all_articles.extend(articles)
    
    # Sort by date if available
    all_articles.sort(key=lambda x: x.get("date", ""), reverse=True)
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "--export":
            print(json.dumps(all_articles[:50], indent=2, default=str))
        elif cmd == "--top":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
            display_news(all_articles, limit)
        elif cmd == "--source" and len(sys.argv) > 2:
            display_news(all_articles, source=sys.argv[2])
        elif cmd == "--sentiment" and len(sys.argv) > 2:
            display_news(all_articles, sentiment=sys.argv[2])
        else:
            display_news(all_articles)
    else:
        display_news(all_articles)

if __name__ == "__main__":
    main()
