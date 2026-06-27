import requests
import re

def test_connection():
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    }

    print("[*] টোকেন খোঁজা হচ্ছে...")
    r = session.get("https://mbasic.facebook.com/login/identify/?ctx=recover", headers=headers)
    
    # পেজ থেকে LSD টোকেন বের করা
    lsd_match = re.search(r'name="lsd" value="([^"]+)"', r.text)
    
    if lsd_match:
        lsd = lsd_match.group(1)
        print(f"[✓] টোকেন পাওয়া গেছে: {lsd}")
        print("[*] এখন রিকভারি পেজে ট্রাই করছি...")
        
        # ডাটা পাঠিয়ে চেক করা
        data = {'lsd': lsd, 'email': '01712345678', 'did_submit': 'Search'}
        r2 = session.post("https://mbasic.facebook.com/login/identify/?ctx=recover", data=data, headers=headers)
        print(f"[*] স্ট্যাটাস কোড: {r2.status_code}")
    else:
        print("[!] টোকেন পাওয়া যায়নি! ফেসবুক সম্ভবত স্ক্রিপ্ট ব্লক করেছে।")

if __name__ == '__main__':
    test_connection()
