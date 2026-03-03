@echo off
REM Djezzy Bot - Windows Launcher
REM محقق التشغيل لـ Windows

setlocal enabledelayedexpansion

REM Get the directory where this script is located
cd /d "%~dp0"

echo.
echo ██████╗ ██╗███████╗███████╗███████╗██╗   ██╗ ██████╗ ██████╗ ████████╗
echo ██╔══██╗██║██╔════╝╚════██║██╔════╝╚██╗ ██╔╝██╔════╝██╔═══██╗╚══██╔══╝
echo ██║  ██║██║█████╗      ██╔╝█████╗   ╚████╔╝ ██║     ██║   ██║   ██║
echo ██║  ██║██║██╔══╝     ██╔╝ ██╔══╝    ╚██╔╝  ██║     ██║   ██║   ██║
echo ██████╔╝██║███████╗   ██║  ███████╗   ██║   ╚██████╗╚██████╔╝   ██║
echo ╚═════╝ ╚═╝╚══════╝   ╚═╝  ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝    ╚═╝
echo.
echo   مرحباً بك في بوت جيزي
echo   Djezzy Bot - Standalone
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 غير مثبت
    echo يرجى تثبيت Python 3 من: https://www.python.org
    pause
    exit /b 1
)

echo [OK] Python 3 موجود
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] إنشاء بيئة وهمية...
    python -m venv venv
)

REM Activate virtual environment
echo [INFO] تفعيل البيئة الوهمية...
call venv\Scripts\activate.bat

REM Install requirements
echo [INFO] تثبيت المكتبات...
pip install -q -r requirements.txt 2>nul

REM Create necessary directories
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "config" mkdir config

echo.
echo ════════════════════════════════════════════
echo اختر وضع التشغيل:
echo ════════════════════════════════════════════
echo.
echo 1) 🤖 بوت Telegram
echo 2) 💻 واجهة سطر الأوامر (CLI)
echo 3) 🔧 برنامج الإعداد
echo 4) 📖 عرض الفهرس
echo 5) ❌ خروج
echo.

set /p choice="اختر (1-5): "

if "%choice%"=="1" (
    echo.
    echo [INFO] بدء بوت Telegram...
    echo.
    python djezzy_bot.py
) else if "%choice%"=="2" (
    echo.
    echo [INFO] بدء واجهة سطر الأوامر...
    echo.
    python cli_runner.py
) else if "%choice%"=="3" (
    echo.
    echo [INFO] بدء برنامج الإعداد...
    echo.
    python setup.py
) else if "%choice%"=="4" (
    echo.
    echo [INFO] عرض الفهرس...
    echo.
    python INDEX.py
) else if "%choice%"=="5" (
    echo.
    echo شكراً لاستخدامك الأداة!
    echo.
    exit /b 0
) else (
    echo.
    echo [ERROR] اختيار غير صحيح
    echo.
    pause
    exit /b 1
)

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

pause
