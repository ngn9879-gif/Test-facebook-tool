import requests

def test_connection():
    # ফেসবুক লাইটের রিকভারি এন্ডপয়েন্ট
    url = "https://lite.facebook.com/login/identify/?ctx=recover"
    
    # ব্রাউজার হিসেবে ফেসবুককে ধোঁকা দেওয়ার জন্য হেডার্স
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
    }

    try:
        session = requests.Session()
        print("[*] ফেসবুকের সাথে কানেক্ট হচ্ছে...")
        response = session.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("[✓] সফল! ফেসবুক আমাদের চিনতে পেরেছে।")
            print(f"[*] রেসপন্স সাইজ: {len(response.text)} bytes")
        else:
            print(f"[!] সমস্যা হয়েছে। স্ট্যাটাস কোড: {response.status_code}")
            
    except Exception as e:
        print(f"[✗] এরর: {e}")

if __name__ == '__main__':
    test_connection()
