#!/bin/bash

# Requires: pip install pymupdf
# And: cd /target/folder (inside which you want each PDF's text to be extracted into a .txt file in same folder as original PDF)

# Enable recursive globbing (**)
shopt -s globstar

for filename_with_spaces in **/*.pdf; do
    python -m pymupdf gettext "$filename_with_spaces" || echo "Failed for $filename_with_spaces , continuing."
done