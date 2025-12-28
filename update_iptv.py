import requests
import json
import os

# আপনার পছন্দের চ্যানেলগুলোর নাম
TARGET_CHANNELS = [
"tSports", # ক্রিকেট ও বাংলাদেশী চ্যানেল
"Star Sports 1", 
"Star Sports 2", 
"Sony Ten 1", 
"Sony Ten 2", 
"Sony Six",  
"GTV", 
"Sports18", 
"Willow Cricket",
"Geo Super",
"PTV Sports",
"Star Sports Select 1", # ফুটবল ও আন্তর্জাতিক
"Sony Ten 5", 
"BeIN Sports", 
"Sky Sports Football",
"BT Sport 1", 
"TNT Sports 1", 
"TNT Sports 2",
"SuperSport Football"
]

def fetch_iptv_links():
    M3U_URL = "https://iptv-org.github.io/iptv/index.m3u"
    print("M3U লিস্ট ডাউনলোড হচ্ছে...")
    
    try:
        response = requests.get(M3U_URL, timeout=30)
        lines = response.text.splitlines()
        
        found_links = []
        
        for i in range(len(lines)):
            if lines[i].startswith("#EXTINF"):
                # প্রতি লাইনের জন্য টার্গেট চ্যানেলগুলো চেক করবে
                for target in TARGET_CHANNELS:
                    if target.lower() in lines[i].lower():
                        # নিশ্চিত করা যে পরবর্তী লাইনে লিঙ্ক আছে
                        if i + 1 < len(lines):
                            stream_url = lines[i+1]
                            if stream_url.startswith("http"):
                                found_links.append({
                                    "name": target,
                                    "url": stream_url
                                })
                                print(f"পাওয়া গেছে: {target} -> {stream_url[:30]}...")
                # এখানে কোনো break হবে না, যাতে একই নামের সব লিঙ্ক চেক করে।
                                
        return found_links
    except Exception as e:
        print(f"Error: {e}")
        return []

# ডাটা সংগ্রহ এবং সেভ
channels_data = fetch_iptv_links()

if channels_data:
    with open('links.json', 'w', encoding='utf-8') as f:
        json.dump(channels_data, f, indent=4, ensure_ascii=False)
    print(f"সফলভাবে {len(channels_data)} টি লিঙ্ক links.json এ সেভ হয়েছে।")
