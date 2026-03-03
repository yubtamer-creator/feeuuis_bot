#!/bin/bash

# Export a minimal standalone copy suitable for pushing to a separate
# Termux-specific Git repository.  The resulting directory will contain all
# Python sources, scripts, requirements, and the Termux helpers but will not
# include virtualenvs, logs, data, or the original git history.
#
# Usage:
#   ./termux/export_for_git.sh [output-dir]
#
# If no output directory is specified, it defaults to `termux_termux_repo`.

OUTPUT_DIR=${1:-termux_project}

echo "🔧 Preparing standalone Termux repo in $OUTPUT_DIR"

# ensure we are invoked from project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# remove any existing export
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# copy necessary files
COPY_LIST=(
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
    "termux/README.md"
)

for f in "${COPY_LIST[@]}"; do
    if [ -e "$f" ]; then
        mkdir -p "$(dirname "$OUTPUT_DIR/$f")"
        cp -a "$f" "$OUTPUT_DIR/$f"
    fi
done

# create a minimal .gitignore
cat > "$OUTPUT_DIR/.gitignore" <<'EOF'
venv/
*.pyc
*.log
data/
logs/
.env
EOF

# add a helper README note
cat >> "$OUTPUT_DIR/README.md" <<'EOF'

---
This repository is a Termux-specific subset of the full Djezzy Bot project.
Use `./termux/install.sh` to finish setup on the phone.
EOF

echo "✅ standalone Termux directory created at $OUTPUT_DIR"

echo "You can now cd $OUTPUT_DIR && git init && git add . && git commit -m 'Initial Termux bundle'"
