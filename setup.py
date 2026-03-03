#!/usr/bin/env python3
"""
دليل الإعداد والتثبيت
Setup Guide - Djezzy Tool
"""

import os
import sys
import subprocess
import platform


def print_header(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def check_python_version():
    """Check if Python version is compatible"""
    print_header("1️⃣  فحص إصدار Python")
    
    version = sys.version_info
    print(f"إصدار Python الحالي: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ الإصدار مناسب!")
        return True
    else:
        print("❌ يجب استخدام Python 3.8 أو أحدث")
        return False


def install_requirements():
    """Install required packages"""
    print_header("2️⃣  تثبيت المكتبات المطلوبة")
    
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ لم يتم العثور على {requirements_file}")
        return False
    
    try:
        print("جاري تثبيت المكتبات...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("\n✅ تم تثبيت جميع المكتبات بنجاح!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ فشل التثبيت: {e}")
        return False


def check_files():
    """Check if all required files exist"""
    print_header("3️⃣  فحص الملفات المطلوبة")
    
    required_files = {
        "djezzy_utils.py": "وحدة الأداة الأساسية",
        "djezzy_bot.py": "بوت Telegram",
        "cli_runner.py": "واجهة سطر الأوامر",
        "requirements.txt": "قائمة المكتبات",
    }
    
    all_exist = True
    for filename, description in required_files.items():
        if os.path.exists(filename):
            print(f"✅ {filename:<20} - {description}")
        else:
            print(f"❌ {filename:<20} - {description} (مفقود)")
            all_exist = False
    
    return all_exist


def setup_environment():
    """Setup environment"""
    print_header("4️⃣  إعداد البيئة")
    
    # Create logs directory if needed
    log_dir = os.path.dirname("djezzy_tool.log")
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"✅ تم إنشاء مجلد السجلات")
    
    # Check permissions
    if not os.access(".", os.W_OK):
        print("❌ لا توجد صلاحيات الكتابة في المجلد الحالي")
        return False
    
    print("✅ البيئة جاهزة للعمل")
    return True


def show_usage_guide():
    """Show usage guide"""
    print_header("📖 دليل الاستخدام")
    
    print("""
1️⃣  تشغيل بوت Telegram:
    python djezzy_bot.py
    
    (تأكد من وضع Telegram Bot Token قبل التشغيل)

2️⃣  تشغيل واجهة سطر الأوامر (CLI):
    python cli_runner.py
    
    (واجهة تفاعلية بسيطة بدون الحاجة إلى Telegram)

3️⃣  استخدام الوحدة في مشروع آخر:
    
    from djezzy_utils import *
    
    # طلب OTP
    response = request_otp("213770123456")
    
    # تسجيل الدخول
    token = login_with_otp("213770123456", "123456")
    
    # تسجيل رقم
    success, message, data = register_with_number(
        "213770123456", 
        "123456"
    )
""")


def show_telegram_setup():
    """Show Telegram bot setup instructions"""
    print_header("🤖 إعداد بوت Telegram")
    
    print("""
خطوات:

1. افتح Telegram وابحث عن @BotFather
2. أرسل /newbot
3. اتبع التعليمات:
   - اختر اسم للبوت (مثال: Djezzy Bot)
   - اختر username (مثال: djezzy_algo_bot)
4. سيرسل لك Telegram رسالة تحتوي على Token
5. انسخ Token واحفظه
6. افتح dlezzy_bot.py وضع Token في المكان المحدد:
   
   TOKEN = "YOUR_ACTUAL_BOT_TOKEN"

7. شغّل:
   python djezzy_bot.py

8. ابدأ محادثة مع البوت على Telegram
   أرسل /start
""")


def create_config_template():
    """Create config file template"""
    print_header("⚙️  إنشاء ملف الإعدادات (اختياري)")
    
    config_content = """{
    "telegram": {
        "token": "YOUR_BOT_TOKEN_HERE",
        "debug": false
    },
    "djezzy": {
        "max_attempts": 50,
        "timeout": 10,
        "retry_delay": 1
    },
    "logging": {
        "level": "INFO",
        "file": "djezzy_tool.log"
    }
}
"""
    
    config_file = "config.json"
    if not os.path.exists(config_file):
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"✅ تم إنشاء {config_file}")
        print("   يمكن تعديل الإعدادات في هذا الملف")
    else:
        print(f"ℹ️  الملف {config_file} موجود بالفعل")


def final_checklist():
    """Show final checklist"""
    print_header("✅ قائمة التحقق النهائية")
    
    checklist = [
        ("Python 3.8+", "إصدار Python"),
        ("python-telegram-bot", "مكتبة Telegram"),
        ("requests", "مكتبة requests"),
        ("djezzy_utils.py", "الملف الأساسي"),
        ("djezzy_bot.py", "ملف البوت"),
        ("cli_runner.py", "واجهة سطر الأوامر"),
    ]
    
    print("تحقق من التالي:")
    for item, desc in checklist:
        print(f"  ☐ {item:<30} - {desc}")
    
    print("\n" + "="*60)
    print("🎉 الآن أنت جاهز للبدء!")
    print("="*60)


def main():
    """Main setup process"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  دليل الإعداد - أداة اتصالات الجزائر".center(58) + "█")
    print("█" + "  Djezzy Tool - Setup Guide".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    # Run checks
    if not check_python_version():
        print("\n❌ وقف الإعداد: إصدار Python غير مناسب")
        return False
    
    if not check_files():
        print("\n⚠️  تحذير: بعض الملفات مفقودة")
    
    if input("\n🔧 تثبيت المتطلبات؟ (y/n): ").lower() == 'y':
        if not install_requirements():
            print("\n❌ فشل التثبيت")
            return False
    
    if not setup_environment():
        print("\n❌ فشل الإعداد")
        return False
    
    show_usage_guide()
    
    if input("\n📖 عرض دليل إعداد Telegram Bot؟ (y/n): ").lower() == 'y':
        show_telegram_setup()
    
    if input("\n⚙️  إنشاء ملف الإعدادات؟ (y/n): ").lower() == 'y':
        create_config_template()
    
    final_checklist()
    
    print("\n" + "="*60)
    print("\n💡 النصائح:")
    print("  • احفظ Token البوت في مكان آمن")
    print("  • لا تشارك Token مع أحد")
    print("  • استخدم متغيرات البيئة للـ Token في الإنتاج")
    print("  • اقرأ README.md للمزيد من المعلومات")
    print("  • تحقق من السجلات 'djezzy_tool.log' عند الأخطاء")
    
    print("\n" + "="*60)
    print("\n👋 البعدء:")
    print("  • تشغيل البوت: python djezzy_bot.py")
    print("  • واجهة سطر الأوامر: python cli_runner.py")
    
    print("\n" + "="*60 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ تم إيقاف الإعداد")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
