import cloudscraper
import json
import re

def get_tokens():
    scraper = cloudscraper.create_scraper()
    # আমরা ফেসবুকের মেইন পেজ থেকে টোকেন সংগ্রহ করব
    url = "https://m.facebook.com/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    }
    
    print("[*] Connecting to Facebook to fetch tokens...")
    r = scraper.get(url, headers=headers)
    
    # টোকেন খোঁজার লজিক
    dtsg_match = re.search(r'"dtsg":"([^"]+)"', r.text)
    jazoest_match = re.search(r'"jazoest":"([^"]+)"', r.text)
    
    if dtsg_match and jazoest_match:
        dtsg = dtsg_match.group(1)
        jazoest = jazoest_match.group(1)
        print(f"\n[✓] Tokens Found!")
        print(f"[+] fb_dtsg : {dtsg}")
        print(f"[+] jazoest : {jazoest}")
        return dtsg, jazoest
    else:
        print("\n[!] Tokens not found! Re-checking...")
        return None, None

if __name__ == '__main__':
    get_tokens()
