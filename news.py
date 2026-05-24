#!/usr/bin/env python3
"""
Crypto News Aggregator - Aggregate news from multiple sources
Provides real-time crypto news and sentiment analysis

BTC Tips: 1KPUa9Njq86NJwmwqVmdjZ4oC8eHrXKqf9
"""
import json
import urllib.request
import sys
from datetime import datetime
import re

def fetch_rss_feed(url, limit=10):
    """Fetch and parse RSS feed"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('utf-8')
        
        items = []
        # Simple RSS parsing
        for item in re.finditer(r'<item>(.*?)</item>', data, re.DOTALL):
            title = re.search(r'<title>(.*?)</title>', item.group(1))
            link = re.search(r'<link>(.*?)</link>', item.group(1))
            pubdate = re.search(r'<pubDate>(.*?)</pubDate>', item.group(1))
            if title:
                items.append({
                    'title': title.group(1).strip(),
                    'link': link.group(1).strip() if link else '',
                    'date': pubdate.group(1).strip() if pubdate else ''
                })
            if len(items) >= limit:
                break
        
        return items[:limit]
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return []

def fetch_crypto_panic():
    """Fetch news from CryptoPanic"""
    url = "https://api.cryptopanic.com/api/v1/news?apikey=demo"
    try:
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            return data.get('data', [])[:20]
    except:
        return []

def display_news():
    """Display aggregated news"""
    print("=" * 70)
    print("CRYPTO NEWS AGGREGATOR")
    print(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Fetch from multiple sources
    sources = {
        'CryptoPanic': fetch_crypto_panic(),
        'CoinDesk': fetch_rss_feed('https://www.coindesk.com/arc/outboundfeeds/rss/'),
        'Decrypt': fetch_rss_feed('https://decrypt.co/rss'),
    }
    
    for source, items in sources.items():
        if items:
            print(f"\n--- {source} ---")
            for i, item in enumerate(items[:8], 1):
                title = item.get('title', item.get('name', 'Unknown'))
                if isinstance(title, dict):
                    title = title.get('plain', 'Unknown')
                print(f"  {i}. {title[:80]}")
                if item.get('url'):
                    print(f"     {item['url']}")
    
    print(f"\nBTC Tips: 1KPUa9Njq86NJwmwqVmdjZ4oC8eHrXKqf9")

def main():
    display_news()

if __name__ == "__main__":
    main()
