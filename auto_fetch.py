import os
import requests
import datetime
import re

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

CATEGORIES = [
    {"type": "category", "query": "technology", "display_name": "Tech & Media"},
    {"type": "category", "query": "business", "display_name": "World News"},
    {"type": "everything", "query": '("Premier League" OR "Champions League" OR "Serie A" OR "La Liga" OR "transfers") AND NOT rugby', "display_name": "Football"}
]

os.makedirs("content/posts", exist_ok=True)

for cat in CATEGORIES:
    if cat["type"] == "category":
        url = f"https://newsapi.org/v2/top-headlines?category={cat['query']}&language=en&apiKey={NEWS_API_KEY}"
    else:
        url = f"https://newsapi.org/v2/everything?q={cat['query']}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        
    response = requests.get(url).json()
    articles = response.get("articles", [])
    
    for i, article in enumerate(articles[:3]):
        title = article.get("title", "").replace('"', '\\"')
        if not title or title == "[Removed]":
            continue

        description = article.get("description", "") or ""
        image_url = article.get("urlToImage", "") or ""
        
        # 1. GET THE ORIGINAL ARTICLE URL & SOURCE NAME
        original_url = article.get("url", "#")
        source_name = article.get("source", {}).get("name", "Original Publisher")
        
        date_str = datetime.date.today().isoformat()
        
        slug_title = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower())[:30].strip('-')
        filename = f"content/posts/{date_str}-{cat['display_name'].lower()}-{slug_title}-{i}.md"
        
        # 2. BUILD THE POST WITH A CLEAN SUMMARY AND READ MORE BUTTON
        post_content = f"""---
title: "{title}"
date: {date_str}
category: "{cat['display_name']}"
thumbnail: "{image_url}"
excerpt: "{description.replace('"', '\\"')}"
---

{description}

<br/>

<a href="{original_url}" target="_blank" rel="noopener noreferrer" style="display: inline-block; background-color: #1A1A1A; color: #ffffff; padding: 10px 18px; border-radius: 6px; text-decoration: none; font-weight: bold; margin-top: 15px;">
  Read Full Article on {source_name} &rarr;
</a>
"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(post_content)
        print(f"Saved: {filename}")