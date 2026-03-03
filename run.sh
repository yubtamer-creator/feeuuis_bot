#!/bin/bash

# Djezzy Bot - Linux/macOS Launcher
# محقق التشغيل لـ Linux و macOS

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}"
echo "╔════════════════════════════════════════╗"
echo "║   مرحباً بك في بوت اتصالات الجزائر   ║"
echo "║      Djezzy Bot - Standalone       ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ خطأ: Python 3 غير مثبت${NC}"
    echo "يرجى تثبيت Python 3 من: https://www.python.org"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 موجود${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 إنشاء بيئة وهمية...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}🔄 تفعيل البيئة الوهمية...${NC}"
source venv/bin/activate

# Load environment variables from .env if the file exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}📄 تحميل متغيرات البيئة من .env...${NC}"
    # export all variables defined in .env
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
fi

# allow shorthand environment variable when invoking the script
# BOT_TOKEN is commonly used in examples; map it to TELEGRAM_BOT_TOKEN
if [ -n "$BOT_TOKEN" ]; then
    TELEGRAM_BOT_TOKEN="$BOT_TOKEN"
fi

# simple sanity check in shell to catch default placeholder and format validity
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_BOT_TOKEN" = "YOUR_TELEGRAM_BOT_TOKEN_HERE" ]; then
    echo -e "${RED}❌ متغير TELEGRAM_BOT_TOKEN غير مضبوط أو يحتوي على القيمة الافتراضي!${NC}"
    echo "تأكد من ضبطه في .env أو تصديره قبل التشغيل. يمكنك أيضاً استخدام BOT_TOKEN=... عند استدعاء run.sh."
    exit 1
fi
if ! [[ "$TELEGRAM_BOT_TOKEN" =~ ^[0-9]+:[A-Za-z0-9_-]+$ ]]; then
    echo -e "${RED}❌ يبدو أن قيمة TELEGRAM_BOT_TOKEN غير صحيحة (تنسيق غير صالح).${NC}"
    echo "يجب أن يكون على شكل 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh"
    exit 1
fi

# optional admin/chat id sanity check
if [ -n "$ADMIN_ID" ] && ! [[ "$ADMIN_ID" =~ ^[0-9]+(,[0-9]+)*$ ]]; then
    echo -e "${YELLOW}⚠️  تحذير: قيمة ADMIN_ID تبدو غير صالحة (يجب أن تكون أرقامًا مفصولة بفواصل).${NC}"
fi
if [ -n "$CHAT_ID" ] && ! [[ "$CHAT_ID" =~ ^[0-9]+$ ]]; then
    echo -e "${YELLOW}⚠️  تحذير: قيمة CHAT_ID تبدو غير صالحة (يجب أن تكون عبارة عن رقم واحد).${NC}"
fi

# Install requirements
# use --break-system-packages to avoid Debian/Ubuntu managed-env errors (PEP 668)
echo -e "${YELLOW}📥 تثبيت المكتبات...${NC}"
# prefer venv's pip but fall back via python3 -m pip
if ! pip install -q --break-system-packages -r requirements.txt; then
    echo -e "${YELLOW}⚠️  إعادة محاولة باستخدام python -m pip...${NC}"
    python3 -m pip install -q --break-system-packages -r requirements.txt
fi

# Create necessary directories
mkdir -p data logs config

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}اختر وضع التشغيل:${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "1️⃣  🤖 بوت Telegram"
echo "2️⃣  💻 واجهة سطر الأوامر (CLI)"
echo "3️⃣  🔧 برنامج الإعداد"
echo "4️⃣  📖 عرض الفهرس"
echo "5️⃣  🔄 تنظيف المشروع"
echo "6️⃣  ❌ خروج"
echo ""

read -p "اختر (1-5): " choice

case $choice in
    1)
        echo -e "${YELLOW}🤖 بدء بوت Telegram...${NC}"
        echo ""
        python3 djezzy_bot.py
        ;;
    2)
        echo -e "${YELLOW}💻 بدء واجهة سطر الأوامر...${NC}"
        echo ""
        python3 cli_runner.py
        ;;
    3)
        echo -e "${YELLOW}🔧 بدء برنامج الإعداد...${NC}"
        echo ""
        python3 setup.py
        ;;
    4)
        echo -e "${YELLOW}📖 عرض الفهرس...${NC}"
        echo ""
        python3 INDEX.py
        ;;
    5)
        echo -e "${YELLOW}🔄 تنظيف المشروع...${NC}"
        echo ""
        ./clean.sh
        ;;
    6)
        echo -e "${GREEN}👋 شكراً لاستخدامك الأداة!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ اختيار غير صحيح${NC}"
        exit 1
        ;;
esac

# Deactivate virtual environment on exit
deactivate 2>/dev/null || true
