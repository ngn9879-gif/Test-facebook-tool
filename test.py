import cloudscraper
from bs4 import BeautifulSoup
import time

# কালার কোড
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

scraper = cloudscraper.create_scraper()

def log(msg, color=RESET):
    print(f"{color}[*] {msg}{RESET}")

def get_page(url, data=None):
    if data:
        return scraper.post(url, data=data)
    return scraper.get(url)

def main():
    log(f"{BOLD}FB AUTO RECOVERY STARTING...{RESET}", GREEN)
    phone = input(f"{YELLOW}➜ Enter Mobile Number: {RESET}")
    
    # স্টেপ ১: আইডি সার্চ করা
    url = "https://mbasic.facebook.com/login/identify/?ctx=recover"
    r = get_page(url)
    
    # ফর্মের টোকেন বের করা
    soup = BeautifulSoup(r.text, 'html.parser')
    lsd = soup.find('input', {'name': 'lsd'})['value']
    jazoest = soup.find('input', {'name': 'jazoest'})['value']
    
    log("Searching for account...")
    data = {'lsd': lsd, 'jazoest': jazoest, 'email': phone, 'did_submit': 'Search'}
    r2 = get_page(url, data=data)
    
    # স্টেপ ২: পেজ চেনা (Decision Logic)
    content = r2.text
    
    if "No search results" in content:
        log("Account not found!", RED)
        
    elif "Choose your account" in content:
        log("Multiple accounts found! (Logic: Picking first one)", YELLOW)
        # এখানে আমরা পরবর্তী আইডি নির্বাচনের লজিক বসাবো
        
    elif "Enter password" in content:
        log("Password page detected. Looking for 'Try another way'...", YELLOW)
        # এখানে 'Try another way' বাটনের লিংক ক্লিক করার লজিক বসবে
        
    elif "Confirm your account" in content:
        log("Success! SMS option reached.", GREEN)
        
    elif "Enter the letters and numbers" in content:
        log("CAPTCHA DETECTED! Manually solve it.", RED)
        
    else:
        log("Unknown page detected! Please check logs.", RED)
        # ডিবাগ করার জন্য পুরো পেজটা পরে দেখবো
        
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
