import requests
import json
from urllib.parse import urlparse

# নাম ঠিক করার জন্য ম্যাপিং (অগোছালো নামকে সুন্দর করবে)
CHANNELS_MAP = {
    "T SPORTS": "T Sports", 
    "WILLOW": "Willow Cricket",
    "PTV": "PTV Sports",    
    "STAR HINDI": "Star Sports Hindi",
    "STAR 1": "Star Sports 1", 
    "STAR 2": "Star Sports 2", 
    "TEN 1": "Sony Ten 1",   
    "GEO": "Geo Super",
    "TEN 2": "Sony Ten 2", 
    "SIX ": "Sony Six",    
    "SELECT 1": "Star Sports Select", 
    "TEN 5": "Sony Ten 5", 
    "BeIN": "Bein Sports",
    "XTRA": "BeIN SPORTS XTRA",
    "BeIN U": "beIN Sports USA", 
    "SKY": "Sky Sports Football",
    "BT 1": "BT Sport 1", 
    "TNT 1": "TNT Sports 1", 
    "TNT 2": "TNT Sports 2",
    "SUPER": "SuperSport Football"
}

M3U_SOURCES = [
    "https://github.com/asmaakther/personal-iptv-links/raw/refs/heads/main/custom.txt",
    "https://iptv-org.github.io/iptv/index.m3u",
    "https://raw.githubusercontent.com/asmaakther/personal-iptv-links/main/custom.txt",

]
def fetch_and_filter():
    final_links = []
    # চ্যানেল অনুযায়ী ডোমেইন চেক করার জন্য ডিকশনারি
    channel_domains = {json_name: set() for json_name in CHANNELS_MAP.keys()}

    print("লিঙ্ক সংগ্রহের কাজ শুরু হচ্ছে...")

    for source_url in M3U_SOURCES:
        try:
            response = requests.get(source_url, timeout=20)
            if response.status_code != 200: continue
            
            lines = response.text.splitlines()
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    channel_info = lines[i] # অরিজিনাল নাম রাখলাম সার্চের জন্য
                    
                    # ম্যাপিং লুপ
                    for json_name, search_name in CHANNELS_MAP.items():
                        # এখানে search_name (ডান পাশের নাম) দিয়ে খোঁজা হচ্ছে
                        if search_name.lower() in channel_info.lower():
                            if i + 1 < len(lines):
                                stream_url = lines[i+1].strip()
                                
                                if stream_url.startswith("http") and ".m3u8" in stream_url.lower():
                                    domain = urlparse(stream_url).netloc
                                    
                                    # ডোমেইন চেক (একই চ্যানেলের জন্য একই সার্ভার দুইবার নেবে না)
                                    if domain and domain not in channel_domains[json_name]:
                                        final_links.append({
                                            "name": json_name, # এখানে JSON-এ বাম পাশের নাম বসবে
                                            "url": stream_url
                                        })
                                        channel_domains[json_name].add(domain)
                                        print(f"পাওয়া গেছে: {json_name} (সার্চ হয়েছে: {search_name})")
                                        break 
                                    
        except Exception as e:
            print(f"Error: {e}")

    with open('links.json', 'w', encoding='utf-8') as f:
        json.dump(final_links, f, indent=4, ensure_ascii=False)
    
    print(f"\nমোট {len(final_links)}টি লিঙ্ক সেভ হয়েছে।")

if __name__ == "__main__":
    fetch_and_filter()
