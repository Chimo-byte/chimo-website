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
    
    # Grab top 3 articles for each category
    for i, article in enumerate(articles[:3]):
        title = article.get("title", "").replace('"', '\\"')
        if not title or title == "[Removed]":
            continue

        description = article.get("description", "") or ""
        content = article.get("content", "") or description
        image_url = article.get("urlToImage", "") or ""
        date_str = datetime.date.today().isoformat()
        
        # Create unique filename for each of the 3 articles
        slug_title = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower())[:30].strip('-')
        filename = f"content/posts/{date_str}-{cat['display_name'].lower()}-{slug_title}-{i}.md"
        
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