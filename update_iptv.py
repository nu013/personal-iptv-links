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
    "SELECT 1": "Star Sports Select 1", 
    "TEN 5": "Sony Ten 5", 
    "BeIN": "Bein Sports",
    "XTRA": "Bein xtra", 
    "SKY": "Sky Sports Football",
    "BT": "BT Sport 1", 
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
    seen_urls = set()
    # ডোমেইন চেক করার জন্য ডিকশনারি (চ্যানেল নাম অনুযায়ী ডোমেইন সেট থাকবে)
    channel_domains = {name: set() for name in CHANNELS_MAP.values()}

    print("লিঙ্ক সংগ্রহের কাজ শুরু হচ্ছে...")

    for source_url in M3U_SOURCES:
        try:
            response = requests.get(source_url, timeout=20)
            if response.status_code != 200: continue
            
            lines = response.text.splitlines()
            
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    channel_info = lines[i].upper() # সব বড় হাতের করে চেক করা হচ্ছে
                    
                    for key, target_name in CHANNELS_MAP.items():
                        if key.upper() in channel_info:
                            if i + 1 < len(lines):
                                stream_url = lines[i+1].strip()
                                
                                # ১. শুধু m3u8 লিঙ্ক চেক
                                # ২. ডুপ্লিকেট ইউআরএল চেক
                                if stream_url.lower().endswith(".m3u8") and stream_url not in seen_urls:
                                    
                                    # ৩. একই ডোমেইন চেক
                                    domain = urlparse(stream_url).netloc
                                    if domain not in channel_domains[target_name]:
                                        
                                        final_links.append({
                                            "name": target_name,
                                            "url": stream_url
                                        })
                                        
                                        seen_urls.add(stream_url)
                                        channel_domains[target_name].add(domain) # এই ডোমেইনটি এই চ্যানেলের জন্য লক করা হলো
                                        print(f"সংগৃহীত: {target_name} ({domain})")
                                        
        except Exception as e:
            print(f"Error reading {source_url}: {e}")

    # JSON ফাইলে সেভ করা
    with open('links.json', 'w', encoding='utf-8') as f:
        json.dump(final_links, f, indent=4, ensure_ascii=False)
    
    print(f"\nমোট {len(final_links)}টি ইউনিক ডোমেইন লিঙ্ক সেভ করা হয়েছে।")

if __name__ == "__main__":
    fetch_and_filter()
