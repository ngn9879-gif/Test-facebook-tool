import cloudscraper

def main():
    scraper = cloudscraper.create_scraper()
    # আমরা সরাসরি একটি সেশন শুরু করছি
    url = "https://lite.facebook.com/login/identify/?ctx=recover"
    
    print("[*] Bypassing Security Challenge...")
    
    # এবার আমরা রিকোয়েস্ট পাঠাচ্ছি 'Browser-like' হেডার দিয়ে
    r = scraper.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Referer': 'https://lite.facebook.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    })
    
    # পুরো পেজটা না দেখে আমরা শুধু দেখব সে আমাদের কোনো 'LSD' টোকেন দিচ্ছে কি না
    if 'lsd' in r.text:
        print("[✓] LSD Token Found!")
    else:
        print("[!] Still no tokens. Let's look for form inputs:")
        # এখানে আমরা দেখব পেজে কোন কোন ইনপুট ফিল্ড আছে
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, 'html.parser')
        inputs = soup.find_all('input')
        for i in inputs:
            print(f"Found input name: {i.get('name')}")

if __name__ == '__main__':
    main()
