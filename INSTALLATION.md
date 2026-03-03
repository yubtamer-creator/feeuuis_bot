# تعليمات التشغيل المحمول

## Portable Installation Guide

## 📦 المشروع الآن محمول تماماً!

يمكنك نقل فولدر `djezzy_bot` بأكمله إلى أي مكان والتشغيل المباشر.

---

## 🚀 التشغيل السريع

### Windows 🪟

```bash
# انقر مرتين على:
run.bat

# أو من موجه التطبيق:
run.bat
```

### Linux/macOS 🐧

```bash
# اجعل البرنامج قابل للتنفيذ:
chmod +x run.sh

# شغّل:
./run.sh
```

> 💡 يمكنك أيضاً تمرير التوكن (وأحياناً chat id) مباشرة من سطر الأوامر دون الحاجة لملف `.env`:
>
> ```bash
> BOT_TOKEN="123456:ABC..." CHAT_ID="987654" ./run.sh
> # run.sh يدعم كلتا المتغيرين ويترجم BOT_TOKEN إلى TELEGRAM_BOT_TOKEN
> ```
>
> ⚠️ انتبه عند نسخ التوكن من المتصفح أو الوثائق: بعض المُحرّرات أو المواقع قد تُدرج شرطة غير عادية مثل “–” أو “‑” بدل “-”.
> سيتم الآن تحويل هذه الشرطات تلقائياً، لكن إذا ظهرت رسالة تنسيق خاطئ فحاول إعادة كتابة التوكن يدوياً أو استخدام الخيار:
>
> ```bash
> # إزالة الفراغات والشرطة العجيبة
> TELEGRAM_BOT_TOKEN=$(echo "$TELEGRAM_BOT_TOKEN" | tr '‑–—' '-')
> ```
>
> 📌 **جدول القائمة الرئيسية في `run.sh`:**
>
> ```text
> 1️⃣  🤖 بوت Telegram
> 2️⃣  💻 واجهة سطر الأوامر (CLI)
> 3️⃣  🔧 برنامج الإعداد
> 4️⃣  📖 عرض الفهرس
> 5️⃣  🔄 تنظيف المشروع   ← الخيار الجديد
> 6️⃣  ❌ خروج
> ```
>
> يُعد خيار التنظيف طريقة سريعة لمسح البيئة، السجلات، والبيانات المؤقتة قبل تشغيل البوت أو مشاركته.

---

## 📁 بنية المجلد المحمول

```
djezzy_bot/          ← انقل هذا المجلد بأكمله
├── 🐍 Python Files
│   ├── djezzy_utils.py      (الوحدة الأساسية)
│   ├── djezzy_bot.py        (بوت Telegram)
│   ├── cli_runner.py        (واجهة سطر الأوامر)
│   ├── setup.py             (برنامج الإعداد)
│   ├── config.py            (الإعدادات - محدّث ✨)
│   └── INDEX.py             (الفهرس)
│
├── 🔧 Run Scripts
│   ├── run.sh              (Linux/macOS)
│   └── run.bat             (Windows)
│
├── 📋 Configuration
│   ├── requirements.txt      (المكتبات)
│   ├── .env.example         (مثال الإعدادات)
│   └── .gitignore          (للـ Git)
│
├── 📚 Documentation
│   ├── INSTALLATION.md       (هذا الملف))
│   ├── README.md            (الدليل الكامل)
│   ├── QUICKSTART.md        (بدء سريع)
│   └── PROJECT_SUMMARY.md   (ملخص المشروع)
│
└── 📂 Auto-created Folders
    ├── data/               (البيانات)
    │   └── registered_numbers.json
    ├── logs/               (السجلات)
    │   └── djezzy.log
    ├── config/             (الإعدادات)
    └── venv/               (البيئة الوهمية - عند التشغيل أول مرة)
```

---

## ✨ المميزات المحمولة

✅ **مستقل تماماً** - لا يعتمد على المسارات المطلقة  
✅ **موارد منظمة** - جميع البيانات في مجلدات منفصلة  
✅ **تشغيل سهل** - اضغط على run.sh أو run.bat  
✅ **بيئة وهمية تلقائية** - تُنشأ عند أول تشغيل  
✅ **توافق كامل** - يعمل على Windows و Linux و macOS

---

## 🔧 التثبيت اليدوي

إذا واجهت مشاكل مع ملفات run:

> 💡 **تنبيه Debian/Ubuntu**: قد تحصل رسالة `externally-managed-environment` أثناء تثبيت الحزم. إذا ظهرت، فسيقوم "run.sh" تلقائياً بإعادة المحاولة مع الخيار `--break-system-packages`. يمكنك حل المشكلة يدوياً بتنفيذ:
>
> ```bash
> python3 -m pip install --break-system-packages -r requirements.txt
> ```

### Windows:

```cmd
# 1. افتح Command Prompt
# 2. انتقل للمجلد
cd path\to\djezzy_bot

# 3. أنشئ بيئة وهمية
python -m venv venv

# 4. فعّلها
venv\Scripts\activate.bat

# 5. ثبّت المكتبات
pip install -r requirements.txt

# 6. شغّل
python cli_runner.py
```

### Linux/macOS:

```bash
# 1. افتح Terminal
# 2. انتقل للمجلد
cd path/to/djezzy_bot

# 3. أنشئ بيئة وهمية
python3 -m venv venv

# 4. فعّلها
source venv/bin/activate

# 5. ثبّت المكتبات
pip install -r requirements.txt

# 6. شغّل
python3 cli_runner.py
```

---

## 🗂️ شرح المجلدات الجديدة

### `data/` 📊

- يحتوي على جميع بيانات التطبيق
- `registered_numbers.json` - سجل الأرقام المسجلة
- يتم إنشاؤه تلقائياً

### `logs/` 📝

- جميع السجلات والأخطاء
- `djezzy.log` - سجل العمليات
- يتم إنشاؤه تلقائياً

### `config/` ⚙️

- الإعدادات والتكوينات
- `config.json` - الإعدادات الرئيسية
- يتم إنشاؤه تلقائياً

### `venv/` 🐍

- البيئة الوهمية (Python Virtual Environment)
- يتم إنشاؤها تلقائياً عند أول تشغيل
- تحتوي على جميع المكتبات المثبتة

---

## 📍 المسارات المرنة

الملف الجديد `config.py` يتعامل مع جميع المسارات تلقائياً:

```python
# بدلاً من:
REGISTERED_NUMBERS_FILE = "registered_numbers.json"

# الآن يستخدم:
from config import REGISTERED_NUMBERS_FILE
# الذي يساوي: project_root/data/registered_numbers.json
```

---

## 🔐 الأمان والخصوصية

```
.gitignore يخفي تلقائياً:
- ملفات البيئة (.env)
- ملفات الـ Log (*.log)
- البيانات الحساسة
- البيئة الوهمية (venv/)
```

إذا كنت ستضع المشروع على GitHub:

```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

---

## 📱 تثبيت خاص بترمكس (Termux)

إذا كنت تستخدم Termux على هاتف أندرويد، افتح تطبيق Termux ثم نفّذ الأوامر التالية:

```bash
# نسخ المستودع
git clone https://github.com/zalsofoy-dev/zalsofoy-code.git
cd zalsofoy-code
chmod +x termux/install.sh

# تشغيل المثبّت مع تمرير التوكن و (اختياري) معرف المشرف
BOT_TOKEN="8497332276:AAE-TDh_tUafbpNE9vwBIC0RooOMLCoaKwg" \
CHAT_ID="7713662350" \
./termux/install.sh
```

السكربت سيقوم بتحديث الحزم، تثبيت بايثون وgit، إنشاء البيئة الوهمية، وملف `.env` يحتوي على المتغيرات المطلوبة.

> 💡 إذا كنت ترغب بنسخة مصغرة من المشروع للرفع إلى الهاتف، استخدم سكربت `termux/bundle.sh` من الحاسوب لإنشاء أرشيف مستقل `djezzy_termux.tar.gz` ثم انقله إلى الهاتف وفك ضغطه قبل تشغيل `install.sh`.

يمكنك تعديل `ADMIN_ID` أو `CHAT_ID` داخل `.env` لاحقاً لتحديد من يمكنه رؤية الإحصاءات والمعلومات.

---

## ⚠️ ملاحظات مهمة

### تنظيف المشروع

إذا أردت إعادة المشروع إلى حالة "طازجة" أو قبل إنشاء حزمة، استخدم السكربت التالي:

```bash
chmod +x clean.sh
./clean.sh
```

هذا سيحذف البيئة الوهمية، السجلات، البيانات المؤقتة، ملفات pyc، و `.env` (إذا وجدت). يمكنك بعدها إجراء `git clean -fdx` بحذر لتخليص المستودع من الملفات غير المتتبعة.

### عند نقل المشروع:

```
❌ لا تنسى:
✓ جميع الملفات .py
✓ ملف requirements.txt
✓ مجلد data/ للبيانات
✓ ملفات run.sh و run.bat
✓ ملفات التوثيق

❌ لا تحتاج:
✓ مجلد venv/ (سينشأ تلقائياً)
✓ ملفات *.log و *.pyc
✓ ملف .env (استخدم .env.example كمثال)
```

---

## 🐛 استكشاف الأخطاء

### المشكلة: خطأ "Python not found"

```
الحل:
1. تأكد من تثبيت Python 3.8+
2. أضفه إلى PATH
3. استخدم: python3 بدلاً من python
```

### المشكلة: خطأ "Module not found"

```
الحل:
1. تأكد من تشغيل run.sh أو run.bat
2. أو ثبّت يدويً: pip install -r requirements.txt
```

### المشكلة: صلاحيات الملف (Linux/macOS)

```bash
chmod +x run.sh
chmod +x djezzy_bot.py
chmod +x cli_runner.py
```

---

## 📱 نقل المشروع بين الأجهزة

### الطريقة 1: Zip

```bash
# ضغط المجلد
zip -r djezzy_bot.zip djezzy_bot/

# فك الضغط في الوجهة الجديدة
unzip djezzy_bot.zip

# التشغيل
./djezzy_bot/run.sh
```

### الطريقة 2: Git

```bash
git clone your_repo_url
cd djezzy_bot
./run.sh  # أو run.bat على Windows
```

### الطريقة 3: USB Drive

```
1. انسخ مجلد djezzy_bot/ إلى USB
2. ضعه في أي جهاز
3. شغّل run.sh أو run.bat
   - لا تحتاج لتثبيت إضافي!
```

---

## 🎉 النتيجة

الآن المشروع:

- ✅ **محمول 100%** - نقله أينما شئت
- ✅ **مستقل تماماً** - لا يحتاج تكوين إضافي
- ✅ **سهل التشغيل** - اضغط على run.sh أو run.bat
- ✅ **منظم** - جميع البيانات والسجلات في مكان واحد
- ✅ **موثوق** - يعمل على Windows و Linux و macOS

---

## 📞 الدعم

### للمزيد من المعلومات:

- اقرأ: `README.md` - الدليل الكامل
- اقرأ: `QUICKSTART.md` - بدء سريع
- شغّل: `python INDEX.py` - عرض الفهرس

---

**استمتع بالاستخدام! 🚀**

_آخر تحديث: مارس 2024_
