#!/bin/bash

# Display guide for adding token and running on Linux

clear

cat << 'EOF'

╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║        ✅ ملفات جديدة لإضافة Token والتشغيل على Linux                  ║
║                                                                           ║
║        New Guides: Add Telegram Token & Run on Linux                     ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝


📋 الملفات الجديدة:
═══════════════════════════════════════════════════════════════════════════

1️⃣  SETUP_TOKEN_LINUX.md              📖 دليل تفصيلي (الأفضل للقراءة)
   → شرح مفصل لكل خطوة
   → أمثلة واقعية
   → حل المشاكل الشائعة

2️⃣  SETUP_TOKEN_LINUX.py              🐍 برنامج تفاعلي
   → اقرأ الدليل كاملاً في الطرفية
   → استخدم:
     $ python3 SETUP_TOKEN_LINUX.py

3️⃣  setup_token.sh                    🔧 سكريبت إعداد تفاعلي
   → خطوات تفاعلية
   → إضافة Token تلقائية
   → اختبار الإعدادات
   → استخدم:
     $ ./setup_token.sh

4️⃣  COMPLETE_GUIDE_LINUX.py           📚 دليل شامل جداً
   → شرح بالتفصيل
   → كل الطرق والبدائل
   → نصائح وحيل
   → استخدم:
     $ python3 COMPLETE_GUIDE_LINUX.py

5️⃣  QUICK_START.txt                   ⚡ ملخص سريع جداً
   → 3 خطوات فقط
   → للسريعين
   → قراءة سريعة


🚀 الخطوات السريعة:
═══════════════════════════════════════════════════════════════════════════

1️⃣  احصل على Token من Telegram:

   • افتح Telegram
   • ابحث عن: @BotFather
   • أرسل: /newbot
   • اتبع التعليمات
   • انسخ Token (الرقم الطويل)


2️⃣  أضف Token على جهازك:

   $ cd ~/Desktop/github_project/djezzy/djezzy_bot
   
   # الطريقة السهلة:
   $ ./setup_token.sh
   
   # أو يدويً:
   $ cp .env.example .env
   $ nano .env
   # ضع Token وحفظ (Ctrl+X, Y, Enter)


3️⃣  شغّل البوت على Linux:

   $ ./run.sh
   # اختر 1 للبوت


✅ جاهز!


📖 كيف تختار أفضل دليل؟
═══════════════════════════════════════════════════════════════════════════

اختر حسب احتياجك:

  📖 للقراءة:           SETUP_TOKEN_LINUX.md
  🐍 للبرمجيين:        SETUP_TOKEN_LINUX.py
  🔧 للإعداد التفاعلي: setup_token.sh
  📚 للشرح الكامل:     COMPLETE_GUIDE_LINUX.py
  ⚡ للسريعين:         QUICK_START.txt


🎯 ماذا تريد الآن؟
═══════════════════════════════════════════════════════════════════════════

اختر:

  1. اقرأ الدليل (Markdown):
     cat SETUP_TOKEN_LINUX.md

  2. شغّل الدليل التفاعلي (Python):
     python3 SETUP_TOKEN_LINUX.py

  3. برنامج الإعداد التفاعلي (Bash):
     ./setup_token.sh

  4. الدليل الشامل:
     python3 COMPLETE_GUIDE_LINUX.py

  5. ملخص سريع:
     cat QUICK_START.txt

  6. شغّل البوت مباشرة:
     ./run.sh


════════════════════════════════════════════════════════════════════════════════════════════════════

                    Ready to Start? استعد للبدء!

════════════════════════════════════════════════════════════════════════════════════════════════════

EOF

echo ""
echo "ما الذي تريد أن تفعله؟"
echo ""
read -p "اختر (1-6): " choice

case $choice in
    1)
        cat SETUP_TOKEN_LINUX.md
        ;;
    2)
        python3 SETUP_TOKEN_LINUX.py
        ;;
    3)
        ./setup_token.sh
        ;;
    4)
        python3 COMPLETE_GUIDE_LINUX.py
        ;;
    5)
        cat QUICK_START.txt
        ;;
    6)
        ./run.sh
        ;;
    *)
        echo "اختر من 1 إلى 6"
        exit 1
        ;;
esac
EOF
chmod +x /tmp/launch_guides.sh && echo "✅ تم إنشاء ملفات الأدلة بنجاح!" && echo "" && cat << 'EOF'

📍 الملفات الجديدة متاحة في:
   /home/djab/Desktop/github_project/djezzy/djezzy_bot/

📂 الملفات:
   ✅ SETUP_TOKEN_LINUX.md         → دليل مفصل 
   ✅ SETUP_TOKEN_LINUX.py         → برنامج Py
   ✅ setup_token.sh               → برنامج Bash
   ✅ COMPLETE_GUIDE_LINUX.py      → دليل شامل
   ✅ QUICK_START.txt              → ملخص سريع

🚀 للبدء:
   cd ~/Desktop/github_project/djezzy/djezzy_bot
   
   # اختر واحد:
   ./setup_token.sh                 (تفاعلي)
   python3 SETUP_TOKEN_LINUX.py     (دليل Py)
   cat SETUP_TOKEN_LINUX.md         (دليل مفصل)

✅ استمتع!

EOF
