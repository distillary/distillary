#!/bin/bash
# Distillary setup — run once after cloning
pip install pyyaml ebooklib beautifulsoup4
mkdir -p brain/sources brain/shared/concepts brain/shared/analytics brain/personal/annotations books
echo "Ready. Open this folder in Claude Code and say: add books/my-book.epub to my brain"
