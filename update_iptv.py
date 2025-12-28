import requests
import json
import os

# আপনার পছন্দের চ্যানেলগুলোর নাম ঠিক যেভাবে iptv-org লিস্টে আছে
# এখানে আপনি আপনার ইচ্ছামতো নাম যোগ বা বিয়োগ করতে পারেন
TARGET_CHANNELS = [
    "Star Sports 1",
   "Star Sports 2",
    "tSports",
    "Sony Ten 1", 
    "Disney Channel", 
    "Somoy TV",
    "Independent TV",
    "Al Jazeera English",
    "Pogo"
]

def fetch_iptv_links():
    # iptv-org এর গ্লোবাল ইনডেক্স লিস্ট
    M3U_URL = "https://iptv-org.github.io/iptv/index.m3u"
    print("M3U লিস্ট ডাউনলোড হচ্ছে...")
    
    try:
        response = requests.get(M3U_URL, timeout=30)
        lines = response.text.splitlines()
        
        found_links = []
        
        for i in range(len(lines)):
            if lines[i].startswith("#EXTINF"):
                for target in TARGET_CHANNELS:
                    # নামের মধ্যে মিল খুঁজবে
                    if target.lower() in lines[i].lower():
                        stream_url = lines[i+1]
                        if stream_url.startswith("http"):
                            found_links.append({
                                "name": target,
                                "url": stream_url
                            })
                            print(f"পাওয়া গেছে: {target}")
                            break
        return found_links
    except Exception as e:
        print(f"Error: {e}")
        return []

# ডাটা সংগ্রহ এবং সেভ
channels_data = fetch_iptv_links()

if channels_data:
    with open('links.json', 'w', encoding='utf-8') as f:
        json.dump(channels_data, f, indent=4, ensure_ascii=False)
    print("links.json ফাইলটি সফলভাবে তৈরি হয়েছে।")
