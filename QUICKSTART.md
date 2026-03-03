# الدليل السريع - Quick Start Guide 🚀

## ماذا تم إنشاؤه؟

تم فصل الملف الأصلي `djezzy_tool.py` وإنشاء نسخة **مستقلة تماماً** من ثلاثة أجزاء:

### 1️⃣ `djezzy_utils.py` - الوحدة الأساسية (المستقلة)

- ✅ لا تعتمد على أي شيء خارج Python الأساسي
- ✅ يمكن استخدامها في أي مشروع
- ✅ تحتوي جميع وظائف Djezzy

### 2️⃣ `djezzy_bot.py` - بوت Telegram كامل

- ✅ يستخدم `python-telegram-bot`
- ✅ واجهة رسومية سهلة
- ✅ متعدد المستخدمين

### 3️⃣ `cli_runner.py` - واجهة سطر أوامر بسيطة

- ✅ بدون الحاجة إلى Telegram
- ✅ واجهة تفاعلية
- ✅ سهلة الاستخدام

---

## 🎯 كيف تبدأ (5 دقائق)

### الخطوة 1️⃣: التثبيت

```bash
# انتقل إلى مجلد المشروع
cd /home/djab/Desktop/github_project/djezzy/djezzy_bot

# شغّل برنامج الإعداد
python setup.py

# أو اتبع النقاط التالية يدويّاً
```

### الخطوة 2️⃣: تثبيت المكتبات

```bash
pip install -r requirements.txt
```

### الخطوة 3️⃣: اختر طريقة الاستخدام

#### ✅ الطريقة الأولى: واجهة سطر الأوامر (الأسهل)

```bash
python cli_runner.py
```

#### ✅ الطريقة الثانية: بوت Telegram (الأفضل للاستخدام المتعدد)

1. احصل على Token من @BotFather
2. ضعه في `djezzy_bot.py`
3. شغّل:

```bash
python djezzy_bot.py
```

#### ✅ الطريقة الثالثة: استخدام الكود مباشرة

```python
from djezzy_utils import register_with_number, request_otp

# طلب OTP
request_otp("213770123456")

# تسجيل (بدون تخزين سجل حتى لا يتم إنشاء أي ملف بيانات)
success, message, data = register_with_number(
    "213770123456", "123456", record=False
)
if success:
    print("نجح!")

# يمكنك أيضاً معالجة مجموعة من الأرقام عبر
# `register_users_concurrently()` إذا رغبت في التشغيل المتوازي.
```

---

## 📁 البنية الجديدة

```
djezzy_bot/
├── djezzy_utils.py          # ⭐ الأساس (مستقل)
├── djezzy_bot.py            # بوت Telegram
├── cli_runner.py            # واجهة سطر الأوامر
├── setup.py                 # برنامج الإعداد
├── requirements.txt         # المكتبات
├── .env.example             # مثال للإعدادات
├── README.md                # الدليل الكامل
├── QUICKSTART.md            # هذا الملف
│
├── registered_numbers.json  # 📊 سجل الأرقام (ينشأ تلقائياً)
└── djezzy_tool.log         # 📝 السجل (ينشأ تلقائياً)
```

---

## ⚡ الاستخدام السريع

### CLI (الأسهل):

```bash
python cli_runner.py
```

اتبع الخطوات على الشاشة

### Telegram Bot:

```bash
# 1. احصل على Token
# (راسل @BotFather على Telegram)

# 2. عديل الملف
nano djezzy_bot.py
# ثم غيّر: TOKEN = "your_token_here"

# 3. شغّل
python djezzy_bot.py

# 4. ابحث عن البوت في Telegram وأرسل /start
```

### Python Script:

```python
#!/usr/bin/env python3
import djezzy_utils

# طلب OTP
resp = djezzy_utils.request_otp("213770123456")
print(f"Status: {resp.status_code}")

# تسجيل
result = djezzy_utils.register_with_number(
    "213770123456",
    "123456",  # OTP
    max_attempts=50,
    record=False  # عدم حفظ أي سجل للنتيجة
)
print(result)  # (success, message, data)
```

---

## ❓ أسئلة شائعة

**س: هل المكتبات مثبتة؟**

```bash
pip list | grep -E "telegram|requests"
```

**س: كيف أحصل على Bot Token؟**

1. افتح Telegram
2. ابحث عن `@BotFather`
3. أرسل `/newbot`
4. اتبع التعليمات
5. انسخ Token

**س: أريد استخدام Telegram؟**

```bash
# تأكد من تعيين المتغير في البيئة أولاً:
export TELEGRAM_BOT_TOKEN="123456:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh"
# أو أنشئ ملف .env يحتوي على السطر نفسه
python djezzy_bot.py
```

**س: أريد المزيد من المعلومات؟**
اقرأ `README.md`

---

## 🔒 الأمان

### 🔧 ميزات المشرف

إذا قمت بتعيين نفسك كمشرف (`ADMIN_ID` أو `CHAT_ID` في .env)، فستحصل على زر إضافي "⚙️ إدارة" عند الضغط على /start. من هناك يمكنك:

- بث رسالة إلى كل المستخدمين الذين بدأوا المحادثة (حتى لو لم يسجلوا رقم)
- حظر أو رفع حظر عن مستخدمين
- الاطلاع على قائمة المعرفات والأسماء المسجلة

المستخدمون العاديون سيرون نفس الأزرار لكنهم سيعرضون بياناتهم الشخصية فقط عند الضغط على إحصائيات / تسجيلات.

⚠️ **هام جداً:**

````bash
# ❌ لا تفعل هذا:
python -c "TOKEN='...' python djezzy_bot.py"

# ✅ افعل هذا (أيضاً يمكنك وضعه في .env):
export TELEGRAM_BOT_TOKEN="your_token"

# الملاحظة: سيتم التأكد من أن هذا المتغير يحتوي على التنسيق الصحيح (أرقام متبوعة بنقطتين ثم مفتاح).
# ⚠️ إذا نسخت التوكن من مكان آخر وقد تظهر رسالة خطأ بخصوص التنسيق، فقد تحتوي الشرطة على حرف غير ASCII.
#    السكربت سيحوّل الشرطات الغريبة إلى '-' ويزيل المسافات تلقائياً، لكن يمكنك إعادة كتابة التوكن يدوياً.
python djezzy_bot.py

> 💡 لتنظيف المشروع وإعادة الحالة الافتراضية يمكنك تشغيل:
>
> ```bash
> bash clean.sh           # سكربت التنظيف الأوتوماتيكي
> python setup.py --clean # خيار داخل أداة الإعداد
> ```
````

أو استخدم `.env` file:

```bash
# نسخ الملف مثال
cp .env.example .env

# عديل الملف
nano .env

# أضف:
TELEGRAM_BOT_TOKEN=your_actual_token

# استخدمه في الكود
import os
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# the bot code later validates that TOKEN matches the expected pattern
```

---

## 📞 الدعم

إذا واجهت مشاكل:

1. **تحقق من السجلات:**

   ```bash
   tail -f djezzy_tool.log
   ```

2. **تحقق من الرقم:**
   - يجب أن يكون رقم اتصالات جزائري
   - الصيغة: `0770123456` أو `213770123456`

3. **تحقق من الإنترنت:**

   ```bash
   ping google.com
   ```

4. **أعد التثبيت:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

---

## 🎉 ملخص الفوائد

| الميزة | CLI  | Telegram | Code |
| ------ | ---- | -------- | ---- |
| سريع   | ✅   | ✅       | ✅   |
| سهل    | ✅✅ | ✅✅     | ⭐   |
| متعدد  | ❌   | ✅✅     | ⭐   |
| مستقل  | ✅   | ✅       | ✅✅ |

---

## 🚀 البدء الآن

```bash
# تثبيت سريع
pip install python-telegram-bot requests

# استخدام سريع
python cli_runner.py

# أو
python djezzy_bot.py
```

---

**تم تصنيعه بحب ❤️**
