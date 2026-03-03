#!/bin/bash

# Create a minimal bundle of the project suitable for transferring to Termux
# Usage:
#   ./termux/bundle.sh [output-filename]
# defaults to djezzy_termux.tar.gz

OUTPUT=${1:-djezzy_termux.tar.gz}

echo "📦 building archive $OUTPUT ..."

# ensure we are in project root (script is in termux/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# exclude common unnecessary directories
EXCLUDES=(
    "./venv" "./.git" "./logs" "./data" "./termux/bundle.sh" "./termux/README.md"
)

tar czf "$OUTPUT" \
    --exclude="${EXCLUDES[0]}" \
    --exclude="${EXCLUDES[1]}" \
    --exclude="${EXCLUDES[2]}" \
    --exclude="${EXCLUDES[3]}" \
    --exclude="${EXCLUDES[4]}" \
    --exclude="${EXCLUDES[5]}" \
    .

echo "✅ created $OUTPUT. يمكنك الآن نقل هذا الملف إلى هاتف Termux وفك الضغط."