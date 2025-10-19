#!/bin/bash

echo "=== Starting FCC tool run at $(date) ==="
/usr/local/bin/python3 /app/src/fcc_tool.py --update --non-interactive --keep-files
echo "=== Finished FCC tool run at $(date) ==="