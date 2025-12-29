import requests
import json
import os

# আপনার পছন্দের চ্যানেলগুলোর নাম
TARGET_CHANNELS = [
"T Sports", # ক্রিকেট ও বাংলাদেশী চ্যানেল
"Willow Cricket",
"PTV Sports",   
"Star Sports Hindi",
"Star Sports 1", 
"Star Sports 2", 
"Sony Ten 1",   
"Sports18", 
"Geo Super",
"Sony Ten 2", 
"Sony Six",   
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
     "https://github.com/asmaakther/personal-iptv-links/raw/refs/heads/main/custom.txt",
    "https://iptv-org.github.io/iptv/index.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/bd.m3u",
"https://raw.githubusercontent.com/asmaakther/personal-iptv-links/main/custom.txt",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/in.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/pk.m3u",
]

def fetch_and_filter():
    final_links = []
    seen_urls = set() # ডুপ্লিকেট লিঙ্ক বাদ দেওয়ার জন্য

    print("লিঙ্ক সংগ্রহের কাজ শুরু হচ্ছে...")

    for source_url in M3U_SOURCES:
        try:
            # সোর্স ফাইলটি ডাউনলোড করা হচ্ছে
            response = requests.get(source_url, timeout=20)
            if response.status_code != 200:
                continue
                
            lines = response.text.splitlines()
            
            for i in range(len(lines)):
                # যদি লাইনে #EXTINF থাকে (মানে এটি চ্যানেলের নাম)
                if lines[i].startswith("#EXTINF"):
                    channel_info = lines[i]
                    
                    # আমাদের টার্গেট লিস্টের সাথে মিলিয়ে দেখা
                    for target in TARGET_CHANNELS:
                        # নাম ছোট-বড় হাতের অক্ষরের পার্থক্য মুছে চেক করা হচ্ছে
                        if target.lower() in channel_info.lower():
                            # ঠিক পরের লাইনেই লিঙ্ক থাকে
                            if i + 1 < len(lines):
                                stream_url = lines[i+1].strip()
                                
                                # লিঙ্কটি যদি সঠিক হয় এবং আগে না পাওয়া গিয়ে থাকে
                                if stream_url.startswith("http") and stream_url not in seen_urls:
                                    final_links.append({
                                        "name": target,
                                        "url": stream_url
                                    })
                                    seen_urls.add(stream_url)
                                    print(f"পাওয়া গেছে: {target}")
                                    
        except Exception as e:
            print(f"Error reading {source_url}: {e}")

    # ৩. ফলাফল links.json ফাইলে সেভ করা
    with open('links.json', 'w', encoding='utf-8') as f:
        json.dump(final_links, f, indent=4, ensure_ascii=False)
    
    print(f"মোট {len(final_links)}টি লিঙ্ক সেভ করা হয়েছে।")

if __name__ == "__main__":
    fetch_and_filter()
