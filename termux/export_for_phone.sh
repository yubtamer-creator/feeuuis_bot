#!/bin/bash

# Create a standalone repository package containing one or more project
# directories (e.g. djezzy_bot and djezzy_app_free) prepared for use on a
# phone/Termux environment.  The output is a new folder that you can
# directly push to GitHub or copy to your device.
#
# Usage:
#   ./termux/export_for_phone.sh output-dir project1 [project2 ...]
#
# Example:
#   ./termux/export_for_phone.sh phone_bundle djezzy_bot djezzy_app_free

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 OUTPUT_DIR PROJECT_DIR [PROJECT_DIR ...]"
    exit 1
fi

OUTPUT="$1"
shift

echo "📦 building phone repo in $OUTPUT"
rm -rf "$OUTPUT"
mkdir -p "$OUTPUT"

for proj in "$@"; do
    if [ -d "$proj" ]; then
        echo "  copying project $proj"
        cp -a "$proj" "$OUTPUT/"
    else
        echo "⚠️  project directory '$proj' not found, skipping"
    fi
done

# add common Termux helpers if they exist in current workspace
if [ -d "termux" ]; then
    echo "  adding termux helpers"
    mkdir -p "$OUTPUT/termux"
    cp -a termux/*.sh "$OUTPUT/termux/" 2>/dev/null || true
    cp -a termux/README.md "$OUTPUT/termux/" 2>/dev/null || true
fi

# create generic .gitignore
cat > "$OUTPUT/.gitignore" <<'EOF'
venv/
*.pyc
*.log
data/
logs/
.env
EOF

echo "✅ phone-ready bundle created at $OUTPUT"

echo "To initialize git:"
cat <<MSG

cd $OUTPUT
git init
git add .
git commit -m 'Initial phone bundle'
MSG
