#!/bin/bash

# clean.sh - remove generated and sensitive files to return project to fresh state
# usage: ./clean.sh  (runs in project root)

set -e

echo "🔄 تنظيف المشروع..."

# remove virtual environment
if [ -d "venv" ]; then
    echo "🗑️  حذف venv/"
    rm -rf venv
fi

# remove environment file
if [ -f ".env" ]; then
    echo "🗑️  حذف .env (احذف يدويًا إذا كان يحتوي على بيانات حساسة)"
    rm -f .env
fi

# remove logs and data
echo "🗑️  حذف محتويات logs/ وdata/"
rm -rf logs/* data/*

# remove compiled python files and caches
echo "🗑️  حذف ملفات __pycache__ و *.pyc"
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# optional: remove termux bundle artifacts
if [ -d "termux" ]; then
    echo "🗑️  تنظيف مجلد termux"
    rm -f termux/*.tar.gz
fi

# suggest git clean for untracked files
cat <<'EOF'

✅ الانتهاء. إذا كنت تستخدم Git وتريد حذف الملفات غير المتتبعة/غير المرغوب فيها:
   git clean -fdx  # ⚠️ احذر أنه سيحذف كل شيء غير متتبع

EOF
