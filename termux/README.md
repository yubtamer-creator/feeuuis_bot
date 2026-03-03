# Termux Bundle

هذا المجلد يحتوي على الأدوات المخصصة لاستخدام المشروع داخل Termux على هاتف أندرويد.

### الملفات الموجودة

- `install.sh` : سكربت تثبيت يُنَفّذ على الجهاز لتجهيز البيئة وبدء البوت.
- `bundle.sh` : (اختياري) سكربت لإنشاء أرشيف (tar.gz) يحتوي على الملفات الضرورية فقط حتى تتمكن من رفعها إلى الهاتف بدون مجلدات غير مطلوبة.
- `export_for_git.sh` : يُنشئ نسخة مستقلة من المشروع في مجلد جديد يمكن تحويله إلى مستودع Git مستقل في حال أردت رفع الملفات فقط.
- `export_for_phone.sh` : يجمع مجموعة من مجلدات المشاريع (مثلاً `djezzy_bot` و`djezzy_app_free`) في حزمة واحدة جاهزة للرفع إلى Git واستخدامها على الهاتف.

### إنشاء أرشيف مستقل

إذا كنت تريد إرسال نسخة مصغرة من المشروع إلى الهاتف (بدون مجلد `venv`، أو `.git`، أو البيانات المحلية)، يمكنك استعمال الأمر التالي من داخل مجلد الجذر للمشروع:

```bash
cd /path/to/djezzy_bot
chmod +x termux/bundle.sh
./termux/bundle.sh   # سينتج ملف djezzy_termux.tar.gz في نفس المجلد
```

ثم انقل الأرشيف إلى هاتفك وافك الضغط:

```bash
tar xzf djezzy_termux.tar.gz
cd djezzy_bot
chmod +x termux/install.sh
BOT_TOKEN="..." CHAT_ID="..." ./termux/install.sh
```

الأرشيف يحتوي على جميع ملفات البوت Python، `requirements.txt`، `run.sh`، إلخ.

### نسخ الملفات لمشروع جديد

يمكنك أيضاً نسخ مجموعة الملفات الضرورية مباشرة إلى مشروع جديد باستخدام السكربت التالي:

```bash
chmod +x termux/copy_to_project.sh
./termux/copy_to_project.sh /path/to/new/project
```

ستُنسخ إلى الوجهة:

- جميع ملفات البوت (`*.py`)
- `run.sh`, `requirements.txt`
- المستندات (`INSTALLATION.md`, `README.md`, `QUICKSTART.md`)
- مجلد `termux/` نفسه

وهذا يسمح لك بفتح المجلد الناتج وبدء العمل فوراً.

### استخدام مباشر من جيت

إذا كان لديك اتصال إنترنت على الهاتف، فإن أسهل طريقة هي ببساطة تنفيذ:

```bash
pkg install git
git clone https://github.com/zalsofoy-dev/zalsofoy-code.git
cd zalsofoy-code
chmod +x termux/install.sh
BOT_TOKEN="..." CHAT_ID="..." ./termux/install.sh
```

ولكن الخيار السابق مفيد عندما تريد نقل المشروع بواسطة USB أو بدون اتصال.
