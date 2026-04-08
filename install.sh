#!/bin/bash
set -e

# Distillary installer
# Usage: curl -fsSL https://raw.githubusercontent.com/distillary/distillary/main/install.sh | bash

REPO="https://github.com/distillary/distillary.git"
DIR="${DISTILLARY_DIR:-$HOME/distillary}"

echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║          D I S T I L L A R Y         ║"
echo "  ║  Knowledge distillation with agents  ║"
echo "  ╚══════════════════════════════════════╝"
echo ""

# Check dependencies
check_dep() {
    if ! command -v "$1" &>/dev/null; then
        echo "  ✗ $1 not found. $2"
        return 1
    fi
    echo "  ✓ $1 $(command -v "$1")"
    return 0
}

echo "Checking dependencies..."
MISSING=0
check_dep python3 "Install Python 3.11+: https://python.org" || MISSING=1
check_dep pip3 "Comes with Python" || check_dep pip "Comes with Python" || MISSING=1

if [ $MISSING -eq 1 ]; then
    echo ""
    echo "Install missing dependencies and try again."
    exit 1
fi

# Clone or update
if [ -d "$DIR" ]; then
    echo ""
    echo "Updating existing installation at $DIR..."
    cd "$DIR" && git pull --quiet
else
    echo ""
    echo "Installing to $DIR..."
    git clone --quiet "$REPO" "$DIR"
fi

cd "$DIR"

# Install Python deps
echo "Installing Python dependencies..."
pip3 install --quiet pyyaml ebooklib beautifulsoup4 2>/dev/null || pip install --quiet pyyaml ebooklib beautifulsoup4

# Create brain structure
mkdir -p brain/sources brain/shared/concepts brain/shared/analytics brain/personal/annotations

echo ""
echo "  ✓ Installed to $DIR"
echo ""
echo "  Next:"
echo ""
echo "    cd $DIR && claude"
echo "    > Add ~/Downloads/my-book.epub to my brain"
echo ""
echo "  That's it. ~15 minutes for a 300-page book."
echo ""
