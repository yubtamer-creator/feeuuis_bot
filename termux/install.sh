#!/bin/bash

# Termux installation helper for Djezzy Bot
# Usage example:
#   git clone https://github.com/zalsofoy-dev/zalsofoy-code.git
#   cd zalsofoy-code
#   chmod +x install.sh
#   BOT_TOKEN="..." CHAT_ID="123456" ./install.sh

set -e

# ensure we are running inside termux
if [[ -z "$PREFIX" || ! -d "$PREFIX" ]]; then
    echo "⚠️  يبدو أنك لا تعمل داخل Termux. افعل ذلك ثم أعد تشغيل السكربت."
    exit 1
fi

echo "📦 تحديث الحزم"
pkg update -y && pkg upgrade -y

# install python and git if needed
pkg install -y python git

# create virtual environment
if [ ! -d "venv" ]; then
    echo "🐍 إنشاء البيئة الوهمية (venv) ..."
    python3 -m venv venv
fi

# activate
source venv/bin/activate

# install requirements
pip install -r requirements.txt

# write .env file from provided variables
if [ -z "$BOT_TOKEN" ]; then
    echo "❌ متغير BOT_TOKEN غير مضبوط. تحديده قبل تشغيل السكربت مثال: BOT_TOKEN=..."
    exit 1
fi

# basic token format check
if ! [[ "$BOT_TOKEN" =~ ^[0-9]+:[A-Za-z0-9_-]+$ ]]; then
    echo "❌ التنسيق المتوقع لـ BOT_TOKEN خاطئ. يجب أن يكون على شكل 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh"
    exit 1
fi

# chat id validation
if [ -n "$CHAT_ID" ] && ! [[ "$CHAT_ID" =~ ^[0-9]+$ ]]; then
    echo "⚠️ تحذير: CHAT_ID غير رقمي، سيتم تخطيه. يرجى التأكد من إدخال معرف المستخدم الصحيح."
fi

cat > .env <<EOF
TELEGRAM_BOT_TOKEN=$BOT_TOKEN
# optional administrator/user allowed to see stats
ADMIN_ID=${CHAT_ID:-}
EOF

echo "✅ ملف .env تم إنشاؤه."

# create data directories just in case
mkdir -p data logs config

# finally start
echo "🚀 بدء البوت..." 
python3 run.sh
