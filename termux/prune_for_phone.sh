ًًًًًً#!/bin/bash

# Prune the current repository to a minimal set of files needed for the
# Termux/phone version of the project.  This will remove any files and
# directories that are not explicitly required (see list below).
#
# WARNING: this script permanently deletes files.  Run it at your own risk.
# It is intended to be used in a working copy that can be discarded afterward
# (e.g. after you've exported a clean bundle with export_for_phone.sh).
#
# Usage: cd /path/to/djezzy_bot && chmod +x termux/prune_for_phone.sh && ./termux/prune_for_phone.sh

set -e

KEEP=(
    "djezzy_bot.py"
    "djezzy_utils.py"
    "config.py"
    "run.sh"
    "requirements.txt"
    "INSTALLATION.md"
    "README.md"
    "QUICKSTART.md"
    "termux/install.sh"
    "termux/bundle.sh"
    "termux/export_for_git.sh"
    "termux/export_for_phone.sh"
    "termux/copy_to_project.sh"
    "termux/README.md"
)

# convert KEEP list to absolute canonical paths
ROOT="$(pwd)"
keep_paths=()
for f in "${KEEP[@]}"; do
    keep_paths+=("$ROOT/$f")
done

# walk tree and delete everything not in keep_paths

echo "🔎 Pruning repository; only the following items will be preserved:"
for p in "${keep_paths[@]}"; do
    echo "  - ${p#$ROOT/}"
done

echo ""
read -p "هل أنت متأكد أنك تريد حذف باقي الملفات؟ (y/N) " ans
if [[ "$ans" != "y" && "$ans" != "Y" ]]; then
    echo "Aborting."
    exit 0
fi

# perform deletion
find "$ROOT" -mindepth 1 | while read -r item; do
    # check if item matches any keep path or is an ancestor of one
    keep=false
    for kp in "${keep_paths[@]}"; do
        if [[ "$item" == "$kp" || "$item" == "$kp"/* ]]; then
            keep=true
            break
        fi
    done
    if ! $keep; then
        echo "rm -rf '$item'"
        rm -rf "$item"
    fi
done

echo "✅ repository pruned to phone-only layout."
