#!/bin/bash

# Interactive Setup Script for Token and Linux Launch
# سكريبت إعداد تفاعلي لـ Token والتشغيل على Linux

set -e

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║     🤖 محقق إعداد Telegram Bot Token على Linux              ║"
echo "║        Interactive Setup - Add Token & Launch                ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# Function to display menu
show_menu() {
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}القائمة الرئيسية - Main Menu${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}\n"
    
    echo "1️⃣  🔑 إضافة Telegram Bot Token"
    echo "2️⃣  🤖 تشغيل بوت Telegram"
    echo "3️⃣  💻 تشغيل واجهة الأوامر (CLI)"
    echo "4️⃣  🧪 اختبار الإعدادات"
    echo "5️⃣  📖 عرض الدليل"
    echo "6️⃣  ❌ خروج"
    echo ""
}

# Function to add token
add_token() {
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🔑 إضافة Telegram Bot Token${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}\n"
    
    echo -e "${YELLOW}خطوات الحصول على Token:${NC}\n"
    echo "1. افتح Telegram وابحث عن: @BotFather"
    echo "2. أرسل: /newbot"
    echo "3. عند الانتهاء ستحصل على Token"
    echo ""
    echo -e "${YELLOW}Token يبدو هكذا:${NC}"
    echo "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh"
    echo ""
    
    read -p "اضغط Enter عندما تكون مستعد..."
    
    echo ""
    read -p "أدخل Telegram Bot Token: " token
    
    if [ -z "$token" ]; then
        echo -e "${RED}❌ Token فارغ!${NC}"
        return 1
    fi

    # basic format validation (123456789:ABC...)
    if [[ ! "$token" =~ ^[0-9]+:[A-Za-z0-9_-]+$ ]]; then
        echo -e "${RED}❌ تنسيق Token غير صحيح! يجب أن يكون مثل 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh${NC}"
        return 1
    fi

    # optional chat/admin id prompt
    read -p "(اختياري) أدخل chat id للمشرف أو اضغط Enter لتجاهل: " chat_id
    if [ -n "$chat_id" ]; then
        if ! [[ "$chat_id" =~ ^[0-9]+$ ]]; then
            echo -e "${RED}❌ قيمة CHAT_ID غير صحيحة، يجب أن تحتوي على أرقام فقط.${NC}"
            chat_id=""
        fi
    fi
    
    # Create .env file
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}📝 إنشاء ملف .env...${NC}"
        cp .env.example .env 2>/dev/null || echo "TELEGRAM_BOT_TOKEN=" > .env
    fi
    
    # Add token to .env
    if grep -q "TELEGRAM_BOT_TOKEN=" .env; then
        sed -i "s|TELEGRAM_BOT_TOKEN=.*|TELEGRAM_BOT_TOKEN=$token|" .env
    else
        echo "TELEGRAM_BOT_TOKEN=$token" >> .env
    fi

    # if chat_id was entered, write it as ADMIN_ID (maintain compatibility)
    if [ -n "$chat_id" ]; then
        if grep -q "ADMIN_ID=" .env || grep -q "CHAT_ID=" .env; then
            # replace existing value
            if grep -q "ADMIN_ID=" .env; then
                sed -i "s|ADMIN_ID=.*|ADMIN_ID=$chat_id|" .env
            else
                sed -i "s|CHAT_ID=.*|CHAT_ID=$chat_id|" .env
            fi
        else
            echo "ADMIN_ID=$chat_id" >> .env
        fi
        echo -e "${GREEN}✅ تم حفظ Chat ID للمشرف!${NC}"
    fi

    echo -e "${GREEN}✅ تم حفظ Token بنجاح!${NC}"
    echo -e "${YELLOW}في الملف: .env${NC}\n"
}

# Function to setup environment
setup_environment() {
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}⚙️  إعداد البيئة${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}\n"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 غير مثبت!${NC}"
        echo "للتثبيت:"
        echo "  $ sudo apt update"
        echo "  $ sudo apt install python3 python3-pip"
        return 1
    fi
    
    echo -e "${GREEN}✅ Python 3 موجود: $(python3 --version)${NC}"
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}📦 إنشاء البيئة الوهمية...${NC}"
        python3 -m venv venv
    fi
    
    echo -e "${YELLOW}🔄 تفعيل البيئة الوهمية...${NC}"
    source venv/bin/activate
    
    echo -e "${YELLOW}📥 تثبيت المكتبات...${NC}"
    pip install -q -r requirements.txt
    
    echo -e "${GREEN}✅ البيئة جاهزة!${NC}\n"
}

# Function to run bot
run_bot() {
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🤖 تشغيل بوت Telegram${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}\n"
    
    setup_environment || return 1
    
    if [ ! -f ".env" ]; then
        echo -e "${RED}❌ ملف .env غير موجود!${NC}"
        echo -e "${YELLOW}الرجاء أضافة Token أولاً (الخيار 1)${NC}\n"
        return 1
    fi
    
    source .env
    
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        echo -e "${RED}❌ Token غير موجود في .env!${NC}\n"
        return 1
    fi
    
    echo -e "${GREEN}✅ Token موجود${NC}"
    echo -e "${YELLOW}🚀 بدء بوت Telegram...${NC}\n"
    
    python3 djezzy_bot.py
}

# Function to run CLI
run_cli() {
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}💻 تشغيل واجهة الأوامر${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}\n"
    
    setup_environment || return 1
    
    echo -e "${YELLOW}🚀 بدء واجهة الأوامر...${NC}\n"
    python3 cli_runner.py
}

# Function to test setup
test_setup() {
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}🧪 اختبار الإعدادات${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}\n"
    
    echo "1. التحقق من Python..."
    if command -v python3 &> /dev/null; then
        echo -e "   ${GREEN}✅ $(python3 --version)${NC}"
    else
        echo -e "   ${RED}❌ Python 3 غير مثبت${NC}"
    fi
    
    echo ""
    echo "2. التحقق من pip..."
    if command -v pip3 &> /dev/null; then
        echo -e "   ${GREEN}✅ pip3 موجود${NC}"
    else
        echo -e "   ${RED}❌ pip3 غير موجود${NC}"
    fi
    
    echo ""
    echo "3. التحقق من ملف .env..."
    if [ -f ".env" ]; then
        echo -e "   ${GREEN}✅ ملف .env موجود${NC}"
        
        if grep -q "TELEGRAM_BOT_TOKEN" .env; then
            token=$(grep "TELEGRAM_BOT_TOKEN" .env | cut -d'=' -f2)
            if [ ! -z "$token" ] && [ "$token" != "your_bot_token_here_paste_your_actual_token" ]; then
                echo -e "   ${GREEN}✅ Token موجود${NC}"
            else
                echo -e "   ${RED}❌ Token غير محدد أو افتراضي${NC}"
            fi
        fi
    else
        echo -e "   ${RED}❌ ملف .env غير موجود${NC}"
    fi
    
    echo ""
    echo "4. التحقق من المكتبات..."
    if [ -d "venv" ]; then
        source venv/bin/activate 2>/dev/null
        if python3 -c "import telegram" 2>/dev/null; then
            echo -e "   ${GREEN}✅ python-telegram-bot مثبت${NC}"
        else
            echo -e "   ${RED}❌ python-telegram-bot غير مثبت${NC}"
        fi
    else
        echo -e "   ${YELLOW}⚠️  البيئة الوهمية لم تُنشأ بعد${NC}"
    fi
    
    echo ""
    echo "5. التحقق من الملفات..."
    files=("djezzy_bot.py" "cli_runner.py" "djezzy_utils.py")
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            echo -e "   ${GREEN}✅ $file${NC}"
        else
            echo -e "   ${RED}❌ $file غير موجود${NC}"
        fi
    done
    
    echo ""
}

# Function to show guide
show_guide() {
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}📖 دليل سريع${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}\n"
    
    less SETUP_TOKEN_LINUX.md 2>/dev/null || cat SETUP_TOKEN_LINUX.md
}

# Main loop
while true; do
    show_menu
    read -p "اختر (1-6): " choice
    
    echo ""
    
    case $choice in
        1)
            add_token
            ;;
        2)
            run_bot
            break
            ;;
        3)
            run_cli
            break
            ;;
        4)
            test_setup
            ;;
        5)
            show_guide
            ;;
        6)
            echo -e "${GREEN}👋 شكراً لاستخدامك البوت!${NC}\n"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ اختيار غير صحيح${NC}\n"
            ;;
    esac
    
    read -p "اضغط Enter للمتابعة..." dummy
    echo ""
done
