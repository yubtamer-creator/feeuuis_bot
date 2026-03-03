#!/usr/bin/env python3
"""
دليل إضافة Token والتشغيل على Linux
Guide to Add Telegram Bot Token & Run on Linux
"""

def print_guide():
    guide = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║        🤖 دليل إضافة Telegram Bot Token و التشغيل على Linux    ║
║                                                                   ║
║         Guide: Add Telegram Bot Token & Run on Linux             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝


📋 الخطوة 1️⃣: الحصول على Telegram Bot Token
═════════════════════════════════════════════════════════════════════

A. افتح Telegram على هاتفك أو تطبيق سطح المكتب

B. ابحث عن: @BotFather
   (النسخة الرسمية لـ Telegram لإنشاء البوتات)

C. أرسل الأوامر التالية:
   
   1️⃣  أرسل: /newbot
   
   2️⃣  سيسأل عن اسم البوت:
       اكتب مثلاً: Djezzy Bot
       (أي اسم تريده)
   
   3️⃣  سيسأل عن اسم المستخدم (username):
       اكتب مثلاً: djezzy_algo_bot
       (يجب أن ينتهي بـ _bot)
   
   4️⃣  سيرسل لك رسالة تحتوي على:
       
       ✅ Bot Token (مثال):
          1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
       
       ✅ رابط البوت:
          https://t.me/djezzy_algo_bot
       
       👉 انسخ الـ Token (الجزء الطويل)!


📋 الخطوة 2️⃣: إضافة Token بطريقة آمنة على Linux
═════════════════════════════════════════════════════════════════════

🔒 الطريقة الآمنة (الموصى بها):

أ) انسخ ملف الإعدادات النموذجي:

   $ cd ~/Desktop/github_project/djezzy/djezzy_bot
   
   $ cp .env.example .env

ب) عدّل الملف وأضفِ Token:

   $ nano .env
   
   (أو استخدم أي محرر تفضله: vi, vim, gedit, vscode)

ج) ستجد السطر:

   TELEGRAM_BOT_TOKEN=your_bot_token_here_paste_your_actual_token

   غيّره إلى (مثال):

   TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh

د) احفظ الملف:
   - في nano: Ctrl + X ثم Y ثم Enter
   - في vi: Esc ثم :wq

⚠️  تحذير مهم جداً:
   - لا تشارك Token مع أحد!
   - الملف .env في .gitignore (محمي من Git)
   - لا تضعه على GitHub أبداً!


📋 الخطوة 3️⃣: التشغيل على Linux
═════════════════════════════════════════════════════════════════════

🚀 الطريقة السهلة (الموصى بها):

1. انتقل إلى مجلد المشروع:

   $ cd ~/Desktop/github_project/djezzy/djezzy_bot

2. اجعل ملف التشغيل قابل للتنفيذ:

   $ chmod +x run.sh

3. شغّل:

   $ ./run.sh

4. ستظهر قائمة اختر:

   ════════════════════════════════════════
   اختر وضع التشغيل:
   ════════════════════════════════════════
   
   1️⃣  🤖 بوت Telegram
   2️⃣  💻 واجهة سطر الأوامر (CLI)
   3️⃣  🔧 برنامج الإعداد
   4️⃣  📖 عرض الفهرس
   5️⃣  ❌ خروج

5. اختر 1 لتشغيل بوت Telegram:

   اختر (1-5): 1

6. سيقول:
   - "تفعيل البيئة الوهمية..."
   - "تثبيت المكتبات..."
   - "بدء بوت Telegram..."

7. ستظهر رسالة:
   🤖 تم بدء البوت...

✅ الآن البوت يعمل!


📋 الطريقة 2️⃣: التشغيل اليدوي (بدون run.sh)
═════════════════════════════════════════════════════════════════════

$ cd ~/Desktop/github_project/djezzy/djezzy_bot

# 1. أنشئ بيئة وهمية
$ python3 -m venv venv

# 2. فعّلها
$ source venv/bin/activate

# (سترى (venv) في بداية السطر)

# 3. ثبّت المكتبات
$ pip install -r requirements.txt

# 4. شغّل البوت
$ python3 djezzy_bot.py

# أو واجهة الأوامر:
$ python3 cli_runner.py


📋 الطريقة 3️⃣: استخدام متغيرات البيئة مباشرة
═════════════════════════════════════════════════════════════════════

بدلاً من ملف .env، يمكنك تعيين متغيرات مباشرة:

$ export TELEGRAM_BOT_TOKEN="1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh"

$ python3 djezzy_bot.py

أو بسطر واحد:

$ TELEGRAM_BOT_TOKEN="token_here" python3 djezzy_bot.py


📋 🔍 تصحيح الأخطاء الشائعة على Linux
═════════════════════════════════════════════════════════════════════

❌ خطأ: "Permission denied"

   $ chmod +x run.sh
   $ ./run.sh


❌ خطأ: "Python not found"

   تأكد من تثبيت Python 3:
   
   $ python3 --version
   
   إذا لم يكن مثبت:
   
   $ sudo apt update
   $ sudo apt install python3 python3-venv python3-pip


❌ خطأ: "ModuleNotFoundError: python-telegram-bot"

   1. تأكد من تفعيل البيئة:
      $ source venv/bin/activate
   
   2. ثبّت المكتبات:
      $ pip install -r requirements.txt


❌ خطأ: "Token invalid"

   ✓ تأكد من نسخ Token صحيح من @BotFather
   ✓ تأكد من عدم وجود مسافات إضافية
   ✓ تأكد من أن .env يحتوي على Token الصحيح


❌ خطأ: ".env file not found"

   $ cp .env.example .env
   $ nano .env
   (أضف Token والحفظ)


📋 ✅ التحقق من أن كل شيء يعمل
═════════════════════════════════════════════════════════════════════

1. تحقق من Python:
   $ python3 --version
   (يجب أن يكون 3.8+)

2. تحقق من pip:
   $ pip3 --version

3. تحقق من ملف .env:
   $ cat .env
   (تأكد من وجود Token)

4. جرّب import المكتبات:
   $ python3 -c "import telegram; print('✅ telegram مثبت')"
   $ python3 -c "import requests; print('✅ requests مثبت')"

5. شغّل المشروع:
   $ ./run.sh


📋 💡 نصائح مهمة
═════════════════════════════════════════════════════════════════════

✅ احفظ Token في مكان آمن:
   - ملف .env (محمي من Git)
   - متغير بيئة
   - مدير كلمات مرور

✅ لا تنسَ حفظ البوت:
   - في Telegram ابحث عن اسم البوت الذي أنشأته
   - ابدأ محادثة معه
   - أرسل /start

✅ إذا توقف البوت:
   - تحقق من السجل: tail -f logs/djezzy.log
   - تأكد من الإنترنت
   - أعد التشغيل: ./run.sh

✅ لتشغيل البوت في الخلفية:
   $ nohup python3 djezzy_bot.py &
   
   أو:
   $ screen
   $ ./run.sh
   (Ctrl+A ثم D للخروج)


📋 📂 البنية على Linux
═════════════════════════════════════════════════════════════════════

~/Desktop/github_project/djezzy/djezzy_bot/
├── .env                    ← ضع Token هنا (جديد)
├── run.sh                  ← شغّل هذا
├── djezzy_bot.py          ← البوت الرئيسي
├── djezzy_utils.py        ← الوحدة الأساسية
├── requirements.txt        ← المكتبات
├── venv/                  ← البيئة (تُنشأ تلقائياً)
│   └── bin/
│       └── activate       ← لتفعيل البيئة
├── data/                  ← البيانات
│   └── registered_numbers.json
└── logs/                  ← السجلات
    └── djezzy.log


📋 🚀 ملخص الخطوات السريعة
═════════════════════════════════════════════════════════════════════

1. الحصول على Token من @BotFather ✅

2. أضفه إلى .env:
   $ cd ~/Desktop/github_project/djezzy/djezzy_bot
   $ cp .env.example .env
   $ nano .env
   (أضف Token والحفظ)

3. شغّل على Linux:
   $ chmod +x run.sh
   $ ./run.sh
   (اختر 1 للبوت)

✅ جاهز!


📋 📞 الدعم
═════════════════════════════════════════════════════════════════════

اقرأ التوثيق:
- README.md          → الدليل الكامل
- QUICKSTART.md      → بدء سريع
- START_HERE.md      → دليل البدء

شغّل البرامج:
- python3 INDEX.py              → الفهرس
- python3 folder_manager.py     → عرض البنية
- python3 setup.py              → برنامج الإعداد


═════════════════════════════════════════════════════════════════════

                    🎉 استمتع بالمشروع! 🎉
                    
              Made with ❤️  - مارس 2024
                      
═════════════════════════════════════════════════════════════════════
"""
    print(guide)


if __name__ == "__main__":
    print_guide()
