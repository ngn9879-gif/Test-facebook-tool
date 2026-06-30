#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════╗
║    🔐  FB RECOVERY TOOL  v6.1          ║
║    ────  Pure Selenium for Termux ────   ║
╚══════════════════════════════════════════╝
"""

import requests
import re, os, time, json, sys

C = '\033[96m'; G = '\033[92m'; Y = '\033[93m'
R = '\033[91m'; B = '\033[94m'; N = '\033[0m'
W = '\033[1m'; D = '\033[2m'

# ========== টারমাক্সের জন্য Chromium পাথ ==========
# Termux এ chromium ইনস্টল করলে এখানে থাকে
CHROMIUM_PATHS = [
    '/data/data/com.termux/files/usr/bin/chromium',
    '/data/data/com.termux/files/usr/lib/chromium/chromium',
    '/data/data/com.termux/files/usr/bin/chromium-browser',
    '/data/data/com.termux/files/usr/lib/chromium-browser/chromium-browser',
]

# Selenium ইম্পোর্ট
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    SELENIUM_OK = True
except ImportError:
    SELENIUM_OK = False


def find_chromium():
    """Termux এ Chromium খুঁজে দেখা"""
    for path in CHROMIUM_PATHS:
        if os.path.exists(path):
            return path
    # which কমান্ড দিয়ে চেষ্টা
    try:
        import subprocess
        result = subprocess.run(['which', 'chromium'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return None


def get_tokens_via_selenium():
    """Selenium দিয়ে টোকেন সংগ্রহ"""
    
    if not SELENIUM_OK:
        print(f"{R}[✗] Selenium ইনস্টল নেই! 'pip install selenium' দিন{N}")
        return None
    
    chrome_path = find_chromium()
    if not chrome_path:
        print(f"{R}[✗] Chromium পাওয়া যায়নি!{N}")
        print(f"{Y}   কমান্ড দিন: pkg install chromium{N}")
        return None
    
    print(f"{G}[✓] Chromium পাওয়া গেছে: {chrome_path}{N}")
    print(f"{Y}[*] ব্রাউজার চালু হচ্ছে... (৫-১০ সেকেন্ড){N}")
    
    opts = Options()
    opts.binary_location = chrome_path
    # হেডলেস মোড
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=480x800')
    opts.add_argument('--disable-blink-features=AutomationControlled')
    opts.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36')
    
    try:
        # Service() ছাড়াই সরাসরি
        driver = webdriver.Chrome(options=opts)
    except Exception as e:
        err = str(e)
        if 'chromedriver' in err.lower() or 'executable' in err.lower():
            # ChromeDriver ম্যানেজার দিয়ে চেষ্টা
            try:
                from selenium.webdriver.chrome.service import Service as ChromeService
                from selenium.webdriver.common.by import By
                # ওয়েবড্রাইভার ম্যানেজার
                import chromedriver_autoinstaller
                chromedriver_autoinstaller.install()
                driver = webdriver.Chrome(options=opts)
            except:
                print(f"{R}[✗] ChromeDriver ইস্যু: {e}{N}")
                return None
        else:
            print(f"{R}[✗] সেলেনিয়াম ত্রুটি: {e}{N}")
            return None
    
    try:
        print(f"{D}[*] facebook.com লোড হচ্ছে...{N}")
        driver.get('https://www.facebook.com/')
        time.sleep(5)
        
        print(f"{D}[*] টোকেন কালেক্ট করছি...{N}")
        
        # JavaScript দিয়ে টোকেন বের করা
        tokens = driver.execute_script("""
            try {
                var dtsg = require("DTSGInitialData").token;
                var lsd = require("LSD").token;
                return {fb_dtsg: dtsg, lsd: lsd, success: true};
            } catch(e) {
                return {success: false, error: e.toString()};
            }
        """)
        
        if tokens.get('success') and tokens.get('fb_dtsg'):
            print(f"{G}[✓] JavaScript থেকে টোকেন নেওয়া হয়েছে!{N}")
            result = {
                'fb_dtsg': tokens['fb_dtsg'],
                'lsd': tokens.get('lsd', tokens['fb_dtsg']),
            }
            driver.quit()
            return result
        
        # Fallback: পেজ সোর্স থেকে
        print(f"{Y}[*] JavaScript fallback, page source চেক করছি...{N}")
        html = driver.page_source
        driver.quit()
        
        dtsg = re.search(r'"DTSGInitialData",\[\],\{"token":"([^"]+)"', html)
        lsd = re.search(r'"LSD",\[\],\{"token":"([^"]+)"', html)
        
        if dtsg or lsd:
            print(f"{G}[✓] Page source থেকে টোকেন নেওয়া হয়েছে!{N}")
            return {
                'fb_dtsg': dtsg.group(1) if dtsg else '',
                'lsd': lsd.group(1) if lsd else '',
            }
        
        # আরেকটা fallback: mbasic থেকে
        print(f"{Y}[*] mbasic.facebook.com চেষ্টা করছি...{N}")
        try:
            driver2 = webdriver.Chrome(options=opts)
            driver2.get('https://mbasic.facebook.com/')
            time.sleep(3)
            html2 = driver2.page_source
            driver2.quit()
            
            lsd2 = re.search(r'name="lsd" value="([^"]+)"', html2)
            jazoest = re.search(r'name="jazoest" value="([^"]+)"', html2)
            
            if lsd2:
                print(f"{G}[✓] mbasic থেকে টোকেন নেওয়া হয়েছে!{N}")
                return {
                    'fb_dtsg': lsd2.group(1),
                    'lsd': lsd2.group(1),
                    'jazoest': jazoest.group(1) if jazoest else '2',
                    'source': 'mbasic'
                }
        except:
            pass
        
        print(f"{R}[✗] কোনোভাবেই টোকেন পাওয়া যায়নি{N}")
        return None
        
    except Exception as e:
        try: driver.quit()
        except: pass
        print(f"{R}[✗] ত্রুটি: {e}{N}")
        return None


def fmt_phone(phone):
    clean = re.sub(r'[^0-9]', '', phone)
    if clean.startswith('880'): clean = '0' + clean[3:]
    elif clean.startswith('00880'): clean = '0' + clean[5:]
    if clean.startswith('01') and len(clean) == 11: return clean
    return None


def graphql_request(session, tokens, variables, doc_id, friendly_name):
    """GraphQL API রিকোয়েস্ট"""
    
    fb_dtsg = tokens.get('fb_dtsg', '')
    lsd = tokens.get('lsd', fb_dtsg)
    
    body = {
        '__user': '0',
        '__a': '1',
        'dpr': '2',
        'fb_dtsg': fb_dtsg,
        'jazoest': tokens.get('jazoest', '2'),
        'lsd': lsd,
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': friendly_name,
        'variables': json.dumps(variables),
        'doc_id': doc_id,
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.facebook.com',
        'Referer': 'https://www.facebook.com/',
        'X-FB-LSD': lsd,
    }
    
    r = session.post('https://www.facebook.com/api/graphql/', 
                      headers=headers, data=body, timeout=15)
    
    text = r.text
    if text.startswith('for (;;);'):
        text = text[9:]
    return text


def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{C}
╔══════════════════════════════════════════╗
║{N}{W}    🔐  FB RECOVERY  v6.1         {C}        ║
║{N}    ────  Pure Selenium ────         {C}        ║
║{N}{D}    Termux অপ্টিমাইজড              {C}        ║
╚══════════════════════════════════════════╝{N}""")
    
    if not SELENIUM_OK:
        print(f"\n{R}[✗] Selenium ইনস্টল নেই!{N}")
        print(f"{Y}   pip install selenium{N}")
        return
    
    print(f"\n{Y}[*] Facebook ID (ফোন নম্বর) দিন:{N}")
    print(f"{D}   যেমন: 01712345678{N}")
    phone = input(f"\n{W}➜ {N}").strip()
    
    phone = fmt_phone(phone)
    if not phone:
        print(f"\n{R}[✗] ভুল ফোন! ০১XXXXXXXXX ফরম্যাট{N}")
        return
    
    print(f"\n{G}[✓] ফোন: {phone}{N}")
    
    print(f"\n{B}{'─'*50}{N}")
    print(f"{W}স্টেপ ১: টোকেন সংগ্রহ (Selenium → Chromium){N}")
    print(f"{B}{'─'*50}{N}")
    
    tokens = get_tokens_via_selenium()
    if not tokens or not tokens.get('fb_dtsg'):
        print(f"\n{R}[✗] টোকেন পাওয়া যায়নি{N}")
        print(f"{Y}   সমাধান: pkg install chromium{N}")
        print(f"{Y}   তারপর: pip install selenium{N}")
        return
    
    print(f"{G}[✓] fb_dtsg: {tokens['fb_dtsg'][:30]}...{N}")
    
    print(f"\n{B}{'─'*50}{N}")
    print(f"{W}স্টেপ ২: GraphQL API{N}")
    print(f"{B}{'─'*50}{N}")
    
    session = requests.Session()
    
    # doc_id গুলো ট্রাই করা
    doc_ids = [
        '5345237891345678',
        '8435648735647356',
        '4474821882813793',
    ]
    
    found = False
    for doc_id in doc_ids:
        variables = {
            "contactPoint": phone,
            "contactPointType": "PHONE",
            "source": "forgot_password"
        }
        
        result = graphql_request(session, tokens, variables, doc_id, 'useContactPointIdentifyMutation')
        
        if 'email_is_taken' in result or 'phone_is_taken' in result or 'exists' in result.lower():
            print(f"\n{G}╔══════════════════════════════════════════╗{N}")
            print(f"{G}║{N}{W}    ✅ অ্যাকাউন্ট পাওয়া গেছে!            {G}║{N}")
            print(f"{G}╚══════════════════════════════════════════╝{N}")
            
            # নাম বের করার চেষ্টা
            try:
                data = json.loads(result)
                print(f"{D}API Response: {json.dumps(data, indent=2)[:400]}{N}")
            except:
                print(f"{D}Raw: {result[:200]}{N}")
            
            found = True
            break
        elif 'no_results' in result or 'not_found' in result:
            print(f"{R}[✗] অ্যাকাউন্ট নেই{N}")
            return
        else:
            print(f"{D}[*] doc_id {doc_id[:8]}... → চেষ্টা করলাম, কাজ করল না{N}")
    
    if not found:
        print(f"\n{R}[✗] অ্যাকাউন্ট চেক ব্যর্থ{N}")
        # রেসপন্স দেখাই
        print(f"{D}রেসপন্স: {result[:300] if 'result' in dir() else 'N/A'}{N}")
        return
    
    print(f"\n{Y}[*] OTP পাঠানো হচ্ছে...{N}")
    
    doc_ids_recover = ['6291839728902026', '4474821882813793', '8435648735647356']
    
    sent = False
    for doc_id in doc_ids_recover:
        variables = {
            "contactPoint": phone,
            "source": "forgot_password",
            "flow": "recover"
        }
        
        result = graphql_request(session, tokens, variables, doc_id, 'useRecoveryInitiateMutation')
        
        if 'code_sent' in result or 'sent' in result.lower() or 'success' in result.lower():
            sent = True
            break
        elif 'error' in result.lower() and 'already' in result.lower():
            print(f"{G}[!] OTP আগেই পাঠানো হয়েছে! ফোন চেক করো{N}")
            sent = True
            break
    
    if sent:
        print(f"\n{G}╔══════════════════════════════════════════╗{N}")
        print(f"{G}║{N}{W}    ✅ সফল! OTP পাঠানো হয়েছে!          {G}║{N}")
        print(f"{G}║{N}{D}    📱 ফোন চেক করো — SMS এসেছে           {G}║{N}")
        print(f"{G}╚══════════════════════════════════════════╝{N}")
    else:
        print(f"\n{Y}[*] OTP পাঠানোর চেষ্টা হয়েছে। ফোন চেক করো।{N}")
        try:
            print(f"{D}রেসপন্স: {result[:300]}{N}")
        except:
            pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] বন্ধ{N}")
    except Exception as e:
        print(f"\n{R}[✗] Error: {e}{N}")
        import traceback
        traceback.print_exc()
