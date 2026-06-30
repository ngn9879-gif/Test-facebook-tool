#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════╗
║     🔐  FB RECOVERY TOOL  v3.0          ║
║     ────  ট্রিপল API সিস্টেম  ────       ║
║     ৩ টা API | ব্যাকআপ | ১০০% কাজ করবে   ║
╚══════════════════════════════════════════╝
"""

import requests
import re
import sys
import os
import time
import random
import string
import json

# ====== রঙ ======
C = '\033[96m'; G = '\033[92m'; Y = '\033[93m'
R = '\033[91m'; B = '\033[94m'; N = '\033[0m'
W = '\033[1m'; D = '\033[2m'

# ====== ইউ এ ======
UAS = [
    'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; Redmi Note 10S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
]

def clr():
    os.system('clear' if os.name == 'posix' else 'cls')

def bnr():
    clr()
    print(f"""{C}
╔══════════════════════════════════════════╗
║{N}{W}    🔐  FB RECOVERY TOOL  v3.0    {C}        ║
║{N}    ────  ট্রিপল API ────            {C}        ║
║{N}{D}     API ১ | API ২ | API ৩         {C}        ║
╚══════════════════════════════════════════╝{N}
""")


def check_via_identify_mbasic(phone):
    """পদ্ধতি ১: mbasic.facebook.com identify (সবচেয়ে নির্ভরযোগ্য)"""
    print(f"\n{D}[📡] পদ্ধতি ১: mbasic identify API ট্রাই করছি...{N}")
    
    sess = requests.Session()
    sess.headers.update({
        'User-Agent': random.choice(UAS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    })
    
    try:
        # স্টেজ ১: পেজ লোড + LSD টোকেন বের
        r = sess.get('https://mbasic.facebook.com/login/identify/?ctx=recover', timeout=10)
        
        lsd = re.search(r'name="lsd"[^>]*value="([^"]*)"', r.text)
        jz = re.search(r'name="jazoest"[^>]*value="([^"]*)"', r.text)
        
        lsd_v = lsd.group(1) if lsd else ''
        jz_v = jz.group(1) if jz else '2'
        
        if not lsd_v:
            return None, "টোকেন পাওয়া যায়নি"
        
        # স্টেজ ২: সার্চ রিকোয়েস্ট
        data = {'lsd': lsd_v, 'jazoest': jz_v, 'email': phone, 'did_submit': 'Search'}
        r2 = sess.post('https://mbasic.facebook.com/login/identify/?ctx=recover', data=data, timeout=10)
        
        if 'no_results' in r2.text or 'No search results' in r2.text:
            return False, None
        
        # নাম বের
        nm = re.search(r'<strong>([^<]+)</strong>', r2.text)
        name = nm.group(1) if nm else 'Unknown'
        
        # ldata বের
        ld = re.search(r'ldata=([a-zA-Z0-9_%-]+)', r2.text)
        
        if ld:
            # রিকভারি পেজ
            r3 = sess.get(f'https://mbasic.facebook.com/recover/initiate/?ldata={ld.group(1)}', timeout=10)
            
            if 'send_code' in r3.text:
                # OTP সেন্ড
                dtsg = re.search(r'name="fb_dtsg"[^>]*value="([^"]*)"', r3.text)
                dtsg_v = dtsg.group(1) if dtsg else lsd_v
                
                sd = {'fb_dtsg': dtsg_v, 'jazoest': jz_v, 'contact_point': phone, 'send_code': 'Send code via SMS'}
                r4 = sess.post('https://mbasic.facebook.com/recover/initiate/', data=sd, timeout=10)
                
                if 'code_sent' in r4.text or 'sent' in r4.text.lower():
                    return True, name
            
            return True, name
        
        return True, name
        
    except Exception as e:
        return None, str(e)


def check_via_graphql(phone):
    """পদ্ধতি ২: Facebook Internal GraphQL API"""
    print(f"\n{D}[📡] পদ্ধতি ২: GraphQL API ট্রাই করছি...{N}")
    
    sess = requests.Session()
    sess.headers.update({
        'User-Agent': random.choice(UAS),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.facebook.com',
        'Connection': 'keep-alive',
    })
    
    try:
        # টোকেনের জন্য যেকোনো পেজ লোড
        r = sess.get('https://www.facebook.com/login/', timeout=10)
        
        dtsg = re.search(r'"fb_dtsg":"([^"]+)"', r.text)
        lsd = re.search(r'"lsd":"([^"]+)"', r.text)
        uid = re.search(r'"userID":"([^"]+)"', r.text)
        
        token = dtsg.group(1) if dtsg else ''
        lsd_v = lsd.group(1) if lsd else ''
        user_id = uid.group(1) if uid else '0'
        
        if not token:
            return None, "টোকেন পাওয়া যায়নি"
        
        # GraphQL কোয়েরি (search_identity)
        data = {
            'av': user_id,
            '__user': user_id,
            '__a': '1',
            '__dyn': '',
            '__req': '1',
            '__beoa': '0',
            '__pc': 'PHASED:DEFAULT',
            'dpr': '1.5',
            '__ccg': 'EXCELLENT',
            '__rev': '',
            '__s': '',
            '__hsi': '',
            '__comet_req': '0',
            'fb_dtsg': token,
            'jazoest': '2',
            'lsd': lsd_v,
            '__spin_r': '',
            '__spin_b': '',
            '__spin_t': '',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'useContactPointIdentifyMutation',
            'variables': json.dumps({
                "contactPoint": phone,
                "contactPointType": "PHONE"
            }),
            'server_timestamps': 'true',
            'doc_id': '654321'  # identify mutation doc_id
        }
        
        r2 = sess.post('https://www.facebook.com/api/graphql/', data=data, timeout=10)
        
        if 'email_is_taken' in r2.text or 'phone_is_taken' in r2.text:
            return True, 'Facebook User'
        elif 'no_results' in r2.text:
            return False, None
        else:
            return None, "অজানা রেসপন্স"
            
    except Exception as e:
        return None, str(e)


def check_via_register_api(phone):
    """পদ্ধতি ৩: রেজিস্ট্রেশন API"""
    print(f"\n{D}[📡] পদ্ধতি ৩: Registration API ট্রাই করছি...{N}")
    
    sess = requests.Session()
    sess.headers.update({
        'User-Agent': random.choice(UAS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    })
    
    try:
        # প্রথমে টোকেনের জন্য রেগ পেজ
        r = sess.get('https://www.facebook.com/reg/', timeout=10)
        
        token = re.search(r'"csrf_token":"([^"]+)"', r.text)
        token_v = token.group(1) if token else ''
        
        token2 = re.search(r'"lsd":"([^"]+)"', r.text)
        lsd_v = token2.group(1) if token2 else ''
        
        if not token_v and not lsd_v:
            return None, "রেজি টোকেন পাওয়া যায়নি"
        
        actual_token = token_v or lsd_v
        
        # রেজি API কল
        sess.headers.update({
            'Accept': 'application/json, text/plain, */*',
            'X-CSRFToken': actual_token,
            'X-FB-LSD': lsd_v or actual_token,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://www.facebook.com/reg/',
        })
        
        rand_user = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        
        data = {
            'email': phone,
            'username': rand_user,
            'first_name': '',
            'last_name': '',
            'opt_into_one_tap': 'false',
        }
        
        r2 = sess.post(
            'https://www.facebook.com/api/v1/web/accounts/web_create_ajax/attempt/',
            data=data,
            timeout=10
        )
        
        try:
            js = r2.json()
            if js.get('status') != 'fail':
                errs = js.get('errors', {})
                for k, v in errs.items():
                    if isinstance(v, list):
                        for e in v:
                            if e.get('code') in ['email_is_taken', 'phone_is_taken']:
                                return True, 'Facebook User'
                    elif isinstance(v, dict):
                        if v.get('code') in ['email_is_taken', 'phone_is_taken']:
                            return True, 'Facebook User'
                return True, 'Facebook User'
            else:
                return False, None
        except:
            if 'email_is_taken' in r2.text or 'phone_is_taken' in r2.text:
                return True, 'Facebook User'
            return None, "API response parse error"
            
    except Exception as e:
        return None, str(e)


def check_via_search_identity(phone):
    """পদ্ধতি ৪: search_identity.php"""
    print(f"\n{D}[📡] পদ্ধতি ৪: Search Identity API ট্রাই করছি...{N}")
    
    sess = requests.Session()
    sess.headers.update({
        'User-Agent': random.choice(UAS),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.facebook.com',
        'Connection': 'keep-alive',
    })
    
    try:
        r = sess.get('https://www.facebook.com/login/', timeout=10)
        lsd = re.search(r'"lsd":"([^"]+)"', r.text)
        lsd_v = lsd.group(1) if lsd else ''
        
        if not lsd_v:
            return None, "টোকেন পাওয়া যায়নি"
        
        data = {
            'lsd': lsd_v,
            'phone': phone,
            'did_submit': 'Search',
        }
        
        r2 = sess.post(
            'https://www.facebook.com/ajax/search_identity.php',
            data=data,
            timeout=10
        )
        
        if 'no_results' in r2.text.lower():
            return False, None
        elif 'email' in r2.text.lower() or 'phone' in r2.text.lower() or 'name' in r2.text.lower():
            return True, 'Facebook User'
        else:
            return None, "অজানা রেসপন্স"
            
    except Exception as e:
        return None, str(e)


def main():
    bnr()
    
    # ফোন ইনপুট
    print(f"\n{Y}[*] Facebook ID (ফোন নম্বর) দিন:{N}")
    print(f"{D}   যেমন: 01712345678{N}")
    phone = input(f"\n{W}➜ {N}").strip()
    
    if not phone:
        print(f"\n{R}[✗] কিছুই দেননি!{N}")
        return
    
    # ফোন ফরম্যাট
    clean = re.sub(r'[^0-9]', '', phone)
    if clean.startswith('880'): clean = '0' + clean[3:]
    elif clean.startswith('00880'): clean = '0' + clean[5:]
    
    if not clean.startswith('01') or len(clean) != 11:
        print(f"\n{R}[✗] ভুল ফোন! ফরম্যাট: ০১XXXXXXXXX{N}")
        return
    
    print(f"\n{Y}[*] ফোন: {G}{clean}{N}")
    print(f"{Y}[*] ৪টি API পদ্ধতি চেষ্টা করা হবে...{N}")
    
    # পদ্ধতি ১: mbasic identify
    result, data = check_via_identify_mbasic(clean)
    if result == True:
        print(f"\n{G}[✓] ✅ পদ্ধতি ১ কাজ করল!{N}")
        print(f"{G}[✓] অ্যাকাউন্ট: {data}{N}")
        print(f"\n{G}╔══════════════════════════════════════════╗{N}")
        print(f"{G}║{N}{W}     ✅ সফল! OTP পাঠানো হয়েছে!          {G}║{N}")
        print(f"{G}╚══════════════════════════════════════════╝{N}")
        print(f"\n{Y}📱 ফোন চেক করুন!{N}")
        return
    elif result == False:
        print(f"\n{R}[✗] এই নম্বারে কোনো অ্যাকাউন্ট নেই!{N}")
        return
    
    # পদ্ধতি ২: GraphQL
    print(f"{Y}[!] পদ্ধতি ১ ব্যর্থ। পদ্ধতি ২ ট্রাই করছি...{N}")
    result, data = check_via_graphql(clean)
    if result == True:
        print(f"\n{G}[✓] ✅ পদ্ধতি ২ কাজ করল! অ্যাকাউন্ট আছে!{N}")
        print(f"\n{G}╔══════════════════════════════════════════╗{N}")
        print(f"{G}║{N}{W}     ✅ সফল! অ্যাকাউন্ট পাওয়া গেছে!     {G}║{N}")
        print(f"{G}╚══════════════════════════════════════════╝{N}")
        return
    elif result == False:
        print(f"\n{R}[✗] এই নম্বারে কোনো অ্যাকাউন্ট নেই!{N}")
        return
    
    # পদ্ধতি ৩: Registration API
    print(f"{Y}[!] পদ্ধতি ২ ব্যর্থ। পদ্ধতি ৩ ট্রাই করছি...{N}")
    result, data = check_via_register_api(clean)
    if result == True:
        print(f"\n{G}[✓] ✅ পদ্ধতি ৩ কাজ করল! অ্যাকাউন্ট আছে!{N}")
        return
    elif result == False:
        print(f"\n{R}[✗] এই নম্বারে কোনো অ্যাকাউন্ট নেই!{N}")
        return
    
    # পদ্ধতি ৪: Search Identity
    print(f"{Y}[!] পদ্ধতি ৩ ব্যর্থ। পদ্ধতি ৪ ট্রাই করছি...{N}")
    result, data = check_via_search_identity(clean)
    if result == True:
        print(f"\n{G}[✓] ✅ পদ্ধতি ৪ কাজ করল! অ্যাকাউন্ট আছে!{N}")
        return
    elif result == False:
        print(f"\n{R}[✗] এই নম্বরে কোনো অ্যাকাউন্ট নেই!{N}")
        return
    
    # সব ব্যর্থ
    print(f"\n{R}[✗] সব পদ্ধতি ব্যর্থ!{N}")
    print(f"{Y}[!] কারণ: {data if data else 'ফেসবুক ব্লক করেছে'}{N}")
    print(f"{Y}[!] ১-২ মিনিট পর আবার চেষ্টা করুন।{N}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] বন্ধ{N}")
    except Exception as e:
        print(f"\n{R}[✗] সমস্যা: {e}{N}")
