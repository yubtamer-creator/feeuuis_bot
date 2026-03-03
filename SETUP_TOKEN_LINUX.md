# 🤖 إضافة Telegram Bot Token و التشغيل على Linux

دليل خطوة بخطوة بالعربية

---

## 📋 الخطوة 1️⃣: الحصول على Telegram Bot Token

### من جهازك:

1. **افتح Telegram** (تطبيق أو ويب)

2. **ابحث عن: `@BotFather`**
   - هذا هو البوت الرسمي للأوامر

3. **أرسل `/newbot`**

4. **أجب على الأسئلة:**

   ```
   Q: ما اسم البوت؟
   A: Djezzy Bot  (أو أي اسم تريده)

   Q: ما اسم المستخدم؟
   A: djezzy_algo_bot  (يجب أن ينتهي بـ _bot)
   ```

5. **احصل على Token:**

   ```
   ستتلقى رسالة مثل:

   ✅ Done! Congratulations on your new bot.

   Token: 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
   ```

**👉 انسخ هذا الـ Token!**

---

## 📋 الخطوة 2️⃣: إضافة Token بطريقة آمنة

### على Linux - استخدم `.env` file:

#### الطريقة 1: استخدام البرنامج (الأسهل)

```bash
# انتقل للمشروع
cd ~/Desktop/github_project/djezzy/djezzy_bot

# اجعل البرنامج قابل للتنفيذ
chmod +x run.sh

# شغّل
./run.sh
```

سيطلب منك Token - أدخله!

#### الطريقة 2: تعديل الملف يدويً

```bash
# البدء
cd ~/Desktop/github_project/djezzy/djezzy_bot

# انسخ الملف النموذجي
cp .env.example .env

# افتح الملف بمحرر (اختر واحد):
nano .env          # محرر سهل
# أو
vi .env            # محرر vi
# أو
gedit .env         # في سطح المكتب
```

**داخل الملف:** ابحث عن هذا السطر:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here_paste_your_actual_token
```

**استبدله بـ Token الحقيقي:**

```
TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
```

**احفظ الملف:**

- في `nano`: اضغط `Ctrl + X` ثم `Y` ثم `Enter`
- في `vi`: اضغط `Esc` ثم `:wq` ثم `Enter`

✅ **التحقق:**

```bash
# تأكد من أن Token موجود
cat .env

# ستتوقع أن ترى:
# TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
```

---

## 📋 الخطوة 3️⃣: التشغيل على Linux

### الطريقة الأسهل:

```bash
# 1. انتقل للمشروع
cd ~/Desktop/github_project/djezzy/djezzy_bot

# 2. اجعل run.sh قابل للتنفيذ
chmod +x run.sh

# 3. شغّل
./run.sh
```

**ستظهر قائمة:**

```
════════════════════════════════════════
اختر وضع التشغيل:
════════════════════════════════════════

1️⃣  🤖 بوت Telegram
2️⃣  💻 واجهة سطر الأوامر (CLI)
3️⃣  🔧 برنامج الإعداد
4️⃣  📖 عرض الفهرس
5️⃣  ❌ خروج
```

**اختر 1 للبوت:**

```
اختر (1-5): 1

[INFO] بدء بوت Telegram...
🤖 تم بدء البوت...
```

✅ **البوت يعمل الآن!**

---

### الطريقة اليدوية (بدون run.sh):

```bash
# 1. انتقل للمشروع
cd ~/Desktop/github_project/djezzy/djezzy_bot

# 2. أنشئ بيئة وهمية
python3 -m venv venv

# 3. فعّلها
source venv/bin/activate

# (سيتغير السطر ويبدأ بـ (venv))

# 4. ثبّت المكتبات
pip install -r requirements.txt

# 5. شغّل البوت
python3 djezzy_bot.py
```

---

## 🧪 اختبر البوت

### من Telegram:

1. في Telegram، ابحث عن اسم البوت الذي أنشأته

   ```
   مثال: @djezzy_algo_bot
   ```

2. فتح المحادثة

3. أرسل `/start`

4. ستظهر قائمة البوت! 🎉

---

## 🔐 الأمان

### ⚠️ قواعد مهمة:

```
❌ لا تفعل:
- لا تضع Token في الكود مباشرة
- لا تشارك Token مع أحد
- لا تضع Token على GitHub

✅ افعل:
- استخدم .env file
- احفظه في مكان آمن
- أضفه إلى .gitignore (تم بالفعل)
```

---

## 🐛 حل المشاكل

### ❌ خطأ: `Python not found`

```bash
# تحقق من Python
python3 --version

# إذا لم يكن مثبت:
sudo apt update
sudo apt install python3 python3-pip
```

### ❌ خطأ: `ModuleNotFoundError`

```bash
# تأكد من البيئة
source venv/bin/activate

# ثبّت المكتبات
pip install -r requirements.txt
```

### ❌ خطأ: `Token invalid`

```bash
# تأكد من Token:
cat .env

# تحقق من:
1. نسخت Token صحيح من BotFather ✓
2. بدون مسافات إضافية ✓
3. .env يحتوي على Token ✓
```

### ❌ خطأ: `Permission denied`

```bash
chmod +x run.sh
./run.sh
```

---

## 📝 ملاحظات مهمة

```
✅ Token يبدأ برقم متبوعاً بنقطتين:
   1234567890:ABCDEFGH...

✅ الملف .env محمي (في .gitignore)

✅ البيانات تُحفظ في:
   data/registered_numbers.json

✅ السجلات في:
   logs/djezzy.log

✅ البيئة الوهمية تُنشأ في:
   venv/
```

---

## 🚀 الخطوات السريعة

### ملخص في 5 دقائق:

```bash
# 1. الحصول على Token من @BotFather
# (من Telegram عبر الهاتف)

# 2. إضافة Token
cd ~/Desktop/github_project/djezzy/djezzy_bot
cp .env.example .env
nano .env
# (أضف Token والحفظ)

# 3. التشغيل
chmod +x run.sh
./run.sh
# (اختر 1)

# ✅ جاهز!
```

---

## 💡 نصائح إضافية

### تشغيل البوت في الخلفية:

```bash
# استخدم nohup
nohup python3 djezzy_bot.py &

# أو استخدم screen
screen
./run.sh
# (Ctrl+A ثم D للخروج)

# للعودة:
screen -r
```

### الاطلاع على السجلات:

```bash
# آخر 50 سطر
tail -50 logs/djezzy.log

# مراقبة مباشرة
tail -f logs/djezzy.log

# البحث عن أخطاء
grep ERROR logs/djezzy.log
```

### إعادة تشغيل البوت:

```bash
# توقيف البوت
Ctrl + C

# تشغيل مرة أخرى
./run.sh
```

---

## 📚 المراجع

اطلع على:

- `README.md` - الدليل الكامل
- `START_HERE.md` - دليل البدء
- `QUICKSTART.md` - بدء سريع

شغّل:

```bash
python3 SETUP_TOKEN_LINUX.py   # هذا الدليل بصيغة أخرى
python3 INDEX.py               # الفهرس الكامل
```

---

## ✅ تم!

الآن لديك:

- ✅ Telegram Bot Token
- ✅ ملف .env مع Token
- ✅ بوت يعمل على Linux

استمتع! 🎉

---

_آخر تحديث: مارس 2024_
