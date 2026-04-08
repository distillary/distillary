#!/bin/bash
set -e

# Distillary publish — build brain as static site with agent API
# Usage: ./publish.sh [--serve]

DIR="$(cd "$(dirname "$0")" && pwd)"
SITE="$DIR/.brain-site"

echo "Building Distillary brain..."

# Clone Quartz if needed
if [ ! -f "$SITE/package.json" ]; then
    echo "Setting up Quartz..."
    git clone --depth=1 https://github.com/jackyzha0/quartz.git "$SITE"
    cd "$SITE" && npm i
fi

# Apply Distillary branding
cp "$DIR/quartz-config/quartz.config.ts" "$SITE/"
cp "$DIR/quartz-config/quartz.layout.ts" "$SITE/"
cp "$DIR/quartz-config/Footer.tsx" "$SITE/quartz/components/Footer.tsx"

# Copy brain content
rm -rf "$SITE/content" "$SITE/public"
cp -r "$DIR/brain" "$SITE/content"
rm -rf "$SITE/content/.obsidian"

# Generate agent.json INTO content/static so Quartz copies it to public
cd "$DIR"
mkdir -p "$SITE/content/static"
python3 -c "from distillary.agent_index import generate_agent_index; generate_agent_index('brain', '.brain-site/content/static')"
# Also copy to content root so it's accessible at /agent.json
cp "$SITE/content/static/agent.json" "$SITE/content/agent.json" 2>/dev/null || true

echo ""
echo "agent.json generated"

# Build and optionally serve
cd "$SITE"
if [ "$1" = "--serve" ]; then
    echo "Building + serving at http://localhost:8080"
    npx quartz build --serve
else
    npx quartz build
    echo "Built! Files in .brain-site/public/"
fi
