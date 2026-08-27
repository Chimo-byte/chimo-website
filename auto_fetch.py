import os
import requests
import datetime
import re

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

CATEGORIES = [
    {"type": "category", "query": "technology", "display_name": "Tech & Media"},
    {"type": "category", "query": "business", "display_name": "World News"},
    {"type": "everything", "query": '("Premier League" OR "Champions League" OR "Serie A" OR "La Liga" OR "transfers") AND NOT rugby', "display_name": "Sport"}
]

os.makedirs("content/posts", exist_ok=True)

for cat in CATEGORIES:
    if cat["type"] == "category":
        url = f"https://newsapi.org/v2/top-headlines?category={cat['query']}&language=en&apiKey={NEWS_API_KEY}"
    else:
        url = f"https://newsapi.org/v2/everything?q={cat['query']}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        
    response = requests.get(url).json()
    articles = response.get("articles", [])
    
    if not articles:
        continue
        
    article = articles[0]
    title = article.get("title", "").replace('"', '\\"')
    description = article.get("description", "") or ""
    content = article.get("content", "") or description
    image_url = article.get("urlToImage", "") or ""
    date_str = datetime.date.today().isoformat()
    
    slug_title = re.sub(r'[^a-zA-Z0-9]+', '-', cat['display_name'].lower()).strip('-')
    filename = f"content/posts/{date_str}-{slug_title}.md"
    
    post_content = f"""---
title: "{title}"
date: {date_str}
category: "{cat['display_name']}"
thumbnail: "{image_url}"
excerpt: "{description.replace('"', '\\"')}"
---

{content}
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(post_content)
    print(f"Saved: {filename}")