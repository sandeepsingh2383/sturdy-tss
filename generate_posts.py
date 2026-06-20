import os
import requests
import json

# Load environment variables
API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID") # Add your channel ID here or as a secret

def fetch_videos():
    url = f"https://googleapis.com{API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=10"
    response = requests.get(url).json()
    
    if "items" not in response:
        print("Error fetching videos:", response)
        return

    # Create posts directory if it doesn't exist
    os.makedirs("content/posts", exist_ok=True)

    for item in response["items"]:
        if item["id"]["kind"] == "youtube#video":
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            date = item["snippet"]["publishedAt"].split("T")[0]
            description = item["snippet"]["description"]
            
            # Check if it is a Short or Long-form video
            # Shorts usually have shorts/ in URL or are vertical, but via API we check length or format
            # For automation, we can embed them dynamically
            
            filename = f"content/posts/{video_id}.md"
            
            # Generate Markdown file with Front Matter
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
