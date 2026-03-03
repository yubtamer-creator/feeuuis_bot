#!/usr/bin/env python3
"""
🎯 دليل شامل - إضافة Token والتشغيل على Linux
Complete Guide - Add Token & Run on Linux
"""

def main():
    guide = """

╔═════════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║        🚀 دليل شامل: إضافة Telegram Bot Token و التشغيل على Linux       ║
║                                                                             ║
║    Complete Guide: Add Telegram Bot Token & Run on Linux                   ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  الجزء 1️⃣: الحصول على Telegram Bot Token
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 من تطبيق Telegram (الهاتف أو سطح المكتب):

  الخطوة 1: ابحث عن @BotFather
    • اضغط على عدسة البحث
    • اكتب: @BotFather
    • اختر النتيجة الأولى

  الخطوة 2: ابدأ محادثة
    • اضغط "START"
    • أو أرسل: /start

  الخطوة 3: أنشئ بوت جديد
    • أرسل: /newbot
    
  الخطوة 4: أجب على الأسئلة
    • Q: "Alright, a new bot. How are we going to call it?"
      A: اكتب: Djezzy Bot
      (أي اسم تريده)
    
    • Q: "Good. Now let's choose a username for your bot."
      A: اكتب: djezzy_algo_bot
      (يجب أن ينتهي بـ _bot)

  الخطوة 5: احصل على Token
    • ستتلقى رسالة تقول: "Done! Congratulations on your new bot."
    • ستجد: "Use this token to access the HTTP API:"
    • متبوعة برقم طويل مثل: 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh

👉 انسخ هذا الرقم!


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  الجزء 2️⃣: إضافة Token على Linux
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 الطريقة الأسهل - برنامج تفاعلي:

  $ cd ~/Desktop/github_project/djezzy/djezzy_bot

  $ chmod +x setup_token.sh

  $ ./setup_token.sh

  سيطلب منك Token - الصقه!


📱 الطريقة اليدوية:

  1. انتقل للمجلد:
     $ cd ~/Desktop/github_project/djezzy/djezzy_bot

  2. انسخ الملف النموذجي:
     $ cp .env.example .env

  3. افتح محرر النصوص:
     $ nano .env
     
     (أو استخدم: vi .env أو gedit .env)

  4. ابحث عن هذا السطر:
     TELEGRAM_BOT_TOKEN=your_bot_token_here_paste_your_actual_token

  5. استبدله بـ Token الحقيقي:
     TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
     
     (استخدم Token الذي نسخته من BotFather)

  6. احفظ الملف:
     • في nano: Ctrl + X، ثم اكتب: Y، ثم اضغط: Enter
     • في vi: اضغط Esc، اكتب: :wq، اضغط: Enter


✅ تحقق من أن Token موجود:

  $ cat .env
  
  ستظهر:
  TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  الجزء 3️⃣: التشغيل على Linux
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 الطريقة الأسهل:

  $ cd ~/Desktop/github_project/djezzy/djezzy_bot

  $ chmod +x run.sh

  $ ./run.sh

  ستظهر قائمة:
  ════════════════════════════════════════
  1️⃣  🤖 بوت Telegram
  2️⃣  💻 واجهة سطر الأوامر (CLI)
  3️⃣  🔧 برنامج الإعداد
  4️⃣  📖 عرض الفهرس
  5️⃣  ❌ خروج

  اختر: 1

  ثم:
  - قد يطلب تثبيت مكتبات (سيفعله تلقائياً)
  - ستظهر رسالة: "🤖 تم بدء البوت..."

✅ البوت يعمل!


🚀 الطريقة اليدوية:

  $ cd ~/Desktop/github_project/djezzy/djezzy_bot

  # 1. أنشئ بيئة وهمية
  $ python3 -m venv venvء

  # 2. فعّلها
  $ source venv/bin/activate
  
  (سترى (venv) في بداية السطر)

  # 3. ثبّت المكتبات
  $ pip install -r requirements.txt

  # 4. شغّل البوت
  $ python3 djezzy_bot.py


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  الجزء 4️⃣: اختبر البوت
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ من تطبيق Telegram:

  1. ابحث عن اسم البوت الذي أنشأته
     مثال: @djezzy_algo_bot

  2. افتح المحادثة

  3. اضغط: START
     أو أرسل: /start

  4. ستظهر قائمة البوت! 🎉


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  البحث عن المشاكل 🔍
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ خطأ: "Python not found"

  ✓ تأكد من تثبيت Python:
    $ python3 --version

  ✓ إذا لم يكن مثبت:
    $ sudo apt update
    $ sudo apt install python3 python3-pip


❌ خطأ: "Permission denied" (عند تشغيل run.sh)

  ✓ اجعل الملف قابل للتنفيذ:
    $ chmod +x run.sh


❌ خطأ: ".env: No such file or directory"

  ✓ انسخ الملف النموذجي:
    $ cp .env.example .env


❌ خطأ: "Token invalid" (من الخادم)

  ✓ تأكد من:
    1. Token الصحيح من @BotFather ✓
    2. بدون مسافات إضافية في البداية أو النهاية ✓
    3. ملف .env يحتوي على Token ✓


❌ خطأ: "ModuleNotFoundError: No module named 'telegram'"

  ✓ ثبّت المكتبات:
    $ pip install -r requirements.txt

  ✓ أو في البيئة الوهمية:
    $ source venv/bin/activate
    $ pip install -r requirements.txt


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  نصائح ذهبية 💡
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 الأمان:
   • الملف .env محمي من Git (في .gitignore)
   • لا تشارك Token مع أحد
   • لا تضعه على GitHub


💡 التشغيل في الخلفية:

   # استخدم nohup
   $ nohup python3 djezzy_bot.py &

   # أو استخدم screen
   $ screen
   $ python3 djezzy_bot.py
   (Ctrl+A ثم D للخروج)

   # للعودة:
   $ screen -r


💡 الاطلاع على السجلات:

   # آخر 50 سطر:
   $ tail -50 logs/djezzy.log

   # مراقبة مباشرة:
   $ tail -f logs/djezzy.log

   # البحث عن أخطاء:
   $ grep ERROR logs/djezzy.log


💡 إيقاف البوت:

   # إذا كان يعمل في الواجهة الحالية:
   Ctrl + C

   # إذا كان في الخلفية:
   $ pkill -f "python3 djezzy_bot"


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  الملخص السريع 📝
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  من BotFather على Telegram: احصل على Token

2️⃣  على جهازك:
    cd ~/Desktop/github_project/djezzy/djezzy_bot
    cp .env.example .env
    nano .env
    (أضف Token والحفظ)

3️⃣  شغّل:
    ./run.sh
    (اختر 1)

✅ جاهز!


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  هل تحتاج مساعدة؟ 📚
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

اقرأ هذه الملفات بالعربية:

  • SETUP_TOKEN_LINUX.md  → دليل تفصيلي
  • START_HERE.md         → دليل البدء
  • README.md             → الدليل الكامل
  • QUICKSTART.md         → بدء سريع


شغّل هذه البرامج:

  $ python3 SETUP_TOKEN_LINUX.py    → دليل تفاعلي
  $ ./setup_token.sh                → إعداد تفاعلي
  $ python3 INDEX.py                → الفهرس الكامل


═════════════════════════════════════════════════════════════════════════════════

                        استمتع بالبوت! 🚀

                   Made with ❤️  - مارس 2024

═════════════════════════════════════════════════════════════════════════════════
"""
    
    print(guide)


if __name__ == "__main__":
    main()
