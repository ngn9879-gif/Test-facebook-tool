#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════╗
║    🔐  FB RECOVERY TOOL  v4.0          ║
║    ────  ফাইনাল এডিশন ────              ║
║     Hybrid API System                    ║
╚══════════════════════════════════════════╝
"""

import requests
import re
import os
import time
import json
import random
import string

C = '\033[96m'; G = '\033[92m'; Y = '\033[93m'
R = '\033[91m'; B = '\033[94m'; N = '\033[0m'
W = '\033[1m'; D = '\033[2m'

UAS = [
    'Mozilla/5.0 (Linux; Android 12; SM-S908E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; Redmi Note 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A344 Safari/602.1',
    'Mozilla/5.0 (Linux; Android 10; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
]

def clr():
    os.system('clear' if os.name == 'posix' else 'cls')

def bnr():
    clr()
    print(f"""{C}
╔══════════════════════════════════════════╗
║{N}{W}    🔐  FB RECOVERY  v4.0         {C}        ║
║{N}    ────  প্রো এডিশন ────           {C}        ║
║{N}{D}    হাইব্রিড API | Graph API       {C}        ║
╚══════════════════════════════════════════╝{N}""")

def fmt_phone(phone):
    clean = re.sub(r'[^0-9]', '', phone)
    if clean.startswith('880'): clean = '0' + clean[3:]
    elif clean.startswith('00880'): clean = '0' + clean[5:]
    return clean if (clean.startswith('01') and len(clean) == 11) else None

def extract_json_from_text(text, key):
    """JSON থেকে নির্দিষ্ট key খুঁজে বের করা"""
    pattern = r'"' + key + r'":"([^"]+)"'
    m = re.search(pattern, text)
    return m.group(1) if m else None

def method_mbasic(session, phone):
    """পদ্ধতি: mbasic identify"""
    print(f"\n{D}[1/4] mbasic identify API...{N}")
    try:
        r = session.get('https://mbasic.facebook.com/login/identify/?ctx=recover', timeout=12)
        
        # LSD + jazoest এক্সট্রাক্ট
        lsd = re.search(r'name="lsd"[^>]*value="([^"]*)"', r.text)
        jz = re.search(r'name="jazoest"[^>]*value="([^"]*)"', r.text)
        
        if not lsd:
            return None
            
        data = {
            'lsd': lsd.group(1),
            'jazoest': jz.group(1) if jz else '2',
            'email': phone,
            'did_submit': 'Search'
        }
        
        r2 = session.post('https://mbasic.facebook.com/login/identify/?ctx=recover', data=data, timeout=12)
        
        if 'no_results' in r2.text:
            return False
        if 'ldata=' in r2.text or 'strong' in r2.text:
            # নাম বের করি
            nm = re.search(r'<strong>([^<]+)</strong>', r2.text)
            name = nm.group(1) if nm else 'Found'
            
            # OTP পাঠানোর চেষ্টা
            ld = re.search(r'ldata=([a-zA-Z0-9_%-]+)', r2.text)
            if ld:
                r3 = session.get(f'https://mbasic.facebook.com/recover/initiate/?ldata={ld.group(1)}', timeout=10)
                
                # send_code খুঁজি
                dtsg = re.search(r'name="fb_dtsg"[^>]*value="([^"]*)"', r3.text)
                if 'send_code' in r3.text or 'Send code' in r3.text:
                    sd = {
                        'fb_dtsg': dtsg.group(1) if dtsg else lsd.group(1),
                        'jazoest': jz.group(1) if jz else '2',
                        'contact_point': phone,
                        'send_code': 'Send code via SMS'
                    }
                    r4 = session.post('https://mbasic.facebook.com/recover/initiate/', data=sd, timeout=10)
                    if 'code_sent' in r4.text or 'sent' in r4.text:
                        return 'OTP_SENT', name
            return 'EXISTS', name
        return None
    except:
        return None

def method_graphql_search(session, phone):
    """পদ্ধতি ২: Facebook GraphQL সার্চ API"""
    print(f"\n{D}[2/4] GraphQL search API...{N}")
    try:
        r = session.get('https://www.facebook.com/login/', timeout=10)
        
        # টোকেন বের করি
        fb_dtsg = re.search(r'"fb_dtsg":"([^"]+)"', r.text)
        lsd = re.search(r'"lsd":"([^"]+)"', r.text)
        
        if not fb_dtsg:
            return None
            
        headers = {
            'User-Agent': random.choice(UAS),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-FB-Friendly-Name': 'search',
            'X-FB-Connection-Type': 'WIFI',
            'Origin': 'https://www.facebook.com',
            'Referer': 'https://www.facebook.com/',
        }
        
        # GraphQL search_identity
        data = {
            'fb_dtsg': fb_dtsg.group(1),
            'lsd': lsd.group(1) if lsd else '',
            '__a': '1',
            '__user': '0',
            '__comet_req': '0',
            'jazoest': '2',
            'variables': json.dumps({
                "contact_point": phone,
                "source": "forgot_password"
            }),
            'doc_id': '5345237891345678',  # identify mutation
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'useContactPointLookupQuery',
        }
        
        r2 = session.post('https://www.facebook.com/api/graphql/', headers=headers, data=data, timeout=10)
        
        if 'email_is_taken' in r2.text or 'phone_is_taken' in r2.text or 'account_type' in r2.text:
            # নাম বের করার চেষ্টা
            nm = re.search(r'"name":"([^"]+)"', r2.text)
            name = nm.group(1) if nm else 'Found'
            return 'EXISTS', name
        elif 'no_results' in r2.text or 'not_found' in r2.text:
            return False
        return None
    except:
        return None

def method_free_reg_api(session, phone):
    """পদ্ধতি ৩: Registration API"""
    print(f"\n{D}[3/4] Registration API...{N}")
    try:
        r = session.get('https://www.facebook.com/reg/', timeout=10)
        
        csrf = re.search(r'"csrf_token":"([^"]+)"', r.text)
        lsd = re.search(r'"lsd":"([^"]+)"', r.text)
        token = csrf.group(1) if csrf else (lsd.group(1) if lsd else None)
        
        if not token:
            return None
        
        rand_user = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        
        data = {
            'email': phone,
            'username': rand_user,
            'first_name': '',
            'last_name': '',
        }
        
        headers = {
            'User-Agent': random.choice(UAS),
            'Accept': 'application/json, text/plain, */*',
            'X-CSRFToken': token,
            'X-FB-LSD': lsd.group(1) if lsd else token,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://www.facebook.com/reg/',
        }
        
        r2 = session.post(
            'https://www.facebook.com/api/v1/web/accounts/web_create_ajax/attempt/',
            headers=headers,
            data=data,
            timeout=10
        )
        
        if 'email_is_taken' in r2.text or 'phone_is_taken' in r2.text:
            return 'EXISTS', 'Found'
        elif r2.status_code == 200:
            try:
                js = r2.json()
                if js.get('status') != 'fail':
                    return 'EXISTS', 'Found'
            except:
                pass
            return False
        return None
    except:
        return None

def method_native_form(session, phone):
    """পদ্ধতি ৪: Native Facebook Lite form submit"""
    print(f"\n{D}[4/4] Native form API...{N}")
    try:
        r = session.get('https://www.facebook.com/login/identify?ctx=recover', timeout=10)
        
        lsd = re.search(r'"lsd":"([^"]+)"', r.text)
        if not lsd:
            return None
            
        # Form data prepare
        data = {
            'lsd': lsd.group(1),
            'email': phone,
            'did_submit': 'Search',
        }
        
        headers = {
            'User-Agent': random.choice(UAS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.facebook.com',
        }
        
        r2 = session.post(
            'https://www.facebook.com/ajax/login/help/identify.php?ctx=recover',
            headers=headers,
            data=data,
            timeout=10
        )
        
        if 'no_results' in r2.text:
            return False
        if 'account_switcher' in r2.text or 'recover' in r2.text or 'name' in r2.text.lower():
            return 'EXISTS', 'Found'
        return None
    except:
        return None

def main():
    bnr()
    
    print(f"\n{Y}[*] Facebook ID (ফোন নম্বর) দিন:{N}")
    print(f"{D}   যেমন: 01712345678{N}")
    phone = input(f"\n{W}➜ {N}").strip()
    
    phone = fmt_phone(phone)
    if not phone:
        print(f"\n{R}[✗] ভুল ফোন নম্বর! ০১XXXXXXXXX ফরম্যাটে দিন{N}")
        return
    
    print(f"\n{Y}[*] ফোন: {G}{phone}{N}")
    print(f"{Y}[*] ৪টি পদ্ধতি চেষ্টা করা হবে...{N}")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': random.choice(UAS),
        'Accept-Language': 'en-US,en;q=0.9,bn;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    })
    
    methods = [
        ('mbasic Identify', method_mbasic),
        ('GraphQL Search', method_graphql_search),
        ('Registration API', method_free_reg_api),
        ('Native Form', method_native_form),
    ]
    
    for name, method in methods:
        print(f"{Y}[*] {name} ট্রাই করছি...{N}")
        time.sleep(0.5)
        
        result = method(session, phone)
        
        if result and result[0] in ['EXISTS', 'OTP_SENT']:
            status, user_data = result
            print(f"\n{G}╔══════════════════════════════════════════╗{N}")
            print(f"{G}║{N}{W}     ✅ {name} কাজ করল!                 {G}║{N}")
            if user_data:
                print(f"{G}║{N}     অ্যাকাউন্ট: {user_data}              {G}║{N}")
            print(f"{G}╚══════════════════════════════════════════╝{N}")
            
            if status == 'OTP_SENT':
                print(f"\n{Y}📱 OTP পাঠানো হয়েছে! ফোন চেক করুন!{N}")
            return
        
        elif result == False:
            print(f"{R}[✗] এই নাম্বারে অ্যাকাউন্ট নেই!{N}")
            return
    
    print(f"\n{R}[✗] সব পদ্ধতি ব্যর্থ!{N}")
    print(f"{Y}[!] ফেসবুক ব্লক করেছে। কারণসমূহ:{N}")
    print(f"{Y}    ১. IP ব্লক — VPN বা মোবাইল ডাটা use করুন{N}")
    print(f"{Y}    ২. নাম্বার সঠিক না — অন্য নাম্বার টেস্ট করুন{N}")
    print(f"{Y}    ৩. রেট লিমিট — ৫-১০ মিনিট পর আবার চেষ্টা করুন{N}")
    print(f"{D}────────────────────────────────────────{N}")
    print(f"{D}টিপ: 017/018/019 দিয়ে শুরু নাম্বার use করুন{N}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] বন্ধ{N}")
    except Exception as e:
        print(f"\n{R}[✗] Error: {e}{N}")
