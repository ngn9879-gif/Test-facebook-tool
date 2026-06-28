import cloudscraper

def test_connection():
    # ক্লাউডস্ক্রেপার সেশন তৈরি
    scraper = cloudscraper.create_scraper()
    
    url = "https://mbasic.facebook.com/login/identify/?ctx=recover"
    
    try:
        print("[*] ফেসবুকের প্রটেকশন বাইপাস করার চেষ্টা করছি...")
        response = scraper.get(url)
        
        print(f"[*] স্ট্যাটাস কোড: {response.status_code}")
        
        if response.status_code == 200:
            print("[✓] সফল! ক্লাউডস্ক্রেপার দিয়ে কানেক্ট হওয়া গেছে।")
            if "lsd" in response.text:
                print("[✓] চমৎকার! পেজ থেকে টোকেন পড়ার মতো অবস্থায় আছি।")
            else:
                print("[!] কানেক্ট হয়েছে কিন্তু টোকেন খুঁজে পাচ্ছি না।")
        else:
            print(f"[!] সমস্যা হয়েছে। কোড: {response.status_code}")
            
    except Exception as e:
        print(f"[✗] এরর: {e}")

if __name__ == '__main__':
    test_connection()
