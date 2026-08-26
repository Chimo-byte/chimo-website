import os
import requests
import datetime
import re

API_KEY = os.environ.get("NEWS_API_KEY")

# Define the categories you want to fetch daily
CATEGORIES = [
    {"api_name": "technology", "display_name": "Tech & Media"},
    {"api_name": "business", "display_name": "World News"},
    {"api_name": "entertainment", "display_name": "Cinema & Reviews"}
    {"api_name": "football", "display_name": "Tech & Media"}
]

today_date = datetime.datetime.now().strftime("%Y-%m-%d")
os.makedirs("content/posts", exist_ok=True)

for cat in CATEGORIES:
    url = f"https://newsapi.org/v2/top-headlines?country=us&category={cat['api_name']}&apiKey={API_KEY}"
    
    try:
        response = requests.get(url).json()
        articles = response.get("articles", [])

        if articles:
            article = articles[0]  # Grab top article per category
            
            title = article.get("title", f"Daily {cat['display_name']} Update").replace('"', "'")
            description = article.get("description") or article.get("content") or "Read the full story below."
            description = description.replace('"', "'")
            image_url = article.get("urlToImage") or "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=600&q=80"
            article_url = article.get("url", "")
            
            # Safe slug creation
            clean_title = re.sub(r'[^a-zA-Z0-9]', '-', title.lower())
            slug = re.sub(r'-+', '-', clean_title).strip('-')[:35]
            filename = f"content/posts/{today_date}-{cat['api_name']}-{slug}.md"
            
            post_content = f"""---
title: "{title}"
date: {today_date}
category: {cat['display_name']}
thumbnail: "{image_url}"
video_url: "{article_url}"
excerpt: "{description[:150]}..."
---

{description}

[Read full article source]({article_url})
"""

            with open(filename, "w", encoding="utf-8") as f:
                f.write(post_content)
            print(f"Successfully generated [{cat['display_name']}] post: {filename}")

    except Exception as e:
        print(f"Error fetching category {cat['display_name']}: {e}")
