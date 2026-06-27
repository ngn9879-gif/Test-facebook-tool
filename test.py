import requests

def test_connection():
    # ফেসবুক লাইটের এন্ডপয়েন্ট
    url = "https://mbasic.facebook.com/"
    
    # ব্রাউজার সেশন তৈরি
    session = requests.Session()
    
    # সবথেকে গুরুত্বপূর্ণ হেডারসমূহ
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        print("[*] ফেসবুকের সাথে কানেক্ট হচ্ছে...")
        # প্রথমে মেইন পেজ থেকে কুকি সংগ্রহ করা
        r = session.get(url, headers=headers, timeout=15)
        
        print(f"[*] স্ট্যাটাস কোড: {r.status_code}")
        
        if r.status_code == 200:
            print("[✓] কানেকশন সফল! ফেসবুক কুকি গ্রহণ করেছে।")
            # এবার রিকভারি পেজে যাওয়ার চেষ্টা
            r2 = session.get("https://mbasic.facebook.com/login/identify/?ctx=recover", headers=headers, timeout=15)
            print(f"[*] রিকভারি পেজ স্ট্যাটাস: {r2.status_code}")
        else:
            print(f"[!] কানেকশনে সমস্যা: {r.status_code}")
            
    except Exception as e:
        print(f"[✗] এরর: {e}")

if __name__ == '__main__':
    test_connection()
