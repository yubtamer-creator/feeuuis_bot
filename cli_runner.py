#!/usr/bin/env python3
"""
Standalone CLI Runner - استخدام الأداة بدون البوت
يمكن استخدام djezzy_utils.py بشكل مستقل من أي مكان

استخدام:
    python cli_runner.py
"""

import sys
import os
from datetime import datetime

try:
    import djezzy_utils
except ImportError:
    print("❌ خطأ: لم يتم العثور على djezzy_utils.py")
    print("تأكد من وجود الملف في نفس المجلد")
    sys.exit(1)


def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 50)
    print("     أداة تسجيل 1 جيغا من اتصالات الجزائر")
    print("     (نسخة مستقلة - CLI)")
    print("=" * 50 + "\n")


def print_menu():
    """Print main menu"""
    print("\n" + "-" * 50)
    print("القائمة الرئيسية:")
    print("1. تسجيل رقم جديد")
    print("2. عرض الإحصائيات")
    print("3. عرض آخر التسجيلات")
    print("4. خروج")
    print("-" * 50)


def register_new_number():
    """Register a new number"""
    print("\n📱 تسجيل رقم جديد")
    print("-" * 50)
    
    while True:
        sender = input("\n📱 أدخل رقم اتصالات الجزائر (مثال: 0770123456): ").strip()
        if not sender:
            print("❌ الرقم مطلوب")
            continue
        
        try:
            sender_f = djezzy_utils.format_num(sender)
            break
        except Exception as e:
            print(f"❌ خطأ في تنسيق الرقم: {e}")
            continue
    
    print(f"✓ الرقم المنسق: {sender_f}")
    print("\n🔄 جاري إرسال كود التحقق...")
    
    otp_response = djezzy_utils.request_otp(sender_f)
    
    if otp_response and otp_response.status_code in [200, 201]:
        print("✅ تم إرسال الكود بنجاح")
        otp = input("\n📨 أدخل الكود الذي وصلك: ").strip()
        
        if not otp:
            print("❌ الكود مطلوب")
            return
        
        print("\n🔄 جاري معالجة الطلب...")
        print("📡 سيتم المحاولة حتى يتم العثور على رقم صالح...\n")
        
        def progress(msg):
            print(f"  {msg}")
        
        success, message, data = djezzy_utils.register_with_number(
            sender_f,
            otp,
            max_attempts=50,
            callback=progress
        )
        
        if success:
            print("\n" + "=" * 50)
            print("✅✅✅ تم التسجيل بنجاح! ✅✅✅")
            print("=" * 50)
            print(f"\nالرقم المرسل: {data['sender']}")
            print(f"الرقم المستقبل: {data['target']}")
            print(f"الوقت: {data['timestamp']}")
            print(f"\n🎉 حصلت على 1 جيغا مجاني!")
        else:
            print(f"\n❌ فشلت العملية")
            print(f"الرسالة: {message}")
    else:
        print("❌ فشل إرسال الكود")
        print("تحقق من الرقم وحاول مرة أخرى")


def show_statistics():
    """Show statistics"""
    count = djezzy_utils.get_registered_count()
    print("\n" + "=" * 50)
    print("📊 الإحصائيات")
    print("=" * 50)
    print(f"\n✅ عدد الأرقام المسجلة: {count}")
    print(f"📅 التاريخ والوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def show_recent():
    """Show recent registrations"""
    recent = djezzy_utils.get_recent_registrations(limit=20)
    
    print("\n" + "=" * 50)
    print("📋 آخر التسجيلات")
    print("=" * 50)
    
    if not recent:
        print("\n❌ لا توجد تسجيلات حتى الآن")
    else:
        print(f"\n📊 عدد التسجيلات: {len(recent)}\n")
        print(f"{'#':<4} {'الرقم المرسل':<15} {'الرقم المستقبل':<15} {'الوقت':<20}")
        print("-" * 54)
        
        for i, reg in enumerate(recent[::-1], 1):
            sender = reg['sender'][-10:] if len(reg['sender']) > 10 else reg['sender']
            target = reg['target'][-10:] if len(reg['target']) > 10 else reg['target']
            timestamp = reg['timestamp']
            print(f"{i:<4} {sender:<15} {target:<15} {timestamp:<20}")
    print()


def main():
    """Main function"""
    print_banner()
    
    registered = djezzy_utils.load_registered_numbers()
    if registered:
        print(f"📊 الأرقام المسجلة سابقاً: {len(registered)}\n")
    
    while True:
        print_menu()
        choice = input("\n👉 اختر رقم العملية (1-4): ").strip()
        
        if choice == "1":
            register_new_number()
        elif choice == "2":
            show_statistics()
        elif choice == "3":
            show_recent()
        elif choice == "4":
            print("\n👋 شكراً لاستخدامك الأداة. مع السلامة!\n")
            break
        else:
            print("\n❌ اختيار غير صحيح. حاول مرة أخرى")
        
        input("\n👈 اضغط Enter للمتابعة...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 تم إيقاف البرنامج بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
