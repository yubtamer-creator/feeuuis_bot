#!/bin/bash

# Copy minimal set of files required for Termux usage into another project
# directory.  This allows you to "bootstrap" a new project with Termux
# helpers by copying only the needed Python files and scripts.
#
# Usage:
#   ./termux/copy_to_project.sh /path/to/other/project
#
# The destination folder will receive:
#   - djezzy_bot.py, djezzy_utils.py, config.py
#   - run.sh, requirements.txt
#   - all files under termux/ (install.sh, bundle.sh, etc.)
#   - Documentation files: INSTALLATION.md, README.md, QUICKSTART.md
#
# If the destination does not exist it will be created.

if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/target/project"
    exit 1
fi

TARGET="$1"

# make absolute path
TARGET="$(realpath "$TARGET")"

echo "📁 Preparing target project at $TARGET"
mkdir -p "$TARGET"

COPY_FILES=(
    "djezzy_bot.py"
    "djezzy_utils.py"
    "config.py"
    "run.sh"
    "requirements.txt"
    "INSTALLATION.md"
    "README.md"
    "QUICKSTART.md"
)

for f in "${COPY_FILES[@]}"; do
    if [ -e "$f" ]; then
        echo "  copying $f"
        cp -a "$f" "$TARGET/"
    fi
done

# copy termux helpers
if [ -d "termux" ]; then
    echo "  copying termux/ folder"
    rm -rf "$TARGET/termux"
    cp -a termux "$TARGET/termux"
fi

echo "✅ finished! go to $TARGET and start working."
