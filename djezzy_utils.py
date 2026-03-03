#!/usr/bin/env python3
"""
Djezzy Registration Tool - Standalone Utility Module
أداة تسجيل اتصالات الجزائر - وحدة مستقلة
"""

import requests
import random
import time
import logging
import json
from datetime import datetime
import os

# Import configuration
try:
    from config import REGISTERED_NUMBERS_FILE, LOG_FILE, ensure_data_dirs
except ImportError:
    # Fallback if config module is not available
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).parent.absolute()
    DATA_DIR = PROJECT_ROOT / "data"
    LOGS_DIR = PROJECT_ROOT / "logs"
    DATA_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    REGISTERED_NUMBERS_FILE = DATA_DIR / "registered_numbers.json"
    LOG_FILE = LOGS_DIR / "djezzy.log"
    def ensure_data_dirs(): pass

# Ensure directories exist
ensure_data_dirs()

# Configure logging with absolute path
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(str(LOG_FILE)),
        logging.StreamHandler()
    ]
)

HEADERS = {
    'User-Agent': "MobileApp/3.0.0",
    'Accept': "application/json",
    'Content-Type': "application/json",
    'accept-language': "ar",
    'Connection': "keep-alive"
}


def load_registered_numbers():
    """تحميل الأرقام المسجلة من ملف JSON"""
    if os.path.exists(str(REGISTERED_NUMBERS_FILE)):
        try:
            with open(str(REGISTERED_NUMBERS_FILE), 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"خطأ في تحميل الأرقام: {e}")
            return []
    return []


def save_registered_number(number_data):
    """حفظ رقم مسجل جديد"""
    try:
        numbers = load_registered_numbers()
        numbers.append(number_data)
        with open(str(REGISTERED_NUMBERS_FILE), 'w', encoding='utf-8') as f:
            json.dump(numbers, f, ensure_ascii=False, indent=2)
        logging.info(f"تم حفظ الرقم: {number_data}")
    except Exception as e:
        logging.error(f"خطأ في حفظ الرقم: {e}")


def format_num(phone):
    """تنسيق رقم الهاتف إلى صيغة 213..."""
    phone = str(phone).strip()
    if phone.startswith('0'):
        return "213" + phone[1:]
    elif not phone.startswith('213'):
        return "213" + phone
    return phone


def generate_random_djezzy_no():
    """توليد رقم دجزي عشوائي"""
    prefix = random.choice(["077", "078", "079"])
    number = prefix + "".join([str(random.randint(0, 9)) for _ in range(7)])
    return number


def request_otp(msisdn):
    """طلب كود OTP للرقم"""
    url = "https://apim.djezzy.dz/mobile-api/oauth2/registration"
    params = {
        'msisdn': msisdn,
        'client_id': "87pIExRhxBb3_wGsA5eSEfyATloa",
        'scope': "smsotp"
    }
    payload = {
        "consent-agreement": [{"marketing-notifications": False}],
        "is-consent": True
    }
    try:
        res = requests.post(url, params=params, json=payload, headers=HEADERS, timeout=10)
        logging.info(f"request_otp status: {res.status_code} body: {res.text}")
        return res
    except Exception as e:
        logging.error(f"خطأ في طلب OTP: {e}")
        return None


def login_with_otp(mobile_number, otp):
    """تسجيل الدخول باستخدام OTP"""
    payload = {
        'otp': otp,
        'mobileNumber': mobile_number,
        'scope': "djezzyAppV2",
        'client_id': "87pIExRhxBb3_wGsA5eSEfyATloa",
        'client_secret': "uf82p68Bgisp8Yg1Uz8Pf6_v1XYa",
        'grant_type': "mobile"
    }
    try:
        res = requests.post(
            "https://apim.djezzy.dz/mobile-api/oauth2/token",
            data=payload,
            headers={'User-Agent': "MobileApp/3.0.0"},
            timeout=10
        )
        logging.info(f"login_with_otp status: {res.status_code} body: {res.text}")
        if res.status_code == 200:
            j = res.json()
            token = j.get('access_token') or j.get('accessToken')
            if token:
                return f"Bearer {token}"
        return None
    except Exception as e:
        logging.error(f"خطأ في تسجيل الدخول: {e}")
        return None


def send_invitation(token, sender, receiver):
    """إرسال دعوة لرقم معين"""
    try:
        url = f"https://apim.djezzy.dz/mobile-api/api/v1/services/mgm/send-invitation/{sender}"
        payload = {"msisdnReciever": receiver}
        headers = {**HEADERS, 'Authorization': token}
        inv = requests.post(url, json=payload, headers=headers, timeout=10)
        logging.info(f"send-invitation status: {inv.status_code} body: {inv.text}")
        if inv.status_code in [200, 201]:
            return True
        # محاولة بديلة إذا كان الخادم يتوقع msisdnReceiver
        alt_payload = {"msisdnReceiver": receiver}
        alt = requests.post(url, json=alt_payload, headers=headers, timeout=10)
        logging.info(f"send-invitation (alt) status: {alt.status_code} body: {alt.text}")
        return alt.status_code in [200, 201]
    except Exception as e:
        logging.error(f"خطأ في إرسال الدعوة: {e}")
        return False


def activate_reward(token, sender):
    """تفعيل المكافأة (1 جيغا)"""
    try:
        url = f"https://apim.djezzy.dz/mobile-api/api/v1/services/mgm/activate-reward/{sender}"
        payload = {"packageCode": "MGMBONUS1Go"}
        headers = {**HEADERS, 'Authorization': token}
        act = requests.post(url, json=payload, headers=headers, timeout=10)
        logging.info(f"activate-reward status: {act.status_code} body: {act.text}")
        return act.status_code in [200, 201]
    except Exception as e:
        logging.error(f"خطأ في تفعيل المكافأة: {e}")
        return False


def register_with_number(sender_number, otp, max_attempts=50, callback=None):
    """
    محاولة تسجيل رقم مع OTP
    
    Args:
        sender_number: الرقم المرسل
        otp: كود التحقق
        max_attempts: عدد محاولات الإرسال القصوى
        callback: دالة اختيارية للإبلاغ عن التقدم
    
    Returns:
        tuple: (success: bool, message: str, data: dict)
    """
    logging.info(f"محاولة تسجيل الدخول للرقم {sender_number}")
    
    if callback:
        callback(f"🔄 جاري تسجيل الدخول للرقم {sender_number}...")
    
    token = login_with_otp(sender_number, otp)
    if not token:
        msg = "❌ فشل تسجيل الدخول"
        logging.error(msg)
        if callback:
            callback(msg)
        return False, msg, {}

    for attempt in range(max_attempts):
        target = generate_random_djezzy_no()
        target_f = format_num(target)
        msg = f"محاولة {attempt + 1}/{max_attempts}: إرسال دعوة للرقم {target}"
        logging.info(msg)
        if callback:
            callback(msg)

        if send_invitation(token, sender_number, target_f):
            logging.info(f"✅ تم إرسال الدعوة بنجاح للرقم {target}")
            if callback:
                callback(f"✅ تم إرسال الدعوة للرقم {target}")
            
            otp_resp = request_otp(target_f)
            if otp_resp is None:
                logging.warning("لم يتم استلام استجابة OTP للهدف")
            time.sleep(2)

            if activate_reward(token, sender_number):
                success_msg = f"🎉 تم تفعيل 1 جيغا بنجاح باستخدام الرقم {target}"
                logging.info(success_msg)
                if callback:
                    callback(success_msg)
                
                number_data = {
                    "sender": sender_number,
                    "target": target,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "success"
                }
                save_registered_number(number_data)
                return True, success_msg, number_data
            else:
                warn_msg = f"❌ فشل تفعيل المكافأة مع الرقم {target}"
                logging.warning(warn_msg)
                if callback:
                    callback(warn_msg)
        else:
            warn_msg = f"❌ فشل إرسال الدعوة للرقم {target}"
            logging.warning(warn_msg)
            if callback:
                callback(warn_msg)

        time.sleep(1)

    error_msg = "❌ فشلت جميع محاولات إرسال الدعوات"
    logging.error(error_msg)
    if callback:
        callback(error_msg)
    return False, error_msg, {}


def get_registered_count():
    """الحصول على عدد الأرقام المسجلة"""
    return len(load_registered_numbers())


def get_recent_registrations(limit=5):
    """الحصول على آخر تسجيلات"""
    all_registered = load_registered_numbers()
    return all_registered[-limit:] if all_registered else []
