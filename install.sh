#!/bin/bash
# ZenitPY installer

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is required. Install it with: sudo apt install python3"
    exit 1
fi

# Copy script to /usr/local/bin and make it executable
sudo cp zenitpy.py /usr/local/bin/zenitpy
sudo chmod +x /usr/local/bin/zenitpy

echo "[OK] ZenitPY installed successfully."
echo "     Run: zenitpy --help"
