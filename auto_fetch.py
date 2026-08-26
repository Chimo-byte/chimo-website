import os
import requests
import datetime
import re

# Fetch top news headlines
API_KEY = os.environ.get("NEWS_API_KEY")
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

try:
    response = requests.get(url).json()

    if response.get("articles") and len(response["articles"]) > 0:
        article = response["articles"][0]  # Grab the top headline
        
        title = article.get("title", "Daily Breaking News").replace('"', "'")
        description = article.get("description") or article.get("content") or "Latest breaking story."
        description = description.replace('"', "'")
        image_url = article.get("urlToImage") or "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=600&q=80"
        article_url = article.get("url", "")
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Create a clean filename slug from title
        clean_title = re.sub(r'[^a-zA-Z0-9]', '-', title.lower())
        slug = re.sub(r'-+', '-', clean_title).strip('-')[:35]
        filename = f"content/posts/{today_date}-{slug}.md"
        
        # Format matching Decap CMS frontmatter structure
        post_content = f"""---
title: "{title}"
date: {today_date}
category: Breaking News
thumbnail: "{image_url}"
video_url: "{article_url}"
excerpt: "{description[:150]}..."
---

{description}

[Read full article source]({article_url})
"""

        os.makedirs("content/posts", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(post_content)
        print(f"Successfully generated post: {filename}")

    else:
        print("No articles retrieved from API.")

except Exception as e:
    print(f"Error fetching news: {e}")