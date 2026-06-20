import os
import requests

# Load environment variables
API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID")

def fetch_videos():
    # Base URL remains untouched and safe from string formatting issues
    url = "https://www.googleapis.com/youtube/v3/search"
    
    # Pass variables safely as URL parameters
    params = {
        "key": API_KEY.strip() if API_KEY else "", # Clean hidden spaces/newlines
        "channelId": CHANNEL_ID.strip() if CHANNEL_ID else "",
        "part": "snippet,id",
        "order": "date",
        "maxResults": 10
    }
    
    # requests safely encodes the URL for you
    response = requests.get(url, params=params).json()
    
    if "items" not in response:
        print("Error fetching videos:", response)
        return

    os.makedirs("content/posts", exist_ok=True)

    for item in response["items"]:
        if item["id"]["kind"] == "youtube#video":
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            date = item["snippet"]["publishedAt"].split("T")[0] # Clean date string
            description = item["snippet"]["description"]
            
            filename = f"content/posts/{video_id}.md"
            
            markdown_content = f"""---
title: "{title}"
date: {date}
video_id: "{video_id}"
---

{description}

<iframe width="100%" height="400" src="https://youtube.com{video_id}" frameborder="0" allowfullscreen></iframe>
"""
            with open(filename, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            print(f"Created post for: {title}")

if __name__ == "__main__":
    fetch_videos()
