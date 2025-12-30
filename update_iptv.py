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
    "18": "Sports18", 
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
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/bd.m3u",
    "https://raw.githubusercontent.com/asmaakther/personal-iptv-links/main/custom.txt",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/pk.m3u",
]

def fetch_and_filter():
    final_links = []
    seen_domains = set() # ডোমেইন ডুপ্লিকেট চেক করার জন্য

    print("লিঙ্ক সংগ্রহের কাজ শুরু হচ্ছে...")

    for source_url in M3U_SOURCES:
        try:
            response = requests.get(source_url, timeout=20)
            if response.status_code != 200: continue
            
            lines = response.text.splitlines()
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    channel_info = lines[i]
                    
                    for key in CHANNELS_MAP.keys():
                        if key.lower() in channel_info.lower():
                            if i + 1 < len(lines):
                                stream_url = lines[i+1].strip()
                                
                                # ১. শুধুমাত্র .m3u8 চেক
                                if ".m3u8" in stream_url.lower():
                                    
                                    # ২. ডোমেইন আলাদা করা (যেমন: google.com)
                                    domain = urlparse(stream_url).netloc
                                    
                                    # ৩. ডোমেইন আগে এসেছে কি না চেক করা
                                    if domain and domain not in seen_domains:
                                        final_links.append({
                                            "name": key, # এখানে CHANNELS_MAP[key]থেকে 'key' করা যাতে নাম আসে
                                            "url": stream_url
                                        })
                                        seen_domains.add(domain) # ডোমেইনটি সেভ করে রাখা
                                        print(f"পাওয়া গেছে: {CHANNELS_MAP[key]} ({domain})")
                                    
        except Exception as e:
            print(f"Error reading {source_url}: {e}")

    with open('links.json', 'w', encoding='utf-8') as f:
        json.dump(final_links, f, indent=4, ensure_ascii=False)
    
    print(f"\nমোট {len(final_links)}টি ইউনিক ডোমেইন লিঙ্ক সেভ করা হয়েছে।")

if __name__ == "__main__":
    fetch_and_filter()


if __name__ == "__main__":

    fetch_and_filter()
