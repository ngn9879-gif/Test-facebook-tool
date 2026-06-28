import cloudscraper
from bs4 import BeautifulSoup
import time

scraper = cloudscraper.create_scraper()

def log(msg, color=""):
    print(f"{color}[*] {msg}\033[0m")

def main():
    print("\n\033[92m[+] FB AUTO RECOVERY TOOL v2.0\033[0m\n")
    phone = input("\033[93m➜ Enter Mobile Number: \033[0m").strip()
    
    url = "https://mbasic.facebook.com/login/identify/?ctx=recover"
    
    log("Connecting to Facebook...")
    r = scraper.get(url)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # টোকেন খোঁজার লজিক
    lsd_tag = soup.find('input', {'name': 'lsd'})
    jazoest_tag = soup.find('input', {'name': 'jazoest'})
    
    if lsd_tag and jazoest_tag:
        lsd = lsd_tag['value']
        jazoest = jazoest_tag['value']
        log(f"Tokens found (LSD: {lsd[:5]}...)")
        
        log("Searching for account...")
        data = {'lsd': lsd, 'jazoest': jazoest, 'email': phone, 'did_submit': 'Search'}
        r2 = scraper.post(url, data=data)
        
        content = r2.text
        
        # পেজ চেনার লজিক
        if "No search results" in content:
            log("Account not found!", "\033[91m")
        elif "Choose your account" in content:
            log("Multiple accounts found!", "\033[93m")
        elif "Enter password" in content:
            log("Password page detected!", "\033[93m")
        elif "Confirm your account" in content:
            log("Success! SMS option reached.", "\033[92m")
        elif "Enter the letters and numbers" in content:
            log("CAPTCHA DETECTED!", "\033[91m")
        else:
            log("Unknown page response received.")
            
    else:
        log("Could not find tokens! Printing partial page content for debug:", "\033[91m")
        print(r.text[:300]) 

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
