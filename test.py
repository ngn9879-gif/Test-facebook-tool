import requests

def test_connection():
    # ফেসবুকের রিকভারি পেজ
    url = "https://mbasic.facebook.com/login/identify/?ctx=recover"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.facebook.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        session = requests.Session()
        print("[*] ফেসবুকের সাথে কানেক্ট হচ্ছে...")
        response = session.get(url, headers=headers, timeout=10)
        
        print(f"[*] স্ট্যাটাস কোড: {response.status_code}")
        
        if response.status_code == 200:
            print("[✓] সফল! ফেসবুক আমাদের চিনতে পেরেছে।")
        else:
            print("[!] এখনো ৪শ বা অন্য কোন কোড দিচ্ছে।")
            
    except Exception as e:
        print(f"[✗] এরর: {e}")

if __name__ == '__main__':
    test_connection()
