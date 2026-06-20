import os
import requests
import json

API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID")

def fetch_videos():
    url = "https://googleapis.com"
    params = {
        "key": API_KEY.strip() if API_KEY else "",
        "channelId": CHANNEL_ID.strip() if CHANNEL_ID else "",
        "part": "snippet,id",
        "order": "date",
        "maxResults": 15
    }
    
    response = requests.get(url, params=params).json()
    
    if "items" not in response:
        print("Error fetching videos:", response)
        return

    # Ensure directories are ready
    os.makedirs("content/posts", exist_ok=True)
    
    video_manifest = []

    for item in response["items"]:
        if item["id"]["kind"] == "youtube#video":
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            date = item["snippet"]["publishedAt"].split("T")[0]
            description = item["snippet"]["description"]
            
            # Save to unified memory index for our frontend template
            video_manifest.append({
                "id": video_id,
                "title": title,
                "date": date,
                "description": description
            })
            
            # Optional: Keep markdown file creation active for your archival records
            filename = f"content/posts/{video_id}.md"
            markdown_content = f"---\ntitle: \"{title}\"\ndate: {date}\nvideo_id: \"{video_id}\"\n---\n\n{description}"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(markdown_content)

    # Write out the JSON manifest file that index.html reads
    with open("content/posts/index.json", "w", encoding="utf-8") as json_file:
        json.dump(video_manifest, json_file, indent=4, ensure_ascii=False)
        
    print(f"Successfully cataloged {len(video_manifest)} videos into metadata index.")

if __name__ == "__main__":
    fetch_videos()
