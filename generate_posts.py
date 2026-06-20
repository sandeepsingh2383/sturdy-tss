import os
import requests
import json

API_KEY = os.environ.get("YOUTUBE_API_KEY")
CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID")

def fetch_videos():
    if not API_KEY:
        print("❌ Error: YOUTUBE_API_KEY environment variable is empty!")
    if not CHANNEL_ID:
        print("❌ Error: YOUTUBE_CHANNEL_ID environment variable is empty!")

    # Explicit base URL endpoint path string
    url = "https://googleapis.com"
    
    params = {
        "key": API_KEY.strip() if API_KEY else "",
        "channelId": CHANNEL_ID.strip() if CHANNEL_ID else "",
        "part": "snippet,id",
        "order": "date",
        "maxResults": 15
    }
    
    print(f"Requesting YouTube Feed for Channel: {CHANNEL_ID}")
    raw_response = requests.get(url, params=params)
    
    if raw_response.status_code != 200:
        print(f"❌ Google API Error (Status {raw_response.status_code}):")
        print(raw_response.text)
        return

    try:
        response = raw_response.json()
    except Exception as e:
        print("❌ Failed to parse JSON response. Raw output was:")
        print(raw_response.text)
        return
    
    if "items" not in response:
        print("❌ Error fetching videos:", response)
        return

    os.makedirs("content/posts", exist_ok=True)
    video_manifest = []

    for item in response["items"]:
        if item["id"]["kind"] == "youtube#video":
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            date = item["snippet"]["publishedAt"].split("T")[0] # Clean date layout
            description = item["snippet"]["description"]
            
            video_manifest.append({
                "id": video_id,
                "title": title,
                "date": date,
                "description": description
            })

    with open("content/posts/index.json", "w", encoding="utf-8") as json_file:
        json.dump(video_manifest, json_file, indent=4, ensure_ascii=False)
        
    print(f"✅ Successfully cataloged {len(video_manifest)} videos.")

if __name__ == "__main__":
    fetch_videos()
