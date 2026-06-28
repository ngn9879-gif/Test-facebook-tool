import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

def log(msg, color=""):
    print(f"{color}[*] {msg}\033[0m")

def main():
    print("\n\033[92m[+] FB AUTO RECOVERY TOOL v2.0 (Lite Version)\033[0m\n")
    phone = input("\033[93m➜ Enter Mobile Number: \033[0m").strip()
    
    # এবার আমরা লিট ভার্সন ট্রাই করব
    url = "https://lite.facebook.com/login/identify/?ctx=recover"
    
    log("Connecting to Facebook Lite...")
    r = scraper.get(url)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # লাইট ভার্সনে টোকেনগুলো সাধারণত hidden input হিসেবে থাকে
    lsd_tag = soup.find('input', {'name': 'lsd'})
    jazoest_tag = soup.find('input', {'name': 'jazoest'})
    
    if lsd_tag and jazoest_tag:
        lsd = lsd_tag['value']
        jazoest = jazoest_tag['value']
        log(f"Tokens found! LSD: {lsd[:5]}...")
        
        log("Searching for account...")
        # লাইট ভার্সনে পোস্ট ডাটা
        data = {
            'lsd': lsd,
            'jazoest': jazoest,
            'email': phone,
            'did_submit': 'Search'
        }
        r2 = scraper.post(url, data=data)
        
        if "No search results" in r2.text:
            log("Account not found!", "\033[91m")
        elif "Enter password" in r2.text:
            log("Password page detected!", "\033[93m")
        elif "Confirm your account" in r2.text or "send_code" in r2.text:
            log("Success! Account found and ready for OTP.", "\033[92m")
        else:
            log("Got a response, but couldn't identify the page.")
            print(r2.text[:200]) # ডিবাগিং
            
    else:
        log("Still no tokens found on Lite version!", "\033[91m")
        print("Checking first 500 chars of response:")
        print(r.text[:500])

if __name__ == '__main__':
    main()
