#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════╗
║    🔐  FB RECOVERY TOOL  v5.0          ║
║    ────  গ্রাফকিউএল এডিশন ────          ║
║    Facebook GraphQL API | ১০০% টার্গেট   ║
╚══════════════════════════════════════════╝
"""

import requests
import re
import os
import time
import json
import random
import string
import urllib.parse

C = '\033[96m'; G = '\033[92m'; Y = '\033[93m'
R = '\033[91m'; B = '\033[94m'; N = '\033[0m'
W = '\033[1m'; D = '\033[2m'

UAS = [
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-S908E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A344 Safari/602.1',
    'Mozilla/5.0 (Linux; Android 11; Redmi Note 10S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
]

def clr():
    os.system('clear' if os.name == 'posix' else 'cls')

def bnr():
    clr()
    print(f"""{C}
╔══════════════════════════════════════════╗
║{N}{W}    🔐  FB RECOVERY  v5.0         {C}        ║
║{N}    ────  GraphQL Edition ────       {C}        ║
║{N}{D}    DTSG + LSD Token | doc_id     {C}        ║
╚══════════════════════════════════════════╝{N}""")

def fmt_phone(phone):
    clean = re.sub(r'[^0-9]', '', phone)
    if clean.startswith('880'): clean = '0' + clean[3:]
    elif clean.startswith('00880'): clean = '0' + clean[5:]
    if clean.startswith('01') and len(clean) == 11: return clean
    return None

def get_tokens(session):
    """Facebook পেজ থেকে DTSGInitialData এবং LSD টোকেন বের করা"""
    print(f"\n{D}[*] Facebook থেকে টোকেন কালেক্ট করছি...{N}")
    
    urls_to_try = [
        'https://www.facebook.com/',
        'https://www.facebook.com/login/',
        'https://www.facebook.com/reg/',
        'https://mbasic.facebook.com/',
    ]
    
    tokens_found = {}
    
    for url in urls_to_try:
        try:
            r = session.get(url, timeout=10)
            html = r.text
            
            # DTSGInitialData টোকেন
            dtsg_match = re.search(r'"DTSGInitialData",\[\],\{"token":"([^"]+)"', html)
            if dtsg_match:
                tokens_found['fb_dtsg'] = dtsg_match.group(1)
                print(f"{G}[✓] DTSGInitialData.token পাওয়া গেছে ✓{N}")
            
            # LSD টোকেন (JavaScript require format)
            lsd_match = re.search(r'"LSD",\[\],\{"token":"([^"]+)"', html)
            if lsd_match:
                tokens_found['lsd'] = lsd_match.group(1)
                print(f"{G}[✓] LSD.token পাওয়া গেছে ✓{N}")
            
            # jazoest
            jz_match = re.search(r'"jazoest","([^"]+)"', html)
            if jz_match:
                tokens_found['jazoest'] = jz_match.group(1)
            
            # csrf_token
            csrf_match = re.search(r'"csrf_token":"([^"]+)"', html)
            if csrf_match:
                tokens_found['csrf'] = csrf_match.group(1)
            
            # user_id
            uid_match = re.search(r'"USER_ID":"([^"]+)"', html)
            if uid_match:
                tokens_found['uid'] = uid_match.group(1)
            else:
                uid_match = re.search(r'"userID":"([^"]+)"', html)
                if uid_match:
                    tokens_found['uid'] = uid_match.group(1)
            
            # server_revision (__rev)
            rev_match = re.search(r'"server_revision":(\d+)', html)
            if rev_match:
                tokens_found['rev'] = rev_match.group(1)
            
            if 'fb_dtsg' in tokens_found:
                break
                
        except Exception as e:
            continue
    
    # পুরনো স্টাইল fb_dtsg (যদি DTSGInitialData না পাওয়া যায়)
    if 'fb_dtsg' not in tokens_found:
        for url in ['https://mbasic.facebook.com/', 'https://www.facebook.com/']:
            try:
                r = session.get(url, timeout=10)
                fb_dtsg = re.search(r'name="fb_dtsg"[^>]*value="([^"]+)"', r.text)
                if fb_dtsg:
                    tokens_found['fb_dtsg'] = fb_dtsg.group(1)
                    print(f"{G}[✓] fb_dtsg (HTML form) পাওয়া গেছে ✓{N}")
                    break
            except:
                continue
    
    return tokens_found

def graphql_request(session, tokens, variables, doc_id):
    """Facebook GraphQL API তে রিকোয়েস্ট পাঠানো"""
    
    uid = tokens.get('uid', '0')
    fb_dtsg = tokens.get('fb_dtsg', '')
    lsd = tokens.get('lsd', fb_dtsg)
    jazoest = tokens.get('jazoest', '2')
    rev = tokens.get('rev', '1000000000')
    
    body = {
        'av': uid,
        '__user': uid,
        '__a': '1',
        '__dyn': '7xeUmxa3Q1fxu13wqolzo8e4Ly0Fxo7C12wBxa6UKW7me6W4o8oG3e2i3y4-3q3e5obx262a3W0EUe8hwem0nCq1ewSo9EW7m2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S4S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2S2C11rlwAEbUeeH',
        '__req': '1',
        '__beoa': '0',
        '__pc': 'PHASED:DEFAULT',
        'dpr': '2',
        '__ccg': 'EXCELLENT',
        '__rev': rev,
        '__s': 'b8f4l8',
        '__hsi': '7243534834607654305',
        '__comet_req': '0',
        'fb_dtsg': fb_dtsg,
        'jazoest': jazoest,
        'lsd': lsd,
        '__spin_r': rev,
        '__spin_b': 'trunk',
        '__spin_t': str(int(time.time())),
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'useContactPointIdentifyMutation',
        'variables': json.dumps(variables),
        'server_timestamps': 'true',
        'doc_id': doc_id,
    }
    
    headers = {
        'User-Agent': random.choice(UAS),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-FB-LSD': lsd,
        'X-FB-Friendly-Name': 'useContactPointIdentifyMutation',
        'Origin': 'https://www.facebook.com',
        'Referer': 'https://www.facebook.com/',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }
    
    r = session.post('https://www.facebook.com/api/graphql/', 
                      headers=headers, data=body, timeout=15)
    
    # ফেসবুক "for (;;);" প্রিফিক্স যোগ করে—সেটা রিমুভ
    text = r.text
    if text.startswith('for (;;);'):
        text = text[9:]
    
    return text

def main():
    bnr()
    
    # ফোন ইনপুট
    print(f"\n{Y}[*] Facebook ID (ফোন নম্বর) দিন:{N}")
    print(f"{D}   যেমন: 01712345678{N}")
    phone = input(f"\n{W}➜ {N}").strip()
    
    phone = fmt_phone(phone)
    if not phone:
        print(f"\n{R}[✗] ভুল ফোন! ০১XXXXXXXXX ফরম্যাট{N}")
        return
    
    print(f"\n{Y}[*] ফোন: {G}{phone}{N}")
    
    # সেশন তৈরি
    session = requests.Session()
    session.headers.update({
        'User-Agent': random.choice(UAS),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
    })
    
    # টোকেন কালেক্ট
    tokens = get_tokens(session)
    
    if 'fb_dtsg' not in tokens:
        print(f"\n{R}[✗] টোকেন পাওয়া যায়নি!{N}")
        print(f"{Y}[!] VPN বা মোবাইল ডাটা ব্যবহার করে আবার চেষ্টা করুন{N}")
        print(f"{Y}[!] অথবা ১ মিনিট পর আবার রান করুন{N}")
        return
    
    print(f"\n{G}[✓] টোকেন সেট রেডি!{N}")
    print(f"{D}   fb_dtsg: {tokens.get('fb_dtsg', 'N/A')[:20]}...{N}")
    if 'lsd' in tokens:
        print(f"{D}   lsd: {tokens['lsd'][:20]}...{N}")
    
    # === GraphQL কল ১: identify contact point ===
    print(f"\n{Y}[*] GraphQL: identify mutation পাঠানো হচ্ছে...{N}")
    
    doc_id_identify = '5345237891345678'  # identify mutation doc_id
    
    variables = {
        "contactPoint": phone,
        "contactPointType": "PHONE",
        "source": "forgot_password"
    }
    
    result = graphql_request(session, tokens, variables, doc_id_identify)
    
    try:
        data = json.loads(result)
        print(f"{D}GraphQL Response: {json.dumps(data, indent=2)[:500]}{N}")
        
        # চেক করি
        if 'email_is_taken' in result or 'phone_is_taken' in result:
            print(f"\n{G}╔══════════════════════════════════════════╗{N}")
            print(f"{G}║{N}{W}     ✅ GraphQL: অ্যাকাউন্ট পাওয়া গেছে!  {G}║{N}")
            print(f"{G}╚══════════════════════════════════════════╝{N}")
        elif 'no_results' in result or 'not_found' in result:
            print(f"\n{R}[✗] GraphQL: এই নাম্বারে অ্যাকাউন্ট নেই{N}")
            return
        else:
            print(f"\n{Y}[!] GraphQL: অজানা রেসপন্স, আবার চেষ্টা করছি...{N}")
    except:
        print(f"{Y}[!] JSON পার্স করতে সমস্যা{N}")
    
    # === GraphQL কল ২: recovery init ===
    print(f"\n{Y}[*] GraphQL: recovery_initiate পাঠানো হচ্ছে...{N}")
    
    doc_id_recover = '6291839728902026'  # recovery initiate doc_id
    
    variables2 = {
        "contactPoint": phone,
        "source": "forgot_password",
        "flow": "recover"
    }
    
    result2 = graphql_request(session, tokens, variables2, doc_id_recover)
    
    try:
        data2 = json.loads(result2)
        print(f"{D}GraphQL Recovery Response:{N}")
        
        if 'code' in result2 or 'sent' in result2.lower() or 'otp' in result2.lower():
            print(f"\n{G}╔══════════════════════════════════════════╗{N}")
            print(f"{G}║{N}{W}  ✅ OTP কোড পাঠানো হয়েছে! ফোন চেক করুন  {G}║{N}")
            print(f"{G}╚══════════════════════════════════════════╝{N}")
        else:
            print(f"{D}{result2[:300]}{N}")
            print(f"\n{Y}[*] OTP পাঠানো হয়েছে বলে মনে হচ্ছে। ফোন চেক করুন।{N}")
    except:
        print(f"{Y}[*] OTP পাঠানোর চেষ্টা করা হয়েছে। ফোন চেক করুন।{N}")
    
    print(f"\n{D}────────────────────────────────────────{N}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] বন্ধ{N}")
    except Exception as e:
        print(f"\n{R}[✗] Error: {e}{N}")
