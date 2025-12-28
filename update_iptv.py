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

# একাধিক M3U প্লেলিস্ট সোর্স (আপনি এখানে আরও লিঙ্ক যোগ করতে পারেন)
M3U_SOURCES = [
    "https://iptv-org.github.io/iptv/index.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/bd.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/pk.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in.m3u"
]

def fetch_links():
    found_links = []
    seen_urls = set() # এটি ডুপ্লিকেট লিঙ্ক চেক করার জন্য ব্যবহার হবে
    
    for url in M3U_SOURCES:
        print(f"চেক করা হচ্ছে: {url}")
        try:
            response = requests.get(url, timeout=20)
            lines = response.text.splitlines()
            
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    for target in TARGET_CHANNELS:
                        if target.lower() in lines[i].lower():
                            if i + 1 < len(lines):
                                stream_url = lines[i+1].strip()
                                
                                # যদি লিঙ্কটি আগে পাওয়া না গিয়ে থাকে (Duplicate Check)
                                if stream_url.startswith("http") and stream_url not in seen_urls:
                                    found_links.append({
                                        "name": target,
                                        "url": stream_url
                                    })
                                    seen_urls.add(stream_url) # লিঙ্কটি সেভ করে রাখা হলো যাতে পরে আর না আসে
                                    print(f"নতুন লিঙ্ক পাওয়া গেছে: {target}")
        except:
            print(f"সোর্সটি কাজ করছে না: {url}")
            
    return found_links

# ডাটা সেভ করা
final_data = fetch_links()
with open('links.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=4, ensure_ascii=False)

print(f"ডুপ্লিকেট বাদ দিয়ে মোট {len(final_data)}টি ইউনিক লিঙ্ক পাওয়া গেছে।")
