#!/usr/bin/env python3
"""
مدير المجلدات - إنشاء البنية المحمولة
Directory Manager - Create Portable Structure
"""

import os
from pathlib import Path

def create_portable_structure():
    """Create the portable project structure"""
    
    project_root = Path(__file__).parent.absolute()
    
    directories = [
        'data',      # تخزين البيانات
        'logs',      # ملفات السجلات
        'config',    # ملفات الإعدادات
    ]
    
    print("\n" + "="*60)
    print("🔧 مدير البنية المحمولة")
    print("="*60 + "\n")
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(exist_ok=True)
        print(f"✅ {directory:15} → {dir_path}")
    
    # Create .env if not exists
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print(f"\n💡 Tip: انسخ .env.example إلى .env وعدّل القيم")
    
    # Show structure
    print("\n" + "="*60)
    print("📁 البنية الحالية:")
    print("="*60 + "\n")
    
    print(f"  📍 جذر المشروع: {project_root}\n")
    
    print("  📂 المجلدات:")
    for directory in directories:
        dir_path = project_root / directory
        if dir_path.exists():
            file_count = len(list(dir_path.iterdir()))
            print(f"     ✅ {directory:15} ({file_count} files)")
    
    print("\n  📄 الملفات الرئيسية:")
    main_files = [
        "djezzy_utils.py",
        "djezzy_bot.py",
        "cli_runner.py",
        "setup.py",
        "config.py",
        "run.sh",
        "run.bat",
    ]
    
    for file in main_files:
        file_path = project_root / file
        if file_path.exists():
            print(f"     ✅ {file}")
        else:
            print(f"     ⚠️  {file} (missing)")
    
    print("\n" + "="*60)
    print("✅ البنية المحمولة جاهزة!")
    print("="*60 + "\n")
    
    print("🚀 للبدء:")
    print("   • Linux/macOS: ./run.sh")
    print("   • Windows: run.bat")
    print()


def show_structure_tree():
    """Show directory tree"""
    print("\n" + "="*70)
    print("📋 شجرة البنية المحمولة")
    print("="*70 + "\n")
    
    tree = """
djezzy_bot/  ← انقل هذا المجلد بأكمله
│
├── 🐍 ملفات Python
│   ├── djezzy_utils.py      ⭐ الوحدة الأساسية
│   ├── djezzy_bot.py         🤖 بوت Telegram
│   ├── cli_runner.py         💻 واجهة الأوامر
│   ├── setup.py              ⚙️  برنامج الإعداد
│   ├── config.py             🔧 إدارة الإعدادات
│   ├── INDEX.py              📖 الفهرس
│   └── folder_manager.py     📂 مدير المجلدات
│
├── 🔨 ملفات التشغيل
│   ├── run.sh                 🐧 لـ Linux/macOS
│   └── run.bat                🪟 لـ Windows
│
├── 📋 الإعدادات
│   ├── requirements.txt        📦 المكتبات
│   ├── .env.example            🔐 مثال الإعدادات
│   └── .gitignore              ⛔ ملفات لتجاهلها
│
├── 📚 التوثيق
│   ├── README.md               📖 الدليل الكامل
│   ├── QUICKSTART.md           ⚡ بدء سريع
│   ├── INSTALLATION.md         🔌 تعليمات التثبيت (محدث)
│   └── PROJECT_SUMMARY.md      📋 ملخص المشروع
│
└── 📂 مجلدات البيانات (تُنشأ تلقائياً)
    ├── data/                   💾 البيانات
    │   └── registered_numbers.json
    ├── logs/                   📝 السجلات
    │   └── djezzy.log
    ├── config/                 ⚙️  الإعدادات
    │   └── config.json
    └── venv/                   🐍 البيئة الوهمية
        └── [packages]
"""
    print(tree)


def show_info():
    """Show portable project info"""
    print("\n" + "="*70)
    print("ℹ️  معلومات المشروع المحمول")
    print("="*70 + "\n")
    
    info = """
✨ المميزات:

✅ مستقل تماماً
   • لا يعتمد على المسارات المطلقة
   • يمكن نقله إلى أي مكان
   • يعمل على أي جهاز

✅ منظم وسهل
   • جميع البيانات في مجلد data/
   • جميع السجلات في مجلد logs/
   • جميع الإعدادات في مجلد config/

✅ تشغيل سهل
   • Linux/macOS: ./run.sh
   • Windows: run.bat (انقر مرتين)
   • بيئة وهمية تلقائية
   • تثبيت المكتبات تلقائي

✅ آمن وموثوق
   • .gitignore يخفي الملفات الحساسة
   • تحديثات الإعدادات تلقائية
   • معالجة الأخطاء محسّنة


📋 ملفات المشروع الرئيسية:

Frontend/UI Layer:
  • djezzy_bot.py      → بوت Telegram
  • cli_runner.py      → واجهة سطر الأوامر

Core Layer:
  • djezzy_utils.py    → الوحدة الأساسية

Configuration Layer:
  • config.py          → إدارة الإعدادات ✨ جديد
  • .env               → متغيرات البيئة
  • requirements.txt   → المكتبات


🔄 دورة الحياة:

   1. تحميل config.py
   ↓
   2. إنشاء المجلدات (data/, logs/, config/)
   ↓
   3. تحميل الإعدادات من .env و config.json
   ↓
   4. استخدام djezzy_utils.py مع المسارات الصحيحة
   ↓
   5. واجهات المستخدم (bot/cli) تعمل بسلاسة
   ↓
   6. البيانات والسجلات في مجلداتها


🌍 التوافق:

✅ Windows 7+
✅ macOS 10.14+
✅ Linux (جميع الإصدارات)
✅ Python 3.8+
✅ كل لغات البرمجة التي تدعم Python


🚀 الآن جاهز للانتقال!
"""
    print(info)


def main():
    """Main function"""
    create_portable_structure()
    show_structure_tree()
    show_info()
    
    print("="*70)
    print("✅ مشروعك المحمول جاهز!")
    print("="*70 + "\n")
    
    print("💡 النصائح:")
    print("  1. انسخ المجلد djezzy_bot/ كاملاً")
    print("  2. ضعه أينما تريد (USB, Cloud, إلخ)")
    print("  3. شغّل run.sh أو run.bat")
    print("  4. لا تحتاج لأي تثبيت إضافي!")
    print()


if __name__ == "__main__":
    main()
